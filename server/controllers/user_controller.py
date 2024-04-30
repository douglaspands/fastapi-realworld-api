from fastapi import APIRouter

from server.resources.user_resources import User
from server.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/v1/users/", response_model=list[User])
async def get_users():
    return await user_service.get_users()


@router.get("/v1/users/{pk}", response_model=User)
async def get_user():
    return await user_service.get_users()


@router.post("/v1/users/", response_model=User)
async def create_user():
    return await user_service.get_users()


# @router.put("/v1/users/{pk}", response_model=User)
# async def update_user(pk: int):
#     return await user_service.get_users()


# @router.delete("/v1/users/{pk}")
# async def remove_user(pk: int):
#     await user_service.get_users()


__all__ = ("router",)
