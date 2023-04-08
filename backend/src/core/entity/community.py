from dataclasses import dataclass

from backend.src.core.enum.community import PrivacyEnum


@dataclass
class Community:
    """Community entity"""

    name: str
    description: str
    active: bool
    privacy: PrivacyEnum
