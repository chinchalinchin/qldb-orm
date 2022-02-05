from pyqldb.driver.qldb_driver import QldbDriver
from qldb import settings

from qldb.parser import Parser

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
  def update(driver, document, table, index):
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

    update_statement = f'UPDATE ? {set_clause} WHERE ? = ?'

    return driver.execute_lambda(lambda executor: Driver.execute(
      executor, update_statement, table, *parameters, index, lookup
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
  def __init__(self, table, ledger=settings.LEDGER, index='id'):
    self.driver = Driver.driver(ledger)
    # Table name
    self.table = table
    # Name of the lookup field in the PartiQL table
    self.index = index
    # Fields 'in' the table. 
    self._init_fixtures()

  def _init_fixtures(self):
    # TODO: if the idea is to inherit from this class with every instance of the Model class,
    #       then this method needs to check for the existence of the table and index before
    #       attempting to create them again.
    Driver.create_table(self.driver, self.table)
    Driver.create_index(self.driver, self.table, self.index)

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
    if self.exists():
      return self._update(document)
    return self._insert(document)


class Field():
  def __init__(self):
    pass

  def __get__(self, instance, owner):
    pass

  def __set__(self, instance, value):
    pass

  def __delete__(self, instance):
    pass