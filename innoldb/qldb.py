import uuid
from pyqldb.driver.qldb_driver import QldbDriver
from . import settings
from .parser import Parser
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
    log.debug("executing statement '%s' with parameters %s", statement, params)
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
    parameters = []
    n = len(list(document.items()))

    # unpack dictionary into ordered alternating list of key, values
    # to match the `SET ? = ?` ordering in the PartiQL query.  
    for key, value in document.items():
      if key is not index:
        parameters.append(key)
        parameters.append(value)

    set_clause = Parser.set_parameter_string(n)

    ## NOTE: See notes in prior methods
    ##  TODO: check table string for malicious parameterization
    update_statement = 'UPDATE {} {} WHERE ? = ?'.format(table, set_clause)

    return driver.execute_lambda(lambda executor: Driver.execute(
      executor, update_statement, *parameters, index, lookup
    ))

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
    statement = 'SELECT * FROM {} WHERE ? = ?'.format(table)
    return driver.execute_lambda(lambda executor: Driver.execute(
      executor, statement, field, value
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
    return Driver.insert(self.driver, document, self.table)
  
  def _update(self, document):
    return Driver.update(self.driver, document, self.table, self.index)

  def exists(self, id):
    result = Driver.query_by_field(self.driver, self.index, id, self.table)
    if next(result, None):
      return True
    return False
  
  def save(self, document):
    if self.exists(document[self.index]):
      return self._update(document)
    return self._insert(document)

class Document(Table):
  def __init__(self, name, id = str(uuid.uuid1())):
    super().__init__(table=name)
    self.id = id
    
  def save(self):
    fields = {key: value for key, value in vars(self).items() if key not in ['table', 'driver', 'index']}
    super().save(fields)