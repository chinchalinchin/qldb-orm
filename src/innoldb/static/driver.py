from pyqldb.driver.qldb_driver import QldbDriver
from innoldb.static.logger import getLogger
from innoldb.static import clauses

log = getLogger('innoldb.driver')


class Driver():
    @staticmethod
    def sanitize(query):
        """Remove escape characters from string

        :param query: Query that needs sanitized
        :type query: str
        :return: Sanitized query
        :rtype: str
        """
        for char in ["\\", "\'", "\"", "\b", "\n", "\r", "\t", "\0"]:
            query = query.replace(char, "")
        return query

    @staticmethod
    def execute(transaction_executor, statement, *params):
        r"""Static method for executing transactions with QLDB driver. 

        :param transaction_executor: Executor is injected into callback function through `pyqldb.driver.qldb_driver.execute_lambda` method.
        :param statement: Parameterized PartialQL query.
        :type statement: str
        :param \*params: Arguments for parameterized query.
        """
        sanitized_statement = Driver().sanitize(statement)
        if len(params) == 0:
            return transaction_executor.execute_statement(sanitized_statement)
        sanitized_params = [ Driver().sanitize(param) for param in params ]
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