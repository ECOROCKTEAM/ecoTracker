from src.core.exception.base import RepoError


class UserOperationScoreError(RepoError):
    msg = "Operation={operation} for user={user_id} not allowed"


class GroupOperationScoreError(RepoError):
    msg = "Operation={operation} for group={group_id} not allowed"
