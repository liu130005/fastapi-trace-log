# workflow_engine/core/process_definition.py
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional


class NodeType(Enum):
    START = "start"
    END = "end"
    TASK = "task"
    DECISION = "decision"
    PARALLEL = "parallel"
    JOIN = "join"


class TaskType(Enum):
    USER_TASK = "user_task"
    SERVICE_TASK = "service_task"
    SCRIPT_TASK = "script_task"


@dataclass
class Node:
    id: str
    name: str
    type: NodeType
    properties: Dict[str, Any] = field(default_factory=dict)
    outgoing: List[str] = field(default_factory=list)
    incoming: List[str] = field(default_factory=list)


@dataclass
class ProcessDefinition:
    id: str
    name: str
    version: int
    nodes: Dict[str, Node]
    start_node_id: str
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def get_start_node(self) -> Node:
        return self.nodes[self.start_node_id]

    def get_node(self, node_id: str) -> Optional[Node]:
        return self.nodes.get(node_id)


@dataclass
class ProcessInstance:
    id: str
    process_definition_id: str
    status: str  # running, completed, suspended, terminated
    variables: Dict[str, Any] = field(default_factory=dict)
    current_node_ids: List[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.status == "running"

    def is_completed(self) -> bool:
        return self.status == "completed"
