from flask.json.provider import JSONProvider
from datetime import datetime, date
import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            return super().default(obj)
        except TypeError:
            return str(obj)

class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, cls=CustomJSONEncoder, **kwargs)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)