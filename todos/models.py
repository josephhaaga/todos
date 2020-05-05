from marshmallow import Schema, fields, pprint
from datetime import datetime as dt

from enum import Enum
import random


Colors = Enum("Color", "RED GREEN YELLOW BLUE MAGENTA CYAN")
Status = Enum("Status", "NOT_STARTED IN_PROGRESS COMPLETED")

class Tag:
    def __init__(self, name):
        self.name = name.lower()
        self.color = random.choice(list(Colors)).name

class TagSchema(Schema):
    name = fields.Str(required=True)
    color = fields.Str()

class Todo:
    description = ''
    tags = []
    estimate_in_hours = 1.0
    def __init__(self, title):
        self.title = title
        self.inserted_at = dt.now()
        self.status = Status.NOT_STARTED.name
  
    def add_tag(self, tag):
        self.tags += [tag]

    def set_description(self, description):
        self.description = description

    def set_estimate(self, estimate):
        self.estimate = estimate
   
    def start(self):
        self.started_at = dt.now()
        self.status = Status.IN_PROGRESS.name

    def complete(self):
        self.completed_at = dt.now()
        self.status = Status.COMPLETED.name

class TodoSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str()
    inserted_at = fields.Date()
    estimate_in_hours = fields.Decimal()
    started_at = fields.Date()
    completed_at = fields.Date()
    tags = fields.List(fields.Nested(TagSchema()))
