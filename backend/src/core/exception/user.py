from src.core.exception import DomainError, PermissionError

class CreateUserError(DomainError):
    msg = "username={username} or password={password} problem"


class UserIsNotPremiumError(PermissionError):
    msg = "username={username} isn't premium"


class UserIsNotApplicationAdminError(PermissionError):
    msg = "username={username} isn't admin of application"


class UserIsNotActivateError(PermissionError, DomainError):
    msg = "username={username} isn't activate"