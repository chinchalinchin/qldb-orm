import pytest
import innoldb.static.clauses as clauses

@pytest.mark.parametrize('columns,operator,expected_clause', [
  ([], clauses.EQUALS, None),
  (['1'], clauses.EQUALS,'WHERE 1 = ? '),
  (['a', 'b', 'c'], clauses.EQUALS,'WHERE a = ? AND b = ? AND c = ? '),
  (['moe', 'curly', 'larry'], clauses.EQUALS,'WHERE moe = ? AND curly = ? AND larry = ? '),
  (['Simon', 'Garfunkel'], clauses.EQUALS, 'WHERE Simon = ? AND Garfunkel = ? '),
  ([], clauses.LIKE, None),
  (['1'], clauses.LIKE,'WHERE 1 LIKE ? '),
  (['a', 'b', 'c'], clauses.LIKE,'WHERE a LIKE ? AND b LIKE ? AND c LIKE ? '),
  (['moe', 'curly', 'larry'], clauses.LIKE,'WHERE moe LIKE ? AND curly LIKE ? AND larry LIKE ? '),
  (['Simon', 'Garfunkel'], clauses.LIKE, 'WHERE Simon LIKE ? AND Garfunkel LIKE ? ')
])
def test_where(columns, operator, expected_clause):
  assert(clauses.where(operator, *columns) == expected_clause)