from dataclasses import dataclass
from typing import Optional

from src.core.enum.community import PrivacyEnum


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
    privacy: PrivacyEnum
    description: str = ""
    active: bool = True


@dataclass
class CommunityUpdateDTO:
    name: Optional[str] = None
    privacy: Optional[PrivacyEnum] = None
    description: Optional[str] = None
    active: Optional[bool] = None
