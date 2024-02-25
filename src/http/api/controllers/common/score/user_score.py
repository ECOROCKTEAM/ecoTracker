from typing import Annotated

from fastapi import APIRouter, Depends

from src.core.entity.user import User
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.score.user.user_get_score import UserGetScoreUsecase
from src.http.api.depends.stub import get_uow_stub, get_user_stub
from src.http.api.schemas.score.user import UserScoreSchema

router = APIRouter()


@router.get("/")
async def user_score_get(
    user: Annotated[User, Depends(get_user_stub)],
    uow: Annotated[IUnitOfWork, Depends(get_uow_stub)],
) -> UserScoreSchema:
    uc = UserGetScoreUsecase(uow=uow)
    result = await uc(user=user)
    return UserScoreSchema.from_obj(score=result.item)
