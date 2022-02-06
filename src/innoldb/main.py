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

class KeyValue(argparse.Action):
  # Constructor calling
  def __call__(self, parser, namespace, values, option_string = None):
    setattr(namespace, self.dest, dict())
      
    for value in values:
      key, value = value.split('=')
      getattr(namespace, self.dest)[key] = value
  
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

def insert(table, document, id=None):
  return Document(table=table, id=id, snapshot=document).save()

def update_prop(document, key, value):
  setattr(document, key, value)
  return document.save()

def do_program(cli_args):
  parser = argparse.ArgumentParser()
  parser.add_argument('-id', '--id', help="ID of the document to load")
  parser.add_argument('-tb', '--table', help="Name of the table to query", required=True)
  parser.add_argument('-up', '--update', nargs='*', help="Update fields with `KEY1=VALUE1 KEY2=VALUE2 ...`", action=KeyValue)
  parser.add_argument('-in', '--insert', nargs='*', help="Create document with fields `KEY1=VALUE1 KEY2=VALUE2 ...`", action=KeyValue)
  parser.add_argument('-mo', '--mock', action='store_true', help="Create a new mock document")
  parser.add_argument('-al', '--all', action='store_true', help='Query all documents')
  
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
    if args.id:
      document = load(args.id, args.table)
      for key, value in args.update.items():
        update_prop(document, key, value)
      printer.pprint(document.fields())
    else:
      log.warn("No Document ID specified.")
  
  elif args.insert:
    insert(args.table, args.insert, args.id)
    document = load(args.id, args.table)
    printer.pprint(document)
    

def entrypoint():
  do_program(sys.argv[1:])

if __name__=="__main__":
  do_program(sys.argv[1:])

# if __name__==:""
  # from qldb.qldb import Driver
  # QldbDriver('innolab-Dev-test').execute_lambda(lambda executor: executor.execute_statement('CREATE TABLE test'))
