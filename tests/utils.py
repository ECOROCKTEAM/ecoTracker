import random
import string
from time import perf_counter
from uuid import uuid4


def get_uuid() -> str:
    return str(uuid4())


def get_random_str(size: int = 10) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=size))


class catchtime:
    def __init__(self, msg: str | None = None) -> None:
        self.msg = msg or ""

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self.time = perf_counter() - self.start
        print(f"{self.msg} Time: {self.time:.3f} seconds")
