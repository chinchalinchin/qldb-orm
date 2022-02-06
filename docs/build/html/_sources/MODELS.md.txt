# Document Object Model

This library abstracts much of the QLDB implementation away from its user. All the user has to do is create a `Document` object, add fields to it and then call `save()`. Under the hood, the library will translate the `Document` fields into [PartiQL queries](https://partiql.org/docs.html) and use the [pyqldb Driver](https://amazon-qldb-driver-python.readthedocs.io/en/stable/index.html) to post the queries to the **QLDB** instance on AWS.

**NOTE**: All documents are indexed through the key field `id`. 

## Saving

If you have the **LEDGER** environment variable set, all that is required is to create a `Document` object and pass it the table name from the **QLDB** ledger. If the following lines are feed into an interactive **Python** shell or copied into a script,

```python
from innoldb.qldb import Document

my_document = Document('table-name')
my_document.property_one = 'property 1'
my_document.property_two = 'property 2'
my_document.save()
```

Then a document will be inserted into the **QLDB** ledger table. If you do not have the **LEDGER** environment variable set, you must pass in the ledger name along with the table name through named arguments,

```python
from innoldb.qldb import Document

my_document = Document(table='table-name', ledger='ledger-name')
my_document.property_one = 'property 1'
my_document.property_two = 'property 2'
my_document.save()
```

**NOTE**: The `Document` class will auto-generate a UUID for each document inserted into the ledger table. 

Congratulations! You have saved a document to QLDB!

## Loading

To load a document that exists in the ledger table already, pass in the id of the `Document` when creating a new instance,

```python
from innoldb.qldb import Document

my_document(table='table-name', id='12345')
print(my_document.property_one)
```

## Updating

Updating and saving are different operations, in terms of the **PartiQL** queries that implement these operations, but from the `Document`'s perspective, they are the same operation; the same method is called in either case. The following script will save a value of `test 1` to `field` and then overwrite it with a value of `test 2`,

```python
from innoldb.qldb import Document

my_document = Document('table-name')
my_document.field = 'test 1'
my_document.save()
my_document.field = 'test 2'
my_document.save()
```

Behind the scenes, whenever the `save()` method is called, a query is run to check for the existence of the given `Document`. If the `Document` doesn't exist, the library will create a new one. If the `Document` does exist, the library will overwrite the existing `Document`.

## Fields

The document fields can be returned as a `dict` through the `fields()` method. The following script will loop through the fields on an existing document with `id=test` and print their corresponding values,

```python
from innoldb.qldb import Document

my_document = Document(table='table-name', id='test')

for key, value in my_document.fields().items():
  print(key, '=', value)
```

# Query Object Model

Queries are represented as an object, `Query`. Each `Query` must be initialized with a `table` that it will run **PartialQL** queries against. All queries return a `list` of `Document` objects. 

## All

The following script queries the ledger table for all documents and prints a JSON representation of each document to screen,

```python
from innoldb.qldb import Document, Query

all_documents = Query('table-name').all()
for document in all_documents:
  print(document.fields())
```