import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.const.translate import DEFAULT_LANGUANGE
from src.core.dto.user.score import UserScoreDTO
from src.core.enum.score.operation import ScoreOperationEnum
from src.data.models.user.user import UserModel, UserScoreModel
from src.data.repository.score.user_score import score_model_to_entity


# pytest tests/main/challenges/task/test_task_user_update.py::test_task_user_update_totaly_completed -v -s
@pytest.mark.asyncio
async def test_task_user_update_totaly_completed(session: AsyncSession):
    user = UserModel(id="Punk", username="Test name", active=True, language=DEFAULT_LANGUANGE)
    session.add(user)
    await session.flush()

    user_score_1 = UserScoreModel(
        user_id=user.id,
        task_totaly_completed=1,
        mission_totaly_completed=0,
        value=10,
        operation=ScoreOperationEnum.PLUS,
    )
    user_score_2 = UserScoreModel(
        user_id=user.id,
        task_totaly_completed=0,
        mission_totaly_completed=1,
        value=10,
        operation=ScoreOperationEnum.PLUS,
    )
    user_score_3 = UserScoreModel(
        user_id=user.id,
        task_totaly_completed=1,
        mission_totaly_completed=0,
        value=10,
        operation=ScoreOperationEnum.MINUS,
    )

    user_score_list = [user_score_1, user_score_2, user_score_3]

    session.add_all([user_score_1, user_score_2, user_score_3])
    await session.commit()

    stmt = select(UserScoreModel).where(UserScoreModel.user_id == user.id)
    res = await session.scalars(statement=stmt)
    total_score = UserScoreDTO(user_id=user.id, value=0, task_totaly_completed=0, mission_totaly_completed=0)

    for record in res:
        if record.operation == ScoreOperationEnum.PLUS:
            total_score.task_totaly_completed += record.task_totaly_completed
            total_score.mission_totaly_completed += record.mission_totaly_completed
            total_score.value += record.value
        if record.operation == ScoreOperationEnum.MINUS:
            total_score.task_totaly_completed -= record.task_totaly_completed
            total_score.mission_totaly_completed -= record.mission_totaly_completed
            total_score.value -= record.value

    asrt_task_totaly_completed = 0
    asrt_mission_totaly_completed = 0
    asrt_value = 0

    for user_score in user_score_list:
        if user_score.operation == ScoreOperationEnum.PLUS:
            asrt_task_totaly_completed += user_score.task_totaly_completed
            asrt_mission_totaly_completed += user_score.mission_totaly_completed
            asrt_value += user_score.value
        elif user_score.operation == ScoreOperationEnum.MINUS:
            asrt_task_totaly_completed -= user_score.task_totaly_completed
            asrt_mission_totaly_completed -= user_score.mission_totaly_completed
            asrt_value -= user_score.value

    assert asrt_task_totaly_completed == total_score.task_totaly_completed
    assert asrt_mission_totaly_completed == total_score.mission_totaly_completed
    assert asrt_value == total_score.value

    await session.delete(user_score_1)
    await session.delete(user_score_2)
    await session.delete(user_score_3)
    await session.commit()

    await session.delete(user)
    await session.commit()
