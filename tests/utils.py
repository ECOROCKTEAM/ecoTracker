import random
import string
from uuid import uuid4


def get_uuid() -> str:
    return str(uuid4())


def get_random_str(size: int = 10) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=size))
