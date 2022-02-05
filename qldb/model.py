from .qldb import Table
import uuid

class Model(Table):
  def __init__(self, name, id = str(uuid.uuid1())):
    super().__init__(table=name)
    self.id = id
    
  def save(self):
    super().save(vars(self))