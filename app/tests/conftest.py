import pytest
from datetime import datetime


@pytest.fixture(scope='class')
def input_time() -> datetime:
    """
    Фикстура с кастомным временем
    """
    output_time: datetime = datetime(year=2020,
                           month=10,
                           day=20,
                           hour=9,
                           minute=0,
                           )
    return output_time
