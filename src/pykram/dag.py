from .runtime import ExecutableRuntime
from abc import abstractmethod

class Task(ExecutableRuntime) :

    executable_type = "workflow"
    def __init__(self, **kwargs):
        super().__init__( **kwargs)
        self.executable_type = self.__class__.__name__
    
    @abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError


class Workflow(ExecutableRuntime):

    executable_type = "workflow"
    def __init__(self, **kwargs):
        print("Initializing workflow class ")
        super().__init__(**kwargs)
        
    @abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError

    
    
