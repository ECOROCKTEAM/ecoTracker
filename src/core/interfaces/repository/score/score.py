# from abc import abstractmethod, ABC

# from src.core.dto.community.score import CommunityBoundOffsetDTO, CommunityScoreDTO, CommunityOperationWithScoreDTO
# from src.core.dto.mock import MockObj
# from src.core.dto.user.score import OperationWithScoreUserDTO, UserBoundOffsetDTO, UserScoreDTO


# class IRepositoryScore(ABC):
#     @abstractmethod
#     async def community_change(self, *, obj: CommunityOperationWithScoreDTO) -> CommunityScoreDTO:
#         """Action with community score

#         Args:
#             obj (CommunityOperationWithScoreDTO): DTO of community object, value and math operator

#         Returns:
#             CommunityScoreDTO: DTO of community score object
#         """

#     @abstractmethod
#     async def community_get(self, *, community_id: int) -> CommunityScoreDTO:
#         """Get community score

#         Args:
#             community_id (int): community identify

#         Returns:
#             CommunityScoreDTO: DTO of community score object
#         """

#     @abstractmethod
#     async def user_get(self, *, user_id: int) -> UserScoreDTO:
#         """Get user score

#         Args:
#             user_id (int): user identify

#         Returns:
#             UserScoreDTO: DTO of user score object
#         """

#     @abstractmethod
#     async def community_rating(
#         self,
#         *,
#         order_obj: MockObj,
#         obj: CommunityBoundOffsetDTO | None = None,
#     ) -> dict[int, CommunityScoreDTO]:
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
#     ) -> dict[int, UserScoreDTO]:
#         """Get user rating

#         Args:
#             obj (UserBoundOffsetDTO, optional): DTO for specific user. Defaults to None.
#                                                 If None -> rating of all users.
#             order_obj (MockObj): Order for score value

#         Returns:
#             list[UserScore]: List of DTO user score objects
#         """

#     @abstractmethod
#     async def user_change(self, *, obj: OperationWithScoreUserDTO) -> UserScoreDTO:
#         """Operation with user score (addiction, subtraction, multiplication, division)

#         Args:
#             obj (IncrementScoreUserDTO): DTO of user object, value and math operator

#         Returns:
#             UserScoreDTO: DTO of user value object
#         """
