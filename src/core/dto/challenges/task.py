from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class TaskUserPlanCreateDTO:
    user_id: str
    task_id: int


@dataclass
class TaskUserCreateDTO:
    task_id: int
    status: OccupancyStatusEnum = OccupancyStatusEnum.ACTIVE


@dataclass
class TaskUserUpdateDTO:
    date_close: datetime | None = field(init=False, default=None)
    status: OccupancyStatusEnum | None = None

    def __post_init__(self):
        if self.status in [OccupancyStatusEnum.FINISH, OccupancyStatusEnum.REJECT, OccupancyStatusEnum.OVERDUE]:
            self.date_close = datetime.now(tz=timezone.utc)
