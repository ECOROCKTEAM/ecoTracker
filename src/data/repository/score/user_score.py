from dataclasses import asdict

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.core.dto.mock import MockObj
from src.core.dto.user.score import (
    OperationWithScoreUserDTO,
    UserBoundOffsetDTO,
    UserScoreDTO,
)
from src.core.entity.score import ScoreUser
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.score.user import IRepositoryUserScore
from src.data.models.user.user import UserScoreModel


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
        stmt = insert(UserScoreModel).values(**asdict(obj)).returning(UserScoreModel)
        result = await self.db_context.scalar(stmt)
        if not result:
            raise EntityNotFound()
        return score_model_to_entity(model=result)

    async def user_get(self, *, user_id: int) -> ScoreUser:
        stmt = select(UserScoreModel).where(UserScoreModel.user_id == user_id)
        result = await self.db_context.scalar(stmt)
        if not result:
            raise EntityNotFound()
        return score_model_to_entity(model=result)

    """ Как быть с тестами? Ждать дамба? Или вручную написать? """

    async def user_rating(self, *, obj: UserBoundOffsetDTO, order_obj: MockObj) -> list[UserScoreDTO]:
        inner_stmt = select(
            func.row_number().over(order_by=UserScoreModel.value).label("position"),
            UserScoreModel.user_id,
            UserScoreModel.value,
        ).select_from(UserScoreModel)
        subquery = inner_stmt.subquery()
        alias = aliased(UserScoreModel, subquery)
        user_position_stmt = select(subquery).where(alias.user_id == obj.user_id)
        result = await self.db_context.execute(user_position_stmt)
        result_values = result.first()

        if not result_values:
            raise EntityNotFound()

        position, user_id, value = result_values  # Мб сделать метод для этого дела: внизу ещё есть

        user_position = UserScoreDTO(
            user_id=user_id,
            value=value,
            position=position,
        )

        if (user_position.position - obj.bound_offset) <= 0:
            limit_obj = user_position.position + obj.bound_offset
            offset_obj = 0
        else:
            offset_obj = user_position.position - obj.bound_offset - 1
            limit_obj = (obj.bound_offset * 2) + 1

        stmt = (
            select(
                func.row_number().over(order_by=UserScoreModel.value).label("position"),
                UserScoreModel.user_id,
                UserScoreModel.value,
            )
            .select_from(UserScoreModel)
            .offset(offset_obj)
            .limit(limit_obj)
        )
        result = await self.db_context.execute(stmt)

        if not result:
            raise EntityNotFound()

        user_score_list: list[UserScoreDTO] = []
        for user_score in result:
            position, user_id, value = user_score
            user_score_list.append(UserScoreDTO(user_id=user_id, value=value, position=position))

        return user_score_list
