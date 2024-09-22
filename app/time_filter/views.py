from fastapi import (APIRouter,
                     Query,
                     HTTPException,
                     status,
                     Depends)
from tortoise.expressions import Q, RawSQL

from datetime import datetime
from typing import Annotated, Literal
from loguru import logger

from .schemas import SchemaTask1
from app.config.db.models import EndpointState
from .dependencies import (state_eq,
                           state_gt,
                           state_gte,
                           state_lt,
                           state_lte,
                           get_microseconds_utc_3,
                           )


router = APIRouter(prefix='/time',
                   tags=['search_data'],)

@router.post('/get-record/',
             name='Поиск данных по дате',
             description='Поиск нужного state_id по дате.')
async def get_time(time: SchemaTask1 = Depends(get_microseconds_utc_3)):
    """
    Вывод state_id по дате
    """
    response = (EndpointState.filter(Q(state_start__gte=time) &
                                     Q(endpoint__id=139),
                                     id=RawSQL(
                                         'endpoint_states.id % 3 + endpoint_states.id',
                                         )).
                select_related('endpoint').
                order_by('-state_start'))
    result = await response.all()
    output = dict(filtered_count=len(result),
                  state_id=result[2].state_id if result else None,
                  )
    return output


@router.get('/filter-records/',
            name='Фильтрация по дате',
            description='Фильтрация по дате с Query-параметрами',
            )
async def get_filtered_query(endpoint_id__eq: Annotated[int | None,
                                                        Query(ge=1)] = None,
                             state_name__eq: Literal['Вычисление',
                                                     'Приправка',
                                                     'Работа',
                                                     'Простой',
                                                     'Опоздание',
                                                     'Нерабочее время',
                                                     'Обед',
                                                     ] = Query(default=None),
                             state_reason__eq: Literal['Работа',
                                                       'Причина не указана',
                                                       'В туалете',
                                                       'Перекур',
                                                       'Вычисление',
                                                       'Опоздание',
                                                       'Короткая остановка',
                                                       'Приправка',
                                                       ] = Query(default=None),
                             state_start__eq: Annotated[datetime, Depends(state_eq)] = None,
                             state_start__gt: Annotated[datetime, Depends(state_gt)] = None,
                             state_start__gte: Annotated[datetime, Depends(state_gte)] = None,
                             state_start__lt: Annotated[datetime, Depends(state_lt)] = None,
                             state_start__lte: Annotated[datetime, Depends(state_lte)] = None,
                             ):
    """
    Энд поинт по фильтрации даты
    """    
    query_para = dict(endpoint_id=endpoint_id__eq,
                      state_name=state_name__eq,
                      state_reason=state_reason__eq,
                      state_start__eq=state_start__eq,
                      state_start__gt=state_start__gt,
                      state_start__gte=state_start__gte,
                      state_start__lt=state_start__lt,
                      state_start__lte=state_start__lte,
                      )
    logger.info(f'get {query_para}')
    clear_params = {key: value for key, value in query_para.items() if value}
    if not clear_params:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=dict(No_contains_Query_Parameters='Неоходимо указать хотяб один параметр'))
    logger.info(f'clear data {clear_params}')
    filtered_query = EndpointState.filter(**clear_params).order_by('-state_start').all()
    return await filtered_query
