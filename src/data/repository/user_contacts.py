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

    async def create(self, *, obj: ContactUserCreateDTO) -> ContactUserDTO:
        return await super().create(obj=obj)

    async def get(self, *, user_id: str, contact_id: int) -> ContactUserDTO:
        return await super().get(user_id=user_id, contact_id=contact_id)

    async def get_favorite(self, *, user_id: str) -> ContactUserDTO:
        return await super().get_favorite(user_id=user_id)

    async def delete(self, *, contact_id: int, user_id: str) -> int:
        return await super().delete(contact_id=contact_id, user_id=user_id)

    async def list(
        self,
        *,
        user_id: str,
        filter_obj: UserContactFilter | None = None,
        sorting_obj: UserContactSorting | None = None,
        order_obj: UserContactOrder | None = None,
    ) -> list[ContactUserDTO]:
        return await super().list(user_id=user_id, filter_obj=filter_obj, sorting_obj=sorting_obj, order_obj=order_obj)

    async def update(self, *, user_id: str, obj: ContactUserUpdateDTO) -> ContactUserDTO:
        return await super().update(user_id=user_id, obj=obj)

    async def set_favorite(self, *, user_id: str, contact_id: int, is_favorite: bool) -> ContactUserDTO:
        return await super().set_favorite(user_id=user_id, contact_id=contact_id, is_favorite=is_favorite)
