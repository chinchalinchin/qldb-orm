# Command Line Usage

Installing the `innoldb` package puts a command line utility on your path. This tool allows you to query the QLDB ledger directly from the command line. 

The `--table` argument is required. Queries can be constructed against this table by passing in other arguments. See below for examples of the different queries.

Be sure to export the **LEDGER** environment variable before executing any of these commands,

```shell
export LEDGER='ledger-name'
```

## Find Document By ID

```shell
innoldb --table <table-name> --id <id>
```

## Find All Documents

```shell
innoldb --table <table-name> --all
```

## Generate New Mock Document

```shell
innoldb --table <table-name> --mock
```

## Update Field in Document

```shell
innoldb --table <table-name> --id <id> --update <field>=<value> <field>=<value> ...
```

## Insert Document

```shell
innoldb --table <table-name> --insert <field>=<value> <field>=<value> ...
```


### Full Specification

```shell
innoldb -h
usage: innoldb [-h] -tb TABLE [-ind INDEX] [-meta META] [-up [UPDATE ...]] [-in [INSERT ...]] [-fi [FIND ...]] [-lo] [-mo] [-uh] [-hst] [-al]

optional arguments:
  -h, --help            Show this help message and exit
  -tb TABLE, --table TABLE
                        Name of the table to query
  -ind INDEX, --index INDEX
                        Index ID of the document
  -meta META, --meta META
                        Meta ID of the document
  -up [UPDATE ...], --update [UPDATE ...]
                        Requires --id. Update fields with `KEY1=VAL1 KEY2=VAL2 ...`
  -in [INSERT ...], --insert [INSERT ...]
                        Create document with fields `KEY1=VAL1 KEY2=VAL2 ...`
  -fi [FIND ...], --find [FIND ...]
                        Query by field equality `KEY1=VAL1 KEY2=VAL2...`
  -lo, --load           Requires --id. Load a document by index.
  -mo, --mock           Create a new mock document
  -uh, --unhide         Show hidden document fields
  -hst, --history       Requires --meta. Retrieve document history by 'meta.id'.
  -al, --all            Query all documents
```