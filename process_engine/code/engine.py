# workflow_engine/core/engine.py
import uuid
from typing import Dict, Optional, Any

from process_engine.code.process_definition import ProcessDefinition, ProcessInstance
from process_engine.code.task import TaskStatus
from process_engine.executor.flow_executor import FlowExecutor
from process_engine.repository.definition_repository import DefinitionRepository
from process_engine.repository.instance_repository import InstanceRepository


class WorkflowEngine:
    def __init__(self):
        self.definition_repository = DefinitionRepository()
        self.instance_repository = InstanceRepository()
        self.flow_executor = FlowExecutor(self)

    def deploy_process(self, process_definition: ProcessDefinition) -> str:
        """
        部署流程定义
        """
        self.definition_repository.save(process_definition)
        return process_definition.id

    def start_process(self, process_definition_id: str, variables: Dict[str, Any] = None) -> str:
        """
        启动流程实例
        """
        process_definition = self.definition_repository.find_by_id(process_definition_id)
        if not process_definition or not process_definition.is_active:
            raise ValueError(f"Process definition {process_definition_id} not found or not active")

        # 创建流程实例
        process_instance = ProcessInstance(
            id=str(uuid.uuid4()),
            process_definition_id=process_definition_id,
            status="running",
            variables=variables or {},
            current_node_ids=[process_definition.start_node_id]
        )

        # 保存流程实例
        self.instance_repository.save(process_instance)

        # 执行流程
        self.flow_executor.execute(process_instance)

        return process_instance.id

    def get_process_instance(self, instance_id: str) -> Optional[ProcessInstance]:
        """
        获取流程实例
        """
        return self.instance_repository.find_by_id(instance_id)

    def get_process_definition(self, definition_id: str) -> Optional[ProcessDefinition]:
        """
        获取流程定义
        """
        return self.definition_repository.find_by_id(definition_id)

    def complete_task(self, task_id: str, variables: Dict[str, Any] = None):
        """
        完成任务
        """
        task = self.instance_repository.find_task_by_id(task_id)
        if not task or task.status != TaskStatus.IN_PROGRESS:
            raise ValueError(f"Task {task_id} not found or not in progress")

        task.complete()
        if variables:
            task.variables.update(variables)

        self.instance_repository.update_task(task)

        # 继续执行流程
        process_instance = self.instance_repository.find_by_id(task.process_instance_id)
        self.flow_executor.execute(process_instance)
