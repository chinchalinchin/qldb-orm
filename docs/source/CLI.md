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
