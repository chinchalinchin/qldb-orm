import argparse
import random
from innoldb.qldb import Document, Query
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
  return Document(table='innolab', id=id)

def update_prop(document, key, value):
  setattr(document, key, value)
  document.save()

if __name__=="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--load', help="ID of the document to load")
  parser.add_argument('--update', help="KEY=VALUE")
  parser.add_argument('--create', action='store_true', help="Create a new document")
  parser.add_argument('--all', action='store_true', help='Query all documents')
  parser.add_argument('--display', action='store_true', help="Print document to screen")
  
  args = parser.parse_args()
  
  if args.load:
    document = load(args.load)
    log.info("Loaded DOCUMENT(%s = %s)", document.index, document.fields()[document.index])

  if args.create:  
    document = create()
    log.info("Created DOCUMENT(%s = %s)", document.index, document.fields()[document.index])

  if args.all:
    results = Query('innolab').all()
    for result in results:
      print(result.fields())

  if args.update:
    key, value = args.update.split("=")
    update_prop(document, key, value)

  if args.display:
    print(document.fields())


# if __name__==:""
  # from qldb.qldb import Driver
  # QldbDriver('innolab-Dev-test').execute_lambda(lambda executor: executor.execute_statement('CREATE TABLE test'))
