from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from server.core.context import Context
from server.core.database import get_sessionio
from server.core.settings import get_settings
from server.repositories import user_repository
from server.resources.token_resource import Token

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/v1/token")

credentials_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pass_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pass_context.hash(password)


async def authenticate_user(ctx: Context, username: str, password: str) -> Token:
    users = await user_repository.get_all(
        session=ctx.session, limit=1, username=username, active=True
    )
    if not users:
        raise credentials_error
    user = users[0]
    if not verify_password(plain_password=password, hashed_password=user.password):
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
            users = await user_repository.get_all(
                session=session, limit=1, username=username, active=True
            )
            if not (users and users[0].active):
                raise credentials_error
            yield Context(session=session, user=users[0])
            break
    except JWTError:
        raise credentials_error


__all__ = ("check_access_token", "authenticate_user", "get_password_hash")
