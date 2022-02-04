from pyqldb.driver.qldb_driver import QldbDriver

class Driver():
  @staticmethod 
  def execute(transaction_executor, statement, *params):
    r"""Static method for executing transactions with QLDB driver. 

    :param transaction_executor: Executor is injected into callback function through `pyqldb.driver.qldb_driver.execute_lambda` method.
    :param statement: Parameterized PartialQL query.
    :type statement: str
    :param \*params: Arguments for parameterized query.
    """
    transaction_executor.execute_statement(statement, params)

  @staticmethod
  def driver(ledger):
    """Static method for retrieving a QLDB driver

    :param ledger: Name of the ledger
    :type ledger: str
    """
    return QldbDriver(ledger_name=ledger).qldb_driver
    
  @staticmethod
  def create_table(driver, table):
    """Static method for creating a table within a ledger

    :param table: table to be updated
    :type table: str

    :return: iterable containing result
    """
    return driver.execute_lambda(lambda executor: Driver.execute(
      executor, 'CREATE TABLE ?', table
    ))

  @staticmethod
  def create_index(driver, table, index):
    """Static method for generating an index on table

    :param table: table to be updated
    :type table: str
    :param index: index to search against
    :type index: str

    :return: iterable containing result
    """
    return driver.execute_lambda(lambda executor: Driver.execute(
      executor, 'CREATE INDEX ?(?)', table, index
    ))
  
  @staticmethod
  def insert(driver, document, table):
    """Static method for inserting document into table

    :param document: document containing fields to insert
    :type document: dict
    :param table: table into which document is inserted
    :type table: str

    :return: iterable containing result
    """
    return driver.execute_lambda(lambda executor: Driver.execute(
      executor, 'INSERT INTO ? ?', table, document
    ))
  
  @staticmethod
  def update(driver, field, value, lookup, table, index):
    """Static method for updating table field in document
    :param field: field to be updated
    :type field: str
    :param value: updated value
    :type value: str
    :param lookup: index to be updated
    :type lookup: str
    :param table: table to be updated
    :type table: str
    :param index: index to search against
    :type index: str

    :return: iterable containing result
    """
    return driver.execute_lambda(lambda executor: Driver.execute(
      executor, 'UPDATE ? SET ? = ? WHERE ? = ?', table, field, value, index, lookup
    ))

  @staticmethod
  def query_by_field(driver, field, value, table):
    """Static method for querying table by field.

    :param field: field to be searched
    :type field: str
    :param value: search value
    :type value: str
    :param table: table to be quiered
    :type table: str
  
    :return: iterable containing result
    """
    return driver.execute_lambda(lambda executor: Driver.execute(
      executor, 'SELECT * FROM ? WHERE ? = ?', table, field, value
    ))

class Table():
  def __init__(self, ledger, table, index='id'):
    self.driver = Driver.driver(ledger)
    self.table = table
    self.index = index
    self.fields = {}
    self._init_fixtures()

  def _init_fixtures(self):
    Driver.create_table(self.driver, self.table)
    Driver.create_index(self.driver, self.table, self.index)

  def insert(self, id):
    result = Driver.query_by_field(self.driver, self.index, self.id, self.table)
    if next(result, None):
      return None
    self.fields.id = id
    return Driver.insert(self.driver, self.fields, self.table)