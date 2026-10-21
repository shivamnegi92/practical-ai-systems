import unittest
from systems.bounded_agent.app import BoundedAgent

class ApprovalDefaultsTests(unittest.TestCase):
 def test_omitted_and_none_gate_all_tools(self):
  for agent in (BoundedAgent({'read':lambda:'ok'},{'read'}),BoundedAgent({'read':lambda:'ok'},{'read'},None)):
   plan=agent.plan({'action':'read'})
   self.assertTrue(plan.requires_approval)
   self.assertEqual(agent.run(plan)['status'],'awaiting_approval')
 def test_explicit_empty_set_and_partial_set_are_preserved(self):
  tools={'read':lambda:'ok','write':lambda:'done'}; allowed=set(tools)
  for required in (set(),{'write'}):
   agent=BoundedAgent(tools,allowed,required)
   self.assertEqual(agent.run(agent.plan({'action':'read'}))['result'],'ok')
   self.assertEqual(agent.plan({'action':'write'}).requires_approval,'write' in required)
   with self.assertRaises(ValueError): agent.plan({'action':'unknown'})
