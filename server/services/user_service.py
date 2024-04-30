from typing import Any

from server.models.user_model import User
from server.repositories import user_repository


async def get_users(session: Any) -> list[User]:
    return await user_repository.get_all(session=session)
