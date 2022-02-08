from json import loads, dumps
from amazon.ion.simple_types import IonPyDict
from amazon.ion.json_encoder import IonToJSONEncoder
from pyqldb.driver.qldb_driver import QldbDriver
from innoldb.static.logger import getLogger
from innoldb.static import clauses

log = getLogger('innoldb.driver')


class Driver():
    @staticmethod
    def down_convert(ion_obj):
        """Down nonvert an `amazon.ion` ION object

        :param ion_obj: an `Amazon.ion` object.
        :type ion_obj: [type]
        :return: JSON object
        :rtype: dict
        """
        return loads(dumps(ion_obj, cls=IonToJSONEncoder))

    @staticmethod
    def sanitize(obj):
        """Remove escape characters from data type

        :param query: Statement that needs sanitized
        :type query: str
        :return: Sanitized query
        """
        dict_flag, list_flag = False, False

        if isinstance(obj, (int, float)):
            return obj

        if isinstance(obj, (dict, IonPyDict)):
            dict_flag = True
            obj = dumps(obj, cls=IonToJSONEncoder)

        elif isinstance(obj, list):
            list_flag = True
            obj = "~~".join(str(param) for param in obj)

        for char in ["\\", "\'", "\"", "\b", "\n", "\r", "\t", "\0"]:
            if not dict_flag or not char == "\"":
                obj = obj.replace(char, "")

        if dict_flag:
            obj = loads(obj)

        elif list_flag:
            obj = obj.split("~~")

        return obj

    @staticmethod
    def execute(transaction_executor, statement, *params, unsafe=False):
        r"""Static method for executing transactions with QLDB driver. 

        :param transaction_executor: Executor is injected into callback function through `pyqldb.driver.qldb_driver.execute_lambda` method.
        :param statement: Parameterized PartialQL query.
        :type statement: str
        :param \*params: Arguments for parameterized query.
        """
        sanitized_statement = Driver().sanitize(statement)
        if len(params) == 0:
            log.debug(
                "Executing statement: \n\t\t\t\t\t\t\t %s \n", sanitized_statement)
            return transaction_executor.execute_statement(sanitized_statement)

        if unsafe:
            sanitized_params = params
        else:
            sanitized_params = tuple(Driver().sanitize(param) for param in params)
        log.debug(
            "Executing statement: \n\t\t\t\t\t\t\t %s \n\t\t\t\t\t\t\t parameters: %s \n", sanitized_statement, sanitized_params)
        return transaction_executor.execute_statement(sanitized_statement, *sanitized_params)

    @staticmethod
    def driver(ledger):
        """Static method for retrieving a QLDB driver

        :param ledger: Name of the ledger
        :type ledger: str
        :return: QLDB Driver
        :rtype: :class:`pyqldb.driver.qldb_driver.QldbDriver`
        """
        return QldbDriver(ledger_name=ledger)

    @staticmethod
    def query(driver, query, unsafe=False):
        return driver.execute_lambda(lambda executor: Driver.execute(executor, query, unsafe=unsafe))

    @staticmethod
    def tables(ledger):
        return QldbDriver(ledger_name=ledger).list_tables()

    @staticmethod
    def create_table(driver, table):
        """Static method for creating a table within a ledger

        :param driver: QLDB Driver
        :type driver: :class:`pyqldb.driver.qldb_driver.QldbDriver`
        :param table: table to be updated
        :type table: str
        :return: iterable containing result
        """
        # NOTE: I don't like directly formatting strings with query parameters that will
        # be run directly against the persistence layer (since malicious users could inject
        # bad parameters), but the driver won't parameterize `Create`` queries for some reason.
        # What follows is how the official documentation does it:
        # https://docs.aws.amazon.com/qldb/latest/developerguide/getting-started.python.step-3.html
        # NOTE: This is going to necessitate some logic in this library to prevent malicious strings from
        # gettings injected through parameters.
        statement = 'Create TABLE {}'.format(table)
        return driver.execute_lambda(lambda executor: Driver.execute(executor, statement))

    @staticmethod
    def create_index(driver, table, index):
        """Static method for generating an index on table

        :param driver: QLDB Driver
        :type driver: :class:`pyqldb.driver.qldb_driver.QldbDriver`
        :param table: table to be updated
        :type table: str
        :param index: index to search against
        :type index: str
        :return: iterable containing result
        """
        # NOTE: See above note.
        statement = 'CREATE INDEX on {} ({})'.format(table, index)
        return driver.execute_lambda(lambda executor: Driver.execute(executor, statement))

    @staticmethod
    def history(driver, table, index, id):
        statement = 'SELECT * FROM history({}) WHERE metadata.{} = ?'.format(table, index)
        return driver.execute_lambda(lambda executor: Driver.execute(executor, statement, id))

    @staticmethod
    def history_full(driver, table):
        statement = 'SELECT * FROM history({})'.format(table)
        return driver.execute_lambda(lambda executor: Driver.execute(executor, statement))

    @staticmethod
    def insert(driver, document, table):
        """Static method for inserting document into table

        :param driver: QLDB Driver
        :type driver: :class:`pyqldb.driver.qldb_driver.QldbDriver`
        :param document: document containing fields to insert
        :type document: dict
        :param table: table into which document is inserted
        :type table: str
        :return: iterable containing result
        """
        # NOTE: See above note.
        # TODO: check table string for malicious parameterization
        statement = 'INSERT INTO {} ?'.format(table)
        return driver.execute_lambda(lambda executor: Driver.execute(executor, statement, document))

    @staticmethod
    def update(driver, document, table, index):
        """Static method for updating QLDB table

        :param driver: QLDB Driver
        :type driver: :class:`pyqldb.driver.qldb_driver.QldbDriver`
        :param document: document to be updated
        :type document: dict
        :param table: name of the table where the document is
        :type table: dict
        :param index: name of the table index
        :type index: str
        :return: iterable containing result set
        """
        lookup = document[index]
        # NOTE: See notes in prior methods
        # TODO: check table string for malicious parameterization
        query = 'UPDATE {} as p SET p = ? WHERE {} = ?'.format(table, index)
        return driver.execute_lambda(lambda executor: Driver.execute(
            executor, query, document, lookup
        ))

    @staticmethod
    def query_all(driver, table):
        """Static method for querying table by field.

        :param driver: QLDB Driver
        :type driver: :class:`pyqldb.driver.qldb_driver.QldbDriver`
        :param field: field to be searched
        :type field: str
        :param value: search value
        :type value: str
        :param table: table to be quiered
        :type table: str
        :return: iterable containing result
        """
        statement = 'SELECT * FROM {}'.format(table)
        return driver.execute_lambda(lambda executor: Driver.execute(
            executor, statement
        ))

    @staticmethod
    def query_by_fields(driver, table, **fields):
        """Static method for querying table by field.

        :param driver: QLDB Driver
        :type driver: :class:`pyqldb.driver.qldb_driver.QldbDriver`
        :param fields: Keyword arguments. A dictionary containing the fields used to construct `WHERE` clause in query.
        :type fields: dict
        :type table: str
        :return: iterable containing result
        """
        columns, values = list(fields.keys()), list(fields.values())
        where_clause = clauses.where_equals(*columns)
        statement = 'SELECT * FROM {} {}'.format(table, where_clause)
        return driver.execute_lambda(lambda executor: Driver.execute(
            executor, statement, *values
        ))

    @staticmethod
    def query_in_fields(driver, table, **fields):
        """Static method for querying table where fields match a value in a collection

        :param driver: [description]
        :type driver: [type]
        :param table: [description]
        :type table: [type]

        ..note::
          ```python
          Driver().query_in_fields(driver, table, **{ 'a': ['b', 'c' , 'd'], '1': [ 2, 3, 4] })
          ```
          will search all documents where a field `a` has a value belonging to the set `('b', 'c', 'd')` *and* a field `1` whose value belongs to the set `(2, 3, 4)`.
        """
        column_numbers = {key: len(value) for key, value in fields.items()}
        where_clause = clauses.where_in(**column_numbers)

        unpacked_fields = []
        for value in fields.values():
            if isinstance(value, list):
                for subval in value:
                    unpacked_fields.append(subval)
            elif isinstance(value, (int, float, str)):
                unpacked_fields.append(value)

        statement = 'SELECT * FROM {} {}'.format(table, where_clause)
        return driver.execute_lambda(lambda executor: Driver.execute(
            executor, statement, *unpacked_fields
        ))
