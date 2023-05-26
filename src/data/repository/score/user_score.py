from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

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


# def user_score_to_rating_list(rating_position: int, model: UserScoreModel) -> dict[int, UserScoreDTO]:
#     return {rating_position: UserScoreDTO(user_id=model.user_id, value=model.value)}


def user_rating_to_dto(model) -> UserScoreDTO:  # хз какой формат придёт после запроса. Дописать type hit в model
    return UserScoreDTO(
        user_id=model.user_id,
        value=model.value,
        position=model.position,
    )


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

    """ Как быть с тестами? Ждать дамба? Или вручную написать? Typehitting в функции к model аргументу """

    async def user_rating(self, *, obj: UserBoundOffsetDTO, order_obj: MockObj):
        inner_stmt = select(
            func.row_number().over(order_by=UserScoreModel.value),
            UserScoreModel.user_id,
            UserScoreModel.value,
        ).select_from(UserScoreModel)

        subquery = inner_stmt.subquery()
        alias = aliased(UserScoreModel, subquery)
        user_position_stmt = select(subquery).where(alias.user_id == obj.user_id)
        result = await self.db_context.scalar(user_position_stmt)
        if not result:
            raise EntityNotFound()

        user_position = user_rating_to_dto(result)

        if (user_position.position - obj.bound_offset) <= 0:
            limit_obj = obj.bound_offset + (obj.bound_offset - user_position.position) + 1
            offset_obj = 1
        else:
            offset_obj = user_position.position - obj.bound_offset
            limit_obj = (obj.bound_offset * 2) + 1

        stmt = (
            select(func.row_number().over(order_by=UserScoreModel.value), UserScoreModel.user_id, UserScoreModel.value)
            .select_from(UserScoreModel)
            .offset(offset_obj)
            .limit(limit_obj)
        )

        result = await self.db_context.scalars(stmt)
        return [user_rating_to_dto(model=model) for model in result]
