# workflow_engine/executor/flow_executor.py
import uuid

from process_engine.code.process_definition import ProcessInstance, ProcessDefinition, Node, NodeType
from process_engine.code.task import Task


class FlowExecutor:
    def __init__(self, engine):
        self.engine = engine

    def execute(self, process_instance: ProcessInstance):
        """
        执行流程实例
        """
        process_definition = self.engine.get_process_definition(process_instance.process_definition_id)

        if not process_definition:
            raise ValueError(f"Process definition not found: {process_instance.process_definition_id}")

        # 获取当前节点
        current_nodes = [process_definition.get_node(node_id) for node_id in process_instance.current_node_ids]
        current_nodes = [node for node in current_nodes if node is not None]

        # 执行每个当前节点
        for node in current_nodes:
            self._execute_node(process_instance, process_definition, node)

    def _execute_node(self, process_instance: ProcessInstance, process_definition: ProcessDefinition, node: Node):
        """
        执行单个节点
        """
        if node.type == NodeType.START:
            self._execute_start_node(process_instance, process_definition, node)
        elif node.type == NodeType.TASK:
            self._execute_task_node(process_instance, process_definition, node)
        elif node.type == NodeType.END:
            self._execute_end_node(process_instance, process_definition, node)
        elif node.type == NodeType.DECISION:
            self._execute_decision_node(process_instance, process_definition, node)
        # 其他节点类型可以继续扩展

    def _execute_start_node(self, process_instance: ProcessInstance, process_definition: ProcessDefinition, node: Node):
        """
        执行开始节点
        """
        # 直接转移到下一个节点
        if node.outgoing:
            next_node_id = node.outgoing[0]  # 简化处理，实际应考虑多出口
            process_instance.current_node_ids = [next_node_id]
            self.engine.instance_repository.update(process_instance)

            # 继续执行下一个节点
            next_node = process_definition.get_node(next_node_id)
            if next_node:
                self._execute_node(process_instance, process_definition, next_node)

    def _execute_task_node(self, process_instance: ProcessInstance, process_definition: ProcessDefinition, node: Node):
        """
        执行任务节点
        """
        # 创建任务
        task = Task(
            id=str(uuid.uuid4()),
            process_instance_id=process_instance.id,
            node_id=node.id,
            name=node.name,
            task_type=node.properties.get("task_type", "user_task"),
            assignee=node.properties.get("assignee"),
            due_date=node.properties.get("due_date")
        )

        # 保存任务
        self.engine.instance_repository.save_task(task)

        # 如果是自动任务，直接执行
        if task.task_type == "service_task":
            task.start_work()
            task.complete()
            self.engine.instance_repository.update_task(task)

            # 转移到下一个节点
            if node.outgoing:
                next_node_id = node.outgoing[0]
                process_instance.current_node_ids = [next_node_id]
                self.engine.instance_repository.update(process_instance)

                next_node = process_definition.get_node(next_node_id)
                if next_node:
                    self._execute_node(process_instance, process_definition, next_node)

    def _execute_end_node(self, process_instance: ProcessInstance):
        """
        执行结束节点
        """
        process_instance.status = "completed"
        process_instance.completed_at = __import__('datetime').datetime.now()
        self.engine.instance_repository.update(process_instance)

    def _execute_decision_node(self, process_instance: ProcessInstance, process_definition: ProcessDefinition,
                               node: Node):
        """
        执行决策节点
        """
        # 简化实现：根据变量值选择路径
        condition = node.properties.get("condition")
        default_path = node.outgoing[-1] if node.outgoing else None

        next_node_id = default_path

        # 根据条件选择路径
        if condition and isinstance(condition, str):
            # 简单的条件判断示例
            if "{{" in condition and "}}" in condition:
                var_name = condition.replace("{{", "").replace("}}", "")
                if var_name in process_instance.variables:
                    var_value = process_instance.variables[var_name]
                    # 根据变量值选择路径
                    for i, outgoing_id in enumerate(node.outgoing):
                        if i < len(node.outgoing) - 1:  # 除了默认路径
                            # 简化：假设条件是值匹配
                            if str(var_value) == str(i):
                                next_node_id = outgoing_id
                                break

        if next_node_id:
            process_instance.current_node_ids = [next_node_id]
            self.engine.instance_repository.update(process_instance)

            next_node = process_definition.get_node(next_node_id)
            if next_node:
                self._execute_node(process_instance, process_definition, next_node)
