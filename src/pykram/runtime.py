from enum import Enum
from abc import abstractmethod
from datetime import datetime
from bson.objectid import ObjectId

class RuntimeState(Enum):
    CREATED = "created"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    
class ExecutableRuntime:

    context = {}

    def __init__(self, db_connector = None):
        print("Initializing runtime")
        self.context = {}
        self.state = RuntimeState.CREATED.value
        self.persist = True
        self.parent_execution_id = None
        
        self.execution_id = None
        self.db_connector = db_connector
        if db_connector is None:
            self.persist = False

    @abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError

    def __persist(self):
        if not self.persist:
            return
        collection = self.db_connector["pykram_executions"]
        data = {
            "name": self.__class__.__name__,
            "type": self.executable_type,
            "state": self.state,
            "parent_execution_id": self.parent_execution_id, 
            "context": self.context,
        }
        if not self.execution_id:
            # Insert new doucment
            data["created_at"] = datetime.now()
            result = collection.insert_one(data)
            execution_id = str(result.inserted_id)
            print(f" Record inserted. ID: {execution_id}. Type of ID: {type(execution_id)}")
            self.execution_id = execution_id
        else:
            # Update existing doucment
            data["updated_at"] = datetime.now()

            result = collection.update_one({"_id": ObjectId(self.execution_id)}, {"$set": data})
            print(f"\t[OK!] Execution with ID: {self.execution_id} updated.")

        
    def set_parent(self, parent_execution_id):
        self.parent_execution_id = parent_execution_id
        self.__persist()

    def set_context(self, new_context):
        self.context = new_context
        self.__persist()

    def __set_state(self, state:RuntimeState):
        self.state = state.value
        self.__persist()
    
    def start(self, **kwargs):
        print("Executable started")
        self.__set_state(RuntimeState.RUNNING)
        self.run(**kwargs)
    
    def complete(self, **kwargs):
        self.__set_state(RuntimeState.SUCCESS)

    def fail(self, **kwargs):
        self.__set_state(RuntimeState.FAILED)
