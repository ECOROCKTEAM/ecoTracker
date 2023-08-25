from dataclasses import dataclass

from src.core.enum.group.privacy import GroupPrivacyEnum


@dataclass
class GroupCreateDTO:
    name: str
    privacy: GroupPrivacyEnum
    description: str = ""
    active: bool = True


@dataclass
class GroupUpdateDTO:
    name: str | None = None
    description: str | None = None
    active: bool | None = None
    privacy: GroupPrivacyEnum | None = None
