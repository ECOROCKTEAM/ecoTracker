from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.score.user.user_get_rating import UserGetRatingUsecase
from src.core.usecases.score.user.user_get_rating_top import UserGetRatingTopUsecase
from src.core.usecases.score.user.user_get_rating_window import (
    UserGetRatingWindowUsecase,
)
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.score.user import UserRatingListSchema, UserRatingSchema

router = APIRouter()


@router.get("/")
async def user_rating_get(
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
) -> UserRatingSchema:
    uc = UserGetRatingUsecase(uow=uow)
    result = await uc(user=user)
    return UserRatingSchema.from_obj(rating=result.item)


@router.get("/window")
async def user_rating_window_get(
    window_offset: int,
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
) -> UserRatingListSchema:
    uc = UserGetRatingWindowUsecase(uow=uow)
    result = await uc(user=user, window_offset=window_offset)
    return UserRatingListSchema.from_obj(rating_list=result.items)


@router.get("/top")
async def user_rating_top_get(
    size: int,
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
) -> UserRatingListSchema:
    uc = UserGetRatingTopUsecase(uow=uow)
    result = await uc(user=user, size=size)
    return UserRatingListSchema.from_obj(rating_list=result.items)
