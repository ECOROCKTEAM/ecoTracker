from dataclasses import dataclass

from src.core.interfaces.repository.user.user import IUserRepository
from src.core.entity.user import User, UserUpdateDTO


@dataclass
class Result:
    item: User


class UserUpdateUseCase:
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    async def __call__(self, *, obj: UserUpdateDTO) -> Result:
        # У нас UserUpdateDTO имеет поле subscription. Тут мы обновляем пользователя вместе с подпиской?
        # Ведь у нас есть отдельный метод на обновление подписки...
        # Возможно, что изменение пользователя самого будет происходить в личном кабинете и изменять он будет всё, что касается User, без подписки.
        # Подписку он будет изменять в разделе "Подписка" в приложении и околотого. Может в UserUpdateDTO убрать в таком случае subscription?

        user = await self.repo.update(obj=obj)
        return Result(item=user)
