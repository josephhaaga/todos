import datetime
import os

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


class Agenda:
    day = datetime.datetime.now()
    events = {time: [] for time in generate_times(DAY_START, DAY_END)}

    def populate_events(self, calendar_events=[]):
        print(self.events)
        for event in calendar_events:
            event_start_time = datetime.datetime.fromisoformat(
                event["start"]["dateTime"]
            )
            # If an event doesn't start on 0, 15, 30, 45, will it still show up?
            event_end_time = datetime.datetime.fromisoformat(event["end"]["dateTime"])
            times_spent_in_event = generate_times(event_start_time, event_end_time)
            for time in times_spent_in_event:
                self.events[time] += [event["summary"]]

    def print_agenda(self):
        print(self.day.strftime("%A %B %-m, %Y").center(TERMINAL_WIDTH // 2))
        for time, events in self.events.items():
            print(f'{time.strftime("%H:%M")} {", ".join(events)}')

    def fill_with_todos(self):
        pass


def main():
    calendar_events = [
        {
            "summary": "Some calendar event",
            "start": {
                "dateTime": "2020-05-29T09:00:00-04:00",
                "timeZone": "America/New_York",
            },
            "end": {
                "dateTime": "2020-05-29T10:00:00-04:00",
                "timeZone": "America/New_York",
            },
        },
        {
            "summary": "another calendar event",
            "start": {
                "dateTime": "2020-05-29T13:00:00-04:00",
                "timeZone": "America/New_York",
            },
            "end": {
                "dateTime": "2020-05-29T15:00:00-04:00",
                "timeZone": "America/New_York",
            },
        },
    ]
    a = Agenda()
    a.populate_events(calendar_events)
    a.print_agenda()


if __name__ == "__main__":
    main()
