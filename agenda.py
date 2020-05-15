import datetime
import os

rows, columns = os.popen("stty size", "r").read().split()
TERMINAL_WIDTH = int(columns)

DAY_START = 6
DAY_END = 22


def generate_times(increment_in_minutes=15):
    """Returns a list of times."""
    results = []
    for hour in range(DAY_END, DAY_START, -1):
        results += [
            datetime.time(hour=hour, minute=timestamp)
            for timestamp in reversed(range(0, 60, increment_in_minutes))
        ]
    return results


class Agenda:
    day = datetime.datetime.now()
    events = {time: [] for time in generate_times()}

    def print_agenda(self):
        print(self.day.strftime("%A %B %-m, %Y").center(TERMINAL_WIDTH // 2))
        for hour in range(DAY_START, DAY_END + 1):
            print(datetime.time(hour=hour).strftime("%H:%M"), end="\n\n")

    def fill_with_todos(self):
        pass


def main():
    a = Agenda()
    a.print_agenda()


if __name__ == "__main__":
    main()
    times = generate_times()
