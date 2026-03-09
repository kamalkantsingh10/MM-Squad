"""Tests for PM workflow step-file refactor — Story 2.9."""

from pathlib import Path
import yaml
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PM_WORKFLOWS_DIR = PROJECT_ROOT / "_bmad" / "mm" / "workflows" / "pm"

# Expected step files per workflow
WORKFLOW_STEPS = {
    "sprint-status": [
        "step-01-identify-active-milestone.md",
        "step-02-get-burndown-and-status.md",
        "step-03-identify-blockers-and-risks.md",
        "step-04-update-readme.md",
        "step-05-present-status-report.md",
    ],
    "create-story": [
        "step-00-discover-documents.md",
        "step-01-gather-module-information.md",
        "step-02-create-module-issue.md",
        "step-03-assign-to-milestone-and-epic.md",
        "step-04-report.md",
    ],
    "sprint-planning": [
        "step-00-discover-documents.md",
        "step-01-review-migration-order.md",
        "step-02-gather-sprint-parameters.md",
        "step-03-create-sprint-milestone.md",
        "step-04-assign-issues-to-milestone.md",
        "step-05-report-sprint-summary.md",
    ],
    "create-epics-and-stories": [
        "step-00-discover-documents.md",
        "step-01-confirm-project-readiness.md",
        "step-02-initialise-gitlab-project.md",
        "step-03-create-epics.md",
        "step-04-create-module-issues.md",
        "step-05-assign-issues-to-epics.md",
        "step-06-update-readme-and-report.md",
    ],
    "correct-course": [
        "step-00-discover-documents.md",
        "step-01-review-current-sprint-state.md",
        "step-02-identify-changes-needed.md",
        "step-03-validate-changes.md",
        "step-04-execute-changes-in-gitlab.md",
        "step-05-report-updated-sprint-state.md",
    ],
    "retrospective": [
        "step-01-gather-scope.md",
        "step-02-get-sprint-metrics.md",
        "step-03-review-completed-modules.md",
        "step-04-gather-qualitative-feedback.md",
        "step-05-generate-report.md",
        "step-06-post-to-epic-and-report.md",
    ],
}

ALL_WORKFLOWS = list(WORKFLOW_STEPS.keys())


# ---------------------------------------------------------------------------
# AC1: All 6 PM workflows have steps/ directory
# ---------------------------------------------------------------------------

class TestStepsDirectoryExists:
    """AC#1: Each PM workflow has a steps/ subdirectory."""

    @pytest.mark.parametrize("workflow", ALL_WORKFLOWS)
    def test_steps_dir_exists(self, workflow):
        steps_dir = PM_WORKFLOWS_DIR / workflow / "steps"
        assert steps_dir.is_dir(), f"{workflow}: missing steps/ directory"


# ---------------------------------------------------------------------------
# AC2 & AC4: Step files exist with correct naming convention
# ---------------------------------------------------------------------------

class TestStepFilesExist:
    """AC#2 & AC4: Step files exist with step-NN-goal-name.md naming."""

    @pytest.mark.parametrize("workflow,step_file", [
        (wf, sf) for wf, steps in WORKFLOW_STEPS.items() for sf in steps
    ])
    def test_step_file_exists(self, workflow, step_file):
        path = PM_WORKFLOWS_DIR / workflow / "steps" / step_file
        assert path.exists(), f"{workflow}: missing step file {step_file}"

    @pytest.mark.parametrize("workflow,step_file", [
        (wf, sf) for wf, steps in WORKFLOW_STEPS.items() for sf in steps
    ])
    def test_step_file_naming_convention(self, workflow, step_file):
        """File must match pattern step-NN-goal-name.md."""
        import re
        assert re.match(r"^step-\d{2}-.+\.md$", step_file), \
            f"{workflow}: {step_file} does not match step-NN-goal-name.md pattern"


# ---------------------------------------------------------------------------
# AC1: No instructions.md files remain in PM workflow directories
# ---------------------------------------------------------------------------

