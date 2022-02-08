from innoldb.qldb import Query
from pprint import pprint

if __name__=="__main__":

  general = Query('shell_test').history()

  docIds = []
  [ docIds.append(record.metadata.id) for record in general if record.metadata.id not in docIds ]

  print('--------------------------------------------------------------------------------------------')
  print('SELECT * FROM history(table)')
  print('--------------------------------------------------------------------------------------------')

  for record in general:
    pprint(vars(record))
    pprint(vars(record.metadata))
    print('-------------------------------------')

  for docId in docIds:
    print('--------------------------------------------------------------------------------------------')
    print('SELECT * FROM history(table) WHERE metadata.id = ', docId)
    print('--------------------------------------------------------------------------------------------')

    specific = Query('shell_test').history(id=docId)

    for record in specific:
        pprint(vars(record))
        pprint(vars(record.metadata))
        print('-------------------------------------')
