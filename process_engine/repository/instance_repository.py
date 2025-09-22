# workflow_engine/repository/instance_repository.py
from typing import Dict, List, Optional

from process_engine.code.process_definition import ProcessInstance
from process_engine.code.task import Task


class InstanceRepository:
    def __init__(self):
        self.instances: Dict[str, ProcessInstance] = {}
        self.tasks: Dict[str, Task] = {}

    def save(self, instance: ProcessInstance):
        self.instances[instance.id] = instance

    def find_by_id(self, instance_id: str) -> Optional[ProcessInstance]:
        return self.instances.get(instance_id)

    def update(self, instance: ProcessInstance):
        self.instances[instance.id] = instance

    def save_task(self, task: Task):
        self.tasks[task.id] = task

    def find_task_by_id(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def update_task(self, task: Task):
        self.tasks[task.id] = task

    def find_tasks_by_instance_id(self, instance_id: str) -> List[Task]:
        return [task for task in self.tasks.values() if task.process_instance_id == instance_id]
