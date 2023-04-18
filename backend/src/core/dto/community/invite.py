from dataclasses import dataclass

@dataclass
class CommunityInviteDTO:
    id: int
    community_id: str
    code: str
    expire_time: int


@dataclass
class CommunityInviteCreateDTO:
    community_id: str
    code: str
    expire_time: int


@dataclass
class CommunityInviteUpdateDTO:
    community_id: str
    code: str
    expire_time: int
