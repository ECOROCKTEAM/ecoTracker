import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.group.score import GroupScoreDTO
from src.core.enum.group.privacy import GroupPrivacyEnum
from src.core.enum.score.operation import ScoreOperationEnum
from src.data.models.group.group import GroupModel, GroupScoreModel


# pytest tests/main/challenges/mission/test_mission_user_update.py::test_group_score_counting_ok -v -s
@pytest.mark.asyncio
async def test_group_score_counting_ok(session: AsyncSession):
    group = GroupModel(name="Test group name", description="", active=True, privacy=GroupPrivacyEnum.PUBLIC)

    session.add(group)
    await session.flush()

    group_score_1 = GroupScoreModel(
        group_id=group.id, operation=ScoreOperationEnum.PLUS, value=10, mission_totaly_completed=1
    )
    group_score_2 = GroupScoreModel(
        group_id=group.id, operation=ScoreOperationEnum.PLUS, value=10, mission_totaly_completed=1
    )
    group_score_3 = GroupScoreModel(
        group_id=group.id, operation=ScoreOperationEnum.MINUS, value=10, mission_totaly_completed=1
    )

    group_score_list = [group_score_3, group_score_2, group_score_1]

    session.add_all([group_score_1, group_score_2, group_score_3])
    await session.commit()

    asrt_mission_total_count = 0
    asrt_total_value = 0
    for group_score in group_score_list:
        if group_score.operation == ScoreOperationEnum.PLUS:
            asrt_mission_total_count += group_score.mission_totaly_completed
            asrt_total_value += group_score.value
        if group_score.operation == ScoreOperationEnum.MINUS:
            asrt_mission_total_count -= group_score.mission_totaly_completed
            asrt_total_value -= group_score.value

    group_rating = GroupScoreDTO(group_id=group.id, value=0, mission_totaly_completed=0)

    stmt = select(GroupScoreModel).where(GroupScoreModel.group_id == group.id)
    res = await session.scalars(statement=stmt)

    for record in res:
        if record.operation == ScoreOperationEnum.PLUS:
            group_rating.mission_totaly_completed += record.mission_totaly_completed
            group_rating.value += record.value
        if record.operation == ScoreOperationEnum.MINUS:
            group_rating.mission_totaly_completed -= record.mission_totaly_completed
            group_rating.value -= record.value

    assert asrt_mission_total_count == group_rating.mission_totaly_completed
    assert asrt_total_value == group_rating.value

    await session.delete(group_score_1)
    await session.delete(group_score_2)
    await session.delete(group_score_3)
    await session.commit()

    await session.delete(group)
    await session.commit()
