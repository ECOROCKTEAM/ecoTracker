from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.const.translate import DEFAULT_LANGUANGE
from src.core.entity.occupancy import OccupancyCategory
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound, TranslateNotFound
from src.core.interfaces.repository.challenges.occupancy import (
    IRepositoryOccupancyCategory,
)
from src.data.models.challenges.occupancy import (
    OccupancyCategoryModel,
    OccupancyCategoryTranslateModel,
)


def occupancy_model_to_entity(
    model: OccupancyCategoryModel, translated_model: OccupancyCategoryTranslateModel
) -> OccupancyCategory:
    return OccupancyCategory(
        id=model.id,
        name=translated_model.name,
        language=translated_model.language,
    )


class RepositoryOccupancyCategory(IRepositoryOccupancyCategory):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, id: int, lang: LanguageEnum) -> OccupancyCategory:
        stmt = (
            select(OccupancyCategoryModel, OccupancyCategoryTranslateModel)
            .join(
                OccupancyCategoryTranslateModel,
                and_(
                    OccupancyCategoryModel.id == OccupancyCategoryTranslateModel.category_id,
                    OccupancyCategoryTranslateModel.language == lang,
                ),
                isouter=True,
            )
            .where(OccupancyCategoryModel.id == id)
        )
        record = await self.db_context.execute(stmt)
        result = record.one_or_none()
        if result is None:
            raise EntityNotFound(msg=f"OccupancyCategory.id={id} not found")
        oc, oc_translate = result
        if oc_translate is None:
            oc_default_lang = select(OccupancyCategoryTranslateModel).where(
                and_(
                    OccupancyCategoryTranslateModel.category_id == id,
                    OccupancyCategoryTranslateModel.language == DEFAULT_LANGUANGE,
                )
            )
            oc_translate = await self.db_context.scalar(oc_default_lang)
            if oc_translate is None:
                raise TranslateNotFound(msg=f"OccupancyCategory={oc} with lang={lang} not found")
        return occupancy_model_to_entity(model=oc, translated_model=oc_translate)

    # async def lst(self, lang: LanguageEnum) -> list[OccupancyCategory]:
    #     stmt = select(OccupancyCategoryTranslateModel).where(OccupancyCategoryTranslateModel.language == lang)
    #     result = await self.db_context.scalars(stmt)
    #     if not result:
    #         stmt = select(OccupancyCategoryTranslateModel).where(
    #             OccupancyCategoryTranslateModel.language == DEFAULT_LANGUANGE
    #         )
    #         result = await self.db_context.scalars(stmt)
    #         if not result:
    #             raise EntityNotFound(msg=f"Occupancy with lang={lang} and default_lang={DEFAULT_LANGUANGE} not found")
    #     return [occupancy_model_to_entity(model=model) for model in result]

    async def lst(self, *, lang: LanguageEnum) -> list[OccupancyCategory]:
        stmt = select(OccupancyCategoryModel, OccupancyCategoryTranslateModel).join(
            OccupancyCategoryTranslateModel,
            and_(
                OccupancyCategoryModel.id == OccupancyCategoryTranslateModel.category_id,
                OccupancyCategoryTranslateModel.language == lang,
            ),
            isouter=True,
        )
        coro = await self.db_context.execute(stmt)
        result = coro.all()
        holder = {}
        for oc, oc_translate in result:
            holder[oc.id] = {}
            holder[oc.id]["oc"] = oc
            if oc_translate is None:
                oc_default_lang = select(OccupancyCategoryTranslateModel).where(
                    and_(
                        OccupancyCategoryTranslateModel.category_id == oc.id,
                        OccupancyCategoryTranslateModel.language == DEFAULT_LANGUANGE,
                    )
                )
                result = await self.db_context.scalar(oc_default_lang)
                if not result:
                    raise TranslateNotFound(msg=f"{oc=}, {oc_translate=}")
                holder[oc.id]["translate"] = result
            else:
                holder[oc.id]["translate"] = oc_translate

        return [
            occupancy_model_to_entity(model=models["oc"], translated_model=models["translate"])
            for models in holder.values()
        ]
