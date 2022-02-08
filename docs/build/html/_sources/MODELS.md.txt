# Document Object Model

This library abstracts much of the QLDB implementation away from its user. All the user has to do is create a `Document` object, add fields to it and then call `save()`. Under the hood, the library will translate the `Document` fields into [PartiQL queries](https://partiql.org/docs.html) and use the [pyqldb Driver](https://amazon-qldb-driver-python.readthedocs.io/en/stable/index.html) to post the queries to the **QLDB** instance on AWS.

.. note::
  All documents are indexed through the key field `id`. 

## Saving

If you have the **LEDGER** environment variable set, all that is required is to create a `Document` object and pass it the table name from the **QLDB** ledger. If the following lines are feed into an interactive **Python** shell or copied into a script,

```python
from innoldb.qldb import Document

my_document = Document('table_name')
my_document.property_one = 'property 1'
my_document.property_two = 'property 2'
my_document.save()
```

Then a document will be inserted into the **QLDB** ledger table. If you do not have the **LEDGER** environment variable set, you must pass in the ledger name along with the table name through named arguments,

```python
from innoldb.qldb import Document

my_document = Document(table='table_name', ledger='ledger_name')
my_document.property_one = 'property 1'
my_document.property_two = 'property 2'
my_document.save()
```

.. note::
The `Document` class will auto-generate a UUID for each document inserted into the ledger table. 

Congratulations! You have saved a document to QLDB!

## Loading

To load a document that exists in the ledger table already, pass in the id of the `Document` when creating a new instance,

```python
from innoldb.qldb import Document

my_document(table='table_name', id='12345')
print(my_document.property_one)
```

## Updating

Updating and saving are different operations, in terms of the **PartiQL** queries that implement these operations, but from the `Document`'s perspective, they are the same operation; the same method is called in either case. The following script will save a value of `test 1` to `field` and then overwrite it with a value of `test 2`,

```python
from innoldb.qldb import Document

my_document = Document('table_name')
my_document.field = 'test 1'
my_document.save()
my_document.field = 'test 2'
my_document.save()
print(my_document.id)
print(my_document.field)
```

Behind the scenes, whenever the `save()` method is called, a query is run to check for the existence of the given `Document`. If the `Document` doesn't exist, the library will create a new one. If the `Document` does exist, the library will overwrite the existing `Document`.

## Fields

The document fields can be returned as a `dict` through the `fields()` method. The following script will loop through the fields on an existing document with `id=test` and print their corresponding values,

```python
from innoldb.qldb import Document

my_document = Document(table='table_name', id='test')

for key, value in my_document.fields().items():
  print(key, '=', value)
```

## Native Object Attribute Nesting

A document returned in nested format,

```json
{
  "prop_1": {
    "prop_2": {
      "prop_3": {
        "prop_4" : 5
      }
    }
  }
}
```

is deserialized into nestable attributes on the `Document` object, i.e.

```python 
assert document.prop_1.prop_2.prop_3.prop_4 == 5
```

# Query Object Model

Queries are represented as an object, `Query`. Each `Query` must be initialized with a `table` that it will run **PartialQL** queries against. All queries return a `list` of `Document` objects. 

## All

The following script queries the ledger table for all documents and prints a JSON representation of each document to screen,

```python
from innoldb.qldb import Query

all_documents = Query('table_name').get_all()
for document in all_documents:
  print(document.fields())
```

## History

One of the unique features of **QLDB** is its *immutability*; as a result of its implementation, **QLDB** keeps a log of all transactions that have occured on a table. This features is accessible in **PartiQL** through the `history()` function in the query `SELECT * FROM history(table)`. The `Query` class provides a wrapper around this query that parses it into a collection of `Documents`, i.e. the transaction history is traversible in the same way a document model is,

```python
from innoldb.qldb import Query

transaction = Query('table_name').history()

for result in results:
  print(result.data)
  print(result.metadata)
```

## Find By

The `find_by()` method accepts `**kwarg` aruments for any of the fields you want to query by; Note, the query is filtering on equality, i.e. it searches for all documents where the fields exactly equal their specified values.

```python
from innoldb.qldb import Query

search_documents = Query('table_name').find_by(company='Makpar')
search_documents_kwargs = Query('table_name').find_by(**{ 'company' : 'Makpar', 'department': 'Innovation' })
```

## Find In

This method will execute a `SELECT* FROM table WHERE a in (?, ? ... ? )` **PartiQL** query. The `find_in` methods accepts `**kwarg` arguments for any of the fields you want to query by, where the values of each keyword are an array of values to search by. For example,

```python
from innoldb.qldb import Query

search_documents = Query('table_name').find_in(company=['Makpar','Company'], number=[1,2,3])
```

will execute the following query,

```sql
SELECT * FROM table_name WHERE company IN ('Makpar', 'Company') AND number IN (1, 2, 3)
```