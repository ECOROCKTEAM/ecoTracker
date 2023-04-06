from dataclasses import dataclass

from backend.src.core.dto.achievement import AchievementCategoryDTO


@dataclass
class AchievementProgress:
    achievement_id: int
    entity_id: int
    entity_name: str
    counter: int
    active: bool


@dataclass
class AchievementBase:
    name: str
    description: str
    category: AchievementCategoryDTO
    total: int
