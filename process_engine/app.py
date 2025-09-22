# workflow_engine/app.py
import uuid

from process_engine.code.engine import WorkflowEngine
from process_engine.code.process_definition import Node, NodeType, ProcessDefinition
from process_engine.service.process_service import ProcessService
from process_engine.service.task_service import TaskService


class WorkflowApplication:
    def __init__(self):
        self.engine = WorkflowEngine()
        self.process_service = ProcessService(self.engine)
        self.task_service = TaskService(self.engine)

    def create_sample_process(self) -> str:
        """
        创建示例流程
        """
        # 创建节点
        nodes = {}

        # 开始节点
        start_node = Node(
            id="start_1",
            name="开始",
            type=NodeType.START,
            outgoing=["task_1"]
        )
        nodes[start_node.id] = start_node

        # 任务节点1
        task1_node = Node(
            id="task_1",
            name="审批任务",
            type=NodeType.TASK,
            properties={
                "task_type": "user_task",
                "assignee": "admin"
            },
            outgoing=["decision_1"],
            incoming=["start_1"]
        )
        nodes[task1_node.id] = task1_node

        # 决策节点
        decision_node = Node(
            id="decision_1",
            name="是否通过",
            type=NodeType.DECISION,
            properties={
                "condition": "{{approval_result}}"
            },
            outgoing=["task_2", "task_3"],  # 通过走task_2，不通过走task_3
            incoming=["task_1"]
        )
        nodes[decision_node.id] = decision_node

        # 通过任务节点
        task2_node = Node(
            id="task_2",
            name="归档处理",
            type=NodeType.TASK,
            properties={
                "task_type": "service_task"
            },
            outgoing=["end_1"],
            incoming=["decision_1"]
        )
        nodes[task2_node.id] = task2_node

        # 不通过任务节点
        task3_node = Node(
            id="task_3",
            name="重新提交",
            type=NodeType.TASK,
            properties={
                "task_type": "user_task",
                "assignee": "user"
            },
            outgoing=["end_1"],
            incoming=["decision_1"]
        )
        nodes[task3_node.id] = task3_node

        # 结束节点
        end_node = Node(
            id="end_1",
            name="结束",
            type=NodeType.END,
            incoming=["task_2", "task_3"]
        )
        nodes[end_node.id] = end_node

        # 创建流程定义
        process_def = ProcessDefinition(
            id=str(uuid.uuid4()),
            name="审批流程",
            version=1,
            nodes=nodes,
            start_node_id="start_1"
        )

        return self.engine.deploy_process(process_def)

    def run_sample(self):
        """
        运行示例
        """
        # 创建流程
        process_id = self.create_sample_process()
        print(f"流程定义创建成功: {process_id}")

        # 启动流程实例
        variables = {
            "applicant": "张三",
            "amount": 10000
        }
        instance_id = self.process_service.start_process_instance(process_id, variables)
        print(f"流程实例启动成功: {instance_id}")

        # 获取流程实例
        instance = self.process_service.get_process_instance(instance_id)
        print(f"流程实例状态: {instance.status}")

        # 查看生成的任务
        tasks = self.engine.instance_repository.find_tasks_by_instance_id(instance_id)
        print(f"生成任务数: {len(tasks)}")
        for task in tasks:
            print(f"  - 任务: {task.name}, 状态: {task.status.value}, 处理人: {task.assignee}")


def main():
    app = WorkflowApplication()
    app.run_sample()


if __name__ == "__main__":
    main()
