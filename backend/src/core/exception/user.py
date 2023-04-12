from src.core.exception.base import DomainError, RepoError, PermissionError


class UserError(DomainError):
    msg_template = "user_id={user_id} problem"


class UserPermissionError(UserError, PermissionError):
    msg_template = "user_id={user_id} permission problem"


class UserIsNotCommunitySuperUserError(UserPermissionError):
    msg_template = "User with id={user_id} is not super user in community with id={community_id}"


class UserIsNotCommunityAdminUserError(UserPermissionError):
    msg_template = "User with id={user_id} is not admin user in community with id={community_id}"


class UserIsNotPremiumError(UserPermissionError):
    msg_template = "User with id={user_id} not have Premium subscription"


class UserNotFoundError(UserError, RepoError):
    msg_template = "User with id={user_id} not found"
