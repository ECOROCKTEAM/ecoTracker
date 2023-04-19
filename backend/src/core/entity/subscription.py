from dataclasses import dataclass

<<<<<<< HEAD
@dataclass
class Subscription:
    """"""
=======
from src.core.enum.base import VariableTypeEnum
from src.core.dto.subscription import SubscriptionPeriodDTO, SubscriptionTypeDTO


@dataclass
class Subscription:
    """Subscription entity"""

    name: str
    type: SubscriptionTypeDTO
    period: SubscriptionPeriodDTO
    canceled: bool
    untildate: datetime


@dataclass
class Constraint:
    id: str
    name: str
    value: str
    value_type: VariableTypeEnum
>>>>>>> origin/develop
