import json

class Strut:
    """Simple object to parse `innoldb.qldb.Document`. Used to deserialize **QLDB** responses into Python native objects, with attributes accessible through object properties, i.e., the document
    ```json
    {
      'a': {
        'b' : {
          'c' : 'd'
        }
      }
    }
    ```
    gets parsed into an object, such that
    ```python
    object.a.b.c == 'd'
    ```
    """

    def __init__(self, **kwargs):
        """Pass in `**kwargs` to assign attributes to the object
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.__dict__.update(kwargs)

class StrutEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Strut):
            return vars(obj)
        return json.JSONEncoder.default(self, obj)