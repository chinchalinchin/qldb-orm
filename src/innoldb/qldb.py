import uuid
from amazon.ion.simpleion import dumps, loads
from boto3 import client
from pyqldb.driver.qldb_driver import QldbDriver
from innoldb import clauses, settings
from innoldb.logger import getLogger

log = getLogger('innoldb.qldb')

class Driver():
  @staticmethod 
  def ledger(ledger=settings.LEDGER):
    return client('qldb').create_ledger(
      Name=ledger,
      PermissionsMode='STANDARD',
      DeletionProtection=False,
    )

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
  def driver(ledger=settings.LEDGER):
    """Static method for retrieving a QLDB driver

    :param ledger: Name of the ledger
    :type ledger: str
    :return: QLDB Driver
    :rtype: :class:`pyqldb.driver.qldb_driver.QldbDriver`
    """
    return QldbDriver(ledger_name=ledger)
    
  @staticmethod
  def tables(ledger=settings.LEDGER):
    return QldbDriver(ledger_name=ledger).list_tables()

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
    result = Driver.query_by_fields(driver, table, **{index: lookup})
    results = []

    ## ERROR HERE. Buffer document can have more keys
    for row in result:
      saved_document = loads(dumps(row))
      for (key, buffer_value) in buffer_document.items():
        saved_value = saved_document.get(key, None)
        log.debug('Comparing saved value: %s \n\t\t\t\t\t\t\t to buffer value: %s', saved_value, buffer_value)
        if saved_value != buffer_value:
          update_statement = 'UPDATE {} SET {} = ? WHERE {} = ?'.format(table, key, index)
          results += driver.execute_lambda(lambda executor: Driver.execute(
                              executor, update_statement, buffer_value, lookup
                          ))
    return results

  @staticmethod
  def query_all(driver, table):
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
    statement = 'SELECT * FROM {}'.format(table)
    return driver.execute_lambda(lambda executor: Driver.execute(
      executor, statement
    ))

  @staticmethod
  def query_by_fields(driver, table, **fields):
    """Static method for querying table by field.

    :param driver: QLDB Driver
    :type driver: :class:`pyqldb.driver.qldb_driver.QldbDriver`
    :param fields: Keyword arguments. A dictionary containing the fields used to construct `WHERE` clause in query.
    :type fields: dict
    :type table: str
    :return: iterable containing result
    """
    columns, values = fields.keys(), fields.values()
    where_clause = clauses.where(operator=clauses.OPERATORS.EQUALS, *columns)
    statement = 'SELECT * FROM {} {}'.format(table, where_clause)
    return driver.execute_lambda(lambda executor: Driver.execute(
      executor, statement, *values
    ))

  @staticmethod
  def query_like_fields(driver, table, **fields):
    pass

class Ledger():
  def __init__(self, table, ledger=settings.LEDGER):
    self.table = table
    self.ledger = ledger
    self.index = 'id'

class Document(Ledger):
  def __init__(self, table, id=None, snapshot=None, ledger=settings.LEDGER):
    super().__init__(table=table, ledger=ledger)
    if id is None:
      self.id = str(uuid.uuid1())        
    else:
      self.id = id
      snapshot = self.get(self.id)
  
    self._init_fixtures()
    self._load(snapshot)

  def _init_fixtures(self):
    if self.table not in Driver.tables(self.ledger):
      try:
        Driver.create_table(Driver.driver(self.ledger), self.table)
        Driver.create_index(Driver.driver(self.ledger), self.table, self.index)
      except Exception as e:
        log.error(e)

  def _load(self, snapshot=None):
    if snapshot is not None:
      for key, value in snapshot.items():
        setattr(self, key, value)
      
  def _insert(self, document):
    log.debug("Inserting DOCUMENT(%s = %s)", self.index, document[self.index])
    return Driver.insert(Driver.driver(self.ledger), document, self.table)
  
  def _update(self, document):
    log.debug("Updating DOCUMENT(%s = %s)", self.index, document[self.index])
    return Driver.update(Driver.driver(self.ledger), document, self.table, self.index)

  def exists(self, id):
    log.debug("Checking existence of DOCUMENT(%s = %s)", self.index, id)
    result = Driver.query_by_fields(Driver.driver(self.ledger), self.table, **{self.index: id })
    if next(result, None):
      return True
    return False

  def fields(self):
    return {key: value for key, value in vars(self).items() if key not in ['table', 'driver', 'index', 'ledger']}

  def get(self, id):
    log.debug("Returning DOCUMENT(%s = %s)", self.index, id)
    return loads(dumps(next(Driver.query_by_fields(Driver.driver(self.ledger), self.table, **{self.index: id }))))
  
  def save(self):
    fields = self.fields()
    log.debug("Saving DOCUMENT(%s = %s)", self.index, fields[self.index])
    if self.exists(fields[self.index]):
      return next(self._update(fields))
    return next(self._insert(fields))

class Query(Ledger):
  def __init__(self, table, ledger=settings.LEDGER):
    super().__init__(table=table, ledger=ledger)
  
  def all(self):
    results = Driver.query_all(Driver.driver(self.ledger), self.table)
    return [ Document(table=self.table, snapshot=loads(dumps(result))) for result in results]
  
  def find_by(self, **kwargs):
    results = Driver.query_by_fields(Driver.driver(self.ledger), self.table, **kwargs)
    return [ Document(table = self.table, snapshot=loads(dumps(result))) for result in results]
    
