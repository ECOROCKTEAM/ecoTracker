from fastapi import APIRouter, Depends, Path

from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.score.user.user_get_score import UserGetScoreUsecase
from src.http.api.depends import get_uow, get_user
from src.http.api.score.schemas.score import UserScoreDTO

router = APIRouter(tags=["Score user"])


@router.get(
    "/score/user/{id}",
    responses={
        200: {"model": UserScoreDTO, "description": "OK"},
        401: {"description": "User not active"},
        422: {"description": "Unprocessable Entity (WebDAV)"},
    },
    summary="User score",
    response_model_by_alias=True,
)
async def score_user_get(
    id: int = Path(description="user id"),
    user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> UserScoreDTO:
    """Get user score"""
    uc = UserGetScoreUsecase(uow=uow)
    result = await uc(user=user, id=id)
    return result.item
