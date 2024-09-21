from datetime import datetime
from pydantic import BaseModel


class SchemaTask1(BaseModel):
    input_start: datetime
