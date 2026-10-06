"""A deterministic, allow-listed workflow with explicit human approval."""
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Plan:
 action: str
 arguments: dict
 requires_approval: bool

class BoundedAgent:
 def __init__(self, tools: dict[str,Callable], allowed: set[str], approval_required: set[str] | None = None):
  self.tools=tools; self.allowed=allowed; self.approval_required=approval_required or set(allowed)
 def plan(self, request: dict) -> Plan:
  action=request.get('action','')
  if action not in self.allowed or action not in self.tools:
   raise ValueError('action is not allow-listed')
  args=request.get('arguments',{})
  if not isinstance(args,dict): raise ValueError('arguments must be an object')
  return Plan(action,args,action in self.approval_required)
 def run(self, plan: Plan, approved: bool=False):
  if plan.action not in self.allowed or plan.action not in self.tools: raise ValueError('action is not allow-listed')
  if not isinstance(plan.arguments,dict): raise ValueError('arguments must be an object')
  if plan.requires_approval and not approved: return {'status':'awaiting_approval','action':plan.action}
  return {'status':'completed','action':plan.action,'result':self.tools[plan.action](**plan.arguments)}
