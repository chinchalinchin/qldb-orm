import pytest
import innoldb.clauses as clauses

@pytest.mark.parametrize('columns,operator,expected_clause', [
  ([], clauses.OPERATORS.EQUALS, None),
  (['1'], clauses.OPERATORS.EQUALS,'WHERE 1 = ? '),
  (['a', 'b', 'c'], clauses.OPERATORS.EQUALS,'WHERE a = ? AND b = ? AND c = ? '),
  (['moe', 'curly', 'larry'], clauses.OPERATORS.EQUALS,'WHERE moe = ? AND curly = ? AND larry = ? '),
  (['Simon', 'Garfunkel'], clauses.OPERATORS.EQUALS, 'WHERE Simon = ? AND Garfunkel = ? '),
  ([], clauses.OPERATORS.LIKE, None),
  (['1'], clauses.OPERATORS.LIKE,'WHERE 1 LIKE ? '),
  (['a', 'b', 'c'], clauses.OPERATORS.LIKE,'WHERE a LIKE ? AND b LIKE ? AND c LIKE ? '),
  (['moe', 'curly', 'larry'], clauses.OPERATORS.LIKE,'WHERE moe LIKE ? AND curly LIKE ? AND larry LIKE ? '),
  (['Simon', 'Garfunkel'], clauses.OPERATORS.LIKE, 'WHERE Simon LIKE ? AND Garfunkel LIKE ? ')
])
def test_where(columns, operator, expected_clause):
  assert(clauses.where(operator, *columns) == expected_clause)