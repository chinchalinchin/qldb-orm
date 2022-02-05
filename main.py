from qldb.model import Model

if __name__=="__main__":
  test = Model('test11')
  test.test_field = 'warning, this is a not a test'
  test.save()
  
  # from qldb.qldb import Driver
  # QldbDriver('innolab-Dev-test').execute_lambda(lambda executor: executor.execute_statement('CREATE TABLE test'))
