import sys
import unittest

from src.control_panel.actions import PROJECT_ROOT, build_actions
from src.control_panel.theme import BUTTON_COLORS, PALETTE, PANEL_BG, TITLE_LETTER_COLORS
from src.control_panel.workflow import WorkflowState


class ControlPanelActionsTest(unittest.TestCase):
    def test_actions_follow_safe_operational_order(self):
        actions = build_actions()
        self.assertEqual(
            [action.key for action in actions[:3]],
            ["reset_schema", "validate_api", "etl_api_snapshot"],
        )

    def test_reset_is_explicitly_destructive(self):
        reset = build_actions()[0]
        self.assertTrue(reset.destructive)
        self.assertIn("--yes", reset.command)

    def test_real_etl_triggers_are_marked_as_snapshot_actions(self):
        actions = {action.key: action for action in build_actions()}
        self.assertTrue(actions["etl_api_snapshot"].stores_snapshot)
        self.assertTrue(actions["etl_raw_snapshot"].stores_snapshot)
        self.assertFalse(actions["validate_api"].stores_snapshot)
        self.assertIn("--dry-run", actions["validate_api"].command)
        self.assertTrue(actions["etl_api_snapshot"].primary)
        self.assertFalse(actions["etl_raw_snapshot"].primary)

    def test_api_snapshot_is_the_only_primary_shortcut(self):
        primary = [action.key for action in build_actions() if action.primary]
        self.assertEqual(primary, ["etl_api_snapshot"])

    def test_commands_use_current_python_and_project_paths(self):
        for action in build_actions():
            self.assertEqual(action.command[0], sys.executable)
        self.assertTrue((PROJECT_ROOT / "sql" / "schema.sql").exists())

    def test_button_colors_come_from_project_palette(self):
        self.assertEqual(
            tuple(action.color for action in build_actions()),
            BUTTON_COLORS,
        )
        self.assertEqual(
            set(PALETTE.values()),
            {"#355070", "#6d597a", "#b56576", "#e56b6f", "#eaac8b"},
        )
        self.assertEqual(TITLE_LETTER_COLORS, tuple(PALETTE.values()))
        self.assertEqual(PANEL_BG, "#f6ded1")


class WorkflowStateTest(unittest.TestCase):
    def test_only_first_step_is_initially_enabled(self):
        workflow = WorkflowState(6)
        self.assertEqual([workflow.is_enabled(i) for i in range(6)], [True, False, False, False, False, False])

    def test_success_releases_only_successor(self):
        workflow = WorkflowState(6)
        workflow.complete(0, True)
        self.assertEqual(workflow.current_index, 1)
        self.assertTrue(workflow.is_enabled(1))
        self.assertFalse(workflow.is_enabled(0))

    def test_failure_keeps_same_step_enabled(self):
        workflow = WorkflowState(6)
        workflow.complete(0, False)
        self.assertEqual(workflow.current_index, 0)

    def test_last_success_restarts_cycle(self):
        workflow = WorkflowState(6)
        for index in range(6):
            workflow.complete(index, True)
        self.assertEqual(workflow.current_index, 0)
        self.assertTrue(workflow.is_enabled(0))
        self.assertFalse(any(workflow.is_enabled(i) for i in range(1, 6)))


if __name__ == "__main__":
    unittest.main()
