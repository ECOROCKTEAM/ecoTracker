from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.http.api.depends.deps import get_user_stub

router = APIRouter()


@router.get(
    "/me",
)
async def user_me(user: Annotated[User, Depends(get_user_stub)]) -> User:
    return user
