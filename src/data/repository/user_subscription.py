from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.m2m.user.subscription import (
    UserSubscription,
    UserSubscriptionCreateDTO,
    UserSubscriptionUpdateDTO,
)
from src.core.interfaces.repository.user.subscription import IUserSubscriptionRepository


class UserSubscriptionRepository(IUserSubscriptionRepository):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def delete(self, user_id: str, sub_id: int) -> int:
        return await super().delete(user_id, sub_id)

    async def update(self, *, obj: UserSubscriptionUpdateDTO) -> UserSubscription:
        return await super().update(obj=obj)

    async def get(self, *, user_id: str, sub_id: int) -> UserSubscription:
        return await super().get(user_id=user_id, sub_id=sub_id)

    async def list(self) -> list[UserSubscription]:
        return await super().list()

    async def create(self, *, obj: UserSubscriptionCreateDTO) -> UserSubscription:
        return await super().create(obj=obj)
