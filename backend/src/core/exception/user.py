from src.core.exception import DomainError

class CreateUserError(DomainError):
    msg = "username={username} of password={password} problem"