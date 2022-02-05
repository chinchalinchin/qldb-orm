# QLDB Interface

A simple [Object-Relation-Mapping](https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping) for a serverless [AWS Quantum Ledger Database](https://docs.aws.amazon.com/qldb/latest/developerguide/what-is.html) backend. The user or process using this library must have an [IAM policy that allows access to QLDB](https://docs.aws.amazon.com/qldb/latest/developerguide/security-iam.html).

## Overview

1. Create QLDB ledger
2. Configure IAM user/role permissions
3. Create model

## Setup

0. Configure Environment

```shell
cp ./env/.sample.env ./env/.env
```

The environment variable **LEDGER** should point to the **QLDB** ledger 

1. Create Ledger

A **QLDB** CloudFormation template is available in the *master* branch of *innolab-cloudformation*. From the *innolab-cloudformation* repository, execute the following script and specify the `<ledger-name>` to create a ledger on QLDB,

```shell
./scripts/stacks/serverless/qldb-stack --ledger <ledger-name>
```

2. Configure User Permissions

TODO


3. Create Model


## References 
- [Amazon QLDB Python Driver Documentation](https://amazon-qldb-driver-python.readthedocs.io/en/stable/index.html)