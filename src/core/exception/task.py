from src.core.exception.base import DomainError


class TaskAlreadyTakenError(DomainError):
    msg = "For user={user_id} task={task} already taken"


class TaskAlreadyDeactivatedError(DomainError):
    msg = "Task_id={task_id} already deactivated."


class TaskDeactivatedError(DomainError):
    msg = "Task_id={task_id} deactivated"
