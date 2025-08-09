from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, agent_name, model, api_key):
        self.agent_name = agent_name
        self.model = model
        # self.endpoint = endpoint
        self.api_key = api_key

    @abstractmethod
    def parse(self, text: str) -> str:
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented parse()")

    @abstractmethod
    def analyst(self, income, expense, balance) -> str:
        raise NotImplementedError(f"{self.__class__.__name__} has not implemented ocr()")

    # @abstractmethod
    # def ocr(self, image_path: str) -> str:
    #     raise NotImplementedError(f"{self.__class__.__name__} has not implemented ocr()")