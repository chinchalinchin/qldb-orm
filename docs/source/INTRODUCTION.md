# makpar-innolab

## innoldb

A simple [Object-Relation-Mapping](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) for a serverless [AWS Quantum Ledger Database](https://docs.aws.amazon.com/qldb/latest/developerguide/what-is.html) backend, and a command line utility for querying tables on those ledgers.

**NOTE**: The user or process using this library must have an [IAM policy that allows access to QLDB](https://docs.aws.amazon.com/qldb/latest/developerguide/security-iam.html).


### ORM

The idea behind the *ORM* is to map document fields to native Python object attributes, so that document values can be accessed by traversing the object property tree.

**CRUD OPERATIONS**

```python
from innoldb.qldb import Document

# Create a document on `my_table` table.
document = Document('my_table')
document.field = {
  'nested_data': {
    'array': ['colllection', 'of', 'things']
  }
}
document.save()
```

```python
from innoldb.qldb import Document

# Load a document from `my_table` table.
document = Document('my_table', id="123456")
for val in document.nested_data.array:
  print(val)
```

**Queries**
```python
from innoldb.qldb import Query

query = Query('my-table').find_by(field_name='field value')
for document in query:
  print(f'Document({document.id}).field_name = {document.field_name}')
```

### CLI

**CRUD Operations**
```shell
innoldb --table your-table --insert col1=val1 col2=val2 ...
innoldb --table your-table --id 123 --update col1=newval1 col2=newval2
```

**Queries**
```shell
innoldb --table your-table --find column=this
```

### Code Quality

- [![DeepSource](https://deepsource.io/gh/Makpar-Innovation-Laboratory/innoldb.svg/?label=active+issues&show_trend=true&token=0yUpU0SKBmqEg7qNHU2C65C6)](https://deepsource.io/gh/Makpar-Innovation-Laboratory/innoldb/?ref=repository-badge)
- [![DeepSource](https://deepsource.io/gh/Makpar-Innovation-Laboratory/innoldb.svg/?label=resolved+issues&show_trend=true&token=0yUpU0SKBmqEg7qNHU2C65C6)](https://deepsource.io/gh/Makpar-Innovation-Laboratory/innoldb/?ref=repository-badge)
