import argparse
import pprint
import random
import sys
from innoldb.qldb import Document, Query
from innoldb.logger import getLogger

log = getLogger('main')
printer = pprint.PrettyPrinter(indent=4)

departments = ['Business Development', 'Research and Development', 'Innovation and Technology']
locations = ['Virgina', 'Maryland', 'Florida', 'Minnesota', 'West Virginia']
teams = ['Innovation', 'InnoLab', 'Innovation Lab', 'Inno Lab', 'Laboratory']
specialities = ['Application Development', 'Cloud Migration', 'Data Analytics', 'Machine Learning']
members = [{'UI/UX': 'Phung'}, {'Solutions': 'Justin'}, { 'Capabilities': 'Peter' }, 
           {'Developer #1': 'Thomas'}, {'Developer #2': 'Aurora'}, {'DevSecOps': 'Grant'},
           {'Scrum': 'Selah'}, { 'Architect': 'Tariq' }]

def mock(table):
  document = Document(table)
  document.company = 'Makpar'
  document.department = departments[random.randint(0, len(departments) - 1)]
  document.location = locations[random.randint(0, len(locations) - 1)]
  document.team = teams[random.randint(0, len(teams) - 1)]
  document.specialty = specialities[random.randint(0, len(specialities) - 1)]
  document.members = members[:random.randint(0, len(members) - 1)]
  document.save()
  return document

def load(id, table):
  return Document(table=table, id=id)

def update_prop(document, key, value):
  setattr(document, key, value)
  document.save()

def do_program(cli_args):
  parser = argparse.ArgumentParser()
  parser.add_argument('--id', help="ID of the document to load")
  parser.add_argument('--table', help="Name of the table to query", required=True)
  parser.add_argument('--update', help="KEY=VALUE")
  parser.add_argument('--mock', action='store_true', help="Create a new mock document")
  parser.add_argument('--all', action='store_true', help='Query all documents')
  
  args = parser.parse_args(cli_args)
  
  if args.id:
    document = load(args.id, args.table)
    printer.pprint(document.fields())

  elif args.mock:  
    document = mock(args.table)
    printer.pprint(document.fields())

  elif args.all:
    results = Query(args.table).all()
    for result in results:
      printer.pprint(result.fields())

  elif args.update:
    if '=' in args.update and len(args.update.split("=")) == 2:
      if args.id:
        document = load(args.id)
        key, value = args.update.split("=")
        update_prop(document, key, value)
      else:
        log.warn("No Document ID specified.")
    else:
        log.warn("Field update must be inputted '--update KEY=VALUE'")

def entrypoint():
  do_program(sys.argv[1:])

if __name__=="__main__":
  do_program(sys.argv[1:])

# if __name__==:""
  # from qldb.qldb import Driver
  # QldbDriver('innolab-Dev-test').execute_lambda(lambda executor: executor.execute_statement('CREATE TABLE test'))
