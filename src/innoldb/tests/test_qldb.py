from unittest.mock import patch
import pytest
import itertools
import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(TEST_DIR)
sys.path.append(APP_DIR)

from qldb import Document, Strut, QLDB, Query

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
    assert QLDB(table, ledger).table == table and QLDB(
        table, ledger).ledger == ledger


@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
def test_document_driver_init(mock_create_index, mock_create_table, mock_tables, mock_driver):
    document = Document(table='table', ledger='ledger')
    assert mock_driver.call_count == 2
    assert mock_tables.call_count == 1
    assert mock_create_table.call_count == 1
    assert mock_create_index.call_count == 1
    assert document.table == 'table'
    assert document.ledger == 'ledger'
    assert document.index == 'id'
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
def test_document_snapshot_nested_deserialization(mock_create_index, mock_create_table, mock_tables, mock_driver):
    document = Document(table='table', ledger='ledger', snapshot={
                        'test': { 
                          'test2': 'value' 
                        }
                })
    assert mock_driver.call_count == 2
    assert isinstance(document.test, Strut)
    assert document.test.test2 == 'value'


@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
def test_document_snapshot_nested_deserialization_more(mock_create_index, mock_create_table, mock_tables, mock_driver):
    document = Document(table='table', ledger='ledger', snapshot={
                        'test': { 
                          'test2': 'value', 'test3': 'another value', 'test4': 'yet another value' 
                        }
                })
    assert mock_driver.call_count == 2
    assert isinstance(document.test, Strut)
    assert document.test.test2 == 'value'
    assert document.test.test3 == 'another value'
    assert document.test.test4 == 'yet another value'


@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
def test_document_snapshot_nested_deserialization_one_layer(mock_create_index, mock_create_table, mock_tables, mock_driver):
    document = Document(table='table', ledger='ledger', snapshot={
                        'test_1': { 
                            'test_2': { 
                                'test_3': 45, 
                            }, 
                        }
                })
    assert mock_driver.call_count == 2
    assert isinstance(document.test_1, Strut)
    assert isinstance(document.test_1.test_2, Strut)
    assert document.test_1.test_2.test_3 == 45


@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
def test_document_snapshot_nested_deserialization_one_layer_more(mock_create_index, mock_create_table, mock_tables, mock_driver):
    document = Document(table='table', ledger='ledger', snapshot={
                        'test_1': { 
                            'test_2': { 
                                'test_3': 45, 
                                'test_4': 100,
                                'test_5': 'tester'
                            }, 
                        }
                })
    assert mock_driver.call_count == 2
    assert isinstance(document.test_1, Strut)
    assert isinstance(document.test_1.test_2, Strut)
    assert document.test_1.test_2.test_3 == 45
    assert document.test_1.test_2.test_4 == 100
    assert document.test_1.test_2.test_5 == 'tester'


@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
def test_document_snapshot_nested_deserialization_one_layer_complex(mock_create_index, mock_create_table, mock_tables, mock_driver):
    document = Document(table='table', ledger='ledger', snapshot={
                        'test_1': { 
                            'test_2': { 
                                'test_3': 45, 
                                'test_4': 100,
                                'test_5': 'tester'
                            }, 
                            'test_6': {
                              'test_7': 'will it work?'
                            },
                            'test_8': 'last but not least'
                        }
                })
    assert mock_driver.call_count == 2
    assert isinstance(document.test_1, Strut)
    assert isinstance(document.test_1.test_2, Strut)
    assert isinstance(document.test_1.test_6, Strut)
    assert document.test_1.test_2.test_3 == 45
    assert document.test_1.test_2.test_4 == 100
    assert document.test_1.test_2.test_5 == 'tester'
    assert document.test_1.test_6.test_7 == 'will it work?'
    assert document.test_1.test_8 == 'last but not least'


@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
def test_document_snapshot_nested_deserialization_big_mother(mock_create_index, mock_create_table, mock_tables, mock_driver):
    document = Document(table='table', ledger='ledger', snapshot={
                        'test_1': { 
                            'test_2': { 
                                'test_3': 45, 
                                'test_4': [ 'a', 'b', 'c'],
                                'test_5': {
                                  'test_6': {
                                    'test_7': 'succeeded'
                                  }
                                }
                            }, 
                        }, 
                        'test_a':{
                          'test_b':{
                            'test_c':{
                              'test_d': 6
                            }
                          }
                        }
                })
    assert mock_driver.call_count == 2
    assert isinstance(document.test_1, Strut)
    assert isinstance(document.test_1.test_2, Strut)
    assert isinstance(document.test_1.test_2.test_5, Strut)
    assert isinstance(document.test_1.test_2.test_5.test_6, Strut)
    assert isinstance(document.test_a, Strut)
    assert isinstance(document.test_a.test_b, Strut)
    assert isinstance(document.test_a.test_b.test_c, Strut)
    assert document.test_a.test_b.test_c.test_d == 6
    assert document.test_1.test_2.test_3 == 45
    assert document.test_1.test_2.test_4 == [ 'a', 'b', 'c']
    assert document.test_1.test_2.test_5.test_6.test_7 == 'succeeded'



@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
@patch('qldb.Driver.query_by_fields',
       return_value=itertools.cycle([]))
@patch('qldb.Driver.insert',
       return_value=itertools.cycle([{'property': 'value'}]))
def test_document_driver_save(mock_insert, mock_query, mock_create_index, mock_create_table, mock_tables, mock_driver):
    document = Document(table='table', ledger='ledger')
    document.test_field = 'test value'
    document.save()
    assert mock_driver.call_count == 4
    assert mock_query.call_count == 1
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
    assert mock_driver.call_count == 5
    assert mock_query.call_count == 2
    assert mock_update.call_count == 1

@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
def test_document_fields(mock_create_index, mock_create_table, mock_tables, mock_driver):
  document = Document(table='table', ledger='ledger', snapshot= {'test': 'prop', 'test2': 'prop2'})
  assert 'index' not in list(document.fields().keys())
  assert 'table' not in list(document.fields().keys())
  assert 'test' in list(document.fields().keys())
  assert 'test2' in list(document.fields().keys())
  assert 'prop' in list(document.fields().values())
  assert 'prop2' in list(document.fields().values())

def test_query_init():
  query = Query('table', 'ledger')
  assert query.table == 'table'
  assert query.ledger == 'ledger'
  assert query.index == 'id'
  
@patch('qldb.Driver.driver')
@patch('qldb.Driver.tables')
@patch('qldb.Driver.create_table')
@patch('qldb.Driver.create_index')
@patch('qldb.Driver.query_all',
       return_value=iter([{'property': 'value'}, {'money': 'moolah'}]))
def test_query_all(mock_all, mock_create_index, mock_create_table, mock_tables, mock_driver):
  query = Query('table', 'ledger').get_all()
  assert mock_driver.call_count == 5
  assert mock_create_index.call_count == 2
  assert mock_create_table.call_count == 2
  assert mock_tables.call_count == 2
  assert mock_all.call_count == 1
  assert len(query) == 2
  assert query[0].property == 'value'
  assert query[1].money == 'moolah'