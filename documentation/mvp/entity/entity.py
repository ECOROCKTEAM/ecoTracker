from dataclasses import dataclass, field
from typing import List, Union
from enum import Enum


# BASE DTO


@dataclass
class TypeDTO:
    name: str


@dataclass
class OccupancyDTO(TypeDTO):
    """"""


# Enum


class AchivmentRelatedWithEnum(str, Enum):
    TASK = "TASK"
    SUBSCRIPTION = "SUBSCRIPTION"
    MISSION = "MISSION"
    NUMBER_OF_USERS = "NUMBER_OF_USERS"


class VariableTypeEnum(Enum):
    STR = str
    INT = int
    BOOL = bool


class OccupancyStatusEnum(str, Enum):
    ACTIVE = "ACTIVE"
    FINISH = "FINISH"
    REJECT = "REJECT"
    OVERDUE = "OVERDUE"


class PrivacyEnum(str, Enum):
    PUBLICK = "PUBLICK"
    PRIVATE = "PRIVATE"


class RelatedEnum(str, Enum):
    USER = "USER"
    COMMUNITY = "COMMUNITY"


class RoleEnum(str, Enum):
    SUPERUSER = "SUPERUSER"
    ADMIN = "ADMIN"
    USER = "USER"


class AchievementStatusEnum(str, Enum):
    RECEIVED = "RECEIVED"
    UNCOMPLETED = "UNCOMPLETED"


# Types

VariableValueType = Union[int, str, bool]

# Mixin


@dataclass
class VariableTypeCastMixin:
    def __cast_to_bool(self, value: str) -> bool:
        return bool(value)

    def __cast_to_int(self, value: str) -> int:
        return int(value)

    @property
    def __cast_op(self) -> dict:
        return {
            VariableTypeEnum.STR: lambda x: x,
            VariableTypeEnum.INT: self.__cast_to_int,
            VariableTypeEnum.BOOL: self.__cast_to_bool,
        }

    def _cast_type(self, value: str, to_type: VariableTypeEnum) -> VariableValueType:
        f = self.__cast_op.get(to_type)
        if f is None:
            raise Exception("Not found caster")
        converted_value = f(value)
        if not isinstance(converted_value, to_type.value):
            raise Exception("Can't cast value")
        return converted_value


# Shared DTO


@dataclass
class OccupancyCategoryDTO:
    id: int
    name: str


# DTO


@dataclass
class UserContactTypeDTO(TypeDTO):
    """"""


@dataclass
class UserContactDTO:
    value: str
    active: bool
    type: UserContactTypeDTO


@dataclass
class UserContactListDTO:
    contacts: List[UserContactDTO]

    def __getattr__(self, request_type: str):
        tmp = None
        for contact in self.contacts:
            if contact.type.name == request_type:
                tmp = contact
                break
        else:
            raise Exception("Not found")
        return tmp


@dataclass
class SubscriptionPeriodTypeDTO(TypeDTO):
    name: str


@dataclass
class SubscriptionPeriodDTO:
    name: str
    value: int
    type: SubscriptionPeriodTypeDTO


@dataclass
class SubscriptionConstrainsDTO(VariableTypeCastMixin):
    name: str
    _raw_value: str
    type: VariableTypeEnum

    @property
    def value(self) -> VariableValueType:
        return self._cast_type(value=self._raw_value, to_type=self.type)


@dataclass
class SubscriptionListConstrainsDTO:
    name: str
    constrains: List[SubscriptionConstrainsDTO]


@dataclass
class SubscriptionTypeDTO:
    name: str


@dataclass
class Subscription:
    """Subscription entity"""

    name: str
    type: SubscriptionTypeDTO
    period: SubscriptionPeriodDTO


@dataclass
class User:
    """User entity"""

    username: str
    password: str
    active: bool
    subscription: Subscription


@dataclass
class UserCommunityRoleDTO:
    user_pointer: str
    community_pointer: str
    role: RoleEnum


@dataclass
class Community:
    """Community entity"""

    name: str
    description: str
    active: bool
    privacy: PrivacyEnum


@dataclass
class Task:
    id: int
    name: str
    description: str
    score: int
    category: OccupancyCategoryDTO
    status: OccupancyStatusEnum


@dataclass
class MissionBase:
    id: int
    name: str
    description: str
    instruction: str
    score: int
    author: str  # user.username
    category: OccupancyCategoryDTO
    status: OccupancyStatusEnum
    related: RelatedEnum = field(init=False)


@dataclass
class MisssionUser(MissionBase):
    def __post_init__(self):
        self.related = RelatedEnum.USER


@dataclass
class MissionCommunity(MissionBase):

    place: str
    meeting_date: int
    people_required: int
    people_max: int
    comment: str

    def __post_init__(self):
        self.related = RelatedEnum.COMMUNITY


@dataclass
class ScoreBaseDTO:
    value: int
    related: RelatedEnum = field(init=False)


@dataclass
class ScoreUserDTO(ScoreBaseDTO):
    def __post_init__(self):
        self.related = RelatedEnum.USER


@dataclass
class ScoreCommunityDTO(ScoreBaseDTO):
    def __post_init__(self):
        self.related = RelatedEnum.COMMUNITY


@dataclass
class NotificationType(TypeDTO):
    """"""


@dataclass
class Notification:
    id: int
    active: bool
    type: NotificationType


@dataclass
class Language:
    language_code: str
    language_name: str


@dataclass
class Setting:
    name: str
    notification: Notification
    language: Language


@dataclass
class AchievementCategoryDTO(TypeDTO):
    """"""


@dataclass
class AchievementProgress:
    related_achiev_id: int
    point_counter: int
    active_status: bool
    entity_id: int
    entity_name: str


@dataclass
class AchievementBase:
    name: str
    description: str
    category: AchievementCategoryDTO
    status: AchievementStatusEnum
    related: RelatedEnum = field(init=False)
    total: int


@dataclass
class AchievementCommunity(AchievementBase):
    def __post_init__(self):
        self.related = RelatedEnum.COMMUNITY


@dataclass
class AchievementUser(AchievementBase):
    def __post_init__(self):
        self.related = RelatedEnum.USER



