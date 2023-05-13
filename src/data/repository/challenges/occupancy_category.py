from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dto.challenges.category import OccupancyCategoryDTO
from src.core.enum.language import LanguageEnum

from src.core.interfaces.repository.challenges.occupancy import IRepositoryOccupancyCategory


class RepositoryOccupancyCategory(IRepositoryOccupancyCategory):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, id: int, lang: LanguageEnum) -> OccupancyCategoryDTO:
        return await super().get(id=id, lang=lang)

    async def lst(self, lang: LanguageEnum) -> list[OccupancyCategoryDTO]:
        return await super().lst(lang)
