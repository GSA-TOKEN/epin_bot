from fastapi import APIRouter
from .users import router as users_router
from .admin import router as admin_router
from .orders import router as orders_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(orders_router, prefix="/orders", tags=["orders"])
