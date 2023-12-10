from __future__ import annotations

from pydantic import BaseModel, Field


class GroupJoinByCode(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    GroupJoinByCode - a model defined in OpenAPI

        code: The code of this GroupJoinByCode [Optional].
    """

    code: str = Field(alias="code", default=None)


GroupJoinByCode.update_forward_refs()