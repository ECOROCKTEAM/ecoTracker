from src.core.exception.base import DomainError, RepoError


class MissionError(DomainError):
    msg_template = "mission={mission_id} problem"


class MissionDeactivatedError(MissionError):
    msg_template = "mission={mission_id} deactivated"