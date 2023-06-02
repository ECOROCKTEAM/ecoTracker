import asyncio
import random
from datetime import datetime, timedelta
from typing import AsyncGenerator
from uuid import uuid4

import faker
import pytest
import pytest_asyncio
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.database.base import (
    Base,
    create_async_engine,
    create_session_factory,
)
from src.application.settings import settings

# from src.core.dto.challenges.category import OccupancyCategoryDTO
from src.core.dto.community.invite import CommunityInviteDTO
from src.core.dto.m2m.user.community import UserCommunityDTO
from src.core.entity.community import Community
from src.core.entity.mission import Mission, MissionCommunity, MissionUser
from src.core.entity.score import ScoreCommunity, ScoreUser
from src.core.entity.user import User
from src.core.enum.challenges.status import OccupancyStatusEnum
from src.core.enum.community.privacy import CommunityPrivacyEnum
from src.core.enum.community.role import CommunityRoleEnum
from src.core.enum.language import LanguageEnum
from src.core.enum.score.operation import ScoreOperationEnum
from src.data.models.challenges.mission import MissionModel, MissionTranslateModel
from src.data.models.challenges.occupancy import (
    OccupancyCategoryModel,
    OccupancyCategoryTranslateModel,
)
from src.data.models.community.community import (
    CommunityMissionModel,
    CommunityModel,
    CommunityScoreModel,
)
from src.data.models.user.user import (
    UserCommunityModel,
    UserMissionModel,
    UserModel,
    UserScoreModel,
)

fake = faker.Faker()


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop

    pending = asyncio.tasks.all_tasks(loop)
    loop.run_until_complete(asyncio.gather(*pending))
    loop.run_until_complete(asyncio.sleep(1))

    loop.close()


