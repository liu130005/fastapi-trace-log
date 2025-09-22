# workflow_engine/service/process_service.py
import uuid
from typing import Dict, List, Optional

from ..code.engine import WorkflowEngine
from ..code.process_definition import ProcessInstance


class ProcessService:
    def __init__(self, engine: WorkflowEngine):
        self.engine = engine

    def create_process_definition(self, name: str, nodes: Dict, start_node_id: str, ProcessDefinition=None) -> str:
        """
        创建流程定义
        """

        process_def = ProcessDefinition(
            id=str(uuid.uuid4()),
            name=name,
            version=1,
            nodes=nodes,
            start_node_id=start_node_id
        )

        return self.engine.deploy_process(process_def)

    def start_process_instance(self, process_definition_id: str, variables: Dict = None) -> str:
        """
        启动流程实例
        """
        return self.engine.start_process(process_definition_id, variables)

    def get_process_instance(self, instance_id: str) -> Optional[ProcessInstance]:
        """
        获取流程实例详情
        """
        return self.engine.get_process_instance(instance_id)

    def get_process_instances(self) -> List[ProcessInstance]:
        """
        获取所有流程实例
        """
        # 这里需要在repository中添加相应方法
        return []
