import sys
import random
from innoldb.qldb import Document

specialities = ['Application Development', 'Cloud Migration', 'Data Analytics', 'Machine Learning']

def create(document):
  document.company = 'Makpar'
  document.department = 'Innovation and Technology'
  document.location = 'Virginia'
  document.team = 'Innovation Lab'
  document.specialty = specialities[random.randint(0, len(specialities) - 1)]
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

def update_speciality(document):
  document.specialty = specialities[random.randint(0, len(specialities) - 1)]
  document.save()

def update_prop(document, key, value):
  setattr(document, key, value)
  document.save()

if __name__=="__main__":
  document = Document('innolab')
  routines = ['create']
  if len(sys.argv) > 1:
    routines += sys.argv[1:]
  
  for routine in routines:
    if routine == 'create':
      create(document)
    elif routine == 'update_spec':
      update_speciality(document)
    elif routine == 'update_prop_1':
      update_prop(document, 'favorite_movie', 'children of men')
    elif routine == 'update_prop_2':
      update_prop(document, 'favorite_movie', 'pulp fiction')
    elif routine == 'update_prop_3':
      update_prop(document, 'favorite_movie', 'lords of salem')
# if __name__==:""
  # from qldb.qldb import Driver
  # QldbDriver('innolab-Dev-test').execute_lambda(lambda executor: executor.execute_statement('CREATE TABLE test'))
