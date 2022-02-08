import os
from pprint import pprint

if __name__=="__main__":

    # NOTE: Point `innoldb` to the Ledger from which you are reading/writing through the environment
    os.environ['LEDGER'] = 'innolab'
    # NOTE: Import needs to come after environment variable has been set! The library will scan the environment
    #       on import and set the ledger. 
    from innoldb.qldb import Query

    the_first_query = Query('lab').all()

    # `find_by` accepts **kwargs arguments, so you can pass any field you want to query by directly into the method.
    the_second_query = Query('lab').find_by(team='InnoLab')

    # `find_in` accepts **kwargs arguments where each keyword is a list of values to compare the field against.
    # another_query = Query('lab').find_in(department=['InnoLab', 'Inno Lab'])

    # Document has extra attributes for meta data: (index, table, ledger). To hide them, call `fields()`
    print('SELECT * FROM TABLE')
    print('--------------------------------------------------------------------------------------------')
    for result in the_first_query:
        print(f'Document({result.id})')
        print('-----------------------')
        pprint(result.fields(),indent=5)
        print('\n')

    print('SELECT * FROM TABLE WHERE ? = ?')
    print('--------------------------------------------------------------------------------------------')
    for result in the_second_query:
        print(f'Document({result.id})')
        print('-----------------------')
        pprint(result.fields(), indent=5)
        print('\n')

    # for result in another_query:
    #     print(f'Document({result.id})')
    #     pprint(result.fields())
