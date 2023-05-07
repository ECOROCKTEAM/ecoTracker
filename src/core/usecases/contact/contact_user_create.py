from dataclasses import dataclass
from src.core.usecases.verification.contact.contact import contact_value_type_check

from src.core.dto.m2m.user.contact import ContactUserCreateDTO, ContactUserDTO
from src.core.dto.user.contact import ContactCreateDTO
from src.core.interfaces.repository.user.contact import IUserContactRepository
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: ContactUserDTO


class ContactUserCreateUseCase:
    def __init__(self, repo: IUserContactRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: ContactCreateDTO) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        await contact_value_type_check(contact=obj.value, type=obj.type)

        contact = await self.repo.create(
            obj=ContactUserCreateDTO(
                user_id=user.id,
                value=obj.value,
                type=obj.type,
            )
        )
        return Result(item=contact)
