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
    """Encoder object to deserialize `innoldb.static.objects.Strut` into string.

    """
    def default(self, obj):
        """Method to convert `innoldb.static.objects.Strut` into deserializable object. Overrides `json.default` and adds a check for `Strut` objects. 
        """
        if isinstance(obj, Strut):
            return vars(obj)
        return json.JSONEncoder.default(self, obj)