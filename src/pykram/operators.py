from abc import ABC, abstractmethod
from types import MethodType
from .dag import Workflow
from .utils import run_executable_with_parameters

class ExecutionRuntime:
    '''
        @brief: This class contain the information about the workflow that is running.
        This implements the Context Manger protocol.
    '''

    def __init__(self, workflow_instance:Workflow):
        self.workflow_instance = workflow_instance

    def __enter__(self):
        return self
    
    def __exit__(self, x,y,z):
        print(f"Closing the execution runtime; x={x}, y={y}, z={z}")
        return self
    
    # the Execution runtime also contains several functions that are exposed to the user to be used for defining the workflow

    def set_vars_(self, **kwargs):
        '''
            Recieves a set of variable names and values. Sets these variables in the workflow context. 
            Existing variables in the workflow context with the same name gets overridden.
        '''
        for key, value in kwargs.items():
            self.workflow_instance.workflow_context[key] = value

                
    def execute_(self, task_class):
        task_instance = task_class()
        run_executable_with_parameters(
            task_instance, self.workflow_instance.workflow_context)
        





    
    




