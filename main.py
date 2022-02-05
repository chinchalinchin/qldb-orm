from innoldb.qldb import Document

if __name__=="__main__":
  document = Document('innolab')
  document.company = 'Makpar'
  document.department = 'Innovation and Technology'
  document.location = 'Virginia'
  document.team = 'Innovation Lab'
  document.specialty = 'Application Development'
  document.members = {
    'UI/UX': 'Phung',
    'Solutions': 'Justin',
    'Capabilities': 'Peter',
    'Developer #1': 'Thomas',
    'Developer #2': 'Aurora',
    'DevSecOps': 'Grant',
    'Scrum': 'Selah',
    'Architect': 'Tariq'
  }
  document.save()
  
# if __name__==:""
  # from qldb.qldb import Driver
  # QldbDriver('innolab-Dev-test').execute_lambda(lambda executor: executor.execute_statement('CREATE TABLE test'))
