from datetime import datetime
from enum import Enum
from .runtime import ExecutableRuntime
from .helper import parse_output_fields, parse_inputfields



class ExecutableRunner:

    def __init__(self, executable_class:ExecutableRuntime, parent=None, db_connector=None,):
        self.db_connector = db_connector
        self.executable = executable_class(db_connector=self.db_connector)
        if parent is not None:
            self.executable.set_parent(parent.execution_id)
            

    def run(self,  **kwargs):
        
        try:
            print("\t[DEBUG] Starting executable")
            input_params = parse_inputfields(self.executable, kwargs)
            print(f"Input params: {input_params}")
            self.executable.start(**input_params)
            print("\t[DEBUG] Will parse the output params")
            output = parse_output_fields(self.executable, self.executable.context)
            print("\t[DEBUG] Will mark the executable as complete")
            self.executable.complete()
            return output
        except Exception as e:
            print(f"\tError: {e}")
            self.executable.fail()


    