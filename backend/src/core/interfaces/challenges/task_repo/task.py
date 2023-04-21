from abc import abstractmethod, ABC

class ITaskRepository(ABC):

    @abstractmethod
    async def task_list(
                        self, *, 
                        sorting_obj: MockObj, 
                        paggination_obj: MockObj, 
                        filter_obj: MockObj
                        ) -> List[TaskDTO]:
        """ List of tasks

        Args:
            sorting_obj (str): sorting object
            paggination_obj (str): paggination object
            filter_obj (str): filter object

        Returns:
            List[TaskDTO]: List of DTO task objects
        """

    @abstractmethod
    async def task_get(self, *, task_id: int) -> TaskDTO: 
        """Get task

        Args:
            task_id (int): task identify

        Returns:
            TaskDTO: DTO of task object
        """
        pass

    @abstractmethod
    async def task_update(self, *, task_id: int, obj: TaskUpdateDTO) -> TaskDTO:
        """Task update

        Args:
            task_id (int): task identify
            obj (TaskUpdateDTO): DTO for update task method

        Returns:
            TaskDTO: DTO of task object
        """

    @abstractmethod
    async def task_delete(self, *, task_id: int) -> int:
        """delete task 

        Args:
            task_id (int): task identify

        Returns:
            int: id of deleted task
        """

    @abstractmethod
    async def task_create(self, *, obj: TaskCreateDTO) -> TaskDTO:
        """Create task

        Args:
            obj (TaskCreateDTO): DTO for creating task

        Returns:
            TaskDTO: DTO of task object
        """
        pass
