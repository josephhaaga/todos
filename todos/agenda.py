from dataclasses import dataclass
import datetime
from typing import List, Union


@dataclass
class TimeBlock:
    start: datetime.datetime = None
    end: datetime.datetime = None

    def get_duration(self) -> datetime.timedelta:
        return self.end - self.start

    def contains_time(self, time: datetime.datetime) -> bool:
        return time <= self.end and time >= self.start


class CalendarEvent:
    time: TimeBlock
    title: str

    def __init__(
        self, title: str, start_time: datetime.datetime, end_time: datetime.datetime
    ):
        self.time = TimeBlock(start=start_time, end=end_time)
        self.title = title

    def conflicts_with(self, event: "CalendarEvent") -> bool:
        if self.time.contains_time(event.time.start) or self.time.contains_time(
            event.time.end
        ):
            return True
        if event.time.contains_time(self.time.start) or event.time.contains_time(
            self.time.end
        ):
            return True
        return False


class Agenda:
    date: datetime.date
    events: List[CalendarEvent] = []
    free_time: List[TimeBlock]

    def add_event(self, event: CalendarEvent):
        self.events += [event]
        # update `free_time`


def main():
    now = datetime.datetime.now()
    nine_am = now.replace(hour=9, minute=0, second=0, microsecond=0)
    noon = now.replace(hour=12, minute=0, second=0, microsecond=0)

    event = CalendarEvent("a meeting", nine_am, noon)

    # agenda = Agenda()
    # agenda.add_event(event)

    # todos = todo_service.list()
    # agenda.fill_free_time_with_todos(todos)


if __name__ == "__main__":
    main()
