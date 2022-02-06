# Setup
### Overview
1. (Optional) Configure environment
2. Create **QLDB** Ledger
3. Configure IAM user/role permissions for ledger
4. Install library

### Steps

1. (Optional) Configure Environment

This library needs to be informed of the QLDB Ledger to write against on your AWS environment. There are several ways to configure the Ledger setting. 

Before you start a Python shell, export the**LEDGER** environment variable,

```shell
export LEDGER='ledger-name'
python
```

Alternatively, configure the variable directly in a Python script

```python
import os

os.environ['LEDGER'] = 'ledger=name'
```

The environment variable **LEDGER** should point to the **QLDB** ledger so the application knows to which ledger to write. If you do not configure the **LEDGER** environment variable, you will need to pass in the ledger name to the `Document` object. See [below](#documents) for more information.

2. Create a **QLDB** Ledger

Boto3 Client
------------

The easiest way to create a ledger is through the `boto3` wrapper function in `innoldb.qldb.Driver`,

```python
from innoldb.qldb import Driver

Driver.ledger('my-ledger')
```

**NOTE**: You must install the `innoldb` package from [PyPi](https://pypi.org/project/innoldb/) before creating a ledger this way. See *Step 4* for more information.

CloudFormation
--------------

A **QLDB** CloudFormation template is also available in the *cf* directory of this project's [Github](https://github.com/Makpar-Innovation-Laboratory/innoldb). A script has been provided to post this template to **CloudFormation**, assuming your [AWS CLI has been authenticated and configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html). Clone the repository and then from the project root, execute the following script and specify the `<ledger-name>` to create a ledger on the **QLDB** service,

```shell
./scripts/cf-stack --ledger <ledger-name>
```

**NOTE**: The `<ledger-name>` must match the value of the **LEDGER** environment variable. The name of the ledger that is stood up on AWS is passed to the library through this environment variable.

**NOTE**: This script has other optional arguments detailed in the comments of the script itself.

3. Configure User Permissions

In production, you will want to limit the permissions of the application client to the ledger and table to which it is authorized to read and write. For the purposes of using this library locally, you can add a blanket policy to your user account by [following the instructions here](https://docs.aws.amazon.com/qldb/latest/developerguide/getting-started.prereqs.html#getting-started.prereqs.permissions).

If you are configuring an application role to use this library for a particular ledger and table, you will need to scope the permissions using [this reference](https://docs.aws.amazon.com/qldb/latest/developerguide/getting-started-standard-mode.html).

4. Install `innoldb`

```shell
pip install innoldb
```