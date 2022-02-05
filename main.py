from innoldb.qldb import Document

if __name__=="__main__":
  test = Document('innolab')
  test.company = 'Makpar'
  test.department = 'Innovation and Technology'
  test.location = 'Virginia'
  test.team = 'Innovation Lab'
  test.specialty = 'Application Development'
  test.save()
  
# if __name__==:""
  # from qldb.qldb import Driver
  # QldbDriver('innolab-Dev-test').execute_lambda(lambda executor: executor.execute_statement('CREATE TABLE test'))
