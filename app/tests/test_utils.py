import pytest
from datetime import datetime
from pydantic import ValidationError

from app.utils import UTCTimeCast


@pytest.mark.utc
class TestUTCTimeCast:
    """
    Тесты UTC конвертора
    """

    def test_duck_params(self, input_time):
        """
        Тесты не правильных значений
        """
        with pytest.raises(ValidationError):
            UTCTimeCast(input_time='some_string', UTC=10)
        with pytest.raises(ValidationError):
            UTCTimeCast(input_time=input_time, UTC=13)
        with pytest.raises(ValidationError):
            UTCTimeCast(input_time=input_time, UTC=-13)
        with pytest.raises(ValidationError):
            UTCTimeCast(input_time=input_time, UTC='some_string')

    def test_right_params(self, input_time):
        """
        Тест правильных значений
        """
        time_utc = UTCTimeCast(input_time=input_time,
                               UTC=3,
                               )

        assert str(time_utc) == '3'

    def test_output_time(self, input_time):
        """
        Тест вывода времени
        """
        time_utc = UTCTimeCast(input_time=input_time,
                               UTC=3,
                               )
        result: datetime = time_utc.get_UTC_set_time()

        assert result.hour == 6

    def test_microseconds(self, input_time):
        """
        Тест вывода микросекундр из времени
        """
        time_utc = UTCTimeCast(input_time=input_time,
                               UTC=3,
                               )
        microseconds: int = time_utc.get_microseconds_off_UTC_time()
        assert microseconds == 1603162800000
