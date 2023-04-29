from src.core.exception.base import DomainError


class TaskAlreadyTakenError(DomainError):
    msg = "For user={username} task={task} already taken"
