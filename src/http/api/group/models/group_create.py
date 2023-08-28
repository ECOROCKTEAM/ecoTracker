from __future__ import annotations

from pydantic import BaseModel, Field

from src.core.enum.group.privacy import GroupPrivacyEnum


class GroupCreate(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    GroupCreate - a model defined in OpenAPI

        name: The name of this GroupCreate.
        privacy: The privacy of this GroupCreate.
        description: The description of this GroupCreate [Optional].
    """

    name: str = Field(alias="name")
    privacy: GroupPrivacyEnum = Field(alias="privacy")
    description: str | None = Field(alias="description", default=None)


GroupCreate.update_forward_refs()
