from dataclasses import dataclass
from typing import Optional

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
    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    privacy_id: Optional[int] = None
