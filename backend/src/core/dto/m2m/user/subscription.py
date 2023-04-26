from dataclasses import dataclass


@dataclass
class UserSubscriptionDTO:
    id: int
    username: str
    subscription_id: int
    cancelled: bool
    until_date: int


@dataclass
class UserSubscriptionCreateDTO:
    username: str
    subscription_id: int
    until_date: int
    cancelled: bool = False


@dataclass
class UserSubscriptionUpdateDTO:
    id: int
    subscription_id: int
    cancelled: bool 
    until_date: int

    # Хотим ли мы вообще иметь поле cancelled в подписке? Смысл с этого поля? Отменить подписку? Зачем?
    # Допустим, что у нас пользователь отменил платную подписку, хотя я вряд ли такое допускаю, что возможно.
    # Что тогда? Может просто тогда менять саму подписку с платной, на бесплатную, если ему уже так захотелось "отмениться".