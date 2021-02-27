import typing
from abc import ABC, abstractmethod

class IRecordWriter(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def write_record(self, record: object) -> bool:
        raise NotImplementedError
