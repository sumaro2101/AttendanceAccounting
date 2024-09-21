from fastapi import APIRouter

from .views import router as time_filter


router = APIRouter(prefix='/api/v1')
router.include_router(time_filter)
