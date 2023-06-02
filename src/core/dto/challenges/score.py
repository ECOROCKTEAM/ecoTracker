from dataclasses import dataclass

from src.core.enum.score.operation import ScoreOperationEnum


@dataclass
class ScoreOperationValueDTO:
    value: int
    operation: ScoreOperationEnum
