from amazon.ion.json_encoder import IonToJSONEncoder
from amazon.ion.simpleion import loads
import json

value = loads(
    '{data: annot::{foo: null.string, bar: (2 + 2)}, time: 1969-07-20T20:18Z}')
json_string = json.dumps(value, cls=IonToJSONEncoder)
print(json_string)
