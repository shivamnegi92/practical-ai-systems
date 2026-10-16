import unittest
from systems.redteam_harness.app import BoundedAgent, Plan

class RunPolicyTests(unittest.TestCase):
 def test_forged_flag_cannot_bypass_current_approval_policy(self):
  calls=[]
  agent=BoundedAgent({'write':lambda:calls.append('called')},{'write'},{'write'})
  plan=Plan('write',{},False)
  self.assertEqual(agent.run(plan)['status'],'awaiting_approval')
  self.assertEqual(calls,[])
  self.assertEqual(agent.run(plan,approved=True)['status'],'completed')
  self.assertEqual(calls,['called'])
 def test_stricter_plan_and_allow_list_checks_are_preserved(self):
  agent=BoundedAgent({'read':lambda:'ok'},{'read'},{'other'})
  self.assertEqual(agent.run(Plan('read',{},True))['status'],'awaiting_approval')
  self.assertEqual(agent.run(Plan('read',{},False))['result'],'ok')
  with self.assertRaises(ValueError): agent.run(Plan('other',{},False),approved=True)
