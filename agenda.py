import datetime
import os

rows, columns = os.popen("stty size", "r").read().split()
TERMINAL_WIDTH = int(columns)

DAY_START = 9
DAY_END = 22


class Agenda:
    day = datetime.datetime.now()

    def print_linear(self):
        print(self.day.strftime("%A %B %-m, %Y").center(TERMINAL_WIDTH // 2))
        for hour in range(DAY_START, DAY_END + 1):
            print(datetime.time(hour=hour).strftime("%H:%M"), end="\n\n")

    def print_perspective(self):
        print(self.day.strftime("%A %B %-m, %Y").center(TERMINAL_WIDTH // 2))
        current_hour = self.day.hour
        for hour in range(DAY_START, DAY_END + 1):
            pretty_hour = datetime.time(hour=hour).strftime("%H:%M")
            print(pretty_hour)
            difference = hour - current_hour
            if abs(hour - current_hour) < 2:
                print()
                print()


def main():
    a = Agenda()
    a.print_perspective()


if __name__ == "__main__":
    main()
