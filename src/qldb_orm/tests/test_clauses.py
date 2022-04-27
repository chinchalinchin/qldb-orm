from static import clauses
import pytest
import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(TEST_DIR)
sys.path.append(APP_DIR)


@pytest.mark.parametrize('columns,expected_clause', [
    ([], None),
    (['1'], "WHERE 1 = ? "),
    (['a', 'b', 'c'], "WHERE a = ? AND b = ? AND c = ? "),
    (['moe', 'curly', 'larry'], "WHERE moe = ? AND curly = ? AND larry = ? "),
    (['Simon', 'Garfunkel'], "WHERE Simon = ? AND Garfunkel = ? ")
])
def test_where_equals(columns, expected_clause):
    assert clauses.where_equals(*columns) == expected_clause


@pytest.mark.parametrize('columns,ns,expected_clause', [
    (['a', 'b', 'c'], [1, 2, 3], "WHERE a IN (?) AND b IN (?,?) AND c IN (?,?,?) "),
    (['d', 'e'], [3, 2], "WHERE d IN (?,?,?) AND e IN (?,?) "),
    (['g'], [5], "WHERE g IN (?,?,?,?,?) ")
])
def test_where_in(columns, ns, expected_clause):
    column_numbers = {key: value for key, value in zip(columns, ns)}
    assert clauses.where_in(**column_numbers) == expected_clause


@pytest.mark.parametrize('columns,expected_clause', [
    ([], None),
    (['col'], 'SET col = ? '),
    (['col', 'row'], 'SET col = ? , row = ? '),
    (['col', 'row', 'hgt'], 'SET col = ? , row = ? , hgt = ? ')
])
def test_set_statement(columns, expected_clause):
    assert clauses.set_statement(*columns) == expected_clause
