from datetime import datetime
from enum import Enum
from .runtime import ExecutableRuntime



class ExecutableRunner:

    def __init__(self, db_connector=None):
        self.db_connector = db_connector

    def run(self, executable_class:ExecutableRuntime, **kwargs):
        executable = executable_class(db_connector=self.db_connector)
        print(f"Type pf executable: {executable.executable_type}")
        try:
            response = executable.start(**kwargs)
            executable.complete()
        except Exception as e:
            executable.fail()


    