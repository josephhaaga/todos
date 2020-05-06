from marshmallow import Schema, fields, pprint, post_load
from datetime import datetime as dt

from enum import Enum
import random


Colors = Enum("Color", "RED GREEN YELLOW BLUE MAGENTA CYAN")
Status = Enum("Status", "NOT_STARTED IN_PROGRESS COMPLETED")


class Tag:
    def __init__(self, name, color=None):
        self.name = name.lower()
        self.color = color or random.choice(list(Colors)).name

    @post_load
    def make_user(self, data, **kwargs):
        return Tag(**data)


class TagSchema(Schema):
    name = fields.Str(required=True)
    color = fields.Str()


class Todo:
    description = ""
    tags = []
    status = Status.NOT_STARTED.name
    estimate_in_hours = 1.0
    id = 1

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_tag(self, tag):
        self.tags += [tag]

    def set_description(self, description):
        self.description = description

    def set_estimate(self, estimate):
        self.estimate_in_hours = estimate

    def start(self):
        self.started_at = dt.now()
        self.status = Status.IN_PROGRESS.name

    def complete(self):
        self.completed_at = dt.now()
        self.status = Status.COMPLETED.name

    def __str__(self):
        return f"#{self.task_id} {self.title} @est({self.estimate_in_hours}h)" 

class TodoSchema(Schema):
    task_id = fields.Integer()
    title = fields.Str(required=True)
    description = fields.Str()
    status = fields.Str()
    inserted_at = fields.Date()
    estimate_in_hours = fields.Decimal()
    started_at = fields.Date()
    completed_at = fields.Date()
    tags = fields.List(fields.Nested(TagSchema()))

def load_todo(task):
    task_id = task.doc_id
    return Todo(**TodoSchema().load({**task, 'task_id': task_id}))

def dump_todo(todo):
    return TodoSchema().dump(todo)
