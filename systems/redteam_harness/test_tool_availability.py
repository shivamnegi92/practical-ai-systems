import unittest
from systems.redteam_harness.app import BoundedAgent, Plan

class ToolAvailabilityTests(unittest.TestCase):
 def test_noncallable_allowed_entries_are_refused_before_execution(self):
  for value in (None,0,'text',{}):
   agent=BoundedAgent({'broken':value},{'broken'},{'broken'})
   with self.subTest(value=value):
    with self.assertRaisesRegex(ValueError,'allow-listed'):agent.plan({'action':'broken'})
    with self.assertRaisesRegex(ValueError,'allow-listed'):agent.run(Plan('broken',{},False),approved=True)
 def test_callable_tool_and_missing_tool_controls(self):
  agent=BoundedAgent({'owned':lambda:'ok'},{'owned','absent'},{'other'})
  self.assertEqual(agent.run(agent.plan({'action':'owned'}))['result'],'ok')
  with self.assertRaises(ValueError):agent.plan({'action':'absent'})
