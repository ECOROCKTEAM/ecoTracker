from dataclasses import dataclass

from src.core.usecases.verification.contact.contact import contact_value_type_check
from src.core.dto.m2m.user.contact import ContactUserDTO, ContactUserUpdateDTO
from src.core.interfaces.repository.user.contact import IUserContactRepository
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: ContactUserDTO


class ContactUserUpdateUseCase:
    def __init__(self, repo: IUserContactRepository) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, update_obj: ContactUserUpdateDTO) -> Result:
        if not user.active:
            raise UserIsNotActivateError(user_id=user.id)

        old_obj = await self.repo.get(id=update_obj.contact_id)
        await contact_value_type_check(contact=update_obj.contact.value, type=old_obj.type)

        # А тут не сработает проверка на тип контакта (к тому же у нас уже не contact_type, а enum).
        # Я в асинх это делаю, а должен по идее в синх проверять

        obj = await self.repo.update(obj=update_obj)
        return Result(item=obj)
