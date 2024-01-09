from dataclasses import asdict
from typing import Any


def skip_none_dict_factory(d: list[tuple[str, Any]]) -> dict:
    return {k: v for (k, v) in d if v is not None}


def as_dict_skip_none(d) -> dict:
    return asdict(d, dict_factory=skip_none_dict_factory)


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance
