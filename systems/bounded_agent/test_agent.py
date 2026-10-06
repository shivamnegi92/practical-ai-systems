import unittest
from systems.bounded_agent.app import BoundedAgent

class AgentTests(unittest.TestCase):
 def setUp(self): self.agent=BoundedAgent({'lookup':lambda key:key},{'lookup'},approval_required={'lookup'})
 def test_requires_approval(self):
  plan=self.agent.plan({'action':'lookup','arguments':{'key':'x'}})
  self.assertEqual(self.agent.run(plan)['status'],'awaiting_approval')
  self.assertEqual(self.agent.run(plan,approved=True)['status'],'completed')
 def test_rejects_unknown_action(self):
  with self.assertRaises(ValueError): self.agent.plan({'action':'shell','arguments':{}})
 def test_plan_is_immutable(self):
  plan=self.agent.plan({'action':'lookup','arguments':{'key':'x'}})
  with self.assertRaises(Exception): plan.action='shell'
