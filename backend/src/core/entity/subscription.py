from dataclasses import dataclass

from backend.src.core.dto.subscription import SubscriptionPeriodDTO, SubscriptionTypeDTO


@dataclass
class Subscription:
    """Subscription entity"""

    name: str
    type: SubscriptionTypeDTO
    period: SubscriptionPeriodDTO
