from fastapi import FastAPI
from models import WorkflowDefinition, WorkflowInstance
from services import (
    create_workflow,
    get_workflow,
    start_instance,
    get_instance,
    execute_action
)
from typing import Dict, List

app = FastAPI()

@app.post("/workflows", response_model=WorkflowDefinition)
def create_workflow_api(defn: WorkflowDefinition):
    return create_workflow(defn)

@app.get("/workflows/{workflow_id}", response_model=WorkflowDefinition)
def get_workflow_api(workflow_id: str):
    return get_workflow(workflow_id)

@app.post("/instances", response_model=WorkflowInstance)
def start_instance_api(workflow_id: str):
    return start_instance(workflow_id)

@app.get("/instances/{instance_id}", response_model=WorkflowInstance)
def get_instance_api(instance_id: str):
    return get_instance(instance_id)

@app.post("/instances/{instance_id}/actions", response_model=WorkflowInstance)
def execute_action_api(instance_id: str, action_id: str):
    return execute_action(instance_id, action_id)


