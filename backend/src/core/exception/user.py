from src.core.exception import DomainError, PermissionError

class CreateUserError(DomainError):
    msg = "username={username} or password={password} problem"


class UserIsNotPremiumError(PermissionError):
    msg = "username={username} is not premium"