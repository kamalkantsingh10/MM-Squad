"""Tests for Story 1.2: MM Module Configuration & Registry.

Validates AC 1-4: config.yaml, module-help.csv, data templates, party roster.
"""

import csv
import io
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MM = ROOT / "_bmad" / "mm"

AGENTS = ["po", "tigress", "viper", "monkey", "shifu", "oogway", "mantis"]


class TestAC1MmConfigYaml:
    """AC 1: MM config.yaml with all required fields, no credentials."""

    def test_config_exists(self):
        assert (MM / "config.yaml").is_file()

    def test_required_fields(self):
        data = yaml.safe_load((MM / "config.yaml").read_text())
        required = ["db_path", "macro_library_path", "glossary_path", "source_paths", "gitlab_url", "project_name"]
        for field in required:
            assert field in data, f"Missing required field: {field}"

    def test_db_path_default(self):
        data = yaml.safe_load((MM / "config.yaml").read_text())
        assert "specdb.sqlite" in data["db_path"]
        assert "data" in data["db_path"]

    def test_project_name(self):
        data = yaml.safe_load((MM / "config.yaml").read_text())
        assert data["project_name"] == "MM-Squad"

    def test_source_paths_is_list(self):
        data = yaml.safe_load((MM / "config.yaml").read_text())
        assert isinstance(data["source_paths"], list)

    def test_no_credentials(self):
        content = (MM / "config.yaml").read_text().lower()
        assert "password" not in content
        assert "secret" not in content
        assert "token" not in content or "# gitlab_token" in content or "environment variable" in content.lower()

    def test_gitlab_token_env_comment(self):
        content = (MM / "config.yaml").read_text()
        assert "GITLAB_TOKEN" in content
        assert "environment variable" in content.lower() or "env" in content.lower()


class TestAC2ModuleHelpCsv:
    """AC 2: module-help.csv lists all 7 agents and workflows."""

    def test_file_exists(self):
        assert (MM / "module-help.csv").is_file()

    def test_all_agents_listed(self):
        content = (MM / "module-help.csv").read_text()
        for agent in AGENTS:
            assert f"bmad-agent-mm-{agent}" in content, f"Missing agent command: bmad-agent-mm-{agent}"

    def test_workflows_listed(self):
        content = (MM / "module-help.csv").read_text()
        expected_workflows = [
            "bmad-mm-analyse-structure",
            "bmad-mm-map-dependencies",
            "bmad-mm-extract-business-rules",
        ]
        for wf in expected_workflows:
            assert wf in content, f"Missing workflow command: {wf}"

    def test_csv_parseable(self):
        content = (MM / "module-help.csv").read_text()
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        assert len(rows) > 1, "CSV should have header + data rows"

    def test_module_column_is_mm(self):
        content = (MM / "module-help.csv").read_text()
        reader = csv.DictReader(io.StringIO(content))
        for row in reader:
            assert row["module"] == "mm", f"Module should be 'mm', got '{row['module']}'"


class TestAC3DataTemplates:
    """AC 3: Data templates."""

    def test_glossary_template(self):
        path = MM / "data" / "glossary-template.md"
        assert path.is_file()
        content = path.read_text()
        assert "| COBOL Name | Business Term |" in content

    def test_macro_template(self):
        path = MM / "data" / "macro-template.md"
        assert path.is_file()
        content = path.read_text()
        assert len(content.strip()) > 0


class TestAC4PartyModeRoster:
    """AC 4: Party mode roster lists all 7 MM agents."""

    def test_file_exists(self):
        assert (MM / "teams" / "default-party.csv").is_file()

    def test_all_agents_in_roster(self):
        content = (MM / "teams" / "default-party.csv").read_text()
        for agent in AGENTS:
            assert agent in content, f"Missing agent in party roster: {agent}"

    def test_csv_parseable(self):
        content = (MM / "teams" / "default-party.csv").read_text()
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        assert len(rows) >= 8, "Should have header + 7 agent rows"
