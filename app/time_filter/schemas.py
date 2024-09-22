from datetime import datetime
from pydantic import BaseModel

from typing import Union


class SchemaTask1(BaseModel):
    input_start: datetime


class SchemaQueryFilter(BaseModel):
    """
    Схема вывода результата
    """
    state_name: str
    state_id: str
    id: int
    state_reason: str
    client_id: int
    group_id: int
    state_end: Union[int, None]
    info: dict
    reason_group: str
    state_start: int
    endpoint_id: int


class SchemaGetRecord(BaseModel):
    """
    Схема вывода записи
    """
    filtered_count: int
    state_id: Union[str, None]
