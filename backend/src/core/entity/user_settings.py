from dataclasses import dataclass

from backend.src.core.dto.user_settings import NotificationType


@dataclass
class Notification:
    id: int
    active: bool
    type: NotificationType


@dataclass
class Language:
    name: str
    code: str


@dataclass
class Settings:
    name: str
    notification: Notification
    language: Language
