"""Tests for Story 1.1: Project Initialisation & Poetry Monorepo.

Validates AC 1-8: directory scaffolding, pyproject.toml, gitignore, README, templates.
"""

from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parent.parent


class TestAC1PoetryMonorepo:
    """AC 1: Poetry monorepo initialised."""

    def test_pyproject_toml_exists(self):
        assert (ROOT / "pyproject.toml").is_file()

    def test_python_target(self):
        data = tomllib.loads((ROOT / "pyproject.toml").read_text())
        assert data["tool"]["poetry"]["dependencies"]["python"] == "^3.12"

    def test_dependencies_declared(self):
        data = tomllib.loads((ROOT / "pyproject.toml").read_text())
        deps = data["tool"]["poetry"]["dependencies"]
        assert deps["fastmcp"] == "3.1.0"
        assert deps["aiosqlite"] == "0.22.1"
        assert deps["lark"] == "0.12.0"
        assert deps["python-gitlab"] == "8.1.0"

    def test_pytest_dev_dependency(self):
        data = tomllib.loads((ROOT / "pyproject.toml").read_text())
        dev_deps = data["tool"]["poetry"]["group"]["dev"]["dependencies"]
        assert "pytest" in dev_deps

    def test_poetry_lock_exists(self):
        assert (ROOT / "poetry.lock").is_file()

    def test_packages_configuration(self):
        data = tomllib.loads((ROOT / "pyproject.toml").read_text())
        packages = data["tool"]["poetry"]["packages"]
        names = {p["include"] for p in packages}
        assert names == {
            "cobol_parser_mcp",
            "specdb_mcp",
            "delta_macros_mcp",
            "jcl_parser_mcp",
            "gitlab_mcp",
            "shared",
        }
        for p in packages:
            assert p["from"] == "mcp-servers"


class TestAC2McpServerPackages:
    """AC 2: MCP server package directories."""

    PACKAGES = [
        "cobol_parser_mcp",
        "specdb_mcp",
        "delta_macros_mcp",
        "jcl_parser_mcp",
        "gitlab_mcp",
    ]

    def test_mcp_servers_dir_exists(self):
        assert (ROOT / "mcp-servers").is_dir()

    def test_package_directories_with_init(self):
        for pkg in self.PACKAGES:
            assert (ROOT / "mcp-servers" / pkg / "__init__.py").is_file(), f"Missing {pkg}/__init__.py"

    def test_shared_package(self):
        assert (ROOT / "mcp-servers" / "shared" / "__init__.py").is_file()


class TestAC3TestDirectoryStructure:
    """AC 3: Test directory structure mirrors mcp-servers."""

    PACKAGES = [
        "cobol_parser_mcp",
        "specdb_mcp",
        "delta_macros_mcp",
        "jcl_parser_mcp",
        "gitlab_mcp",
    ]

    def test_tests_root_init(self):
        assert (ROOT / "tests" / "__init__.py").is_file()

    def test_test_subdirs_with_init_and_fixtures(self):
        for pkg in self.PACKAGES:
            assert (ROOT / "tests" / pkg / "__init__.py").is_file(), f"Missing tests/{pkg}/__init__.py"
            assert (ROOT / "tests" / pkg / "fixtures").is_dir(), f"Missing tests/{pkg}/fixtures/"

    def test_blackjack_fixture_subdirs(self):
        bj = ROOT / "tests" / "cobol_parser_mcp" / "fixtures" / "blackjack"
        assert (bj / "src").is_dir()
        assert (bj / "copy").is_dir()


class TestAC4RuntimeDirectories:
    """AC 4: Runtime directories with .gitkeep."""

    def test_data_gitkeep(self):
        assert (ROOT / "data" / ".gitkeep").is_file()

    def test_logs_gitkeep(self):
        assert (ROOT / "logs" / ".gitkeep").is_file()


class TestAC5BlackjackDirectory:
    """AC 5: BlackJack directory."""

    def test_glossary_placeholder(self):
        assert (ROOT / "blackjack" / "glossary.md").is_file()

    def test_macros_dir(self):
        assert (ROOT / "blackjack" / "macros").is_dir()


class TestAC6Templates:
    """AC 6: Templates."""

    def test_glossary_template(self):
        content = (ROOT / "templates" / "glossary-template.md").read_text()
        assert "| COBOL Name | Business Term |" in content

    def test_macro_template(self):
        assert (ROOT / "templates" / "macro-template.md").is_file()


class TestAC7Gitignore:
    """AC 7: Gitignore patterns."""

    def test_gitignore_exists(self):
        assert (ROOT / ".gitignore").is_file()

    def test_data_excluded(self):
        content = (ROOT / ".gitignore").read_text()
        assert "data/" in content

    def test_logs_excluded(self):
        content = (ROOT / ".gitignore").read_text()
        assert "logs/" in content

    def test_gitkeep_exceptions(self):
        content = (ROOT / ".gitignore").read_text()
        assert "!data/.gitkeep" in content
        assert "!logs/.gitkeep" in content

    def test_python_patterns(self):
        content = (ROOT / ".gitignore").read_text()
        assert "__pycache__/" in content
        assert "*.pyc" in content
        assert ".pytest_cache/" in content


class TestAC8Readme:
    """AC 8: README.md."""

    def test_readme_exists(self):
        assert (ROOT / "README.md").is_file()

    def test_project_name(self):
        content = (ROOT / "README.md").read_text()
        assert "MM-Squad" in content

    def test_setup_instructions(self):
        content = (ROOT / "README.md").read_text()
        assert "poetry install" in content
