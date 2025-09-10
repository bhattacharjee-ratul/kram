from abc import ABC, abstractmethod

class AbstractTask(ABC):

    @abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError