from __future__ import annotations

from pydantic import BaseModel, Field

from src.core.enum.community.privacy import CommunityPrivacyEnum


class CommunityCreate(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    CommunityCreate - a model defined in OpenAPI

        name: The name of this CommunityCreate.
        privacy: The privacy of this CommunityCreate.
        description: The description of this CommunityCreate [Optional].
    """

    name: str = Field(alias="name")
    privacy: CommunityPrivacyEnum = Field(alias="privacy")
    description: str | None = Field(alias="description", default=None)


CommunityCreate.update_forward_refs()
