import os
import sys
import argparse

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(TEST_DIR)
sys.path.append(APP_DIR)

import pytest
from main import KeyValue

@pytest.mark.parametrize('args,expected_keys,expected_props',[
  ('--test a=b c=d', ['a', 'c'], ['b','d']),
  ('--test spot=dog priscilla=cat barney=horse', ['spot', 'priscilla', 'barney'], ['dog', 'cat', 'horse'])
])
def test_keyvalue_parsing(args, expected_keys, expected_props):
  parser = argparse.ArgumentParser()
  parser.add_argument('--test', nargs='*', help="test", action=KeyValue)
  parsed_args = parser.parse_args(args.split(' '))
  assert all(parsed_args.test.get(key) == value for key, value in zip(expected_keys, expected_props))