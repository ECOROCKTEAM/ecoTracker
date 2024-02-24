from dataclasses import dataclass

from src.core.enum.challenges.status import OccupancyStatusEnum


@dataclass
class OccupancyStatisticFilter:
    status__in: list[OccupancyStatusEnum] | None
