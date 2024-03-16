import itertools
import random
import string
from time import perf_counter
from uuid import uuid4


def get_uuid() -> str:
    return str(uuid4())


def get_random_str(size: int = 10) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=size))


def permutation_by_dict_values(in_: dict) -> list[dict]:
    """Yes, that is permutation without repeat!

    Example:
        fltr_values = {
            "active": [True, False, None],
            "category_id": [1,2,3, None]
        }
        fltr_experiments = fltr_permutation(fltr_values)
        for item in fltr_experiments:
            print(item)

        # On this example that prints!
        {'active': True, 'category_id': 1}
        {'active': True, 'category_id': 2}
        {'active': True, 'category_id': 3}
        {'active': True, 'category_id': None}
        {'active': False, 'category_id': 1}
        {'active': False, 'category_id': 2}
        {'active': False, 'category_id': 3}
        {'active': False, 'category_id': None}
        {'active': None, 'category_id': 1}
        {'active': None, 'category_id': 2}
        {'active': None, 'category_id': 3}
        {'active': None, 'category_id': None}
    """
    experiment_list = []
    keys, values = zip(*in_.items())
    for v in itertools.product(*values):
        experiment = dict(zip(keys, v))
        experiment_list.append(experiment)
    return experiment_list


class catchtime:
    def __init__(self, msg: str | None = None) -> None:
        self.msg = msg or ""

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self.time = perf_counter() - self.start
        print(f"{self.msg} Time: {self.time:.3f} seconds")
