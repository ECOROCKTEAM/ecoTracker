from src.core.exception.base import RepoError


class UserOperationScoreError(RepoError):
    msg = "Operation={operation} for user={user_id} not allowed"


class CommunityOperationScoreError(RepoError):
    msg = "Operation={operation} for community={community_id} not allowed"
