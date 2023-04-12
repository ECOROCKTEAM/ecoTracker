from dataclasses import dataclass
from src.core.dto.base import TypeDTO


@dataclass
class NotificationType(TypeDTO):
    """"""


@dataclass
class NotificationDTO:
    id: int
    active: bool
    type: NotificationType


@dataclass
class LanguageDTO:
    name: str
    code: str


@dataclass
class SettingsDTO:
    name: str
    notification: NotificationDTO
    language: LanguageDTO
