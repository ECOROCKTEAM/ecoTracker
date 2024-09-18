from pydantic import BaseModel

from src.core.entity.mission import Mission
from src.core.enum.language import LanguageEnum
from src.core.enum.utils import SortType
from src.core.interfaces.repository.challenges.mission import (
    MissionFilter,
    SortMissionObj,
)


class MissionSchema(BaseModel):
    id: int
    name: str
    active: bool
    score: int
    description: str
    instruction: str
    category_id: int
    language: LanguageEnum

    @classmethod
    def from_obj(cls, item: Mission) -> "MissionSchema":
        return MissionSchema(
            id=item.id,
            name=item.name,
            active=item.active,
            score=item.score,
            description=item.description,
            instruction=item.instruction,
            category_id=item.category_id,
            language=item.language,
        )


class MissionListSchema(BaseModel):
    items: list[MissionSchema]
    limit: int | None
    offset: int
    total: int

    @classmethod
    def from_obj(cls, mission_list: list[Mission], offset: int, total: int, limit: int | None) -> "MissionListSchema":
        items = [MissionSchema.from_obj(item=mission) for mission in mission_list]
        return MissionListSchema(items=items, limit=limit, offset=offset, total=total)


class MissionFilterSchema(BaseModel):
    active: bool | None = None

    def to_obj(self) -> MissionFilter:
        return MissionFilter(active=self.active)


class MissionSortingSchema(BaseModel):
    field: str = "id"
    type: SortType = SortType.DESC

    def to_obj(self) -> SortMissionObj:
        return SortMissionObj(field=self.field, type=self.type)
