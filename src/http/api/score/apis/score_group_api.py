from fastapi import APIRouter, Depends, Path

from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.score.group.group_get_score import GroupGetScoreUsecase
from src.http.api.depends import get_uow, get_user
from src.http.api.score.schemas.score import GroupScoreDTO

router = APIRouter(tags=["Score group"])


@router.get(
    "/score/groups/{id}",
    responses={
        200: {"model": GroupScoreDTO, "description": "OK"},
        401: {"description": "User not active"},
        422: {"description": "Unprocessable Entity (WebDAV)"},
    },
    summary="Group score",
    response_model_by_alias=True,
)
async def score_group_get(
    id: int = Path(description="group identify"),
    user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> GroupScoreDTO:
    """Get Group score"""
    uc = GroupGetScoreUsecase(uow=uow)
    result = await uc(group_id=id, user=user)
    return result.item
