from .operators import ExecutableRuntime
from abc import abstractmethod

class Task(ExecutableRuntime) :

    def __init__(self):
        self.super().__init__()
    
    @abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError


class Workflow(ExecutableRuntime):

    def __init__(self):
        self.super().__init__()

    @abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError

    
    
