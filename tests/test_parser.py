import pytest
from app.parser import Parser

@pytest.mark.parametrize('n,expected_clause', [
                                                (2, 'SET ? SET ? '), 
                                                (3, 'SET ? SET ? SET ? '), 
                                                (4, 'SET ? SET ? SET ? SET ? '),
                                                (2.5, 'SET ? SET ? '),
                                                (3.75, 'SET ? SET ? SET ? '),
                                                (1.0001, 'SET ? '),
                                                (0, ''),
                                                ('asdf', None)
                                              ])
def test_set_string(n, expected_clause):
  assert Parser.set_parameter_string(n) == expected_clause