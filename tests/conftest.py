import asyncio
from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
import random
import faker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.application.settings import settings
from src.application.database.base import create_async_engine, create_session_factory, Base
from src.core.dto.challenges.category import OccupancyCategoryDTO
from src.core.entity.mission import Mission
from src.core.enum.language import LanguageEnum
from src.data.models.challenges.mission import MissionModel, MissionTranslateModel
from src.data.models.challenges.occupancy import OccupancyCategoryModel, OccupancyCategoryTranslateModel
from src.data.models.user.user import UserModel, UserCommunityModel
from src.data.models.community.community import CommunityModel
from src.core.entity.user import User
from src.core.enum.community.privacy import CommunityPrivacyEnum
from src.core.enum.community.role import CommunityRoleEnum
from src.core.entity.community import Community

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
    test_data = [[{"name": f"test-occupancy-{fake.name()}", "language": lang}] for lang in LanguageEnum]
    category_model_list: list[OccupancyCategoryModel] = []
    async with pool() as s:
        for _ in range(5):
            model = OccupancyCategoryModel()
            s.add(model)
            await s.flush()
            await s.refresh(model)
            for translations in test_data:
                for translate_data in translations:
                    t_model = OccupancyCategoryTranslateModel(**translate_data, category_id=model.id)
                    s.add(t_model)
                    await s.flush()
                await s.refresh(model)
            category_model_list.append(model)
        await s.commit()
    return category_model_list


@pytest_asyncio.fixture(scope="module")
async def test_mission_model_list(
    pool: async_sessionmaker[AsyncSession], test_occupancy_category_model_list: list[OccupancyCategoryModel]
) -> list[MissionModel]:
    test_mission_list_data = []
    for category in test_occupancy_category_model_list:
        test_mission_data = {
            "active": True,
            "author": "",
            "score": random.randint(50, 500),
            "category_id": category.id,
            "translations": [
                {
                    "name": f"test-mission-{fake.name()}",
                    "description": "",
                    "instruction": "",
                    "language": category_t.language,
                }
                for category_t in category.translations
            ],
        }
        test_mission_list_data.append(test_mission_data)
    mission_list: list[MissionModel] = []
    async with pool() as s:
        for mission_data in test_mission_list_data:
            translations = mission_data.pop("translations")
            model = MissionModel(**mission_data)
            s.add(model)
            await s.flush()
            await s.refresh(model)
            for translate_data in translations:
                t_model = MissionTranslateModel(**translate_data, mission_id=model.id)
                s.add(t_model)
                await s.flush()
            await s.refresh(model)
            mission_list.append(model)
        await s.commit()
    return mission_list


@pytest_asyncio.fixture(scope="module")
async def test_mission(test_mission_model_list: list[MissionModel]) -> Mission:
    model = random.choice(test_mission_model_list)
    translation = random.choice(model.translations)
    lang = translation.language
    category = model.category
    category_translation = [category_t for category_t in category.translations if category_t.language == lang][0]
    return Mission(
        id=model.id,
        name=translation.name,
        active=model.active,
        score=model.score,
        description=translation.description,
        instruction=translation.instruction,
        category=OccupancyCategoryDTO(
            id=category.id, name=category_translation.name, language=category_translation.language
        ),
        language=translation.language,
    )
