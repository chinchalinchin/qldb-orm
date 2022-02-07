import argparse
import pprint
import random
import sys
from innoldb.qldb import Document, Query
from innoldb.static.logger import getLogger

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
    setattr(namespace, self.dest, {})
      
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

def insert(table, document):
  document = Document(table=table, snapshot=document)
  document.save()
  return document.id

def all(table):
  return Query(table).all()

def find(table, fields):
  return Query(table).find_by(**fields)

def like(table, fields):
  return Query(table).find_like(**fields)
  
def update_prop(document, **props):
  for key, value in props.items():
    setattr(document, key, value)
    document.save()
  return document

def do_program(cli_args):
  parser = argparse.ArgumentParser()
  parser.add_argument('-tb', '--table', help="Name of the table to query", required=True)
  parser.add_argument('-id', '--id', help="ID of the document")
  parser.add_argument('-up', '--update', nargs='*', help="Requires --id.\n Update fields with `KEY1=VAL1 KEY2=VAL2 ...`", action=KeyValue)
  parser.add_argument('-in', '--insert', nargs='*', help="Create document with fields `KEY1=VAL1 KEY2=VAL2 ...`", action=KeyValue)
  parser.add_argument('-fi', '--find', nargs='*', help="Query by field equality `KEY1=VAL1 KEY2=VAL2...`", action=KeyValue)
  parser.add_argument('-lk', '--like', nargs='*', help="Query by field matching `KEY1=VAL1 KEY2=VAL2 ...`", action=KeyValue)
  parser.add_argument('-lo', '--load', action='store_true', help="Requires --id.\n Load a document.",)
  parser.add_argument('-mo', '--mock', action='store_true', help="Create a new mock document")
  parser.add_argument('-al', '--all', action='store_true', help='Query all documents')
  
  args = parser.parse_args(cli_args)
  
  if args.load:
    if args.id:
      document = load(args.id, args.table)
      printer.pprint(document.fields())
    else:
      log.warn("No Document ID specified.")

  elif args.mock:  
    document = mock(args.table)
    printer.pprint(document.fields())

  elif args.all:
    results = all(args.table)
    for result in results:
      printer.pprint(result.fields())

  elif args.update:
    if args.id:
      document = load(args.id, args.table)
      document = update_prop(document, **args.update)
      printer.pprint(document.fields())
    else:
      log.warn("No Document ID specified.")
  
  elif args.insert:
    insert_id = insert(args.table, args.insert)
    document = load(insert_id, args.table)
    printer.pprint(document.fields())

  elif args.find:
    results = find(args.table, args.find)
    for result in results:
      printer.pprint(result.fields())

  elif args.like:
    results = like(args.table, args.like)
    for result in results:
      printer.pprint(result.fields())
    

def entrypoint():
  do_program(sys.argv[1:])

if __name__=="__main__":
  do_program(sys.argv[1:])