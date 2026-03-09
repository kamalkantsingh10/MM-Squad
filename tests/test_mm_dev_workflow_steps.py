"""Tests for MM dev workflow step-file refactor — Story 3.8."""

from pathlib import Path
import re
import yaml
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEV_WORKFLOWS_DIR = PROJECT_ROOT / "_bmad" / "mm" / "workflows" / "dev"

# Expected step files per workflow
WORKFLOW_STEPS = {
    "dev-story": [
        "step-01-find-story.md",
        "step-02-load-project-context.md",
        "step-03-detect-review-continuation.md",
        "step-04-mark-in-progress.md",
        "step-05-implement-task.md",
        "step-06-verify-test-coverage.md",
        "step-07-run-validations.md",
        "step-08-validate-and-mark-complete.md",
        "step-09-story-completion.md",
        "step-10-completion-communication.md",
    ],
    "code-review": [
        "step-01-load-story-and-discover-changes.md",
        "step-02-build-review-attack-plan.md",
        "step-03-execute-adversarial-review.md",
        "step-04-present-findings-and-fix.md",
        "step-05-update-story-status.md",
    ],
}

ALL_WORKFLOWS = list(WORKFLOW_STEPS.keys())


# ---------------------------------------------------------------------------
# AC1: steps/ directory exists for both MM dev workflows
# ---------------------------------------------------------------------------

class TestStepsDirectoryExists:
    """AC#1: Each MM dev workflow has a steps/ subdirectory."""

    @pytest.mark.parametrize("workflow", ALL_WORKFLOWS)
    def test_steps_dir_exists(self, workflow):
        steps_dir = DEV_WORKFLOWS_DIR / workflow / "steps"
        assert steps_dir.is_dir(), f"{workflow}: missing steps/ directory"


# ---------------------------------------------------------------------------
# AC4: Step files exist with correct naming convention
# ---------------------------------------------------------------------------

class TestStepFilesExist:
    """AC#4: Step files exist with step-NN-goal-name.md naming."""

    @pytest.mark.parametrize("workflow,step_file", [
        (wf, sf) for wf, steps in WORKFLOW_STEPS.items() for sf in steps
    ])
    def test_step_file_exists(self, workflow, step_file):
        path = DEV_WORKFLOWS_DIR / workflow / "steps" / step_file
        assert path.exists(), f"{workflow}: missing step file {step_file}"

    @pytest.mark.parametrize("workflow,step_file", [
        (wf, sf) for wf, steps in WORKFLOW_STEPS.items() for sf in steps
    ])
    def test_step_file_naming_convention(self, workflow, step_file):
        """File must match pattern step-NN-goal-name.md."""
        assert re.match(r"^step-\d{2}-.+\.md$", step_file), \
            f"{workflow}: {step_file} does not match step-NN-goal-name.md pattern"


# ---------------------------------------------------------------------------
# AC1: No instructions.xml files remain in MM dev workflow directories
# ---------------------------------------------------------------------------

class TestNoInstructionsXmlRemains:
    """AC#1: instructions.xml removed from all MM dev workflow directories."""

    @pytest.mark.parametrize("workflow", ALL_WORKFLOWS)
    def test_instructions_xml_removed(self, workflow):
        instructions_path = DEV_WORKFLOWS_DIR / workflow / "instructions.xml"
        assert not instructions_path.exists(), \
            f"{workflow}: instructions.xml still exists — must be removed after refactor"


# ---------------------------------------------------------------------------
# AC1: workflow.yaml instructions: field points to steps/step- path
# ---------------------------------------------------------------------------

class TestWorkflowYamlUpdated:
    """AC#1: workflow.yaml instructions: points to steps/step- entry file."""

    @pytest.mark.parametrize("workflow", ALL_WORKFLOWS)
    def test_workflow_yaml_instructions_points_to_steps(self, workflow):
        yaml_path = DEV_WORKFLOWS_DIR / workflow / "workflow.yaml"
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
            path = DEV_WORKFLOWS_DIR / workflow / "steps" / step_file
            content = path.read_text()
            assert "Proceed to:" in content, \
                f"{workflow}/{step_file}: missing 'Proceed to:' directive"

    @pytest.mark.parametrize("workflow", ALL_WORKFLOWS)
    def test_last_step_has_workflow_complete(self, workflow):
        steps = WORKFLOW_STEPS[workflow]
        last_step = steps[-1]
        path = DEV_WORKFLOWS_DIR / workflow / "steps" / last_step
        content = path.read_text()
        assert "Workflow complete" in content or "workflow complete" in content.lower(), \
            f"{workflow}/{last_step}: last step must indicate 'Workflow complete'"


# ---------------------------------------------------------------------------
# AC2: Step files are self-contained with required structure
# ---------------------------------------------------------------------------

class TestStepFileStructure:
    """AC#2: Step files have CONTEXT BOUNDARIES and EXECUTION RULES sections."""

    @pytest.mark.parametrize("workflow,step_file", [
        (wf, sf) for wf, steps in WORKFLOW_STEPS.items() for sf in steps
    ])
    def test_step_has_context_boundaries(self, workflow, step_file):
        path = DEV_WORKFLOWS_DIR / workflow / "steps" / step_file
        content = path.read_text()
        assert "CONTEXT BOUNDARIES" in content, \
            f"{workflow}/{step_file}: missing CONTEXT BOUNDARIES section"

    @pytest.mark.parametrize("workflow,step_file", [
        (wf, sf) for wf, steps in WORKFLOW_STEPS.items() for sf in steps
    ])
    def test_step_has_execution_rules(self, workflow, step_file):
        path = DEV_WORKFLOWS_DIR / workflow / "steps" / step_file
        content = path.read_text()
        assert "EXECUTION RULES" in content, \
            f"{workflow}/{step_file}: missing EXECUTION RULES section"

    @pytest.mark.parametrize("workflow,step_file", [
        (wf, sf) for wf, steps in WORKFLOW_STEPS.items() for sf in steps
    ])
    def test_step_has_task_section(self, workflow, step_file):
        path = DEV_WORKFLOWS_DIR / workflow / "steps" / step_file
        content = path.read_text()
        assert "YOUR TASK" in content or "## Step" in content, \
            f"{workflow}/{step_file}: missing task/goal content"
