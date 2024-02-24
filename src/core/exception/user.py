from src.core.exception.base import (
    DomainError,
    EntityNotActive,
    PermissionError,
    RepoError,
)


class UserNotActive(EntityNotActive):
    msg_template = "User={id} not active"


class UserError(DomainError):
    msg_template = "user_id={user_id} problem"


class UserPermissionError(UserError, PermissionError):
    msg_template = "user_id={user_id} permission problem"


class UserIsNotGroupSuperUserError(UserPermissionError):
    msg_template = "User with user_id={user_id} is not super user in group with group={group_id}"


class UserIsNotGroupAdminUserError(UserPermissionError):
    msg_template = "User with user_id={user_id} is not admin user in group with group={group_id}"


class UserIsNotPremiumError(UserPermissionError):
    msg_template = "User with user_id={user_id} not have Premium subscription"


class UserNotFoundError(UserError, RepoError):
    msg_template = "User with user_id={user_id} not found"


class UserIsNotActivateError(UserError):
    msg_template = "User with user_id={user_id} not active"


class UserTaskMaxAmountError(UserError, RepoError):
    msg_template = "User with user_id={user_id} has maximum tasks"


class UserTaskStatusError(RepoError):
    msg_template = "Object_id={obj_id} has not status ACTIVE"


class TaskAlreadyTakenError(UserError, RepoError):
    msg_template = "User_id={user_id} already has this task_id={task_id}"


class UserDoesNotHaveThisTaskError(UserError, RepoError):
    msg_template = "User_id={user_id} does not have this task_id{task_id}"


class UserCanNotRejectFinishedTaskError(UserError, RepoError):
    msg_template = "Task_id={task_id} cannot be rejected while he hase 'finish' status"
