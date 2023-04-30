from src.core.exception.base import RepoError


class ConstraintDeleteError(RepoError):
    msg = "This constraint={constraint} is already used by the subscription"
