from src.core.exception.base import DomainError, RepoError


class CommunityError(DomainError):
    msg_template = "community={community_id} problem"


class CommunityDeactivatedError(CommunityError):
    msg_template = "community={community_id} deactivated"


class CommunityLeaveError(CommunityError):
    msg_template = "user={user_id} can't leave community={community_id} "


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


class UserNotInCommunity(CommunityError, RepoError):
    msg_template = "User connected link with id={link_id} in community not found"


class CommunityInviteLinkNotFoundError(CommunityError, RepoError):
    msg_template = "Invite link for Community with id={community_id} not found"
