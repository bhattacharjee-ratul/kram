# kram
a light-weight workflow orchestrator written in python to be used as a dependency 

## Sample Example
### Directory Structure
```
.
├── main.py
├── tasks
│├── __init__.py
│├── calculate_sum.py
│└── generate_numbers.py
└── workflows
    └── calculator_wf.py
```

**File tasks/generate_numbers.py**

from kram.abstract_task import AbstractTask

class GenerateNumbers(AbstractTask):

    def run(self, params):
        return {"numbers": [1,2,3,4,5]}

----------------------------------------------



**File tasks/calculate_sum.py**

from kram.abstract_task import AbstractTask

class CalculateSum(AbstractTask):

    def run(self, params):
        numbers = params['numbers']
        return {"result": sum(numbers)}

--------------------------------------------

**File workflows/calculator_wf.py**

from tasks.calculate_sum import CalculateSum
from tasks.generate_numbers import GenerateNumbers
from kram.base_workflow import BaseWorkflow

class CalculatorWf(BaseWorkflow):

    def __init__(self):
        super().__init__()

    def define(self):
        self.add_task(GenerateNumbers())
        self.add_task(CalculateSum())

------------------------------------------

**File main.py**

from kram.workflow_runner import WorkflowRunner
from workflows.calculator_wf import CalculatorWf


wf_runner = WorkflowRunner()

workflow = CalculatorWf()
status = wf_runner.run_workflow(workflow)
print(status)





