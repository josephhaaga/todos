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
    for hour in range(end_time.hour, start_time.hour - 1, -1):
        results += [
            datetime.datetime.now().replace(hour=hour, minute=timestamp)
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

    def happens_at(self, time: datetime.datetime) -> bool:
        if self.start_time <= time and self.end_time >= time:
            return True
        return False


class Agenda:
    day = datetime.datetime.now()
    events = []
    free_time_blocks = []

    def add_event(self, event: CalendarEvent) -> None:
        self.events += [event]

    def populate_events(self, calendar_events=[]):
        for event in calendar_events:
            self.add_event(event)

    def print_agenda(self):
        print(self.day.strftime("%A %B %-m, %Y").center(TERMINAL_WIDTH // 2))
        times = generate_times(DAY_START, DAY_END)
        for time in times:
            events_occurring_at_this_time = [
                event for event in self.events if event.happens_at(time)
            ]
            print(
                f'{time.strftime("%H:%M")} {", ".join([event.summary for event in events_occurring_at_this_time])}'
            )

        self.print_summary()

    def print_summary(self):
        print(
            f"You have {len(self.events)} meetings today, totalling {self.calculate_total_time_in_meetings()}."
        )
        print(f"This leaves you with {self.calculate_free_time()} free time.")

    def calculate_total_time_in_meetings(self):
        return datetime.timedelta(
            seconds=sum([event.get_duration().total_seconds() for event in self.events])
        )

    def calculate_free_time(self) -> int:
        minutes_in_day = DAY_END - DAY_START
        minutes_in_meetings = self.calculate_total_time_in_meetings()
        return minutes_in_day - minutes_in_meetings

    def get_blocks_of_free_time(self) -> List:
        return self.free_time_blocks

    def fill_with_todos(self, todos: List):
        print(
            f"Filling {self.calculate_free_time()} minutes of free time with Todo items"
        )
        blocks_of_free_time = self.get_blocks_of_free_time()
        items_added_to_agenda = 0
        for todo in todos:
            print(f"{todo}")
            for block in blocks_of_free_time:
                print(f" {block}")
                block_duration_in_hours = block["duration"].seconds // 3600
                if todo.estimate_in_hours < block_duration_in_hours:
                    self.add_event(
                        CalendarEvent(
                            summary=todo.title,
                            start_time=block["start"],
                            end_time=block["start"] + block["duration"],
                        )
                    )
                    items_added_to_agenda += 1
                    todos.remove(todo)
        print(f"Added {items_added_to_agenda} todo items to today's agenda")


def main():
    nine_am = datetime.datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    noon = datetime.datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    three_pm = datetime.datetime.now().replace(
        hour=15, minute=0, second=0, microsecond=0
    )
    six_pm = datetime.datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)

    morning_meeting = CalendarEvent("Some calendar event", nine_am, noon)
    afternoon_meeting = CalendarEvent("Another calendar event", three_pm, six_pm)

    calendar_events = [morning_meeting, afternoon_meeting]

    a = Agenda()
    a.populate_events(calendar_events)
    a.print_agenda()

    blocks = a.get_blocks_of_free_time()

    app = create_app()
    todos = app.todo_service.list()

    a.fill_with_todos(todos)
    a.print_agenda()


if __name__ == "__main__":
    main()
