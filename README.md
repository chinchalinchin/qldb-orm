# QLDB Interface

A simple [Object-Relation-Mapping](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) for a serverless [AWS Quantum Ledger Database](https://docs.aws.amazon.com/qldb/latest/developerguide/what-is.html) backend. The user or process using this library must have an [IAM policy that allows access to QLDB](https://docs.aws.amazon.com/qldb/latest/developerguide/security-iam.html).


```python
from innoldb.qldb import Driver

QldbDriver('innolab-Dev-test').execute_lambda(lambda executor: executor.execute_statement('CREATE TABLE test'))
```

## Overview

1. Create QLDB ledger
2. Configure IAM user/role permissions
3. Create model

## Setup

1. Configure Environment

```shell
cp ./env/.sample.env ./env/.env
```

The environment variable **LEDGER** should point to the **QLDB** ledger 

2. Create Ledger

A **QLDB** CloudFormation template is available in the *cf* directory of this project. A script has been provided to post this template to **CloudFormation**, assuming your [AWS CLI has been authenticated and configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html). From the project root, execute the following script and specify the `<ledger-name>` to create a ledger on QLDB,

```shell
./scripts/qldb-stack --ledger <ledger-name>
```

**NOTE**: The `<ledger-name>` must match the value of the **LEDGER** environment variable. The name of the ledger that is stood up on AWS is passed to the library through this environment variable.

**NOTE**: This script has other optional arguments detailed in the comments of the script itself.

3. Configure User Permissions

TODO


4. Create Model


```python
from innoldb.qldb import Document

my_document = Document('table-name')
my_document.property_one = 'property 1'
my_document.property_two = 'property 2'
my_document.save()
```

You have saved a document to QLDB!

## References 
- [Amazon QLDB Python Driver Documentation](https://amazon-qldb-driver-python.readthedocs.io/en/stable/index.html)