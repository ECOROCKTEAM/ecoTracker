from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entity.occupancy import OccupancyCategory
from src.core.enum.language import LanguageEnum
from src.core.exception.base import EntityNotFound
from src.core.interfaces.repository.challenges.occupancy import (
    IRepositoryOccupancyCategory,
)
from src.data.models.challenges.occupancy import OccupancyCategoryTranslateModel


def occupancy_model_to_entity(model: OccupancyCategoryTranslateModel) -> OccupancyCategory:
    return OccupancyCategory(
        id=model.id,
        name=model.name,
        language=model.language,
    )


class RepositoryOccupancyCategory(IRepositoryOccupancyCategory):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, id: int, lang: LanguageEnum) -> OccupancyCategory:
        stmt = select(OccupancyCategoryTranslateModel).where(
            OccupancyCategoryTranslateModel.category_id == id, OccupancyCategoryTranslateModel.language == lang
        )
        result = await self.db_context.scalar(stmt)
        if not result:
            raise EntityNotFound(msg=f"Category={id} with lang={lang} not found")
        return occupancy_model_to_entity(model=result)

    async def lst(self, lang: LanguageEnum) -> list[OccupancyCategory]:
        stmt = select(OccupancyCategoryTranslateModel).where(OccupancyCategoryTranslateModel.language == lang)
        result = await self.db_context.scalars(stmt)
        if not result:
            raise EntityNotFound(msg=f"Occupancy with lang={lang} not found")
        return [occupancy_model_to_entity(model=model) for model in result]
