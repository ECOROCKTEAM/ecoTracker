from pydantic import BaseModel

from src.core.entity.subscription import Subscription
from src.core.entity.user import User
from src.core.enum.language import LanguageEnum


class SubscriptionSchema(BaseModel):
    @classmethod
    def from_entity(cls, subscription: Subscription) -> "SubscriptionSchema":
        return SubscriptionSchema()


class UserSchema(BaseModel):
    id: str
    username: str
    active: bool
    subscription: SubscriptionSchema
    language: LanguageEnum
    is_premium: bool

    @classmethod
    def from_entity(cls, user: User) -> "UserSchema":
        return UserSchema(
            id=user.id,
            username=user.username,
            active=user.active,
            subscription=SubscriptionSchema.from_entity(subscription=user.subscription),
            language=user.language,
            is_premium=user.is_premium,
        )
