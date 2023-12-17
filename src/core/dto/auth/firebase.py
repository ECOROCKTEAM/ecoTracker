from dataclasses import dataclass

from src.core.enum.auth.providers import AuthProviderEnum


@dataclass
class UserFirebase:
    id: str
    name: str
    active: bool
    pic: str
    firebase_app_name: str
    auth_time: int
    email: str
    provider: AuthProviderEnum
