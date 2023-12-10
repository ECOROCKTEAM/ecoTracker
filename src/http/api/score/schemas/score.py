from pydantic import BaseModel, Field


class GroupScoreDTO(BaseModel):
    """
    GroupScoreDTO - a model defined in OpenAPI

        group_id: The group_id of this GroupScoreDTO.
        value: The value of this GroupScoreDTO.
    """

    group_id: int = Field(alias="group_id", default=None)
    value: int = Field(alias="value", default=None)


class UserScoreDTO(BaseModel):
    """
    UserScoreDTO - a model defined in OpenAPI

        user_id: The user_id of this UserScoreDTO.
        value: The value of this UserScoreDTO.
    """

    user_id: str = Field(alias="user_id", default=None)
    value: int = Field(alias="value", default=None)
