import os

os.environ['LEDGER'] = 'innolab'

# Import needs to come after environment variable has been set!
from innoldb.qldb import Query, Document

query = Query('table_name').all()

for result in query:
    print(f'Document({result.id})')
    print(result.nested_field_2.panopticon)
