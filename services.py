from models import *
from storage import workflow_definitions, workflow_instances
from fastapi import HTTPException
from datetime import datetime
import uuid


def validate_workflow(defn: WorkflowDefinition):
    state_ids = {s.id for s in defn.states}
    if len([s for s in defn.states if s.isInitial]) != 1:
        raise HTTPException(status_code=400, detail="Workflow must have exactly one initial state.")
    if len(state_ids) != len(defn.states):
        raise HTTPException(status_code=400, detail="Duplicate state IDs found.")
    action_ids = {a.id for a in defn.actions}
    if len(action_ids) != len(defn.actions):
        raise HTTPException(status_code=400, detail="Duplicate action IDs found.")
    for action in defn.actions:
        if action.toState not in state_ids:
            raise HTTPException(status_code=400, detail=f"Invalid toState in action {action.id}")
        for fs in action.fromStates:
            if fs not in state_ids:
                raise HTTPException(status_code=400, detail=f"Invalid fromState '{fs}' in action {action.id}")

def create_workflow(defn: WorkflowDefinition):
    validate_workflow(defn)
    if defn.id in workflow_definitions:
        raise HTTPException(status_code=400, detail="Workflow with this ID already exists.")
    workflow_definitions[defn.id] = defn
    return defn

def get_workflow(workflow_id: str):
    if workflow_id not in workflow_definitions:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    return workflow_definitions[workflow_id]

def start_instance(workflow_id: str):
    workflow = get_workflow(workflow_id)
    initial_state = next(s for s in workflow.states if s.isInitial)
    inst_id = str(uuid.uuid4())
    instance = WorkflowInstance(
        id=inst_id,
        workflow_id=workflow_id,
        current_state=initial_state.id
    )
    workflow_instances[inst_id] = instance
    return instance

def get_instance(instance_id: str):
    if instance_id not in workflow_instances:
        raise HTTPException(status_code=404, detail="Instance not found.")
    return workflow_instances[instance_id]

def execute_action(instance_id: str, action_id: str):
    instance = get_instance(instance_id)
    definition = get_workflow(instance.workflow_id)
    current_state = instance.current_state

    if current_state in [s.id for s in definition.states if s.isFinal]:
        raise HTTPException(status_code=400, detail="Cannot execute action from a final state.")

    action = next((a for a in definition.actions if a.id == action_id), None)
    if action is None:
        raise HTTPException(status_code=400, detail="Action not found in workflow.")
    if not action.enabled:
        raise HTTPException(status_code=400, detail="Action is disabled.")
    if current_state not in action.fromStates:
        raise HTTPException(status_code=400, detail="Action not valid from current state.")

    # Perform transition
    instance.current_state = action.toState
    instance.history.append(ActionHistory(action_id=action.id, timestamp=datetime.now()))
    return instance
