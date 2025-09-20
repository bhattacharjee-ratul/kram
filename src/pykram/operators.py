from abc import ABC, abstractmethod
from types import MethodType
from .dag import Workflow
from .utils import run_executable_with_parameters
from .types import OutputField

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
        response = run_executable_with_parameters(
            task_instance, self.workflow_instance.workflow_context)
        import pdb;pdb.set_trace()
        type_of_response = type(response)

        if type_of_response is not tuple:
            response = (response,)
        # Now parse the output fields and store the returned response accordingly
        for index, field in enumerate(task_instance.__dict__.items()):
            field_name, field_definition = field
            if field_definition.__class__ == OutputField:
                 
                value_to_be_stored = response[index]
                # validate the datatype of the output if mentioned in the declaration
                if field_definition.validate_datatype:
                    if type(value_to_be_stored) != field_definition.datatype:
                        raise Exception(f"Wrong datatype provided for field {field_name}")
                
                self.workflow_instance.workflow_context[field_name] = value_to_be_stored
    
        
        

        



        





    
    