class TestNoInstructionsMdRemains:
    """AC#1: instructions.md removed from all PM workflow directories."""

    @pytest.mark.parametrize("workflow", ALL_WORKFLOWS)
    def test_instructions_md_removed(self, workflow):
        instructions_path = PM_WORKFLOWS_DIR / workflow / "instructions.md"
        assert not instructions_path.exists(), \
            f"{workflow}: instructions.md still exists — must be removed after refactor"


# ---------------------------------------------------------------------------
# AC1: workflow.yaml instructions: field points to steps/step- path
# ---------------------------------------------------------------------------

class TestWorkflowYamlUpdated:
    """AC#1: workflow.yaml instructions: points to steps/step- entry file."""

    @pytest.mark.parametrize("workflow", ALL_WORKFLOWS)
    def test_workflow_yaml_instructions_points_to_steps(self, workflow):
        yaml_path = PM_WORKFLOWS_DIR / workflow / "workflow.yaml"
        content = yaml_path.read_text()
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
        instructions = data.get("instructions", "")
        assert "steps/step-" in instructions, \
            f"{workflow}/workflow.yaml: instructions: '{instructions}' must point to steps/step- path"


# ---------------------------------------------------------------------------
# AC2: Step files contain "Proceed to:" directive (except last step)
# ---------------------------------------------------------------------------

class TestStepProceedDirectives:
    """AC#2: Each step file (except last) has 'Proceed to:' directive."""

    @pytest.mark.parametrize("workflow", ALL_WORKFLOWS)
    def test_non_last_steps_have_proceed_to(self, workflow):
        steps = WORKFLOW_STEPS[workflow]
        for step_file in steps[:-1]:  # all except the last
            path = PM_WORKFLOWS_DIR / workflow / "steps" / step_file
            content = path.read_text()
            assert "Proceed to:" in content, \
                f"{workflow}/{step_file}: missing 'Proceed to:' directive"

    @pytest.mark.parametrize("workflow", ALL_WORKFLOWS)
    def test_last_step_has_workflow_complete(self, workflow):
        steps = WORKFLOW_STEPS[workflow]
        last_step = steps[-1]
        path = PM_WORKFLOWS_DIR / workflow / "steps" / last_step
        content = path.read_text()
        assert "Workflow complete" in content or "workflow complete" in content.lower(), \
            f"{workflow}/{last_step}: last step must indicate 'Workflow complete'"


# ---------------------------------------------------------------------------
# AC2: Step files have context boundaries, execution rules, and goal
# ---------------------------------------------------------------------------

class TestStepFileStructure:
    """AC#2: Step files are self-contained with required structure."""

    @pytest.mark.parametrize("workflow,step_file", [
        (wf, sf) for wf, steps in WORKFLOW_STEPS.items() for sf in steps
    ])
    def test_step_has_context_boundaries(self, workflow, step_file):
        path = PM_WORKFLOWS_DIR / workflow / "steps" / step_file
        content = path.read_text()
        assert "CONTEXT BOUNDARIES" in content, \
            f"{workflow}/{step_file}: missing CONTEXT BOUNDARIES section"

    @pytest.mark.parametrize("workflow,step_file", [
        (wf, sf) for wf, steps in WORKFLOW_STEPS.items() for sf in steps
    ])
    def test_step_has_execution_rules(self, workflow, step_file):
        path = PM_WORKFLOWS_DIR / workflow / "steps" / step_file
        content = path.read_text()
        assert "EXECUTION RULES" in content, \
            f"{workflow}/{step_file}: missing EXECUTION RULES section"

    @pytest.mark.parametrize("workflow,step_file", [
        (wf, sf) for wf, steps in WORKFLOW_STEPS.items() for sf in steps
    ])
    def test_step_has_task_section(self, workflow, step_file):
        path = PM_WORKFLOWS_DIR / workflow / "steps" / step_file
        content = path.read_text()
        assert "YOUR TASK" in content or "## Step" in content, \
            f"{workflow}/{step_file}: missing task/goal content"
