from dataclasses import dataclass

from src.core.dto.achievement import AchievementCategoryDTO


@dataclass
class AchievementProgress:
    achievement_name: str
    counter: int
    active: bool
    entity_id: int
    entity_name: str


@dataclass
class Achievement:
    name: str
    description: str
    category: AchievementCategoryDTO
    total: int
    status: bool
