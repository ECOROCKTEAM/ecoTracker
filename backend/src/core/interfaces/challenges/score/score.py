from abc import abstractmethod, ABC


class IScoreRepository(ABC):

    @abstractmethod
    async def user_score_get(self, *, user_id: str) -> UserScoreDTO:
        """ Get score for user

        Args:
            user_id (str): user identify

        Returns:
            UserScoreDTO: DTO for user score
        """

    # @abstractmethod # подумаю в конце
    # async def user_score_list(
    #     self, *, 
    #     username: str = None, 
    #     sorting_obj: str = None,
        
    #     ) -> Union[List[ScoreUserDTO], List[List[ScoreUserDTO], int]]: 
    #     """ Get user score list.

    #     Args:
    #         username (str, optional): if username -> we'll get rating user in this list. Defaults to None.
    #         sorting_obj (str, optional): object for list sorting. Defaults to None.

    #     Returns:
    #         List[ScoreUserDTO]: If username: return user rating and list of DTO user score
    #                             else: return list of DTO user score
    #     """
    #     pass

