import uuid
from itertools import tee
from innoldb import settings
from innoldb.static.logger import getLogger
from innoldb.static.driver import Driver

log = getLogger('innoldb.qldb')

class Ledger():
  def __init__(self, table, ledger=settings.LEDGER):
    """Creates an instance of `innoldb.qldb.Ledger`. This class representation some basic configuration properties of the QLDB ledger.

    :param table: Name of the table onto which transactions will read and write.
    :type table: str
    :param ledger: Name of the ledger where tables are stored, defaults to `innoldb.settings.LEDGER`
    :type ledger: str, optional
    """
    self.table = table
    self.ledger = ledger
    self.index = 'id'

class Strut(object):
  def __init__(self, **kwargs):
    self.__dict__.update( kwargs )
    
class Document(Ledger):
  """A `innoldab.qldb.Document` object, representing an entry in an QLDB Ledger Table. 

  :param Ledger: Ledger configuration
  :type Ledger: :class:`Ledger`
  """

  def __init__(self, table, id=None, snapshot=None, ledger=settings.LEDGER):
    """Creates an instance of `innoldab.qldb.Document`. This call can be initialized in several states, depending on the parameters passed into the constructor. 

    1. **Constructor Arguments**: `table`
    2. **Constructor Arguments**: `table, id`
    3. **Constructor Arguments**: `table, snapshot`

    :param table: [description]
    :type table: [type]
    :param id: [description], defaults to None
    :type id: [type], optional
    :param snapshot: [description], defaults to None
    :type snapshot: [type], optional
    :param ledger: [description], defaults to settings.LEDGER
    :type ledger: [type], optional
    """
    super().__init__(table=table, ledger=ledger)
    if id is None:
      self.id = str(uuid.uuid1()) 
      if snapshot is not None:
        self._load(snapshot)
    elif id is not None:
      self.id = id
      if snapshot is None:
        self._exists(self.id, snapshot=True)
      else:
        self._load(snapshot)
    self._init_fixtures()

  def _init_fixtures(self):
    """Create the table and index on the **QLDB** ledger, if they do not already exist.
    """
    if self.table not in Driver.tables(self.ledger):
      try:
        Driver.create_table(Driver.driver(self.ledger), self.table)
        Driver.create_index(Driver.driver(self.ledger), self.table, self.index)
      except Exception as e:
        log.error(e)

  def _load(self, snapshot=None):
    """Parse the `snapshot` into `innoldab.qldb.Document` attributes.

    :param snapshot: Dictionary of attributes to append to self, defaults to None
    :type snapshot: dict, optional
    """
    if snapshot is not None:
      for key, value in snapshot.items():
        setattr(self, key, value)
      
  def _insert(self, document):
    """Insert a new `innoldab.qldb.Document` into the **QLDB** ledger table.

    :param document: Dictionary containing the fields to be inserted.
    :type document: dict
    :return: Dictionary containing `INSERT` response
    :rtype: dict
    """
    log.debug("Inserting DOCUMENT(%s = %s)", self.index, document[self.index])
    return dict(next(Driver.insert(Driver.driver(self.ledger), document, self.table), None))
  
  def _update(self, document):
    """Update an existing `innoldab.qldb.Document` on the **QLDB** ledger table.

    :param document: Dictionary containing the fields to be updated.
    :type document: dict
    :return: Dictionary containg `UPDATE` response
    :rtype: dict
    """
    log.debug("Updating DOCUMENT(%s = %s)", self.index, document[self.index])
    return dict(next(Driver.update(Driver.driver(self.ledger), document, self.table, self.index), None))

  def _get(self, id):
    """Retrieve an existing `innoldab.qldb.Document` from the **QLDB** ledger table.

    :param id: ID of the `innoldab.qldb.Document` to retrieve
    :type id: str
    :return: Dictionary containing the `SELECT` response
    :rtype: dict
    """
    log.debug("Returning DOCUMENT(%s = %s)", self.index, id)
    return dict(next(Driver.query_by_fields(Driver.driver(self.ledger), self.table, **{self.index: id}), None))
  
  def _exists(self, id, snapshot=False):
    """Check if a `innoldb.qldb.Document` exists in the **QLDB** ledger table.

    :param id: ID of the `innoldb.qldb.Document` whose existence is in question.
    :type id: str
    :param snapshot: Flag to persist values retrieved from existence query to object, defaults to False.
    :type snapshot: bool
    :return: True if exists, False otherwise
    :rtype: bool
    """
    log.debug("Checking existence of DOCUMENT(%s = %s)", self.index, id)
    result = Driver.query_by_fields(Driver.driver(self.ledger), self.table, **{self.index: id})
    first_it, second_it = tee(result)
    if next(first_it, None):
      if snapshot:
        self._load(dict(next(second_it)))
      return True
    return False

  def fields(self):
    """All of the `innoldb.qldb.Document` fields as a key-value dictionary.

    :return: `innoldb.qldb.Document` fields
    :rtype: dict
    """
    return {key: value for key, value in vars(self).items() if key not in ['table', 'driver', 'index', 'ledger']}

  def save(self):
    """Save the current value of the `innoldb.qldb.Document` fields to the **QLDB** ledger table.
    """
    fields = self.fields()
    log.debug("Saving DOCUMENT(%s = %s)", self.index, fields[self.index])
    if self._exists(fields[self.index]):
      self._update(fields)
    self._insert(fields)

class Query(Ledger):
  def __init__(self, table, ledger=settings.LEDGER):
    super().__init__(table=table, ledger=ledger)
  
  def _to_documents(self, results):
    return [ Document(table=self.table, snapshot=dict(result)) for result in results ]

  def all(self):
    """Return all `innoldb.qldb.Document` objects in the **QLDB** ledger table

    :return: List of `innoldb.qldb.Document`
    :rtype: list
    """
    return self._to_documents(Driver.query_all(Driver.driver(self.ledger), self.table))
  
  def find_by(self, **kwargs):
    """Filter `innoldab.qldb.Document` objects by the provided fields. This method accepts `**kwargs` arguments for the field name and values. The document fields must exactly match the fields provided in 

    :param kwargs: Fields by which to filter the query.
    :return: List of `innoldb.qldb.Document`
    :rtype: list
    """
    return self._to_documents(Driver.query_by_fields(Driver.driver(self.ledger), self.table, **kwargs))
  
  # DOESN'T WORK. The PartiQL driver won't parameterize LIKE queries the same way it will = queries.
  #   which is frustrating.
  def find_like(self, **kwargs):
    return self._to_documents(Driver.query_like_fields(Driver.driver(self.ledger), self.table, **kwargs))
