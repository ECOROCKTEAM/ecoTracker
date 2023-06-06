from fastapi import APIRouter, Depends, Path

from src.core.interfaces.unit_of_work import IUnitOfWork
from src.core.usecases.score.community.community_get_score import (
    CommunityGetScoreUseCase,
)
from src.http.api.depends import get_uow, get_user
from src.http.api.score.schemas.score import CommunityScoreDTO

router = APIRouter(tags=["Score community"])


@router.get(
    "/score/community/{id}",
    responses={
        200: {"model": CommunityScoreDTO, "description": "OK"},
        401: {"description": "User not active"},
        422: {"description": "Unprocessable Entity (WebDAV)"},
    },
    summary="Community score",
    response_model_by_alias=True,
)
async def score_community(
    id: int = Path(description="community identify"),
    user=Depends(get_user),
    uow: IUnitOfWork = Depends(get_uow),
) -> CommunityScoreDTO:
    """Get community score"""
    uc = CommunityGetScoreUseCase(uow=uow)
    result = await uc(community_id=id, user=user)
    return result.item
