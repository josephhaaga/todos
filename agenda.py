from dataclasses import dataclass
import datetime
import os
from typing import List

from app import create_app

rows, columns = os.popen("stty size", "r").read().split()
TERMINAL_WIDTH = int(columns)

today = datetime.datetime.now()
DAY_START = today.replace(hour=8, minute=0, second=0, microsecond=0)
DAY_END = today.replace(hour=21, minute=0, second=0, microsecond=0)


def generate_times(
    start_time: datetime, end_time: datetime, increment_in_minutes: int = 30
):
    """Returns a list of datetimes."""
    results = []
    for hour in range(end_time.hour, start_time.hour, -1):
        results += [
            datetime.time(hour=hour, minute=timestamp)
            for timestamp in reversed(range(0, 60, increment_in_minutes))
        ]
    return reversed(results)


@dataclass
class CalendarEvent:
    summary: str
    start_time: datetime.datetime
    end_time: datetime.datetime

    def get_duration(self) -> datetime.timedelta:
        return self.end_time - self.start_time


class Agenda:
    day = datetime.datetime.now()
    agenda = {time: [] for time in generate_times(DAY_START, DAY_END)}
    event_count = 0
    todo_count = 0

    def populate_events(self, calendar_events=[]):
        # TODO refactor this; it does not overwrite agenda completely, meaning subsequent calls to populate_events will corrupt the data
        # either make it declarative (pass in all events), or convert to add_event()
        for event in calendar_events:
            # If an event doesn't start on 0, 15, 30, 45, will it still show up?
            event_start_time = event.start_time
            event_end_time = event.end_time
            times_spent_in_event = generate_times(event_start_time, event_end_time)
            for time in times_spent_in_event:
                self.agenda[time] += [event.summary]
        self.event_count = len(calendar_events)
        self.calendar_events = calendar_events

    def print_agenda(self):
        print(self.day.strftime("%A %B %-m, %Y").center(TERMINAL_WIDTH // 2))
        for time, events in self.agenda.items():
            # TODOs should be printed in a different color than actual calendar events
            # current event/todo should blink!
            print(f'{time.strftime("%H:%M")} {", ".join(events)}')
        self.print_summary()

    def print_summary(self):
        print(
            f"You have {self.event_count} meetings today, totalling {self.calculate_total_time_in_meetings()}."
        )
        print(f"This leaves you with {self.calculate_free_time()} free time.")

    def calculate_total_time_in_meetings(self):
        return datetime.timedelta(
            seconds=sum(
                [event.get_duration().seconds for event in self.calendar_events]
            )
        )

    def calculate_free_time(self):
        minutes_in_day = DAY_END - DAY_START
        minutes_in_meetings = self.calculate_total_time_in_meetings()
        return minutes_in_day - minutes_in_meetings

    def fill_with_todos(self, todos: List):
        prioritizing_function = lambda x, y: 1
        todos_in_priority_order = sorted(todos, prioritizing_function)


def main():
    nine_am = datetime.datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    noon = datetime.datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    three_pm = datetime.datetime.now().replace(
        hour=15, minute=0, second=0, microsecond=0
    )
    six_pm = datetime.datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)

    calendar_events = [
        CalendarEvent("Some calendar event", nine_am, noon),
        CalendarEvent("Another calendar event", three_pm, six_pm),
    ]

    a = Agenda()
    a.populate_events(calendar_events)
    a.print_agenda()

    app = create_app()
    todos = app.todo_service.list()


if __name__ == "__main__":
    main()
