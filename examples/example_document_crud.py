import os
from pprint import pprint

if __name__=="__main__":
  
    # NOTE: Point `qldb-orm` to the Ledger from which you are reading/writing through the environment
    # os.environ['LEDGER'] = 'innolab'

    # NOTE: Import needs to come after environment variable has been set!
    from qldb-orm.qldb import Document

    doc = Document('test_table')

    print('--------------------------------------------------------------------------------------------')
    print('CREATE DOCUMENT')
    print('--------------------------------------------------------------------------------------------')

    doc.nested_field_1 = {
        'title': 'behold',
        'number': 55,
        'why': True,
        'pets': [{'pet': 'cornelius', 'pet': 'oswaldo'}, {'pet': 'chewbacca'}],
        'panopticon': {
            'nest': {
                'title': 'a wise poem',
                'array': ['mary', 'had', 'a', 'little', 'lamb']
            }
        }
    }

    doc.nested_field_2 = {
        'title': 'wonderful',
        'number': 700,
        'why': 'I should say so',
        'panopticon': {
            'nest': {
                'array': ['a', 'list', 'of', 'things']
            }
        }
    }

    doc.save()

    pprint(doc.fields())
