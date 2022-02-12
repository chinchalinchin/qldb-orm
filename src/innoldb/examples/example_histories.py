import os
from pprint import pprint

if __name__=="__main__":

    # NOTE: Point `innoldb` to the Ledger from which you are reading/writing through the environment
    os.environ['LEDGER'] = 'innolab'

    # NOTE: Import needs to come after environment variable has been set! The library will scan the environment
    #       on import and set the ledger. 
    from innoldb.qldb import Query, Document

    # print('--------------------------------------------------------------------------------------------')
    # print('SELECT * FROM table')
    # print('--------------------------------------------------------------------------------------------')

    query = Query('a_new_test').history()()

    for result in query:
      pprint(result.data)
      pprint(result.metadata)

      print('-----------------------------------------------------------')
      # print('SELECT * FROM history(table)')
      # print('-----------------------------------------------------------')
      # hist = Query('lab').history(result.id)
      # for data in hist:
      #   print('------------------------- RECORD')
      #   pprint(vars(data))
      #   print('------------------------- SNAPSHOT')
      #   pprint(vars(data.data))
      #   print('------------------------- METADATA')
      #   pprint(vars(data.metadata))
      