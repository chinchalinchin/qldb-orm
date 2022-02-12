import json
import os
from pprint import pprint

EX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(EX_DIR))), 'schemas')
VERSIONS= ['v1.0.0', 'v1.0.1', 'v1.0.2']

if __name__=="__main__":

    # NOTE: Point `innoldb` to the Ledger from which you are reading/writing through the environment
    os.environ['LEDGER'] = 'schema'

    # NOTE: Import needs to come after environment variable has been set! The library will scan the environment
    #       on import and set the ledger. 
    from innoldb.qldb import Document

    doc_id = None
    for version in VERSIONS:
        with open(os.path.join(SCHEMA_DIR, f'{version}.json'), 'r') as infile:
            schema = json.load(infile)
        doc = Document('version_control', id = doc_id, snapshot=schema)
        doc.save()
        doc_id = doc.id