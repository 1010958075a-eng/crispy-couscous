"""Unit tests for LogService."""

import pytest

from models.log import Log
from services.knowledge_storage import KnowledgeStorage
from services.log_service import LogService


@pytest.fixture
def service(tmp_path):
    storage = KnowledgeStorage(base_path=str(tmp_path / "data"))
    return LogService(storage)


def test_create_log_persists_and_returns(service):
    log = service.create_log(
        log_type="task",
        source_module="task_service",
        source_id="t1",
        action="create",
        status="success",
        message="创建任务",
        risk_level="low",
        details={"k": "v"},
    )
    assert isinstance(log, Log)
    assert log.log_id
    stored = service.get_logs()
    assert len(stored) == 1
    assert stored[0]["message"] == "创建任务"
    assert stored[0]["details"] == {"k": "v"}


def test_get_logs_empty(service):
    assert service.get_logs() == []


def test_get_log_by_id(service):
    log = service.create_log(
        log_type="tool",
        source_module="tool_service",
        source_id=None,
        action="run",
        status="success",
        message="工具执行",
    )
    assert service.get_log(log.log_id)["log_id"] == log.log_id
    assert service.get_log("missing") is None


def test_get_logs_by_type(service):
    service.create_log("task", "m", None, "a", "success", "msg1")
    service.create_log("tool", "m", None, "a", "success", "msg2")
    service.create_log("task", "m", None, "a", "success", "msg3")
    assert len(service.get_logs_by_type("task")) == 2
    assert len(service.get_logs_by_type("tool")) == 1
    assert service.get_logs_by_type("system") == []


def test_get_logs_by_source(service):
    service.create_log("task", "modA", "id1", "a", "success", "m")
    service.create_log("task", "modA", "id2", "a", "success", "m")
    service.create_log("task", "modB", "id3", "a", "success", "m")
    assert len(service.get_logs_by_source("modA")) == 2
    assert len(service.get_logs_by_source("modA", "id1")) == 1
    assert service.get_logs_by_source("modA", "id-missing") == []
