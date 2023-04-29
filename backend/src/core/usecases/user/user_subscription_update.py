from dataclasses import dataclass

from src.core.interfaces.repository.user.user import IUserRepository
from src.core.dto.mock import MockObj
from src.core.interfaces.repository.subscription.subscription import ISubscriptionRepository
from src.core.dto.m2m.user.subscription import UserSubscription, UserSubscriptionUpdateDTO, UserSubscriptionCreateDTO
from src.core.interfaces.repository.user.subscription import IUserSubscriptionRepository
from src.core.entity.user import User


@dataclass
class Result:
    item: UserSubscription


class UserSubscriptionUpdateUseCase:
    def __init__(
        self,
        user_sub_repo: IUserSubscriptionRepository,
        sub_repo: ISubscriptionRepository,
        user_repo: IUserRepository,
    ) -> None:
        self.user_sub_repo = user_sub_repo
        self.sub_repo = sub_repo
        self.user_repo = user_repo

    async def __call__(self, user: User, obj: UserSubscriptionUpdateDTO) -> Result:
        if user.is_premium and user.subscription.id == obj.subscription_id:
            """If user wants to extend date of paid subscription."""

            old_user_sub = await self.user_sub_repo.get(user_id=user.username, sub_id=user.subscription.id)
            old_until_date = old_user_sub.until_date
            obj.until_date += old_until_date

            del_old_sub = await self.user_sub_repo.delete(user_id=user.username, sub_id=user.subscription.id)
            # Некоторые методы имеют переменные, но нигде не используюся потом. Можно заменить на андерскор (_).
            # Подумал, что имена переменных дадут понять, что я удаляю именно старую подписку\обновляю на обычную подписку\удаляю старую платную и тп.
            # Если нужно -> изменю на _

            new_obj = UserSubscriptionCreateDTO(
                username=user.username, subscription_id=obj.subscription_id, until_date=obj.until_date
            )

            new_user_paid_sub = await self.user_sub_repo.create(obj=new_obj)
            return Result(item=new_user_paid_sub)

        if user.is_premium and not obj.subscription_id == user.subscription.id:
            """If the user subscription has ended."""

            id_user_paid_sub = user.subscription.id
            user_sub_free = await self.user_repo.update_subscription(user_id=user.username, sub_id=obj.subscription_id)
            del_paid_sub = await self.user_sub_repo.delete(user_id=user.username, sub_id=id_user_paid_sub)

            user_sub = await self.user_sub_repo.get(
                user_id=user.username, sub_id=user.subscription.id
            )  # Мб тут Юзера вернуть?... Лишний запрос мб?

            return Result(item=user_sub)

        if not user.is_premium:
            """If user bought premium subscription"""

            obj = UserSubscriptionCreateDTO(
                username=user.username, subscription_id=obj.subscription_id, until_date=obj.until_date
            )  # type: ignore

            new_paid_sub = await self.user_sub_repo.create(obj=obj)  # type: ignore
            user_sub_paid = await self.user_repo.update_subscription(user_id=user.username, sub_id=obj.subscription_id)
            return Result(item=new_paid_sub)

        free_sub = await self.sub_repo.list(filter_obj=MockObj)[0]  # type: ignore

        # Пока коммент не удалял, чтобы помнить про cancelled

        # Хотим ли мы вообще иметь поле cancelled в подписке? Смысл с этого поля? Отменить подписку? Зачем?
        # Допустим, что у нас пользователь отменил платную подписку, хотя я вряд ли такое допускаю, что возможно.
        # Что тогда? Может просто тогда менять саму подписку с платной, на бесплатную, если ему уже так захотелось "отмениться"?

        # Если у нас пользователь купил подписку на месяц, к примеру и решил её продлить спустя 10 дней пользования ещё на 10 дней вперёд.
        # Если мы наш obj просто передадим в репозиторий так, как есть, то он обновит наши значения без добавления уже имеющегося времени подписки.
        # Нам может здесь, в usecase, получить текущую подписку, взять until_date из текущей подписки и просуммировать с обновляемым значением until_date.
        # И уже в таком виде передавать? Или опять же: это сделать дальше, когда будем работать с бд?

        # У нас стандартная подписка (не прем) будем иметь неограниченный срок действия. Как нам его присваивать? В каком виде?
        # Может можно поставить в модели это поле как nullable=True и если пользователь будет получать стандарт подписку, то поле будет просто null?

        sub = await self.user_sub_repo.update(obj=obj)
        return Result(item=sub)
