from marshmallow import Schema, fields, pprint, post_load
from datetime import datetime as dt

from enum import Enum
import random

from todos.utils import pretty_print_date

Colors = Enum("Color", "RED GREEN YELLOW BLUE MAGENTA CYAN")
Status = Enum("Status", "NOT_STARTED IN_PROGRESS COMPLETED")


class Tag:
    def __init__(self, name, color=None):
        self.name = name.lower()
        self.color = color or random.choice(list(Colors)).name

    @post_load
    def make_tag(self, data, **kwargs):
        # TODO this may be redundant due to the constructor
        return Tag(**data)


class TagSchema(Schema):
    name = fields.Str(required=True)
    color = fields.Str()


class Note:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def pretty_print(self):
        return f"[{pretty_print_date(self.inserted_at)}] - {self.content}"


class NoteSchema(Schema):
    content = fields.Str()
    inserted_at = fields.DateTime()


class Todo:
    description = ""
    tags = []
    notes = []
    status = Status.NOT_STARTED.name
    estimate_in_hours = 1.0
    location = ""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_tag(self, tag):
        self.tags += [tag]

    def add_note(self, note):
        self.notes += [Note(content=note, inserted_at=dt.now())]

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

    def get_details(self):
        note_strings = "\n".join(
            ["\t" * 2 + Note(**n).pretty_print() for n in self.notes]
        )
        return f"""
    #{self.task_id} {self.title}
        status: {self.status}
        estimate: {self.estimate_in_hours}h
        inserted: {self.inserted_at}
        location: {self.location}

        notes
{note_strings}
        """


class TodoSchema(Schema):
    task_id = fields.Integer()
    title = fields.Str(required=True)
    description = fields.Str()
    location = fields.Str()
    status = fields.Str()
    inserted_at = fields.DateTime()
    estimate_in_hours = fields.Float()
    started_at = fields.DateTime()
    completed_at = fields.DateTime()
    tags = fields.List(fields.Nested(TagSchema()))
    notes = fields.List(fields.Nested(NoteSchema()))


def load_todo(task):
    task_id = task.doc_id
    return Todo(**TodoSchema().load({**task, "task_id": task_id}))


def dump_todo(todo):
    return TodoSchema().dump(todo)
