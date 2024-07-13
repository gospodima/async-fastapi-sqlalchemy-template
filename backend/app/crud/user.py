from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.user as schemas_user
from app.crud.utils import is_object_unique
from app.models.user import UserDB
from app.utils.auth import get_password_hash, verify_password


async def check_user_unique(
    session: AsyncSession,
    user_in: schemas_user.UserBase | schemas_user.UserUpdateMe,
    exclude_id: int | None = None,
) -> None:
    if not await is_user_unique(session, user_in, exclude_id):
        raise HTTPException(
            status_code=400,
            detail="The user with the given email or username already exists.",
        )


async def is_user_unique(
    session: AsyncSession,
    user_in: schemas_user.UserBase | schemas_user.UserUpdateMe,
    exclude_id: int | None = None,
) -> bool:
    return await is_object_unique(
        session,
        UserDB,
        user_in,
        unique_fields=("email", "username"),
        exclude_id=exclude_id,
    )


async def authenticate(
    session: AsyncSession, username: str, password: str
) -> UserDB | None:
    db_user = await get_user_by_username(session, username)
    if not (db_user and verify_password(password, db_user.hashed_password)):
        return None
    return db_user


async def get_user(session: AsyncSession, user_id: int) -> UserDB:
    user = await session.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


async def get_user_by_unique_field(
    session: AsyncSession, field: str, value: str
) -> UserDB | None:
    return (
        await session.scalars(select(UserDB).where(getattr(UserDB, field) == value))
    ).one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> UserDB | None:
    return await get_user_by_unique_field(session, "email", email)


async def get_user_by_username(session: AsyncSession, username: str) -> UserDB | None:
    return await get_user_by_unique_field(session, "username", username)


async def create_user(
    session: AsyncSession, user_in: schemas_user.UserCreate
) -> UserDB:
    db_obj = UserDB(
        **user_in.model_dump(exclude={"password"}),
        hashed_password=get_password_hash(user_in.password)
    )
    session.add(db_obj)
    return db_obj


async def delete_user(session: AsyncSession, user_id: int) -> None:
    await session.delete(await get_user(session, user_id))


async def update_user(
    session: AsyncSession,
    user_id: int,
    user_in: schemas_user.UserUpdate | schemas_user.UserUpdateMe,
) -> UserDB:
    user = await get_user(session, user_id)
    for key, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    return user
