from dataclasses import dataclass
from src.core.enum.community.privacy import CommunityPrivacyEnum


@dataclass
class CommunityCreateDTO:
    name: str
    privacy: CommunityPrivacyEnum
    description: str = ""
    active: bool = True


@dataclass
class CommunityUpdateDTO:
    name: str | None = None
    description: str | None = None
    active: bool | None = None
    privacy: CommunityPrivacyEnum | None = None
