from datetime import datetime
from enum import Enum
from runtime import ExecutableRuntime



class ExecutableRunner:

    def run(self, executable:ExecutableRuntime, **kwargs):
        try:
            response = executable.start(**kwargs)
            executable.complete()
        except Exception as e:
            executable.fail()


    