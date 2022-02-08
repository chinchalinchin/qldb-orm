import os
from pprint import pprint

if __name__=="__main__":

    # NOTE: Point `innoldb` to the Ledger from which you are reading/writing through the environment
    os.environ['LEDGER'] = 'innolab'

    # NOTE: Import needs to come after environment variable has been set! The library will scan the environment
    #       on import and set the ledger. 
    from innoldb.qldb import Query, Document

    query = Query('shell_test').get_all()

    for result in query:
      pprint(result.fields())

    for result in query:
      hist = Query('shell_test').history(result.id)
      for data in hist:
        print(vars(data.metadata))
      