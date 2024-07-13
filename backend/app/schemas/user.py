from pydantic import BaseModel, ConfigDict

from app.utils.decorators import partial_model


class UserBase(BaseModel):
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_superuser: bool = False
    is_active: bool = True


class UserPublic(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserCreate(UserBase):
    password: str


@partial_model
class UserUpdate(UserBase):
    pass


class UserUpdateMe(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    username: str | None = None


class UpdatePassword(BaseModel):
    current_password: str
    new_password: str
