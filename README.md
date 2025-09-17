# kram
a light-weight workflow orchestrator written in python to be used as a dependency 

## Sample Example
```
from pykram.operators import ExecutionRuntime
from pykram.types import define_schema, declare_field, InputField
from pykram.utils import run_workflow
from pykram.dag import Workflow, Task


class ParseEffort(Task):
    def run(self):
        print("Running ParseEffort task")


@define_schema(declare_field(InputField("filename")))
class ReadFile(Task):
    def run(self, filename):
        print("Running ReadFile task; FILENMAE: {}".format(filename))


@define_schema(declare_field(InputField("filename")))
class DocParserWf(Workflow):

    def run(self, filename):
        with ExecutionRuntime(self) as ex_runtime:
            ex_runtime.set_vars_(filename=filename)
            ex_runtime.execute_(ReadFile)
            ex_runtime.execute_(ParseEffort)
        return 0
    
response = run_workflow(DocParserWf,filename="records.csv")
```

