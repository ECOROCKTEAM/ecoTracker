from dataclasses import dataclass

from src.core.dto.community.privacy import PrivacyDTO


@dataclass
class Community:
    """Community entity"""

    name: str
    description: str
    active: bool
    privacy: PrivacyDTO


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
    privacy_id: int | None = None
