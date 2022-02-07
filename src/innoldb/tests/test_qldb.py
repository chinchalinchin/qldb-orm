from qldb import Document, Strut, Ledger
from unittest.mock import patch
import pytest
import itertools
import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(TEST_DIR)
sys.path.append(APP_DIR)


@pytest.mark.parametrize('kwargs,keys,values', [
    ({'a': 'b'}, ['a'], ['b']),
    ({'dog': 'woof', 'cat': 'meow', 'whale': 'waa'}, [
        'dog', 'cat', 'whale'], ['woof', 'meow', 'waa'])
])
def test_strut(kwargs, keys, values):
    keywords = vars(Strut(**kwargs))
    assert all(act_key == exp_key and keywords[act_key] == exp_val
               for act_key, exp_key, exp_val in zip(keywords.keys(), keys, values))


@pytest.mark.parametrize('table,ledger', [
    ('howdy', 'ho'),
    ('alas', 'poor yorick'),
    ('say what', 'again')
])
def test_ledger(table, ledger):
    assert Ledger(table, ledger).table == table and Ledger(
        table, ledger).ledger == ledger


@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
def test_document_driver_init(mock_create_index, mock_create_table, mock_tables, mock_driver):
    document = Document(table='table', ledger='ledger')
    assert mock_driver.called
    assert mock_driver.call_count == 2
    assert mock_tables.called
    assert mock_tables.call_count == 1
    assert mock_create_table.called
    assert mock_create_table.call_count == 1
    assert mock_create_index.called
    assert mock_create_index.call_count == 1
    assert document.table == 'table'
    assert document.ledger == 'ledger'
    assert document.id is not None


@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
def test_document_snapshot(mock_create_index, mock_create_table, mock_tables, mock_driver):
    document = Document(table='table', ledger='ledger', snapshot={
                        'test': 'prop', 'test2': 'prop2'})
    assert mock_driver.call_count == 2
    assert document.test == 'prop'
    assert document.test2 == 'prop2'


@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
@patch('qldb.Driver.query_by_fields',
       return_value=itertools.cycle([{'property': 'value'}]))
@patch('qldb.Driver.insert',
       return_value=itertools.cycle([{'property': 'value'}]))
def test_document_driver_save(mock_insert, mock_query, mock_create_index, mock_create_table, mock_tables, mock_driver):
    document = Document(table='table', ledger='ledger')
    document.test_field = 'test value'
    document.save()
    assert mock_driver.call_count == 5
    assert mock_query.called
    assert mock_query.call_count == 1
    assert mock_insert.called
    assert mock_insert.call_count == 1


@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
@patch('qldb.Driver.query_by_fields',
       return_value=itertools.cycle([{'property': 'value'}]))
@patch('qldb.Driver.update',
       return_value=itertools.cycle([{'property': 'value'}]))
def test_document_driver_load(mock_update, mock_query, mock_create_index, mock_create_table, mock_tables, mock_driver):
    document = Document(table='table', ledger='ledger', id="test")
    document.save()
    assert mock_driver.call_count == 6
    assert mock_query.called
    assert mock_query.call_count == 2
    assert mock_update.called
    assert mock_update.call_count == 1
