from abc import ABC, abstractmethod

class IProducer(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def produce(self, event) -> True:
        raise NotImplementedError
