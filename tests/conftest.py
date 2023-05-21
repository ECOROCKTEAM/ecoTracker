import asyncio
import random
from typing import AsyncGenerator, Generator

import faker
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.database.base import (
    Base,
    create_async_engine,
    create_session_factory,
)
from src.application.settings import settings
from src.core.dto.challenges.category import OccupancyCategoryDTO
from src.core.entity.community import Community
from src.core.entity.mission import Mission
from src.core.entity.score import ScoreCommunity, ScoreUser
from src.core.entity.user import User
from src.core.enum.community.privacy import CommunityPrivacyEnum
from src.core.enum.community.role import CommunityRoleEnum
from src.core.enum.language import LanguageEnum
from src.core.enum.score.operation import ScoreOperationEnum
from src.data.models.challenges.mission import MissionModel, MissionTranslateModel
from src.data.models.challenges.occupancy import (
    OccupancyCategoryModel,
    OccupancyCategoryTranslateModel,
)
from src.data.models.community.community import CommunityModel, CommunityScoreModel
from src.data.models.user.user import UserCommunityModel, UserModel, UserScoreModel

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
            username=user.username, password=user.password, active=True, id=user.id, language="", subscription=""
        )


@pytest_asyncio.fixture(scope="module")
async def test_user_role(pool: async_sessionmaker[AsyncSession]) -> User:
    async with pool() as sess:
        user = UserModel(username="test-role", password="test-role", active=True)
        sess.add(user)
        await sess.commit()
        return User(
            username=user.username, password=user.password, active=True, id=user.id, language="", subscription=""
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
async def test_user_score(pool: async_sessionmaker[AsyncSession], test_user) -> ScoreUser:
    async with pool() as session:
        score_user = UserScoreModel(user_id=test_user.id, value=100, operation=ScoreOperationEnum.PLUS)
        session.add(score_user)
        await session.commit()
        return ScoreUser(user_id=score_user.user_id, value=score_user.value, operation=score_user.operation)


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
async def test_user_community(pool: async_sessionmaker[AsyncSession], test_user, test_community) -> None:
    async with pool() as sess:
        role = UserCommunityModel(
            user_id=test_user.id, community_id=test_community.id, role=CommunityRoleEnum.SUPERUSER
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
async def test_mission(test_mission_model_list: list[MissionModel]) -> Mission:
    model = random.choice(test_mission_model_list)
    translation = random.choice(model.translations)
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
