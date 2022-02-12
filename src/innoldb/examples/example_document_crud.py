import os

if __name__=="__main__":
  
    # NOTE: Point `innoldb` to the Ledger from which you are reading/writing through the environment
    os.environ['LEDGER'] = 'innolab'

    # NOTE: Import needs to come after environment variable has been set!
    from innoldb.qldb import Document

    # doc = Document('a_new_test')

    # doc.nested_field_1 = {
    #     'title': 'behold',
    #     'number': 55,
    #     'why': True,
    #     'pets': [{'pet': 'cornelius', 'pet': 'oswaldo'}, {'pet': 'chewbacca'}],
    #     'panopticon': {
    #         'nest': {
    #             'title': 'a wise poem',
    #             'array': ['mary', 'had', 'a', 'little', 'lamb']
    #         }
    #     }
    # }

    # doc.nested_field_2 = {
    #     'title': 'wonderful',
    #     'number': 700,
    #     'why': 'I should say so',
    #     'panopticon': {
    #         'nest': {
    #             'array': ['a', 'list', 'of', 'things']
    #         }
    #     }
    # }

    # doc.save()

    doc = Document("a_new_test", id='2cf98d228b9811ecb3c9b07d647734f0')

    doc.nested_field_1 = {
      'title': 'another_title',
      'content': 'new field',
      'testing': 'testing'
    }

    doc.save()
