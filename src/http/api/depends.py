from sqlalchemy import select

from src.core.dto.subscription.period import SubscriptionPeriodDTO
from src.core.entity.subscription import Subscription, SubscriptionTranslateDTO
from src.core.entity.user import User
from src.core.enum.language import LanguageEnum
from src.core.enum.subscription.subscription import (
    SubscriptionPeriodUnitEnum,
    SubscriptionTypeEnum,
)
from src.core.interfaces.unit_of_work import IUnitOfWork
from src.data.models.user.user import UserModel
from src.data.unit_of_work import SqlAlchemyUnitOfWork
from src.http.database.manager import db_manager


def get_uow() -> IUnitOfWork:
    return SqlAlchemyUnitOfWork(db_manager.session_factory)


async def get_fake_user() -> User:
    return User(
        id=1337,
        username="shrek",
        password="xdxdxd whaaat??",
        active=True,
        subscription=Subscription(
            id=1,
            period=SubscriptionPeriodDTO(id=1, unit=SubscriptionPeriodUnitEnum.DAY, value=1),
            translations=[
                SubscriptionTranslateDTO(id=1, name="aaa", subscription_id=1, language=LanguageEnum.EN),
                SubscriptionTranslateDTO(id=1, name="aaa", subscription_id=1, language=LanguageEnum.RU),
            ],
            type=SubscriptionTypeEnum.USUAL,
        ),
        language=LanguageEnum.EN,
    )


async def get_user() -> User:
    async with db_manager.session_factory() as sess:
        stmt = select(UserModel).limit(1)
        user = await sess.scalar(stmt)
        if user is None:
            raise NotImplementedError("User not found")
        return User(
            id=user.id,
            username=user.username,
            password=user.password,
            active=user.active,
            subscription=Subscription(
                id=1,
                period=SubscriptionPeriodDTO(id=1, unit=SubscriptionPeriodUnitEnum.DAY, value=1),
                translations=[
                    SubscriptionTranslateDTO(id=1, name="aaa", subscription_id=1, language=LanguageEnum.EN),
                    SubscriptionTranslateDTO(id=1, name="aaa", subscription_id=1, language=LanguageEnum.RU),
                ],
                type=SubscriptionTypeEnum.USUAL,
            ),
            language=LanguageEnum.EN,
        )
