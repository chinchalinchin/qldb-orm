import uuid
from amazon.ion.simpleion import dumps, loads
from pyqldb.driver.qldb_driver import QldbDriver
from . import settings
from .logger import getLogger

log = getLogger('innoldb.qldb')

class Driver():
  @staticmethod 
  def execute(transaction_executor, statement, *params):
    r"""Static method for executing transactions with QLDB driver. 

    :param transaction_executor: Executor is injected into callback function through `pyqldb.driver.qldb_driver.execute_lambda` method.
    :param statement: Parameterized PartialQL query.
    :type statement: str
    :param \*params: Arguments for parameterized query.
    """
    log.debug("Executing statement: \n\t\t\t\t\t\t\t %s \n\t\t\t\t\t\t\t parameters: %s \n", statement, params)
    if len(params) == 0:
      return transaction_executor.execute_statement(statement)
    return transaction_executor.execute_statement(statement, *params)

  @staticmethod
  def driver(ledger):
    """Static method for retrieving a QLDB driver

    :param ledger: Name of the ledger
    :type ledger: str
    :return: QLDB Driver
    :rtype: :class:`pyqldb.driver.qldb_driver.QldbDriver`
    """
    return QldbDriver(ledger_name=ledger)
    
  @staticmethod
  def create_table(driver, table):
    """Static method for creating a table within a ledger

    :param driver: QLDB Driver
    :type driver: :class:`pyqldb.driver.qldb_driver.QldbDriver`
    :param table: table to be updated
    :type table: str
    :return: iterable containing result
    """
    ## NOTE: I don't like directly formatting strings with query parameters that will
    ##      be run directly against the persistence layer (since malicious users could inject
    ##      bad parameters), but the driver won't parameterize `Create`` queries for some reason. 
    ##      What follows is how the official documentation does it:
    ##      https://docs.aws.amazon.com/qldb/latest/developerguide/getting-started.python.step-3.html
    ##  NOTE: This is going to necessitate some logic in this library to prevent malicious strings from 
    ##        gettings injected through parameters.
    statement = 'Create TABLE {}'.format(table)
    return driver.execute_lambda(lambda executor: Driver.execute(executor, statement))

  @staticmethod
  def create_index(driver, table, index):
    """Static method for generating an index on table

    :param driver: QLDB Driver
    :type driver: :class:`pyqldb.driver.qldb_driver.QldbDriver`
    :param table: table to be updated
    :type table: str
    :param index: index to search against
    :type index: str
    :return: iterable containing result
    """
    ## NOTE: See above note.
    statement = 'CREATE INDEX on {} ({})'.format(table, index)
    return driver.execute_lambda(lambda executor: Driver.execute(executor, statement))
  
  @staticmethod
  def insert(driver, document, table):
    """Static method for inserting document into table

    :param driver: QLDB Driver
    :type driver: :class:`pyqldb.driver.qldb_driver.QldbDriver`
    :param document: document containing fields to insert
    :type document: dict
    :param table: table into which document is inserted
    :type table: str
    :return: iterable containing result
    """
    ## NOTE: See above note.
    ##  TODO: check table string for malicious parameterization
    statement = 'INSERT INTO {} ?'.format(table)
    return driver.execute_lambda(lambda executor: Driver.execute(executor, statement, document))
  
  @staticmethod
  def update(driver, document, table, index):
    """Static method for updating QLDB table

    :param driver: QLDB Driver
    :type driver: :class:`pyqldb.driver.qldb_driver.QldbDriver`
    :param document: document to be updated
    :type document: dict
    :param table: name of the table where the document is
    :type table: dict
    :param index: name of the table index
    :type index: str
    :return: iterable containing result set
    """
    lookup = document[index]
    buffer_document = { key: value for key, value in document.items() if key != index }

    ## NOTE: See notes in prior methods
    ##  TODO: check table string for malicious parameterization

    ## NOTE: For some reason, you cannot parameterize more than one field update,
    ##        i.e., `SET column1 = value1 SET column2 = value2` does not work.
    ## TODO: will need to get a snapshot of existing document and iterate through fields 
    ##        to see if any have changed and update 
    result = Driver.query_by_field(driver, index, lookup, table)
    results = []

    ## ERROR HERE. Buffer document can have more keys
    for row in result:
      saved_document = loads(dumps(row))
      for (key, buffer_value) in buffer_document.items():
        saved_value = saved_document.get(key, None)
        log.debug('Comparing saved value: %s \n\t\t\t\t\t\t\t to buffer value: %s', saved_value, buffer_value)
        if saved_value != buffer_value:
          log.debug('Not equal')
          update_statement = 'UPDATE {} SET {} = ? WHERE {} = ?'.format(table, key, index)
          results += driver.execute_lambda(lambda executor: Driver.execute(
                              executor, update_statement, buffer_value, lookup
                          ))
    return results

  @staticmethod
  def query_by_field(driver, field, value, table):
    """Static method for querying table by field.

    :param driver: QLDB Driver
    :type driver: :class:`pyqldb.driver.qldb_driver.QldbDriver`
    :param field: field to be searched
    :type field: str
    :param value: search value
    :type value: str
    :param table: table to be quiered
    :type table: str
    :return: iterable containing result
    """
    statement = 'SELECT * FROM {} WHERE {} = ?'.format(table, field)
    return driver.execute_lambda(lambda executor: Driver.execute(
      executor, statement, value
    ))


class Table():
  def __init__(self, table, ledger=settings.LEDGER, index=settings.DEFAULT_INDEX):
    self.driver = Driver.driver(ledger)
    # Table name
    self.table = table
    # Name of the lookup field in the PartiQL table
    self.index = index
    # Fields 'in' the table. 
    self._init_fixtures()

  def _init_fixtures(self):
    try:
      Driver.create_table(self.driver, self.table)
    except Exception as e:
      log.debug(e)
    try:
      Driver.create_index(self.driver, self.table, self.index)
    except Exception as e:
      log.debug(e)

  def _insert(self, document):
    log.debug("Inserting DOCUMENT(%s = %s)", self.index, document[self.index])
    return Driver.insert(self.driver, document, self.table)
  
  def _update(self, document):
    log.debug("Updating DOCUMENT(%s = %s)", self.index, document[self.index])
    return Driver.update(self.driver, document, self.table, self.index)

  def exists(self, id):
    log.debug("Checking existence of DOCUMENT(%s = %s)", self.index, id)
    result = Driver.query_by_field(self.driver, self.index, id, self.table)
    # for row in result:
    #   log.debug("Query returned with row %s", row)
    if next(result, None):
      return True
    return False
  
  def save(self, document):
    log.debug("Saving Document(%s = %s)", self.index, document[self.index])
    if self.exists(document[self.index]):
      return self._update(document)
    return self._insert(document)


class Document(Table):
  def __init__(self, name, id = str(uuid.uuid1()), ledger=settings.LEDGER):
    super().__init__(table=name, ledger=ledger)
    self.id = id
  
  def fields(self):
    return {key: value for key, value in vars(self).items() if key not in ['table', 'driver', 'index']}

  def save(self):
    result = super().save(self.fields())
    for row in result:
      log.debug('Transaction result: \n\t\t\t\t\t\t\t %s', loads(dumps(row)))