from marshmallow import Schema, fields, pprint
from datetime import datetime as dt

class Todo:
    def __init__(self, title):
        self.title = title

    def start(self):
        self.started_at = dt.now()

class TagSchema(Schema):
    name = fields.Str(required=True)

class TodoSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str()
    started_at = fields.Date()
    tags = fields.List(fields.Nested(TagSchema()))


# t = Todo(title="finish this app")
# t.start()
# TodoSchema().dump(t)
