import sys
from qldb import settings
from pyqldb.driver.qldb_driver import QldbDriver


sys.path.append(settings.APP_DIR)

if __name__=="__main__":
  from qldb.model import Model
  test = Model('test11')
  test.test_field = 'warning, this is a not a test'
  test.save()
  
  # from qldb.qldb import Driver
  # QldbDriver(settings.LEDGER).execute_lambda(lambda executor: executor.execute_statement('CREATE TABLE ?', 'test3'))
