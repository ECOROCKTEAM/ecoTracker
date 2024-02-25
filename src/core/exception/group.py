from src.core.exception.base import DomainError, EntityNotActive, RepoError


class GroupNotActive(EntityNotActive):
    msg_template = "Group={id} not active"


class GroupError(DomainError):
    msg_template = "group={group_id} problem"


class GroupDeactivatedError(GroupError):
    msg_template = "group={group_id} deactivated"


class GroupLeaveError(GroupError):
    msg_template = "user={user_id} can't leave group={group_id} "


class GroupPrivacyError(GroupError):
    msg_template = "group={group_id} problem"


class GroupCreateError(GroupError, RepoError):
    msg_template = "create_obj={by_obj}"


class GroupUpdateError(GroupError, RepoError):
    msg_template = "update_obj={by_obj}"


class GroupDeleteError(GroupError, RepoError):
    msg_template = "id={id}"


class GroupNotFoundError(GroupError, RepoError):
    msg_template = "group with id={group_id} not found"


class UserNotInGroup(GroupError, RepoError):
    msg_template = "User connected link with id={link_id} in group not found"


class GroupInviteLinkNotFoundError(GroupError, RepoError):
    msg_template = "Invite link for group with id={group_id} not found"
