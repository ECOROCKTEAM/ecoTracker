from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.mock import MockObj
from src.core.dto.subscription.period import (
    SubscriptionPeriodCreateDTO,
    SubscriptionPeriodDTO,
)
from src.core.entity.subscription import Subscription, SubscriptionCreateDTO
from src.core.interfaces.repository.subscription.subscription import (
    ISubscriptionRepository,
)


class SubscriptionRepository(ISubscriptionRepository):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def delete(self, *, id: int) -> int:
        return await super().delete(id=id)

    async def get(self, *, id: int) -> Subscription:
        return await super().get(id=id)

    async def create(self, *, obj: SubscriptionCreateDTO) -> Subscription:
        return await super().create(obj=obj)

    async def lst(self, *, filter_obj: MockObj | None = None) -> list[Subscription]:
        return await super().lst(filter_obj=filter_obj)

    async def period_create(self, *, obj: SubscriptionPeriodCreateDTO) -> SubscriptionPeriodDTO:
        return await super().period_create(obj=obj)

    async def period_get(self, *, id: int) -> SubscriptionPeriodDTO:
        return await super().period_get(id=id)

    async def period_list(self) -> list[SubscriptionPeriodDTO]:
        return await super().period_list()
