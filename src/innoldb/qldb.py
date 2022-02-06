import uuid
from amazon.ion.simpleion import dumps, loads
from innoldb import settings
from innoldb.static.logger import getLogger
from innoldb.static.driver import Driver

log = getLogger('innoldb.qldb')

class Ledger():
  def __init__(self, table, ledger=settings.LEDGER):
    self.table = table
    self.ledger = ledger
    self.index = 'id'

class Document(Ledger):
  def __init__(self, table, id=None, snapshot=None, ledger=settings.LEDGER):
    super().__init__(table=table, ledger=ledger)
    if id is None:
      self.id = str(uuid.uuid1())        
    else:
      self.id = id
      snapshot = self.get(self.id)
  
    self._init_fixtures()
    self._load(snapshot)

  def _init_fixtures(self):
    if self.table not in Driver.tables(self.ledger):
      try:
        Driver.create_table(Driver.driver(self.ledger), self.table)
        Driver.create_index(Driver.driver(self.ledger), self.table, self.index)
      except Exception as e:
        log.error(e)

  def _load(self, snapshot=None):
    if snapshot is not None:
      for key, value in snapshot.items():
        setattr(self, key, value)
      
  def _insert(self, document):
    log.debug("Inserting DOCUMENT(%s = %s)", self.index, document[self.index])
    return Driver.insert(Driver.driver(self.ledger), document, self.table)
  
  def _update(self, document):
    log.debug("Updating DOCUMENT(%s = %s)", self.index, document[self.index])
    return Driver.update(Driver.driver(self.ledger), document, self.table, self.index)

  def exists(self, id):
    log.debug("Checking existence of DOCUMENT(%s = %s)", self.index, id)
    result = Driver.query_by_fields(Driver.driver(self.ledger), self.table, **{self.index: id})
    if next(result, None):
      return True
    return False

  def fields(self):
    return {key: value for key, value in vars(self).items() if key not in ['table', 'driver', 'index', 'ledger']}

  def get(self, id):
    log.debug("Returning DOCUMENT(%s = %s)", self.index, id)
    return loads(dumps(next(Driver.query_by_fields(Driver.driver(self.ledger), self.table, **{self.index: id }))))
  
  def save(self):
    fields = self.fields()
    log.debug("Saving DOCUMENT(%s = %s)", self.index, fields[self.index])
    if self.exists(fields[self.index]):
      return next(self._update(fields))
    return next(self._insert(fields))

class Query(Ledger):
  def __init__(self, table, ledger=settings.LEDGER):
    super().__init__(table=table, ledger=ledger)
  
  def _to_documents(self, results):
    return [ Document(table=self.table, snapshot=loads(dumps(result))) for result in results ]

  def all(self):
    return self._to_documents(Driver.query_all(Driver.driver(self.ledger), self.table))
  
  def find_by(self, **kwargs):
    return self._to_documents(Driver.query_by_fields(Driver.driver(self.ledger), self.table, **kwargs))
  
  def find_like(self, **kwargs):
    return self._to_documents(Driver.query_like_fields(Driver.driver(self.ledger), self.table, **kwargs))