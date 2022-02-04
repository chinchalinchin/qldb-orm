from qldb import Table
import settings

class Model():

  def __init__(self, name, index):
    self.name = name
    self.index = index
    self.table = Table(ledger=settings.LEDGER, table=self.name, index=self.index)

  