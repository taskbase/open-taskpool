from fastapi import APIRouter
from .exercise_controller import router as exercise_router
from .healthcheck_controller import router as healthcheck_router

router = APIRouter()

router.include_router(exercise_router)
router.include_router(healthcheck_router)
