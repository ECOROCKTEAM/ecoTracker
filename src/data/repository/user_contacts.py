from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dto.m2m.user.contact import (
    ContactUserCreateDTO,
    ContactUserDTO,
    ContactUserUpdateDTO,
)
from src.core.interfaces.repository.user.contact import (
    IUserContactRepository,
    UserContactFilter,
    UserContactOrder,
    UserContactSorting,
)


class UserContactRepository(IUserContactRepository):
    def __init__(self, db_context: AsyncSession) -> None:
        self.db_context = db_context

    async def get(self, *, id: int) -> ContactUserDTO:
        return await super().get(id=id)

    async def get_favorite(self, *, user_id: str) -> ContactUserDTO:
        return await super().get_favorite(user_id=user_id)

    async def delete(self, *, id: int) -> int:
        return await super().delete(id=id)

    async def set_favorite(self, *, id: int, is_favorite: bool) -> ContactUserDTO:
        return await super().set_favorite(id=id, is_favorite=is_favorite)

    async def create(self, *, user_id: str, obj: ContactUserCreateDTO) -> ContactUserDTO:
        return await super().create(user_id=user_id, obj=obj)

    async def update(self, *, obj: ContactUserUpdateDTO) -> ContactUserDTO:
        return await super().update(obj=obj)

    async def list(
        self,
        *,
        user_id: str,
        filter_obj: UserContactFilter,
        sorting_obj: UserContactSorting,
        order_obj: UserContactOrder,
    ) -> list[ContactUserDTO]:
        return await super().list(user_id=user_id, filter_obj=filter_obj, sorting_obj=sorting_obj, order_obj=order_obj)
