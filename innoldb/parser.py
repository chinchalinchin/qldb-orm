class Parser():

  @staticmethod
  def set_parameter_string(n):
    """Generate a parameterized `SET` clause

    :param n: Number of parameters to include in clause.
    :type n: int
    """
    ""
    if isinstance(n, int) or isinstance(n, float):
      n = int(n)
      return 'SET ? '*n
    return None