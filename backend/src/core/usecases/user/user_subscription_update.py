from dataclasses import dataclass

from src.core.dto.m2m.user.subscription import UserSubscriptionDTO, UserSubscriptionUpdateDTO
from src.core.interfaces.user.subscription import IUserSubscriptionRepository
from src.core.entity.user import User


@dataclass
class Result:
    item: UserSubscriptionDTO


class UserSubscriptionUpdateUseCase:
    def __init__(self, repo: IUserSubscriptionRepository) -> None:
        self.repo = repo

    async def __call__(self, user: User, obj: UserSubscriptionUpdateDTO) -> Result:

    # Хотим ли мы вообще иметь поле cancelled в подписке? Смысл с этого поля? Отменить подписку? Зачем?
    # Допустим, что у нас пользователь отменил платную подписку, хотя я вряд ли такое допускаю, что возможно.
    # Что тогда? Может просто тогда менять саму подписку с платной, на бесплатную, если ему уже так захотелось "отмениться"?

    # Если у нас пользователь купил подписку на месяц, к примеру и решил её продлить спустя 10 дней пользования ещё на 10 дней вперёд.
    # Если мы наш obj просто передадим в репозиторий так, как есть, то он обновит наши значения без добавления уже имеющегося времени подписки.
    # Нам может здесь, в usecase, получить текущую подписку, взять until_date из текущей подписки и просуммировать с обновляемым значением until_date.
    # И уже в таком виде передавать? Или опять же: это сделать дальше, когда будем работать с бд?

    # У нас стандартная подписка (не прем) будем иметь неограниченный срок действия. Как нам его присваивать? В каком виде?
    # Может можно поставить в модели это поле как nullable=True и если пользователь будет получать стандарт подписку, то поле будет просто null?

        sub = await self.repo.update(obj=obj)
        return Result(item=sub)
