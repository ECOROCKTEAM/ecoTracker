from enum import Enum


<<<<<<< HEAD:backend/src/core/enum/community/role.py
class CommunityRoleEnum(str, Enum):
    SUPERUSER = "SUPERUSER"
    ADMIN = "ADMIN"
    USER = "USER"
    BLOCKED = "BLOCKED"
=======
class ApplicationRoleEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class RoleEnum(str, Enum):
    SUPERUSER = "SUPERUSER"
    ADMIN = "ADMIN"
    USER = "USER"

>>>>>>> origin/develop:backend/src/core/enum/role.py
