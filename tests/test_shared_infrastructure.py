"""Tests for Story 1.3: Shared MCP Server Infrastructure.

Validates AC 1-4: config loader, result helpers, dual logging, skeleton servers.
"""

import importlib
import logging
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
SERVERS = ["cobol_parser_mcp", "specdb_mcp", "delta_macros_mcp", "jcl_parser_mcp", "gitlab_mcp"]


class TestAC1ConfigLoader:
    """AC 1: Config loader reads _bmad/mm/config.yaml with typed access and caching."""

    def test_config_loader_module_exists(self):
        assert (ROOT / "mcp-servers" / "shared" / "config_loader.py").is_file()

    def test_load_config_returns_dict(self):
        from shared.config_loader import load_config
        config = load_config()
        assert isinstance(config, dict)

    def test_required_fields_present(self):
        from shared.config_loader import load_config
        config = load_config()
        required = ["db_path", "macro_library_path", "glossary_path", "source_paths", "gitlab_url", "project_name"]
        for field in required:
            assert field in config, f"Missing config field: {field}"

    def test_project_root_resolved(self):
        from shared.config_loader import load_config
        config = load_config()
        assert "<project-root>" not in config["db_path"], "db_path should have <project-root> resolved"

    def test_db_path_is_absolute(self):
        from shared.config_loader import load_config
        config = load_config()
        assert Path(config["db_path"]).is_absolute()

    def test_config_is_cached(self):
        from shared.config_loader import load_config
        config1 = load_config()
        config2 = load_config()
        assert config1 is config2, "Config should be cached (same object)"


class TestAC2ResultHelpers:
    """AC 2: result.py in each server with make_result, make_error, make_warning."""

    def test_result_module_exists_in_all_servers(self):
        for pkg in SERVERS:
            assert (ROOT / "mcp-servers" / pkg / "result.py").is_file(), f"Missing {pkg}/result.py"

    def test_make_result_basic(self):
        from cobol_parser_mcp.result import make_result
        r = make_result(data={"key": "val"}, message="ok")
        assert r["status"] == "ok"
        assert r["data"] == {"key": "val"}
        assert r["message"] == "ok"
        assert r["flags"] == []

    def test_make_result_with_flags(self):
        from cobol_parser_mcp.result import make_result
        flags = [{"code": "TEST_FLAG", "message": "test", "location": "file.cob"}]
        r = make_result(flags=flags)
        assert r["flags"] == flags

    def test_make_error(self):
        from cobol_parser_mcp.result import make_error
        r = make_error("something broke")
        assert r["status"] == "error"
        assert r["message"] == "something broke"
        assert r["data"] is None
        assert r["flags"] == []

    def test_make_error_with_flags(self):
        from cobol_parser_mcp.result import make_error
        flags = [{"code": "FILE_NOT_FOUND", "message": "missing", "location": "/tmp/x.cob"}]
        r = make_error("not found", flags=flags)
        assert r["flags"] == flags

    def test_make_warning(self):
        from cobol_parser_mcp.result import make_warning
        r = make_warning(data={"partial": True}, message="partial result", flags=[])
        assert r["status"] == "warning"
        assert r["data"] == {"partial": True}

    def test_flags_never_none(self):
        from cobol_parser_mcp.result import make_result, make_error
        assert make_result()["flags"] == []
        assert make_error("err")["flags"] == []

    def test_all_servers_have_same_functions(self):
        for pkg in SERVERS:
            mod = importlib.import_module(f"{pkg}.result")
            assert hasattr(mod, "make_result"), f"{pkg}.result missing make_result"
            assert hasattr(mod, "make_error"), f"{pkg}.result missing make_error"
            assert hasattr(mod, "make_warning"), f"{pkg}.result missing make_warning"


class TestAC3DualLogging:
    """AC 3: Dual logging to stderr and log file."""

    def test_logging_setup_exists(self):
        from shared.config_loader import setup_logging
        assert callable(setup_logging)

    def test_logging_creates_logger_with_handlers(self):
        from shared.config_loader import setup_logging
        logger = setup_logging("test-server")
        handler_types = [type(h).__name__ for h in logger.handlers]
        assert "StreamHandler" in handler_types, "Missing StreamHandler for stderr"
        assert "FileHandler" in handler_types, "Missing FileHandler for log file"

    def test_log_file_created(self):
        from shared.config_loader import setup_logging
        setup_logging("test-logging-check")
        log_path = ROOT / "logs" / "test-logging-check.log"
        assert log_path.exists()

    def test_stream_handler_targets_stderr(self):
        from shared.config_loader import setup_logging
        logger = setup_logging("test-stderr-check")
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)]
        assert any(h.stream is sys.stderr for h in stream_handlers), "StreamHandler should target stderr"


class TestAC4SkeletonServers:
    """AC 4: Skeleton server.py files with FastMCP init."""

    def test_server_py_exists_in_all_packages(self):
        for pkg in SERVERS:
            assert (ROOT / "mcp-servers" / pkg / "server.py").is_file(), f"Missing {pkg}/server.py"

    def test_server_imports_fastmcp(self):
        for pkg in SERVERS:
            content = (ROOT / "mcp-servers" / pkg / "server.py").read_text()
            assert "FastMCP" in content, f"{pkg}/server.py missing FastMCP import"

    def test_server_imports_config_loader(self):
        for pkg in SERVERS:
            content = (ROOT / "mcp-servers" / pkg / "server.py").read_text()
            assert "config_loader" in content, f"{pkg}/server.py missing config_loader import"

    def test_server_has_mcp_app(self):
        for pkg in SERVERS:
            content = (ROOT / "mcp-servers" / pkg / "server.py").read_text()
            assert "FastMCP(" in content, f"{pkg}/server.py missing FastMCP app init"

    def test_server_has_main_entry(self):
        for pkg in SERVERS:
            content = (ROOT / "mcp-servers" / pkg / "server.py").read_text()
            assert "__main__" in content or "mcp.run" in content or ".run" in content, \
                f"{pkg}/server.py missing run entry point"

    def test_dunder_main_exists(self):
        for pkg in SERVERS:
            assert (ROOT / "mcp-servers" / pkg / "__main__.py").is_file(), \
                f"Missing {pkg}/__main__.py for python -m support"
