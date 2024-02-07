from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.http.api.depends.stub import get_user_stub
from src.http.api.schemas.user import UserSchema

router = APIRouter()


@router.get("/me")
async def user_me(user: Annotated[User, Depends(get_user_stub)]) -> UserSchema:
    return UserSchema.from_entity(user=user)
