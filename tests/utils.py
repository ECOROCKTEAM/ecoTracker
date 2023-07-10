import random
import string


def get_random_str(size: int = 10) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=size))
