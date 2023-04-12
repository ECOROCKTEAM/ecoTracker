from src.core.exception.base import DomainError, RepoError


class CommunityError(DomainError):
    msg_template = "community_id={community_id} problem"


class CommunityPrivacyError(CommunityError):
    msg_template = "community_id={community_id} problem"


class CommunityCreateError(CommunityError, RepoError):
    msg_template = "create_obj={by_obj}"


class CommunityUpdateError(CommunityError, RepoError):
    msg_template = "update_obj={by_obj}"


class CommunityDeleteError(CommunityError, RepoError):
    msg_template = "id={id}"



class CommunityNotFoundError(CommunityError, RepoError):
    msg_template = "Community with id={user_id} not found"
