def where(*columns):
  """Generates a **PartiQL** `WHERE` clause for an arbitrary number of columns.

  :param *columns: List of columns to include in the where clause.
  :type *columns: list
  :return: `WHERE` clause
  :rtype: str
  """
  clause = None
  for column in columns:
    if clause is None:
      clause = "WHERE {} = ? ".format(column)
    else:
      clause += "AND {} = ? ".format(column)
  return clause