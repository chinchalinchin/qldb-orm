EQUALS = "="
LIKE = "LIKE"
IN = "IN"

def where(operator, *columns):
  """Generates a **PartiQL** `WHERE` clause for an arbitrary number of columns with the specified argument.

  :param *columns: List of columns to include in the where clause.
  :type *columns: list
  :param operator: *Optional*. Operator to apply in the `WHERE` clause. Defaults to equality. Verbs are statically accessible through the `clauses.VERBS` dictionary.
  :return: `WHERE` clause
  :rtype: str
  """
  clause = None
  for column in columns:
    if clause is None:
      if operator == LIKE:
        clause = "WHERE {} {} '%?%' ".format(column, operator)
      else:
        clause = "WHERE {} {} ? ".format(column, operator)
    else:
      if operator == LIKE:
        clause += "AND {} {} '%?%' ".format(column, operator)
      else:
        clause += "AND {} {} ? ".format(column, operator)

  return clause

def set_statement(*columns):
  clause = None
  for column in columns:
    if clause is None:
      clause = 'SET {} = ? '.format(column)
    else:
      clause += ', {} = ? '.format(column)
  return clause