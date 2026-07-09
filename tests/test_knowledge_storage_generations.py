"""Coverage for KnowledgeStorage generic generation/record storage methods.

These storage helpers persist any object exposing ``to_dict()`` and read the
raw dicts back, so lightweight stubs are sufficient to exercise them.
"""

import pytest

from services.knowledge_storage import KnowledgeStorage


class _Stub:
    """Minimal object with a to_dict() method."""

    def __init__(self, payload):
        self._payload = payload

    def to_dict(self):
        return dict(self._payload)


@pytest.fixture
def storage(tmp_path):
    return KnowledgeStorage(base_path=str(tmp_path / "data"))


def test_title_generation_storage(storage):
    storage.save_title_generation(_Stub({"id": "tg1", "titles": ["a"]}))
    records = storage.load_title_generations()
    assert records == [{"id": "tg1", "titles": ["a"]}]


def test_keyword_generation_storage(storage):
    storage.save_keyword_generation(_Stub({"id": "kg1"}))
    assert storage.load_keyword_generations()[0]["id"] == "kg1"


def test_image_prompt_generation_storage(storage):
    storage.save_image_prompt_generation(_Stub({"id": "ip1"}))
    assert len(storage.load_image_prompt_generations()) == 1


def test_listing_package_storage_and_get(storage):
    storage.save_listing_package(_Stub({"id": "lp1", "titles": ["t"]}))
    assert len(storage.load_listing_packages()) == 1
    assert storage.load_listing_package("lp1")["titles"] == ["t"]
    assert storage.load_listing_package("missing") is None


def test_detail_screen_generation_storage(storage):
    storage.save_detail_screen_generation(_Stub({"id": "ds1"}))
    assert len(storage.load_detail_screen_generations()) == 1
    assert storage.load_detail_screen_generation("ds1")["id"] == "ds1"
    assert storage.load_detail_screen_generation("missing") is None


def test_video_script_generation_storage(storage):
    storage.save_video_script_generation(_Stub({"generation_id": "vs1"}))
    assert len(storage.load_video_script_generations()) == 1
    assert storage.load_video_script_generation("vs1")["generation_id"] == "vs1"
    assert storage.load_video_script_generation("missing") is None


def test_xiaohongshu_generation_storage(storage):
    storage.save_xiaohongshu_generation(_Stub({"generation_id": "xh1"}))
    assert len(storage.load_xiaohongshu_generations()) == 1
    assert storage.load_xiaohongshu_generation("xh1")["generation_id"] == "xh1"
    assert storage.load_xiaohongshu_generation("missing") is None


def test_task_storage_crud(storage):
    storage.save_task(_Stub({"task_id": "t1", "status": "pending"}))
    assert len(storage.load_tasks()) == 1
    assert storage.load_task("t1")["status"] == "pending"
    assert storage.load_task("missing") is None

    assert storage.update_task_status("t1", "done") is True
    assert storage.load_task("t1")["status"] == "done"
    assert storage.update_task_status("missing", "done") is False

    assert storage.record_human_confirmation("t1", True, notes="ok") is True
    assert storage.load_task("t1")["final_summary"] == "ok"
    assert storage.record_human_confirmation("t1", True) is True
    assert storage.record_human_confirmation("missing", True) is False


def test_acceptance_report_storage(storage):
    storage.save_acceptance_report(_Stub({"report_id": "ar1"}))
    assert len(storage.load_acceptance_reports()) == 1
    assert storage.load_acceptance_report("ar1")["report_id"] == "ar1"
    assert storage.load_acceptance_report("missing") is None


def test_tool_registry_and_plan_storage(storage):
    storage.save_tool_registry([_Stub({"tool_id": "x"}), _Stub({"tool_id": "y"})])
    assert len(storage.load_tool_registry()) == 2

    storage.save_tool_plan(_Stub({"plan_id": "p1"}))
    assert len(storage.load_tool_plans()) == 1
    assert storage.load_tool_plan("p1")["plan_id"] == "p1"
    assert storage.load_tool_plan("missing") is None


def test_workflow_storage(storage):
    storage.save_workflow(_Stub({"workflow_id": "w1"}))
    assert len(storage.load_workflows()) == 1
    assert storage.load_workflow("w1")["workflow_id"] == "w1"
    assert storage.load_workflow("missing") is None

    storage.save_workflows([{"workflow_id": "a"}, {"workflow_id": "b"}])
    assert len(storage.load_workflows()) == 2