@pytest_asyncio.fixture(scope="module")
async def pool() -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    engine = create_async_engine(url=settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    factory = create_session_factory(engine=engine)
    yield factory


@pytest_asyncio.fixture(scope="function")
async def session(pool: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with pool() as sess:
        yield sess


@pytest_asyncio.fixture(scope="module")
async def test_user(pool: async_sessionmaker[AsyncSession]) -> User:
    async with pool() as sess:
        user = UserModel(username="test", password="test", active=True)
        sess.add(user)
        await sess.commit()
        return User(
            username=user.username, password=user.password, active=True, id=user.id, language="", subscription=""  # type: ignore
        )


@pytest_asyncio.fixture(scope="module")
async def test_user_2(pool: async_sessionmaker[AsyncSession]) -> User:
    async with pool() as sess:
        user = UserModel(username="test-2", password="test", active=True)
        sess.add(user)
        await sess.commit()
        return User(
            username=user.username,
            password=user.password,
            active=True,
            id=user.id,
            language=LanguageEnum.RU,
            subscription="",  # type: ignore
        )


@pytest_asyncio.fixture(scope="module")
async def test_user_join_by_code(pool: async_sessionmaker[AsyncSession]) -> User:
    async with pool() as sess:
        user = UserModel(username="test-join_by_code", password="test", active=True)
        sess.add(user)
        await sess.commit()
        return User(
            username=user.username, password=user.password, active=True, id=user.id, language="", subscription=""
        )


@pytest_asyncio.fixture(scope="module")
async def test_user_join(pool: async_sessionmaker[AsyncSession]) -> User:
    async with pool() as sess:
        user = UserModel(username="test-join", password="test", active=True)
        sess.add(user)
        await sess.commit()
        return User(
            username=user.username, password=user.password, active=True, id=user.id, language="", subscription=""
        )


@pytest_asyncio.fixture(scope="module")
async def test_user_role(pool: async_sessionmaker[AsyncSession]) -> User:
    async with pool() as sess:
        user = UserModel(username="test-role", password="test-role", active=True)
        sess.add(user)
        await sess.commit()
        return User(
            username=user.username, password=user.password, active=True, id=user.id, language="", subscription=""  # type: ignore
        )


@pytest_asyncio.fixture(scope="module")
async def test_user_leave(pool: async_sessionmaker[AsyncSession]) -> User:
    async with pool() as sess:
        user = UserModel(username="test-user-leave", password="test-user-leave", active=True)
        sess.add(user)
        await sess.commit()
        return User(
            username=user.username, password=user.password, active=True, id=user.id, language="", subscription=""
        )


@pytest_asyncio.fixture(scope="module")
async def test_user_score(pool: async_sessionmaker[AsyncSession], test_user) -> ScoreUser:
    async with pool() as session:
        score_user = UserScoreModel(user_id=test_user.id, value=100, operation=ScoreOperationEnum.PLUS)
        session.add(score_user)
        await session.commit()
        return ScoreUser(user_id=score_user.user_id, value=score_user.value, operation=score_user.operation)


@pytest_asyncio.fixture(scope="module")
async def test_community_2(pool: async_sessionmaker[AsyncSession]) -> Community:
    async with pool() as sess:
        community = CommunityModel(
            name="test-com-2", description="test-com", active=True, privacy=CommunityPrivacyEnum.PRIVATE
        )
        sess.add(community)
        await sess.commit()
        return Community(
            name=community.name,
            description=community.description,
            active=True,
            id=community.id,
            privacy=community.privacy,
        )


@pytest_asyncio.fixture(scope="module")
async def test_community_delete(pool: async_sessionmaker[AsyncSession], test_user) -> Community:
    async with pool() as sess:
        community = CommunityModel(
            name="test-com-delete", description="test-com-delete", active=True, privacy=CommunityPrivacyEnum.PRIVATE
        )
        sess.add(community)
        await sess.flush()
        role = UserCommunityModel(user_id=test_user.id, community_id=community.id, role=CommunityRoleEnum.SUPERUSER)
        sess.add(role)
        await sess.commit()
        return Community(
            name=community.name,
            description=community.description,
            active=True,
            id=community.id,
            privacy=community.privacy,
        )


@pytest_asyncio.fixture(scope="module")
async def test_user_community(pool: async_sessionmaker[AsyncSession], test_user, test_community) -> UserCommunityDTO:
    async with pool() as sess:
        role = UserCommunityModel(
            user_id=test_user.id, community_id=test_community.id, role=CommunityRoleEnum.SUPERUSER
        )
        sess.add(role)
        await sess.commit()
    return UserCommunityDTO(user_id=role.user_id, community_id=role.community_id, role=role.role)


@pytest_asyncio.fixture(scope="module")
async def test_user_community_2(pool: async_sessionmaker[AsyncSession], test_user_2, test_community_2) -> None:
    async with pool() as sess:
        role = UserCommunityModel(
            user_id=test_user_2.id, community_id=test_community_2.id, role=CommunityRoleEnum.SUPERUSER
        )
        sess.add(role)
        await sess.commit()


@pytest_asyncio.fixture(scope="module")
async def test_user_community_change(pool: async_sessionmaker[AsyncSession], test_user_role, test_community) -> None:
    async with pool() as sess:
        role = UserCommunityModel(
            user_id=test_user_role.id, community_id=test_community.id, role=CommunityRoleEnum.USER
        )
        sess.add(role)
        await sess.commit()


@pytest_asyncio.fixture(scope="module")
async def test_user_community_leave(
    pool: async_sessionmaker[AsyncSession], test_user_leave, test_community
) -> UserCommunityModel:
    async with pool() as sess:
        role = UserCommunityModel(
            user_id=test_user_leave.id, community_id=test_community.id, role=CommunityRoleEnum.USER
        )
        sess.add(role)
        await sess.commit()
        return role


@pytest_asyncio.fixture(scope="module")
async def test_community_join_code(pool: async_sessionmaker[AsyncSession], test_community) -> CommunityInviteDTO:
    code = uuid4().hex
    expire_time = datetime.now() + timedelta(days=7)
    async with pool() as sess:
        stmt = (
            update(CommunityModel)
            .where(CommunityModel.id == test_community.id)
            .values(code=code, code_expire_time=expire_time)
        )
        await sess.execute(stmt)
        await sess.commit()
    return CommunityInviteDTO(community_id=test_community.id, code=code, expire_time=expire_time)


@pytest_asyncio.fixture(scope="module")
async def test_occupancy_category_model_list(pool: async_sessionmaker[AsyncSession]) -> list[OccupancyCategoryModel]:
    count = 5
    category_model_list: list[OccupancyCategoryModel] = []
    async with pool() as s:
        for _ in range(count):
            model = OccupancyCategoryModel()
            s.add(model)
            await s.flush()
            translate_models = [
                OccupancyCategoryTranslateModel(
                    name=f"{fake.name()}_occupancy_t",
                    category_id=model.id,
                    language=lang,
                )
                for lang in LanguageEnum
            ]
            s.add_all(translate_models)
            await s.flush()
            await s.refresh(model)
            category_model_list.append(model)
        await s.commit()
    return category_model_list


@pytest_asyncio.fixture(scope="module")
async def test_mission_model_list(
    pool: async_sessionmaker[AsyncSession], test_occupancy_category_model_list: list[OccupancyCategoryModel]
) -> list[MissionModel]:
    mission_list: list[MissionModel] = []
    async with pool() as s:
        for category in test_occupancy_category_model_list:
            model = MissionModel(
                active=True,
                author="",
                score=random.randint(50, 500),
                category_id=category.id,
            )
            s.add(model)
            await s.flush()
            translate_models = [
                MissionTranslateModel(
                    name=f"{fake.name()}_mission_t",
                    description="",
                    instruction="",
                    mission_id=model.id,
                    language=lang,
                )
                for lang in LanguageEnum
            ]
            s.add_all(translate_models)
            await s.flush()
            await s.refresh(model)
            mission_list.append(model)
        await s.commit()
    return mission_list


@pytest_asyncio.fixture(scope="module")
async def test_user_mission_model_list(
    pool: async_sessionmaker[AsyncSession], test_user: User, test_mission_model_list: list[MissionModel]
) -> list[UserMissionModel]:
    models = []
    async with pool() as s:
        for mission_model in test_mission_model_list:
            model = UserMissionModel(
                user_id=test_user.id, mission_id=mission_model.id, status=OccupancyStatusEnum.ACTIVE
            )
            models.append(model)
        s.add_all(models)
        await s.commit()
    return models


@pytest_asyncio.fixture(scope="module")
async def test_community_mission_model_list(
    pool: async_sessionmaker[AsyncSession], test_community: Community, test_mission_model_list: list[MissionModel]
) -> list[CommunityMissionModel]:
    models = []
    async with pool() as s:
        for mission_model in test_mission_model_list:
            model = CommunityMissionModel(
                community_id=test_community.id,
                mission_id=mission_model.id,
                status=OccupancyStatusEnum.ACTIVE,
                author="aboba",
            )
            models.append(model)
        s.add_all(models)
        await s.commit()
    return models


@pytest_asyncio.fixture(scope="module")
async def test_mission(pool: async_sessionmaker[AsyncSession], test_mission_model_list: list[MissionModel]) -> Mission:
    model = random.choice(test_mission_model_list)
    async with pool() as s:
        coro = await s.scalars(select(MissionTranslateModel).where(MissionTranslateModel.mission_id == model.id))
        translations = coro.all()
    translation = random.choice(translations)
    return Mission(
        id=model.id,
        name=translation.name,
        active=model.active,
        score=model.score,
        description=translation.description,
        instruction=translation.instruction,
        category_id=model.category_id,
        language=translation.language,
    )


@pytest_asyncio.fixture(scope="module")
async def test_score_community(pool: async_sessionmaker[AsyncSession], test_community: CommunityModel):
    async with pool() as sess:
        item = CommunityScoreModel(
            community_id=test_community.id,
            operation=ScoreOperationEnum.PLUS,
            value=100,
        )
        sess.add(item)
        await sess.commit()
        return ScoreCommunity(community_id=item.community_id, operation=item.operation, value=item.value)


@pytest_asyncio.fixture(scope="module")
async def test_users(pool: async_sessionmaker[AsyncSession]) -> list[User]:
    user_list: list[User] = []
    count = 20
    async with pool() as sess:
        for _ in range(count):
            user = UserModel(username=f"{fake.name()}_test_users", password="123", active=True)
            sess.add(user)
            await sess.flush()
            await sess.refresh(user)
            user_list.append(
                User(
                    id=user.id,
                    username=user.username,
                    password=user.password,
                    active=user.active,
                    subscription="",
                    language="",
                )
            )
        min_value_user = UserModel(id=999, username="MinValue", password="123", active=True)
        sess.add(min_value_user)
        max_value_user = UserModel(id=1000, username="MaxValue", password="123", active=True)
        sess.add(max_value_user)
        await sess.commit()
        user_list.append(
            User(
                id=min_value_user.id,
                username=min_value_user.username,
                password=min_value_user.password,
                active=min_value_user.active,
                subscription="",
                language="",
            )
        )
        user_list.append(
            User(
                id=max_value_user.id,
                username=max_value_user.username,
                password=max_value_user.password,
                active=max_value_user.active,
                subscription="",
                language="",
            )
        )
    return user_list


@pytest_asyncio.fixture(scope="module")
async def test_users_scores(pool: async_sessionmaker[AsyncSession], test_users) -> list[UserScoreModel]:
    user_score_list: list[UserScoreModel] = []
    val = 100
    async with pool() as sess:
        for user in test_users[:-2]:
            user_score = UserScoreModel(user_id=user.id, value=val, operation=ScoreOperationEnum.PLUS)
            val += 10
            sess.add(user_score)
            await sess.flush()
            await sess.refresh(user_score)
            user_score_list.append(user_score)
        await sess.commit()
        min_value_user = UserScoreModel(user_id=999, value=115, operation=ScoreOperationEnum.PLUS)
        sess.add(min_value_user)
        max_value_user = UserScoreModel(
            user_id=1000,
            value=100000,
            operation=ScoreOperationEnum.PLUS,
        )
        sess.add(max_value_user)
        await sess.commit()
    user_score_list.append(max_value_user)
    user_score_list.append(min_value_user)
    return user_score_list


@pytest_asyncio.fixture(scope="module")
async def test_user_for_rating(test_users) -> User:
    user: User = random.choice(test_users)
    return User(
        id=user.id, username=user.username, active=user.active, password=user.password, language="", subscription=""
    )


@pytest_asyncio.fixture(scope="module")
async def test_user_mission(test_user_mission_model_list: list[UserMissionModel]) -> MissionUser:
    model = random.choice(test_user_mission_model_list)
    return MissionUser(
        user_id=model.user_id, mission_id=model.mission_id, status=model.status, date_close=model.date_close
    )


@pytest_asyncio.fixture(scope="module")
async def test_community(pool: async_sessionmaker[AsyncSession]) -> Community:
    async with pool() as sess:
        community = CommunityModel(
            name="test-com", description="test-com", active=True, privacy=CommunityPrivacyEnum.PRIVATE
        )
        sess.add(community)
        await sess.commit()
        return Community(
            name=community.name,
            description=community.description,
            active=True,
            id=community.id,
            privacy=community.privacy,
        )


@pytest_asyncio.fixture(scope="module")
async def test_community_list(pool: async_sessionmaker[AsyncSession]) -> list[CommunityModel]:
    community_list: list[CommunityModel] = []
    async with pool() as sess:
        for _ in range(30):
            community_model = CommunityModel(
                name=fake.name(),
                description="dasw",
                active=True,
                privacy=CommunityPrivacyEnum.PRIVATE,
            )
            sess.add(community_model)
            await sess.flush()
            await sess.refresh(community_model)
            community_list.append(community_model)
        min_value_community = CommunityModel(
            id=1000, name="MinValue", description="low", active=True, privacy=CommunityPrivacyEnum.PRIVATE
        )
        max_value_community = CommunityModel(
            id=1111, name="MaxValue", description="max", active=True, privacy=CommunityPrivacyEnum.PRIVATE
        )
        community_list.append(max_value_community)
        community_list.append(min_value_community)
        sess.add_all((min_value_community, max_value_community))
        await sess.commit()
    return community_list


@pytest_asyncio.fixture(scope="module")
async def test_community_score(pool: async_sessionmaker[AsyncSession], test_community_list: list[Community]):
    community_score_list: list[CommunityScoreModel] = []
    async with pool() as sess:
        for community in test_community_list[:-2]:
            community_score = CommunityScoreModel(
                community_id=community.id,
                operation=ScoreOperationEnum.PLUS,
                value=random.randint(1, 1000),
            )
            sess.add(community_score)
            await sess.flush()
            await sess.refresh(community_score)
            community_score_list.append(community_score)

        min_value = CommunityScoreModel(
            community_id=1000,
            value=1,
            operation=ScoreOperationEnum.PLUS,
        )
        max_value = CommunityScoreModel(
            community_id=1111,
            value=10000000,
            operation=ScoreOperationEnum.PLUS,
        )
        sess.add(max_value)
        sess.add(min_value)
        await sess.commit()
    community_score_list.append(max_value)
    community_score_list.append(min_value)
    return community_score_list


@pytest_asyncio.fixture(scope="module")
async def community_for_rating(test_community_list: list[Community]) -> Community:
    community = test_community_list[-1]
    return Community(
        id=community.id,
        name=community.name,
        description=community.description,
        active=community.active,
        privacy=community.privacy,
    )


@pytest_asyncio.fixture(scope="module")
async def community_operations_list(
    pool: async_sessionmaker[AsyncSession], community_for_rating: Community
) -> list[CommunityScoreModel]:
    community_list: list[CommunityScoreModel] = []
    async with pool() as sess:
        for _ in range(10):
            community_operation = CommunityScoreModel(
                operation=ScoreOperationEnum.PLUS,
                value=10,
                community_id=community_for_rating.id,
            )
            sess.add(community_operation)
            await sess.flush()
            await sess.refresh(community_operation)
            community_list.append(community_operation)
        await sess.commit()
    return community_list


@pytest_asyncio.fixture(scope="module")
async def user_operations_list(pool: async_sessionmaker[AsyncSession], test_user: User):
    user_list: list[UserScoreModel] = []
    async with pool() as sess:
        for _ in range(10):
            user_operation = UserScoreModel(
                user_id=test_user.id,
                value=10,
                operation=ScoreOperationEnum.PLUS,
            )
            sess.add(user_operation)
            await sess.flush()
            await sess.refresh(user_operation)
            user_list.append(user_operation)
        await sess.commit()
    return user_list


async def test_community_mission(test_community_mission_model_list: list[CommunityMissionModel]) -> MissionCommunity:
    model = random.choice(test_community_mission_model_list)
    return MissionCommunity(
        community_id=model.community_id,
        mission_id=model.mission_id,
        status=model.status,
        author=model.author,
        place=model.place,
        meeting_date=model.meeting_date,
        people_required=model.people_required,
        people_max=model.people_max,
        comment=model.comment,
        date_close=model.date_close,
    )
