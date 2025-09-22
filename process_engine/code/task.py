# workflow_engine/core/task.py
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any


class TaskStatus(Enum):
    CREATED = "created"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    process_instance_id: str
    node_id: str
    name: str
    task_type: str
    assignee: Optional[str] = None
    status: TaskStatus = TaskStatus.CREATED
    variables: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    assigned_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    due_date: Optional[datetime] = None

    def assign(self, assignee: str):
        self.assignee = assignee
        self.status = TaskStatus.ASSIGNED
        self.assigned_at = datetime.now()

    def start_work(self):
        if self.status == TaskStatus.ASSIGNED:
            self.status = TaskStatus.IN_PROGRESS

    def complete(self):
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()

    def fail(self):
        self.status = TaskStatus.FAILED
