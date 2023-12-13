from sqlalchemy.ext.asyncio import AsyncSession

from src.core.entity.subscription import Subscription
from src.core.entity.user import User, UserCreateDTO, UserUpdateDTO
from src.core.interfaces.repository.user.user import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, user_id: str) -> User:
        return await super().get(user_id=user_id)

    async def create(self, *, user_obj: UserCreateDTO, sub_obj: Subscription) -> User:
        return await super().create(user_obj=user_obj, sub_obj=sub_obj)

    async def update(self, *, obj: UserUpdateDTO) -> User:
        return await super().update(obj=obj)

    async def update_subscription(self, *, user_id: int, sub_id: int) -> User:
        return await super().update_subscription(user_id=user_id, sub_id=sub_id)
