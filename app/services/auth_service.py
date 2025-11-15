from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.infra.context import Context, IContext
from app.infra.crypt import get_crypt
from app.infra.database import get_sessionio
from app.infra.settings import get_settings
from app.models.user_model import User
from app.repositories import user_repository
from app.resources.token_resource import Token
from app.resources.user_resource import User as UserResource

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/v1/token")

credentials_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

crypt = get_crypt()
settings = get_settings()


async def get_active_user_by_username(ctx: IContext, *, username: str) -> User | None:
    users = await user_repository.get_all(ctx, limit=1, username=username, active=True)
    if not users:
        return None
    return users[0]


async def authenticate_user(ctx: IContext, username: str, password: str) -> Token:
    user = await get_active_user_by_username(ctx, username=username)
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
) -> AsyncGenerator[IContext, Any]:
    try:
        async with get_sessionio() as session:
            payload = jwt.decode(
                token=token,
                key=settings.token_secret_key,
                algorithms=[settings.token_algorithm],
            )
            username: str = payload.get("sub", "")
            user = await get_active_user_by_username(
                Context(session=session), username=username
            )
            if not (username and user):
                raise credentials_error
            user_resource = UserResource(**user.model_dump())
            yield Context(session=session, user=user_resource, request=request)
    except JWTError:
        raise credentials_error


__all__ = ("check_access_token", "authenticate_user")
