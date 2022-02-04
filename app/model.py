from qldb import Table
import settings
import uuid

class Model(Table):
  def __init__(self, name, id = uuid.uuid1()):
    super.__init__(ledger=settings.LEDGER, table=name)
    self.fields.id = id

  def save(self):
    pass

  # TODO: modify __get__ and __set__ so they point to super's fields prop.