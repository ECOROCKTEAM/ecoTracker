from pydantic import BaseModel

from src.core.dto.user.score import UserRatingDTO, UserScoreDTO


class UserScoreSchema(BaseModel):
    user_id: str
    score: int

    @classmethod
    def from_obj(cls, score: UserScoreDTO) -> "UserScoreSchema":
        return UserScoreSchema(user_id=score.user_id, score=score.score)


class UserRatingSchema(BaseModel):
    user_id: str
    score: int
    position: int

    @classmethod
    def from_obj(cls, rating: UserRatingDTO) -> "UserRatingSchema":
        return UserRatingSchema(user_id=rating.user_id, score=rating.score, position=rating.position)


class UserRatingListSchema(BaseModel):
    items: list[UserRatingSchema]

    @classmethod
    def from_obj(cls, rating_list: list[UserRatingDTO]) -> "UserRatingListSchema":
        items = [UserRatingSchema.from_obj(item) for item in rating_list]
        return UserRatingListSchema(items=items)
