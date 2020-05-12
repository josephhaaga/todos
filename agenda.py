import datetime

TERMINAL_WIDTH = 100

DAY_START = 9
DAY_END = 17


class Agenda:
    day = datetime.datetime.now()

    def print_today(self):
        print(self.day.strftime("%Y-%m-%d").center(TERMINAL_WIDTH // 2))
        for hour in range(DAY_START, DAY_END + 1):
            print(datetime.time(hour=hour).strftime("%H:%M"), end="\n\n")


def main():
    a = Agenda()
    a.print_today()


if __name__ == "__main__":
    main()
