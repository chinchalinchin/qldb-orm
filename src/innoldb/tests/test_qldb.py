import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(TEST_DIR)
sys.path.append(APP_DIR)

import pytest
from qldb import Strut, Ledger, Document, Driver

@pytest.mark.parametrize('kwargs,keys,values',[
  ({'a':'b'},['a'], ['b']),
  ({'dog': 'woof', 'cat': 'meow', 'whale': 'waa'}, ['dog', 'cat', 'whale'], ['woof', 'meow', 'waa'])
])
def test_strut(kwargs,keys,values):
  keywords = vars(Strut(**kwargs))
  assert all([ keywords[act_key] == exp_val for act_key, exp_key, exp_val in zip(keywords.keys(), keys, values)])

@pytest.mark.parametrize('table,ledger',[
  ('howdy','ho'),
  ('alas', 'poor yorick'),
  ('say what', 'again')
])
def test_ledger(table, ledger):
  assert Ledger(table, ledger).table == table and Ledger(table, ledger).ledger == ledger

# def test_document_driver(mocker):
#   driver_stub = mocker.stub(name='Driver.drive')
#   tables_stub = mocker.stub(name='Driver.tables')
#   table_stub = mocker.stub(name='Driver.create_table')
#   index_stub = mocker.stub(name='Driver.create_index')
#   Document(table='table', ledger='ledger')
#   assert driver_stub.call_count == 3
#   assert tables_stub.call_count == 1
#   assert table_stub.call_count == 1
#   assert index_stub.call_count == 1