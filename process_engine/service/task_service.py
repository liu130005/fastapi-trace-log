# workflow_engine/service/task_service.py
from typing import List

from process_engine.code.engine import WorkflowEngine
from process_engine.code.task import Task, TaskStatus


class TaskService:
    def __init__(self, engine: WorkflowEngine):
        self.engine = engine

    def get_tasks_by_assignee(self, assignee: str) -> List[Task]:
        """
        根据处理人获取任务
        """
        # 需要在repository中添加相应方法
        all_tasks = []  # 这里应该从repository获取
        return [task for task in all_tasks if task.assignee == assignee]

    def assign_task(self, task_id: str, assignee: str):
        """
        分配任务
        """
        task = self.engine.instance_repository.find_task_by_id(task_id)
        if task:
            task.assign(assignee)
            self.engine.instance_repository.update_task(task)

    def start_task(self, task_id: str):
        """
        开始处理任务
        """
        task = self.engine.instance_repository.find_task_by_id(task_id)
        if task and task.status == TaskStatus.ASSIGNED:
            task.start_work()
            self.engine.instance_repository.update_task(task)

    def complete_task(self, task_id: str, variables: dict = None):
        """
        完成任务
        """
        self.engine.complete_task(task_id, variables)
