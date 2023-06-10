# from typing import AsyncGenerator, Tuple

# import pytest
# import pytest_asyncio
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.core.entity.user import User
# from src.core.enum.language import LanguageEnum
# from src.data.models.challenges.occupancy import (
#     OccupancyCategoryModel,
#     OccupancyCategoryTranslateModel,
# )
# from src.data.models.user.user import UserModel


# @pytest_asyncio.fixture(scope="function")
# async def test_user_premium_ru_entity(test_user_model_ru: UserModel) -> AsyncGenerator[User, None]:
#     yield User(
#         id=test_user_model_ru.id,
#         active=test_user_model_ru.active,
#         username=test_user_model_ru.username,
#         password=test_user_model_ru.password,
#         language=test_user_model_ru.language,
#         subscription="",  # type: ignore
#     )


# @pytest_asyncio.fixture(scope="function")
# async def test_user_premium_en_entity(test_user_model_en: UserModel) -> AsyncGenerator[User, None]:
#     yield User(
#         id=test_user_model_en.id,
#         active=test_user_model_en.active,
#         username=test_user_model_en.username,
#         password=test_user_model_en.password,
#         language=test_user_model_en.language,
#         subscription="",  # type: ignore
#     )


# @pytest_asyncio.fixture(scope="function")
# async def test_user_not_premium_entity(test_user_model_ru: UserModel) -> AsyncGenerator[User, None]:
#     class UserMocked(User):
#         @property
#         def is_premium(self) -> bool:
#             # TODO implement!
#             return False

#     yield UserMocked(
#         id=test_user_model_ru.id,
#         active=test_user_model_ru.active,
#         username=test_user_model_ru.username,
#         password=test_user_model_ru.password,
#         language=test_user_model_ru.language,
#         subscription="",  # type: ignore
#     )


# @pytest_asyncio.fixture(scope="function")
# async def category_model(session: AsyncSession) -> AsyncGenerator[OccupancyCategoryModel, None]:
#     model = OccupancyCategoryModel()
#     session.add(model)
#     await session.commit()

#     yield model

#     await session.delete(model)
#     await session.commit()


# @pytest_asyncio.fixture(scope="function")
# async def category_model_ru(
#     session: AsyncSession, category_model: OccupancyCategoryModel
# ) -> AsyncGenerator[Tuple[OccupancyCategoryModel, OccupancyCategoryTranslateModel], None]:
#     lang = LanguageEnum.RU
#     translate_model = OccupancyCategoryTranslateModel(
#         name=f"f_occupancy_{lang.value}",
#         category_id=category_model.id,
#         language=lang,
#     )
#     session.add(translate_model)
#     await session.flush()
#     await session.refresh(category_model)
#     await session.commit()

#     yield (category_model, translate_model)

#     await session.delete(translate_model)
#     await session.commit()


# @pytest_asyncio.fixture(scope="function")
# async def category_model_en(
#     session: AsyncSession, category_model: OccupancyCategoryModel
# ) -> AsyncGenerator[Tuple[OccupancyCategoryModel, OccupancyCategoryTranslateModel], None]:
#     lang = LanguageEnum.EN
#     translate_model = OccupancyCategoryTranslateModel(
#         name=f"f_occupancy_{lang.value}",
#         category_id=category_model.id,
#         language=lang,
#     )
#     session.add(translate_model)
#     await session.flush()
#     await session.refresh(category_model)
#     await session.commit()

#     yield (category_model, translate_model)

#     await session.delete(translate_model)
#     await session.commit()
