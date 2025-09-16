class BaseWorkflow:

    def __init__(self):
        self.tasks = []

    def add_task(self, task_name):
        self.tasks.append(task_name)