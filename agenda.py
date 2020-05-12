import datetime
import os

rows, columns = os.popen("stty size", "r").read().split()
TERMINAL_WIDTH = int(columns)

DAY_START = 9
DAY_END = 17


class Agenda:
    day = datetime.datetime.now()

    def print_today(self):
        print(self.day.strftime("%A %B %-m, %Y").center(TERMINAL_WIDTH // 2))
        for hour in range(DAY_START, DAY_END + 1):
            print(datetime.time(hour=hour).strftime("%H:%M"), end="\n\n")


def main():
    a = Agenda()
    a.print_today()


if __name__ == "__main__":
    main()
