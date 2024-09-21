from fastapi import APIRouter

from .schemas import SchemaTask1
from app.config.db.models import Client


router = APIRouter(prefix='/time')

@router.post('/get-count-records/')
async def get_time(time: SchemaTask1):
    return await Client.filter().values()
