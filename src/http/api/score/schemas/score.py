from pydantic import BaseModel, Field


class CommunityScoreDTO(BaseModel):
    """
    CommunityScoreDTO - a model defined in OpenAPI

        community_id: The community_id of this CommunityScoreDTO.
        value: The value of this CommunityScoreDTO.
    """

    community_id: int = Field(alias="community_id", default=None)
    value: int = Field(alias="value", default=None)


class UserScoreDTO(BaseModel):
    """
    UserScoreDTO - a model defined in OpenAPI

        user_id: The user_id of this UserScoreDTO.
        value: The value of this UserScoreDTO.
    """

    user_id: int = Field(alias="user_id", default=None)
    value: int = Field(alias="value", default=None)
