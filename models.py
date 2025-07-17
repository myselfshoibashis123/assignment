from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class State(BaseModel):
    id: str
    name: str
    isInitial: bool = False
    isFinal: bool = False
    enabled: bool = True

class Action(BaseModel):
    id: str
    name: str
    enabled: bool = True
    fromStates: List[str]
    toState: str

class WorkflowDefinition(BaseModel):
    id: str
    name: str
    states: List[State]
    actions: List[Action]

class ActionHistory(BaseModel):
    action_id: str
    timestamp: datetime

class WorkflowInstance(BaseModel):
    id: str
    workflow_id: str
    current_state: str
    history: List[ActionHistory] = []
