# workflow_engine/repository/definition_repository.py
from typing import Dict, Optional

from process_engine.code.process_definition import ProcessDefinition


class DefinitionRepository:
    def __init__(self):
        self.definitions: Dict[str, ProcessDefinition] = {}

    def save(self, definition: ProcessDefinition):
        self.definitions[definition.id] = definition

    def find_by_id(self, definition_id: str) -> Optional[ProcessDefinition]:
        return self.definitions.get(definition_id)

    def find_all(self) -> Dict[str, ProcessDefinition]:
        return self.definitions.copy()


