import unittest
from systems.redteam_harness.app import BoundedAgent, run_battery


class ToolErrorTests(unittest.TestCase):
    def test_tool_errors_are_distinct_from_policy_rejections_and_do_not_stop_the_battery(self):
        def fail_type(): raise TypeError('synthetic failure')
        def fail_value(): raise ValueError('synthetic failure')
        names = {'fail_type', 'fail_value', 'ok'}
        agent = BoundedAgent({'fail_type': fail_type, 'fail_value': fail_value, 'ok': lambda: 'ok'}, names, names)
        cases = [{'name': action, 'request': {'action': action, 'arguments': {}}, 'approved': True, 'should_be_allowed': action == 'ok'} for action in ('fail_type', 'fail_value', 'missing', 'ok')]
        report = run_battery(agent, cases)
        self.assertEqual([r['outcome'] for r in report['results']], ['error', 'error', 'rejected', 'completed'])
        self.assertEqual([r.get('error_type') for r in report['results']], ['TypeError', 'ValueError', None, None])
        self.assertEqual(report['error_count'], 2)
        self.assertEqual(report['cases'], 4)
        self.assertEqual(report['breach_rate'], 0)

    def test_empty_battery_has_no_errors(self):
        self.assertEqual(run_battery(BoundedAgent({}, set()), [])['error_count'], 0)
