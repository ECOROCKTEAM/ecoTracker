from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.mock import MockObj
from src.core.dto.user.score import (
    OperationWithScoreUserDTO,
    UserBoundOffsetDTO,
    UserScoreDTO,
)
from src.core.entity.score import ScoreUser
from src.core.enum.score.operation import ScoreOperationEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.score.user import IRepositoryUserScore
from src.data.models.user.user import UserScoreModel
from src.utils import as_dict_skip_none


def rating_calculation(current_value: int, operated_value: int, operation: ScoreOperationEnum) -> int:
    if operation.PLUS:
        return current_value + operated_value
    elif operation.MINUS:
        return current_value - operated_value
    return current_value  # Если не сделать тут return, будет error, что на всех уровнях должно взвращаться int.
    #                     Typeignore?


def user_score_to_rating_list(rating_position: int, model: UserScoreModel) -> dict[int, UserScoreDTO]:
    return {rating_position: UserScoreDTO(user_id=model.user_id, value=model.value)}


def score_model_to_entity(model: UserScoreModel) -> ScoreUser:
    return ScoreUser(
        user_id=model.user_id,
        value=model.value,
        operation=model.operation,
    )


class UserScoreRepository(IRepositoryUserScore):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def change(self, *, obj: OperationWithScoreUserDTO) -> ScoreUser:
        stmt = select(UserScoreModel).where(UserScoreModel.user_id == obj.user_id)
        result = await self.db_context.scalar(stmt)
        if not result:
            raise EntityNotFound()
        new_rating = rating_calculation(current_value=result.value, operated_value=obj.value, operation=obj.operation)
        new_obj = ScoreUser(user_id=obj.user_id, value=new_rating, operation=obj.operation)
        new_stmt = (
            update(UserScoreModel)
            .where(UserScoreModel.user_id == obj.user_id)
            .values(**as_dict_skip_none(new_obj))
            .returning(UserScoreModel)
        )
        new_score = await self.db_context.scalar(new_stmt)
        if not new_score:
            raise EntityNotFound()
        return score_model_to_entity(model=new_score)

    async def user_get(self, *, user_id: int) -> ScoreUser:
        stmt = select(UserScoreModel).where(UserScoreModel.user_id == user_id)
        result = await self.db_context.scalar(stmt)
        if not result:
            raise EntityNotFound()
        return score_model_to_entity(model=result)

    async def user_rating(
        self, *, obj: UserBoundOffsetDTO | None = None, order_obj: MockObj
    ) -> dict[int, UserScoreDTO]:
        return await super().user_rating(obj=obj, order_obj=order_obj)

    # async def user_rating(
    #     self, *, obj: UserBoundOffsetDTO, order_obj: MockObj
    # ):
    #     stmt = select(UserScoreModel)
    #     if obj:
    #         stmt = stmt.where(UserScoreModel.user_id == obj.user_id).order_by(UserScoreModel.value).offset()
    #     result = await self.db_context.scalars(stmt)
    #     if not result:
    #         raise EntityNotFound()
    #     pass
