import pytest
import innoldb.clauses as clauses

@pytest.mark.parametrize('columns,expected_clause', [
  ([], None),
  (['1'], 'WHERE 1 = ? '),
  (['a', 'b', 'c'], 'WHERE a = ? AND b = ? AND c = ? '),
  (['moe', 'curly', 'larry'], 'WHERE moe = ? AND curly = ? AND larry = ? '),
  (['Simon', 'Garfunkel'], 'WHERE Simon = ? AND Garfunkel = ? ')
])
def test_where(columns, expected_clause):
  assert(clauses.where(*columns) == expected_clause)