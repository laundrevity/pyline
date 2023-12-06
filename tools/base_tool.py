from abc import ABC, abstractmethod


class BaseTool(ABC):
    def __init__(self, manager):
        self.manager = manager
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """
        Execute the function.
        This should have an appropriate docstring that describes its functionality and parameters.
        """
        pass
