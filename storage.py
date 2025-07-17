from typing import Dict,List
from models import WorkflowDefinition, WorkflowInstance

# In-memory stores
workflow_definitions: Dict[str, WorkflowDefinition] = {}
workflow_instances: Dict[str, WorkflowInstance] = {}
