from fastapi import APIRouter
from tortoise.expressions import Q, F, RawSQL
from tortoise.functions import Count

from .schemas import SchemaTask1
from app.config.db.models import EndpointState
from app.utils import UTCTimeCast


router = APIRouter(prefix='/time')

@router.post('/get-count-records/')
async def get_time(time: SchemaTask1):
    time_utc = UTCTimeCast(
        input_time=time.input_start,
        UTC=-12,
        )
    microseconds = time_utc.get_microseconds_off_UTC_time()

    response = (EndpointState.filter(Q(state_start__gte=microseconds) &
                                     Q(endpoint__id=139),
                                     id=RawSQL('endpoint_states.id % 3 + endpoint_states.id')).
                select_related('endpoint').
                order_by('-state_start'))
    result = await response.all()
    output = dict(filtered_count=len(result),
                  state_id=result[2].state_id,
                  )
    return output
