from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.http.api.depends import get_fake_user

router = APIRouter(prefix="/auth")


@router.get(
    "/me",
    responses={},
)
async def user_me(
    user: User = Depends(get_fake_user),
):
    return user
