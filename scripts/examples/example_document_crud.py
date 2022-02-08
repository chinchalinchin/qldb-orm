import os

os.environ['LEDGER'] = 'innolab'

# Import needs to come after environment variable has been set!
from innoldb.qldb import Document

doc = Document('table_name')

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
