from dataclasses import dataclass

from src.core.enum.community.privacy import CommunityPrivacyEnum


@dataclass
class Community:
    """Community entity"""

    name: str
    description: str
    active: bool
    privacy: CommunityPrivacyEnum
