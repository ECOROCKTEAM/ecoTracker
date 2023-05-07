from dataclasses import dataclass


@dataclass
class CommunityInviteDTO:
    # Нужен ли нам тут id, если мы поменяли primary key для Community?
    id: int
    community_id: int
    code: str
    expire_time: int


@dataclass
class CommunityInviteCreateDTO:
    community_id: int
    code: str
    expire_time: int


@dataclass
class CommunityInviteUpdateDTO:
    community_id: int
    code: str
    expire_time: int
