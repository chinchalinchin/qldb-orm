# QLDB Implementation

## Overview

1. Create ledger
2. Configure user/role permissions
3. Create model

## Setup

0. Configure Environment

```shell
cp ./env/.sample.env ./env/.env
```

1. Create Ledger

From the *innolab-cloudformation* repository,

```shell
./scripts/stacks/serverless/qldb-stack --ledger <ledger-name>
```

2. Configure User Permissions

TODO


3. Create Model


## References 
- [Amazon QLDB Python Driver Documentation](https://amazon-qldb-driver-python.readthedocs.io/en/stable/index.html)