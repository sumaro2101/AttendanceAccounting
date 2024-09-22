from datetime import datetime
from typing import Any
from loguru import logger

from app.utils import UTCTimeCast
from .schemas import SchemaTask1


def __get_microseconds_utc_0(time: datetime) -> int | None:
    """
    Dependency injection для прерабатывании времени
    в микросекунды
    """
    if time:
        time_utc = UTCTimeCast(input_time=time,
                               UTC=0,
                               )
        microseconds = time_utc.get_microseconds_off_UTC_time()
        return microseconds
    return


def get_microseconds_utc_3(time: SchemaTask1) -> int:
    """
    Dependency injection для прерабатывании времени
    в микросекунды
    """
    time_utc = UTCTimeCast(input_time=time.input_start,
                           UTC=-3,
                           )
    microseconds = time_utc.get_microseconds_off_UTC_time()
    return microseconds


def state_eq(state_start__eq: datetime | None = None):
    if state_start__eq:
            logger.info(f'{__name__} get value {state_start__eq}')
            microseconds = __get_microseconds_utc_0(state_start__eq)
            logger.info(f'{__name__} out value {microseconds}')
            return microseconds


def state_gt(state_start__gt: datetime | None = None):
    if state_start__gt:
            logger.info(f'{__name__} get value {state_start__gt}')
            microseconds = __get_microseconds_utc_0(state_start__gt)
            logger.info(f'{__name__} out value {microseconds}')
            return microseconds


def state_gte(state_start__gte: datetime | None = None):
    if state_start__gte:
        logger.info(f'{__name__} get value {state_start__gte}')
        microseconds = __get_microseconds_utc_0(state_start__gte)
        logger.info(f'{__name__} out value {microseconds}')
        return microseconds


def state_lt(state_start__lt: datetime | None = None):
    if state_start__lt:
        logger.info(f'{__name__} get value {state_start__lt}')
        microseconds = __get_microseconds_utc_0(state_start__lt)
        logger.info(f'{__name__} out value {microseconds}')
        return microseconds


def state_lte(state_start__lte: datetime | None = None):
        if state_start__lte:
            logger.info(f'{__name__} get value {state_start__lte}')
            microseconds = __get_microseconds_utc_0(state_start__lte)
            logger.info(f'{__name__} out value {microseconds}')
            return microseconds
