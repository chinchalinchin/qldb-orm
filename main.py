import sys
import random
from innoldb.qldb import Document
from innoldb.logger import getLogger

log = getLogger('main')

departments = ['Business Development', 'Research and Development', 'Innovation and Technology']
locations = ['Virgina', 'Maryland', 'Florida', 'Minnesota', 'West Virginia']
teams = ['Innovation', 'InnoLab', 'Innovation Lab', 'Inno Lab', 'Laboratory']
specialities = ['Application Development', 'Cloud Migration', 'Data Analytics', 'Machine Learning']
members = [{'UI/UX': 'Phung'}, {'Solutions': 'Justin'}, { 'Capabilities': 'Peter' }, 
           {'Developer #1': 'Thomas'}, {'Developer #2': 'Aurora'}, {'DevSecOps': 'Grant'},
           {'Scrum': 'Selah'}, { 'Architect': 'Tariq' }]

def create():
  document = Document('innolab')
  document.company = 'Makpar'
  document.department = departments[random.randint(0, len(departments) - 1)]
  document.location = locations[random.randint(0, len(locations) - 1)]
  document.team = teams[random.randint(0, len(teams) - 1)]
  document.specialty = specialities[random.randint(0, len(specialities) - 1)]
  document.members = members[:random.randint(0, len(members) - 1)]
  document.save()
  return document

def load(id):
  return Document(name='innolab', id=id)

def update_speciality(document):
  document.specialty = specialities[random.randint(0, len(specialities) - 1)]
  document.save()

def update_prop(document, key, value):
  setattr(document, key, value)
  document.save()

if __name__=="__main__":
  if len(sys.argv) > 1:
    routines = sys.argv[1:]
  
  if routines[0] == 'load':
    document = load('0434ade7-86bb-11ec-935a-34735aabbbc4')
    log.info("Loaded DOCUMENT: \n\t\t\t\t\t\t\t %s", document.fields())

  else:  
    document = create()
    log.info("Created DOCUMENT: \n\t\t\t\t\t\t\t %s", document.fields())

  for routine in routines:
    if routine == 'update_spec':
      update_speciality(document)
    elif routine == 'update_prop_1':
      update_prop(document, 'favorite_movie', 'children of men')
    elif routine == 'update_prop_2':
      update_prop(document, 'favorite_movie', 'pulp fiction')
    elif routine == 'update_prop_3':
      update_prop(document, 'favorite_movie', 'lords of salem')
    elif routine == 'update_prop_4':
      update_prop(document, 'favorite_movie', 'the big lebowski')
    elif routine == 'update_prop_5':
      update_prop(document, 'favorite_movie', 'the evil dead')

# if __name__==:""
  # from qldb.qldb import Driver
  # QldbDriver('innolab-Dev-test').execute_lambda(lambda executor: executor.execute_statement('CREATE TABLE test'))
