from dataclasses import dataclass

from src.core.enum.community.privacy import PrivacyEnum


@dataclass
class Community:
    """Community entity"""

    name: str
    description: str
    active: bool
    privacy: PrivacyEnum


@dataclass
class CommunityCreateDTO:
    name: str
    privacy_id: int
    description: str = ""
    active: bool = True


@dataclass
class CommunityUpdateDTO:
    name: str | None = None
    description: str | None = None
    active: bool | None = None
    privacy: PrivacyEnum | None = None
