from dataclasses import dataclass

from src.core.usecases.verification.contact.contact import contact_value_type_check
from src.core.dto.m2m.user.contact import ContactUserDTO, ContactUserUpdateDTO
from src.core.interfaces.user.contact import IUserContactRepository
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: ContactUserDTO


class ContactUserUpdateUseCase:
    def __init__(self, repo: IUserContactRepository) -> None:
        self.repo = repo

    async def __call__(
        self, *,
        user: User,
        update_obj: ContactUserUpdateDTO
    ) -> Result:
        
        if not user.active:
            raise UserIsNotActivateError(username=user.username)
        
        old_obj = await self.repo.get(id=update_obj.contact_id)
        await contact_value_type_check(value=update_obj.contact, type=old_obj.type)

        # Так как тип обновляемого контакта мы не получаем (пользователь его не вводит), то приходится по id брать старый контакт.
        # Извлекать его тип и отправлять на проверку этот тип старого контакта с новым значением контакта.

        obj = await self.repo.update(obj=update_obj)
        return Result(item=obj)