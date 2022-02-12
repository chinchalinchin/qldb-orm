import argparse
import pprint
import random
import sys
from innoldb.qldb import Document, Query
from innoldb.static.logger import getLogger

log = getLogger('main')
printer = pprint.PrettyPrinter(indent=4)

departments = ['Business Development',
               'Research and Development', 'Innovation and Technology']
locations = ['Virgina', 'Maryland', 'Florida', 'Minnesota', 'West Virginia']
teams = ['Innovation', 'InnoLab', 'Innovation Lab', 'Inno Lab', 'Laboratory']
specialities = ['Application Development',
                'Cloud Migration', 'Data Analytics', 'Machine Learning']
members = [{'UI/UX': 'Phung'}, {'Solutions': 'Justin'}, {'Capabilities': 'Peter'},
           {'Developer #1': 'Thomas'}, {
               'Developer #2': 'Aurora'}, {'DevSecOps': 'Grant'},
           {'Scrum': 'Selah'}, {'Architect': 'Tariq'}]


class KeyValue(argparse.Action):
    """Action class to map CLI input of the form `key1=val1 key2=val2 ...` to an object's properties.

    :param argparse: [description]
    :type argparse: [type]
    """

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, {})

        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value

def print_line(n):
  print('-'*n)

def mock(table):
    """Insert a mock document into a table

    :param table: Name of table to be queried.
    :type table: str
    :return: Document that was mocked
    :rtype: :class:`innoldb.qldb.Document`
    """
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
    """Load a document from a table.

    :param id: ID of the document to load
    :type id: str
    :param table: Name of table to be queried.
    :type table: str
    :return: collection of `innoldb.qldb.Document`
    :rtype: :class:`innoldb.qldb.Document`
    """
    return Document(table=table, id=id)


def insert(table, document):
    """Insert a document into a table

    :param table: Name of table to be queried.
    :type table: str
    :param document: Document to be inserted
    :type document: :class:`innoldb.qldb.Document`
    :return: id of the document inserted
    :rtype: str
    """
    document = Document(table=table, snapshot=document)
    document.save()
    return document.id


def get_all(table):
    """Find all documents in a table

    :param table: Name of table to be queried.
    :type table: str
    :return: collection of `innoldb.qldb.Document`
    :rtype: list
    """
    return Query(table).get_all()


def find(table, fields):
    """Find documents by field equality.

    :param table: Name of table to query
    :type table: str
    :param fields: key-value pairs of the fields
    :type fields: `kwargs`
    :return: collection of `innoldb.qldb.Document`
    :rtype: list
    """
    return Query(table).find_by(**fields)


def history(table, id):
    """Query revision table history for particular metadata ID

    :param table: Table to be queried
    :type table: str
    :param id: ID of the metadata revision
    :type id: str
    :return: collection of `innoldb.qldb.Document`
    :rtype: list
    """
    return Query(table).history(id)


def update_prop(document, **props):
    """Update properties on document and persist to **QLDB**

    :param document: Document to be updated
    :type document: :class:`innoldb.qldb.Document`
    :return: Updated document
    :rtype: :class:`innoldb.qldb.Document`
    """
    for key, value in props.items():
        setattr(document, key, value)
    document.save()
    return document

def view_doc(document, unhide):
  if unhide:
    return vars(document)
  return document.fields()

def do_program(cli_args):
    """Entrypoint for the application.

    :param cli_args: command line arguments, i.e. `sysv[1:]`
    :type cli_args: list
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-tb', '--table', 
                        help="Name of the table to query", required=True)
    parser.add_argument('-ind', '--index', help="Index ID of the document")
    parser.add_argument('-meta', '--meta', help="Meta ID of the document")
    parser.add_argument('-hst', '--history', action='store_true',
                        help="Requires --meta. Retrieve document history by 'meta.id'.")
    parser.add_argument('-al', '--all', action='store_true',
                        help='Query all documents')
    parser.add_argument('-up', '--update', nargs='*', action=KeyValue,
                        help="Requires --id.\n Update fields with `KEY1=VAL1 KEY2=VAL2 ...`")
    parser.add_argument('-in', '--insert', nargs='*', action=KeyValue,
                        help="Create document with fields `KEY1=VAL1 KEY2=VAL2 ...`")
    parser.add_argument('-fi', '--find', nargs='*', action=KeyValue,
                        help="Query by field equality `KEY1=VAL1 KEY2=VAL2...`")
    parser.add_argument('-lo', '--load', action='store_true',
                        help="Requires --id.\n Load a document by index.",)
    parser.add_argument('-mo', '--mock', action='store_true',
                        help="Create a new mock document")
    parser.add_argument('-uh', '--unhide', action='store_true',
                        help="Show hidden document fields")

    args = parser.parse_args(cli_args)

    if args.load:
        if args.index:
            document = load(args.index, args.table)
            printer.pprint(document)
        else:
            log.warning("No Document Index specified.")

    elif args.mock:
        document = mock(args.table)
        printer.pprint(view_doc(document, args.unhide))

    elif args.all:
        results = get_all(args.table)
        for result in results:
            print_line(30)
            printer.pprint(view_doc(result, args.unhide))

    elif args.update:
        if args.index:
            document = load(args.index, args.table)
            document = update_prop(document, **args.update)
            printer.pprint(view_doc(document, args.unhide))
        else:
            log.warning("No Document Index specified.")

    elif args.history:
        if args.meta:
          results = history(args.table, args.meta)
          for result in results:
              print_line(30)
              printer.pprint(vars(result.data))
              print_line(20)
              printer.pprint(vars(result.metadata))
        else:
            log.warning("No Document ID specified.")

    elif args.insert:
        insert_id = insert(args.table, args.insert)
        document = load(insert_id, args.table)
        printer.pprint(view_doc(document, args.unhide))

    elif args.find:
        results = find(args.table, args.find)
        for result in results:
            printer.pprint(view_doc(result.fields(), args.unhide))


def entrypoint():
    """Entrypoint for build package
    """
    do_program(sys.argv[1:])


if __name__ == "__main__":
    do_program(sys.argv[1:])
