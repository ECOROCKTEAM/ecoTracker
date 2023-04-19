from src.core.exception.base import DomainError, RepoError


class CommunityError(DomainError):
    msg_template = "community={community_id} problem"


class CommunityDeactivatedError(CommunityError):
    msg_template = "community={community_id} deactivated"


class CommunityPrivacyError(CommunityError):
    msg_template = "community={community_id} problem"


class CommunityCreateError(CommunityError, RepoError):
    msg_template = "create_obj={by_obj}"


class CommunityUpdateError(CommunityError, RepoError):
    msg_template = "update_obj={by_obj}"


class CommunityDeleteError(CommunityError, RepoError):
    msg_template = "id={id}"


class CommunityNotFoundError(CommunityError, RepoError):
    msg_template = "Community with id={community_id} not found"


class CommunityUserNotFoundError(CommunityError, RepoError):
    msg_template = "CommunityUser with id={link_id} not found"

class CommunityInviteLinkNotFoundError(CommunityError, RepoError):
    msg_template = "Invite link for Community with id={community_id} not found"