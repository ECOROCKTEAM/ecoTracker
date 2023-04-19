from dataclasses import dataclass

from src.core.interfaces.base import IRepositoryCore
from src.core.entity.user import UserSubscription, User
from src.core.exception.user import UserIsNotActivateError
from src.core.exception.task import TaskAlreadyTakenError 



@dataclass
class Result:
    item: UserSubscription


class UserSubscriptionUpdateUseCase:
    
    def __init__(self, repo: IRepositoryCore) -> None:
        self.repo = repo

    async def __call__(self, user: User, subscription_id: int) -> Result:
        
        """
        Ты вроде не работал с интернет-эквайрингом.
        С преобретением подписки сложно: надо определить платёжную систему, типо Фонди или Лава (работал чуть-чуть со второй, но мало).
        Нам по сути короче надо будет id подписок. Из них получаем их стоимость и далее отправляем на сайт подписок для покупки с этой ценой.
        В Lava надо цену умножить на 100, т.к. цена считается в центах, вроде. 
        На нашем сайте чел будет выбирать подписку, нажмёт кнопку 'купить' и мы в эндпоинт будем передавать бабки, которые с него спишут и аресовать
        его на сайт нашего интернет-эквайринга. 
        Тут я хз на что можно проверять
        """

        sub = self.repo.user_subscription_update(user_id=user.username, subscription_id=subscription_id)

        return Result(item=sub)
    
