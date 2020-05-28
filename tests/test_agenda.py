import datetime
import os

import pytest

from todos.agenda import TimeBlock, CalendarEvent


class TestTimeBlock:
    @pytest.mark.parametrize(
        "start_hour, end_hour, expected_duration", [(3, 5, 2), (9, 8, -1)]
    )
    def test_get_duration(self, start_hour, end_hour, expected_duration):
        now = datetime.datetime.now()
        start_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        end_time = now.replace(hour=end_hour, minute=0, second=0, microsecond=0)
        tb = TimeBlock(start=start_time, end=end_time)
        assert tb.get_duration().total_seconds() == expected_duration * 60 * 60

    @pytest.mark.parametrize(
        "start_hour, end_hour, time_to_check, expected",
        [(9, 11, 10, True), (9, 10, 11, False), (19, 17, 18, False)],
    )
    def test_contains_time(self, start_hour, end_hour, time_to_check, expected):
        now = datetime.datetime.now()
        start_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        end_time = now.replace(hour=end_hour, minute=0, second=0, microsecond=0)
        tb = TimeBlock(start=start_time, end=end_time)
        check = now.replace(hour=time_to_check, minute=0, second=0, microsecond=0)
        assert tb.contains_time(check) == expected
