from abc import ABC, abstractmethod

class IStreamHandler(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def handle(self, stream):
        raise NotImplementedError
