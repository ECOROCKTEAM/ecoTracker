from dataclasses import dataclass

from src.core.dto.user import UserUpdateDTO
from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import User


@dataclass
class Result:
    item: User


class UserUpdateUseCase:
    
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, *, user: User, obj: UserUpdateDTO) -> Result:
        
        """
        Тут по идее не на что не проверяем, даже на active. Вдруг мы хотим из active = Fasle сделать True.
        Тогда вопрос следующем: Может ли юзер сам себя активировать? Это во-первых. Во-вторых: а если захотим забанить чела?
        Тогда он сам себе блокировку снимет...
        В mtv версии у нас по сути и банить наверное будет не за что. Разве что за комментарии в чате миссий сообщества, если таковые будут.
        Пока сделал так, чтобы сам себе он блокировку не снимал.
        Можно кстати сделать так, что active пользователя может в False поставить админ приложения. Он же может снять. Если он пользователя
        деактивирует, то и снимается подписка с него. Сам пользователь может снять диактивацию преобретая подписку

        Надо обсудить на созвоне

        """

        user = await self.repo.user_update(user=user, obj=obj)

        return Result(item=user)