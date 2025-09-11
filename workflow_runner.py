from datetime import datetime
from enum import Enum

class WorkflowStateEnum(Enum):
    INIT = "init"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

class TaskStateEnum(Enum):
    INIT = "init"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

class WorkflowRunner:

    def __init__(self, db_connector=None):
        self.persist_in_db = db_connector is not None
        if self.persist_in_db:
            self.db_collection = db_connector["kram_actions"]
        self.context = {}
    
    def __init_workflow_record(self, workflow):
        wf_exec_record = {
            "name": workflow.__class__.__name__,
            "type": "workflow",
            "created_at": datetime.now(),
            "status": WorkflowStateEnum.INIT.value,
            "execution_msg": None,
            "execution_context": {}
        } # The db record depicting the unique wf execution
        try:
            result = self.db_collection.insert_one(wf_exec_record)
            return result.inserted_id
        except Exception as e:
            print(f"[ERROR] Error while persisting execution info in database. Error: {str(e)}")
            return None
        
    def __update_workflow_state_in_db(self, workflow_exec_id, status, msg=None):
        # Fetch the wf execution record from database
        if not workflow_exec_id:
            raise Exception("Workflow execution ID is null")
        if not status:
            raise Exception("Workflow status is null")
        filter_query = {
            "_id": workflow_exec_id
        }
        update_query = {
            "$set": {"status": status, "execution_msg": msg}
        }
        try:
            self.db_collection.update_one(filter_query, update_query)
        except Exception as e:
            print(f'''[ERROR] Failed to update state of wrokflow execution with ID: {workflow_exec_id},
                  Error: {str(e)}''')
            
    def __update_workflow_context_in_db(self, workflow_exec_id, context={}):
        # Fetch the wf execution record from database
        if not workflow_exec_id:
            raise Exception("Workflow execution ID is null")
        filter_query = {
            "_id": workflow_exec_id
        }
        update_query = {
            "$set": {"execution_context": context}
        }
        try:
            self.db_collection.update_one(filter_query, update_query)
        except Exception as e:
            print(f'''[ERROR] Failed to update state of wrokflow execution with ID: {workflow_exec_id},
                  Error: {str(e)}''')
            
    def __init_task_record(self, task, workflow):
        task_exec_record = {
            "name": task.__class__.__name__,
            "workflow_name": workflow.__class__.__name__,
            "type": "task",
            "created_at": datetime.now(),
            "status": TaskStateEnum.INIT.value,
            "execution_msg": None,
            
        } # The db record depicting the unique task execution
        try:
            result = self.db_collection.insert_one(task_exec_record)
            return result.inserted_id
        except Exception as e:
            print(f"[ERROR] Error while persisting execution info in database. Error: {str(e)}")
            return None
        
    def __update_task_state_in_db(self, task_exec_id, status, msg=None):
        # Fetch the wf execution record from database
        if not task_exec_id:
            raise Exception("Task execution ID is null")
        if not status:
            raise Exception("Task status is null")
        filter_query = {
            "_id": task_exec_id
        }
        update_query = {
            "$set": {"status": status, "execution_msg": msg}
        }
        try:
            self.db_collection.update_one(filter_query, update_query)
        except Exception as e:
            print(f'''[ERROR] Failed to update state of task execution with ID: {task_exec_id},
                  Error: {str(e)}''')
            
    



    def run_workflow(self, workflow):
        workflow_execution_id = None
        if self.persist_in_db:
            workflow_execution_id = self.__init_workflow_record(workflow)

        workflow.define()
        is_wf_success = True
        task_execution_status = {}
        if self.persist_in_db and len(workflow.tasks) > 0 :
            self.__update_workflow_state_in_db(
                workflow_execution_id,
                WorkflowStateEnum.RUNNING.value
            )

        for task in workflow.tasks:
            try:
                # run the task 
                task_exec_id = None
                if self.persist_in_db:
                    task_exec_id = self.__init_task_record(task, workflow)
                self.__update_task_state_in_db(task_exec_id, TaskStateEnum.RUNNING.value)
                response = getattr(task, "run")(self.context)
                
                
                self.context = {**self.context, **response}
                task_execution_status[task.__class__.__name__] = {"status": True, "msg": None}
                self.__update_task_state_in_db(task_exec_id, TaskStateEnum.SUCCESS.value)
                self.__update_workflow_context_in_db(workflow_execution_id, context=self.context)

            except Exception as e:
                task_execution_status[task.__class__.__name__] = {"status": False, "msg": str(e)}
                is_wf_success = False
                self.__update_task_state_in_db(task_exec_id, TaskStateEnum.FAILED.value)
                self.__update_workflow_state_in_db(workflow_execution_id, WorkflowStateEnum.FAILED.value)
                break
        self.__update_workflow_state_in_db(workflow_execution_id, WorkflowStateEnum.SUCCESS.value)
        return {
            "status": is_wf_success,
            "tasks": task_execution_status,
            "outputs": self.context
        }

            




        # # Load the workflow metadata
        # wf_metadata = self.__get_workflow_metadata(workflow_name)
        # # execute each task
        # is_wf_success = True
        # for task in wf_metadata.get("tasks", []):
        #     response = self.__execute_task(task)
        #     if not response['status']:
        #         is_wf_success = false
        #         break
        
        # self.__persist_workflow_status(is_wf_success)
        

        
