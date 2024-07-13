from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.api.dependencies.db import SessionDep
from app.config import settings
from app.crud.user import get_user
from app.models.user import UserDB
from app.schemas.auth import TokenPayload
from app.utils.auth import ACCESS_TOKEN_ALGORITHM

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(session: SessionDep, token: TokenDep) -> UserDB:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise InvalidTokenError
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )
    user = await get_user(session, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user.")
    return user


CurrentUser = Annotated[UserDB, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> UserDB:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges."
        )
    return current_user
