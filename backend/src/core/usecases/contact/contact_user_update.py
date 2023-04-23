from dataclasses import dataclass

from src.core.dto.m2m.user.contact import ContactUserDTO
from src.core.dto.user.contact import ContactUpdateDTO, ContactUserUpdateDTO
from src.core.interfaces.user.contact import iUserContactRepository
from src.core.entity.user import User
from src.core.exception.user import UserIsNotActivateError


@dataclass
class Result:
    item: ContactUserDTO


class ContactUserUpdateUseCase:
    def __init__(self, repo: iUserContactRepository) -> None:
        self.repo = repo

    async def __call__(
        self, *, user: User, contact_id: int, update_obj: ContactUpdateDTO
    ) -> Result:
        if not user.active:
            raise UserIsNotActivateError(username=user.username)


        pass
