from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

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


class DbManager:
    def __init__(self):
        self.session_factory = None
        self._engine = None

    async def initialize(self, db_url):
        self._engine = create_async_engine(url=db_url)
        # async with self._engine.begin() as conn:
        #     await conn.run_sync(UserModel.metadata.create_all)
        self.session_factory = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    async def dispose(self):
        await self._engine.dispose()


db_manager = DbManager()


def get_uow() -> IUnitOfWork:
    return SqlAlchemyUnitOfWork(db_manager.session_factory)


async def get_user() -> User:
    async with db_manager.session_factory() as sess:
        stmt = select(UserModel).limit(1)
        user = await sess.scalar(stmt)
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
