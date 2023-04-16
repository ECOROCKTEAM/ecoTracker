from src.core.exception.base import DomainError, RepoError, PermissionError


class UserError(DomainError):
    msg_template = "username={username} problem"


class UserPermissionError(UserError, PermissionError):
    msg_template = "username={username} permission problem"


class UserIsNotCommunitySuperUserError(UserPermissionError):
    msg_template = "User with username={username} is not super user in community with community={community_id}"


class UserIsNotCommunityAdminUserError(UserPermissionError):
    msg_template = "User with username={username} is not admin user in community with community={community_id}"


class UserIsNotPremiumError(UserPermissionError):
    msg_template = "User with username={username} not have Premium subscription"


class UserNotFoundError(UserError, RepoError):
    msg_template = "User with username={username} not found"


class UserIsNotActivateError(UserError):
    msg = "username={username} isn't activate"