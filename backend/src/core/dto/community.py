from dataclasses import dataclass

from src.core.enum.community import PrivacyEnum


@dataclass
class CreateCommunityDTO:
    name: str
    description: str
    privacy: PrivacyEnum