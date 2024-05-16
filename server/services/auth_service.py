from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from server.core.context import Context
from server.core.crypt import get_crypt
from server.core.database import SessionIO, get_sessionio
from server.core.settings import get_settings
from server.models.user_model import User
from server.repositories import user_repository
from server.resources.token_resource import Token
from server.resources.user_resource import User as UserResource

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/v1/token")

credentials_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

crypt = get_crypt()
settings = get_settings()


async def get_active_user_by_username(session: SessionIO, username: str) -> User | None:
    users = await user_repository.get_all(
        session=session, limit=1, username=username, active=True
    )
    if not users:
        return None
    return users[0]


async def authenticate_user(ctx: Context, username: str, password: str) -> Token:
    user = await get_active_user_by_username(session=ctx.session, username=username)
    if not user:
        raise credentials_error
    if not crypt.check_password(password=password, hashed_password=user.password):
        raise credentials_error
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.token_expire_minutes
    )
    access_token = jwt.encode(
        claims={"exp": expire, "sub": user.username},
        key=settings.token_secret_key,
        algorithm=settings.token_algorithm,
    )
    return Token(access_token=access_token)


async def check_access_token(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> AsyncGenerator[Context, Any]:
    try:
        async for session in get_sessionio():
            payload = jwt.decode(
                token=token,
                key=settings.token_secret_key,
                algorithms=[settings.token_algorithm],
            )
            username: str = payload.get("sub", "")
            if not username:
                raise credentials_error
            user = await get_active_user_by_username(session=session, username=username)
            if not user:
                raise credentials_error
            user_resource = UserResource(**user.model_dump())
            yield Context(session=session, user=user_resource, request=request)
    except JWTError:
        raise credentials_error


__all__ = ("check_access_token", "authenticate_user")
