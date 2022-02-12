import os
from pprint import pprint

if __name__=="__main__":

    # NOTE: Point `innoldb` to the Ledger from which you are reading/writing through the environment
    # os.environ['LEDGER'] = 'schema'

    # NOTE: Import needs to come after environment variable has been set! The library will scan the environment
    #       on import and set the ledger. 
    from innoldb.qldb import Query, Document

    print('--------------------------------------------------------------------------------------------')
    print('DOCUMENT STRANDS')
    print('--------------------------------------------------------------------------------------------')

    # `stranded==True` will initialize the document history under the `Document.strands` attribute `list`. Each 
    #  element of the list will be an object of type `innoldb.qldb.Document`
    doc = Document('test_table', id="7e1e93138bfd11ec8b4fb07d647734f0", stranded=True)
    print('----------------------------------------------------------- CURRENT DOCUMENT')
    pprint(vars(doc))
    for i, strand in enumerate(doc.strands):
      print('--------------------------- STRAND ', i)
      pprint(strand.fields())
        