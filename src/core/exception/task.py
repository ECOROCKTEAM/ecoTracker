from src.core.exception.base import DomainError


class TaskAlreadyTakenError(DomainError):
    msg = "For user={user_id} task={task} already taken"
