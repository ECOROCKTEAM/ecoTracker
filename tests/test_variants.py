import itertools
import random
import pytest
from timeit import default_timer as timer
from sqlalchemy import and_, outerjoin, select, text, or_
from sqlalchemy.orm import noload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import literal, literal_column
from src.application.database.base import Base
from src.core.dto.challenges.category import OccupancyCategoryDTO
from src.core.entity.mission import Mission
from src.core.enum.language import LanguageEnum
from src.data.models import MissionModel, MissionTranslateModel, OccupancyCategoryModel, OccupancyCategoryTranslateModel
from src.data.repository.challenges.mission import model_to_dto

# count of languages - 28
COUNT_OCCUPANCY = 500
COUNT_MISSION = 10_000


async def generate_occupancy_category(s, count):
    category_model_list: list[OccupancyCategoryModel] = []
    for _ in range(count):
        model = OccupancyCategoryModel()
        s.add(model)
        await s.flush()
        translate_models = [
            OccupancyCategoryTranslateModel(
                name=f"{lang.name}_occupancy_t",
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


async def generate_mission(s, count, cl):
    mission_list: list[MissionModel] = []
    category_iter = itertools.cycle(cl)
    for idx in range(count):
        category = next(category_iter)
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
                name=f"{idx}_{lang.name}_mission_t",
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


# python -m pytest tests/test_variants.py::test_fill -v -s
# @pytest.mark.asyncio
# async def test_fill(session: AsyncSession):
#     cl = await generate_occupancy_category(s=session, count=COUNT_OCCUPANCY)
#     ml = await generate_mission(s=session, count=COUNT_MISSION, cl=cl)
#     print(len(ml))


# python -m pytest tests/test_variants.py::test_list_select_all_python_find -vv -s --durations=0
@pytest.mark.asyncio
async def test_list_select_all_python_find(session: AsyncSession):
    target_lang = LanguageEnum.Z
    stmt = select(MissionModel)
    res = await session.scalars(stmt)
    conv_res = [model_to_dto(model, target_lang) for model in res]
    # print("\n", conv_res[0])


# python -m pytest tests/test_variants.py::test_list_select_two_in_one_query -vv -s --durations=0
@pytest.mark.asyncio
async def test_list_select_two_in_one_query(session: AsyncSession):
    target_lang = LanguageEnum.RU
    default_lang = LanguageEnum.EN
    stmt = (
        select(
            MissionModel,
            OccupancyCategoryModel,
            func.array_agg(literal_column(MissionTranslateModel.__tablename__)),
            func.array_agg(literal_column(OccupancyCategoryTranslateModel.__tablename__)),
        )
        .options(noload(MissionModel.translations))
        .options(noload(MissionModel.category))
        .options(noload(OccupancyCategoryModel.translations))
        .join(OccupancyCategoryModel, MissionModel.category_id == OccupancyCategoryModel.id)
        .join(
            MissionTranslateModel,
            MissionModel.id == MissionTranslateModel.mission_id,
        )
        .join(OccupancyCategoryTranslateModel, OccupancyCategoryModel.id == OccupancyCategoryTranslateModel.category_id)
        .where(
            MissionTranslateModel.language.in_([target_lang, default_lang]),
            OccupancyCategoryTranslateModel.language.in_([target_lang, default_lang]),
        )
        .group_by(MissionModel.id, OccupancyCategoryModel.id)
    )
    coro = await session.execute(stmt)
    res = coro.all()

    def _to_entity(item):
        mission, category, mission_translate_lst, category_translate_lst = item
        mission_translate_map = {t["language"]: dict(t) for t in mission_translate_lst}
        mission_translate_dict = mission_translate_map.get(
            target_lang.name, mission_translate_map.get(default_lang.name)
        )
        if mission_translate_dict is None:
            raise ValueError("fuck jopa")
        mission_translate_dict["language"] = LanguageEnum[mission_translate_dict["language"]]
        category_translate_map = {t["language"]: dict(t) for t in category_translate_lst}
        category_translate_dict = category_translate_map.get(
            target_lang.name, category_translate_map.get(default_lang.name)
        )
        if category_translate_dict is None:
            raise ValueError("fuck jopa")
        category_translate_dict["language"] = LanguageEnum[category_translate_dict["language"]]

        m = Mission(
            id=mission.id,
            name=mission_translate_dict["name"],
            active=mission.active,
            score=mission.score,
            description=mission_translate_dict["description"],
            instruction=mission_translate_dict["instruction"],
            language=mission_translate_dict["language"],
            category=OccupancyCategoryDTO(
                id=category.id, name=category_translate_dict["name"], language=category_translate_dict["language"]
            ),
        )
        return m

    result_list = [_to_entity(item) for item in res]
    # print(len(result_list))


# python -m pytest tests/test_variants.py::test_list_with_subq_if_not_found -vv -s --durations=0
@pytest.mark.asyncio
async def test_list_with_subq_if_not_found(session: AsyncSession):
    target_lang = LanguageEnum.RU
    default_lang = LanguageEnum.EN

    stmt = (
        select(
            MissionModel,
            OccupancyCategoryModel,
            MissionTranslateModel,
            OccupancyCategoryTranslateModel,
        )
        .options(noload(MissionModel.translations))
        .options(noload(MissionModel.category))
        .options(noload(OccupancyCategoryModel.translations))
        .join(OccupancyCategoryModel, MissionModel.category_id == OccupancyCategoryModel.id)
        .join(
            MissionTranslateModel,
            and_(MissionModel.id == MissionTranslateModel.mission_id, MissionTranslateModel.language == target_lang),
            isouter=True,
        )
        .join(
            OccupancyCategoryTranslateModel,
            and_(
                OccupancyCategoryModel.id == OccupancyCategoryTranslateModel.category_id,
                OccupancyCategoryTranslateModel.language == target_lang,
            ),
            isouter=True,
        )
    )
    # print(stmt.compile(dialect=postgresql.dialect(),compile_kwargs={"literal_binds": True}))

    coro = await session.execute(stmt)
    res = coro.mappings().all()

    mission_default_lang_ids = []
    category_default_lang_ids = []
    holder = {
        "mission": {},
        "mission_translate": {},
        "category": {},
        "category_translate": {},
    }

    # print()
    for item in res:
        mission = item.get("MissionModel")
        category = item.get("OccupancyCategoryModel")
        mission_translate = item.get("MissionTranslateModel")
        category_translate = item.get("OccupancyCategoryTranslateModel")
        # print(mission.id, mission_translate, category_translate)
        if mission_translate is None:
            mission_default_lang_ids.append(mission.id)
        if category_translate is None:
            category_default_lang_ids.append(category.id)
        holder["mission"][mission.id] = mission
        holder["category"][category.id] = category
        holder["mission_translate"][mission.id] = mission_translate
        holder["category_translate"][category.id] = category_translate
    if len(mission_default_lang_ids) > 0:
        # print("negative for mission:", mission_default_lang_ids)
        stmt_mission_negative = select(
            MissionTranslateModel,
        ).where(
            and_(
                MissionTranslateModel.mission_id.in_(mission_default_lang_ids),
                MissionTranslateModel.language == default_lang,
            )
        )
        # print(stmt_mission_negative.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        coro = await session.scalars(stmt_mission_negative)
        result = coro.all()
        for model in result:
            holder["mission_translate"][model.mission_id] = model
    if len(category_default_lang_ids) > 0:
        # print("negative for category:", category_default_lang_ids)
        stmt_category_negative = select(
            OccupancyCategoryTranslateModel,
        ).where(
            and_(
                OccupancyCategoryTranslateModel.category_id.in_(category_default_lang_ids),
                OccupancyCategoryTranslateModel.language == default_lang,
            )
        )
        # print(stmt_category_negative.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        coro = await session.scalars(stmt_category_negative)
        result = coro.all()
        for model in result:
            holder["category_translate"][model.category_id] = model

    entity_list = []
    for _, mission_model in holder["mission"].items():
        mission_translate_model = holder["mission_translate"][mission_model.id]
        category_model = holder["category"][mission_model.category_id]
        category_translate_model = holder["category_translate"][category_model.id]
        entity_list.append(
            Mission(
                id=mission_model.id,
                name=mission_translate_model.name,
                active=mission_model.active,
                score=mission_model.active,
                description=mission_translate_model.description,
                instruction=mission_translate_model.instruction,
                language=mission_translate_model.language,
                category=OccupancyCategoryDTO(
                    id=category_model.id, name=category_translate_model.name, language=category_translate_model.language
                ),
            )
        )
    # print()
    # print(entity_list[0])
    # print(len(entity_list))


# State
# Lang - 28
# Mission - 10_000
# MissionTranslate - 280_000
# Category - 500
# CategoryTranslate - 140_000

# Worst bad fuck situation (all not found target language)
# 5.03s call     tests/test_variants.py::test_list_select_all_python_find
# 0.94s call     tests/test_variants.py::test_list_select_two_in_one_query
# 0.43s call     tests/test_variants.py::test_list_with_subq_if_not_found

# All good
# 5.07s call     tests/test_variants.py::test_list_select_all_python_find
# 1.07s call     tests/test_variants.py::test_list_select_two_in_one_query
# 0.32s call     tests/test_variants.py::test_list_with_subq_if_not_found
