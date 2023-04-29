from dataclasses import dataclass

from src.core.dto.mock import MockObj
from src.core.interfaces.subscription.subscription import ISubscriptionRepository
from src.core.interfaces.user.user import IUserRepository
from src.core.entity.user import User, UserCreateDTO


@dataclass
class Result:
    item: User


class UserCreateUseCase:
    def __init__(self, user_repo: IUserRepository, subscription_repo: ISubscriptionRepository) -> None:
        self.user_repo = user_repo
        self.sub_repo = subscription_repo

    async def __call__(self, *, obj: UserCreateDTO) -> Result:

        subscription = await self.sub_repo.list(filter_obj=MockObj)  # type: ignore

        # Ты вроде говорил, что нельзя сразу передавать enum. Это типо неправильно. Изначально мы не знаем id подписки бесплатной для использования get метода.
        # Даже если знали бы и передавали явно её, то это вроде хардкод. 
        # А так если брать список и оттуда доставать бесплатную, вроде норм. Хз
        # Создавать отдельный UC не хотелось бы.

        # Хотя тут я вроде как хочу получить 1 объект, что говорю используя type hitting, но обращаюсь к list методу в репозитории.
        # Корректно так делать? Можно конечно исправить на list[Subscription]. Можно всё равно проверять список этот полученный на его длинну.
        # Если длина списка будет больше 1 (каким-то образом получит 2 подписки бесплатные или больше), то райзить ошибку... 

        user = await self.user_repo.create(user_obj=obj, sub_obj=subscription) # type: ignore
        return Result(item=user)
