from __future__ import annotations

from pydantic import BaseModel, Field


class CommunityJoinByCode(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    CommunityJoinByCode - a model defined in OpenAPI

        code: The code of this CommunityJoinByCode [Optional].
    """

    code: str = Field(alias="code", default=None)


CommunityJoinByCode.update_forward_refs()