import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(TEST_DIR)
sys.path.append(APP_DIR)

import pytest
from qldb import Strut, Ledger

@pytest.mark.parametrize('kwargs,keys,values',[
  ({'a':'b'},['a'], ['b']),
  ({'dog': 'woof', 'cat': 'meow', 'whale': 'waa'}, ['dog', 'cat', 'whale'], ['woof', 'meow', 'waa'])
])
def test_strut(kwargs,keys,values):
  keywords = vars(Strut(**kwargs))
  assert all([ keywords[act_key] == exp_val for act_key, exp_key, exp_val in zip(keywords.keys(), keys, values)])

