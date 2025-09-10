class WorkflowRunner:

    def __init__(self, database_connector=None):

        # if not database_connector:
        #     raise Exception("Database connection not provided")
        # self.db_conn = database_connector
        self.context = {}

    # def __get_workflow_metadata(self, workflow_name):
    #     query = {}
    #     workflow_metadata = self.db_conn.execute(query)
    #     return workflow_metadata
    
    # def __execute_task(self, task, params={}):
    #     pass
    #     return {
    #         "status": True,
    #         "output": None,
    #         "msg": None
    #         }
    
    # def __persist_workflow_status(self, status):
    #     pass

    def run_workflow(self, workflow):
        workflow.define()
        is_wf_success = True
        task_execution_status = {}
        for task in workflow.tasks:
            try:
                # run the task 
                response = getattr(task, "run")(self.context)
                self.context = {**self.context, **response}
                task_execution_status[task.__class__.__name__] = {"status": True, "msg": None}
            except Exception as e:
                task_execution_status[task.__class__.__name__] = {"status": False, "msg": str(e)}
                is_wf_success = False
                break
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
        

        
