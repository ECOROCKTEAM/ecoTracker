# from abc import abstractmethod, ABC

# from src.core.dto.community.score import CommunityBoundOffsetDTO, CommunityRatingDTO, CommunityOperationWithScoreDTO
# from src.core.dto.mock import MockObj
# from src.core.dto.user.score import OperationWithScoreUserDTO, UserBoundOffsetDTO, UserRatingDTO


# class IRepositoryScore(ABC):
#     @abstractmethod
#     async def community_change(self, *, obj: CommunityOperationWithScoreDTO) -> CommunityRatingDTO:
#         """Action with community score

#         Args:
#             obj (CommunityOperationWithScoreDTO): DTO of community object, value and math operator

#         Returns:
#             CommunityRatingDTO: DTO of community score object
#         """

#     @abstractmethod
#     async def community_get(self, *, community_id: int) -> CommunityRatingDTO:
#         """Get community score

#         Args:
#             community_id (int): community identify

#         Returns:
#             CommunityRatingDTO: DTO of community score object
#         """

#     @abstractmethod
#     async def user_get(self, *, user_id: int) -> UserRatingDTO:
#         """Get user score

#         Args:
#             user_id (int): user identify

#         Returns:
#             UserRatingDTO: DTO of user score object
#         """

#     @abstractmethod
#     async def community_rating(
#         self,
#         *,
#         order_obj: MockObj,
#         obj: CommunityBoundOffsetDTO | None = None,
#     ) -> dict[int, CommunityRatingDTO]:
#         """Get community rating

#         Args:
#             order_obj (MockObj): order object
#             obj (CommunityBoundOffsetDTO | None, optional): DTO of community object.
#                 If not None return rating for specific community with bound offset.
#                 If None return global community rating.
#                 Defaults to None.

#         Returns:
#             dict[int, CommunityRatingDTO]: Dict with rating position as a key and DTO community object as a value.
#         """

#     @abstractmethod
#     async def user_rating(
#         self,
#         *,
#         obj: UserBoundOffsetDTO | None = None,
#         order_obj: MockObj,
#     ) -> dict[int, UserRatingDTO]:
#         """Get user rating

#         Args:
#             obj (UserBoundOffsetDTO, optional): DTO for specific user. Defaults to None.
#                                                 If None -> rating of all users.
#             order_obj (MockObj): Order for score value

#         Returns:
#             list[UserScore]: List of DTO user score objects
#         """

#     @abstractmethod
#     async def user_change(self, *, obj: OperationWithScoreUserDTO) -> UserRatingDTO:
#         """Operation with user score (addiction, subtraction, multiplication, division)

#         Args:
#             obj (IncrementScoreUserDTO): DTO of user object, value and math operator

#         Returns:
#             UserRatingDTO: DTO of user value object
#         """
