from dataclasses import asdict, dataclass

from src.core.typing.base import UNSET


@dataclass
class UpdateDTO:
    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v != UNSET}
