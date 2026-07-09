"""Unit tests for KnowledgeStorage (local JSON persistence)."""

import json

import pytest

from models.learning import (
    KnowledgeRecord,
    LinkLearningRecord,
    LinkLearningStatus,
    LearningTarget,
    MerchantProfile,
    ReviewLearningRecord,
    TableLearningRecord,
    TextLearningRecord,
    DataType,
)
from models.merchant import (
    CompetitorKnowledge,
    KeywordLibrary,
    MerchantProfile as MerchantProfileV2,
    Platform,
    PriceRange,
    ProductKnowledge,
    ReviewRecord,
    VisualStyleLibrary,
)
from models.log import Log
from services.knowledge_storage import KnowledgeStorage


@pytest.fixture
def storage(tmp_path):
    return KnowledgeStorage(base_path=str(tmp_path / "data"))


def test_init_creates_base_path(tmp_path):
    target = tmp_path / "nested" / "data"
    KnowledgeStorage(base_path=str(target))
    assert target.exists()


def test_load_json_missing_returns_empty(storage):
    assert storage._load_json(storage.knowledge_records_file) == []


def test_load_json_corrupt_returns_empty(storage):
    storage.knowledge_records_file.write_text("not-json{", encoding="utf-8")
    assert storage._load_json(storage.knowledge_records_file) == []


def test_generate_id_unique(storage):
    ids = {storage.generate_id() for _ in range(50)}
    assert len(ids) == 50


def test_merchant_profile_v1_roundtrip(storage):
    profile = MerchantProfile(
        id="m1",
        merchant_name="小店",
        main_category="女装",
        price_range="中价",
        positioning="精品",
        target_audience="年轻女性",
        platforms=["淘宝", "天猫"],
    )
    storage.save_merchant_profile(profile)
    loaded = storage.load_merchant_profile()
    assert loaded is not None
    assert loaded.merchant_name == "小店"
    assert loaded.platforms == ["淘宝", "天猫"]


def test_load_merchant_profile_none_when_empty(storage):
    assert storage.load_merchant_profile() is None


def test_knowledge_records_roundtrip_and_filter(storage):
    storage.save_knowledge_record(
        KnowledgeRecord(id="k1", title="标题A", content="内容", category="运营")
    )
    storage.save_knowledge_record(
        KnowledgeRecord(id="k2", title="标题B", content="内容", category="选品")
    )
    records = storage.load_knowledge_records()
    assert len(records) == 2
    operations = storage.get_knowledge_by_category("运营")
    assert len(operations) == 1
    assert operations[0].id == "k1"


def test_link_learning_record_crud(storage):
    record = LinkLearningRecord(
        id="l1",
        url="https://example.com",
        source_platform="淘宝",
        learning_target=LearningTarget.COMPETITOR,
    )
    storage.save_link_learning_record(record)
    assert len(storage.load_link_learning_records()) == 1
    assert storage.get_link_learning_record("l1").url == "https://example.com"
    assert storage.get_link_learning_record("missing") is None

    record.status = LinkLearningStatus.SUCCESS
    record.extracted_title = "已提取"
    storage.update_link_learning_record(record)
    reloaded = storage.get_link_learning_record("l1")
    assert reloaded.status == LinkLearningStatus.SUCCESS.value
    assert reloaded.extracted_title == "已提取"


def test_text_learning_record_roundtrip(storage):
    storage.save_text_learning_record(
        TextLearningRecord(
            id="t1",
            title="经验",
            content="正文",
            category="投放",
            learning_target=LearningTarget.ARTICLE,
            reusable_rules=["规则1"],
        )
    )
    records = storage.load_text_learning_records()
    assert len(records) == 1
    assert records[0].reusable_rules == ["规则1"]


def test_table_learning_record_roundtrip(storage):
    storage.save_table_learning_record(
        TableLearningRecord(
            id="tb1",
            filename="data.xlsx",
            data_type=DataType.AD_DATA,
            row_count=10,
        )
    )
    records = storage.load_table_learning_records()
    assert len(records) == 1
    assert records[0].row_count == 10
    assert records[0].data_type == DataType.AD_DATA.value


def test_review_learning_record_roundtrip(storage):
    storage.save_review_learning_record(
        ReviewLearningRecord(
            id="r1",
            action="调价",
            result="转化提升",
            roi=2.5,
            problems=["曝光下降"],
        )
    )
    records = storage.load_review_learning_records()
    assert len(records) == 1
    assert records[0].roi == 2.5
    assert records[0].problems == ["曝光下降"]


def test_merchant_profile_v2_roundtrip(storage):
    profile = MerchantProfileV2(
        id="mv2",
        merchant_name="旗舰店",
        platforms=[Platform.TAOBAO, Platform.DOUYIN],
        main_category="女装",
        price_range=PriceRange.MEDIUM,
        target_audience="都市白领",
        positioning="轻奢",
        visual_style="简约",
        operation_goal="提升GMV",
    )
    storage.save_merchant_profile_v2(profile)
    loaded = storage.load_merchant_profile_v2()
    assert loaded is not None
    assert loaded.platforms == [Platform.TAOBAO, Platform.DOUYIN]
    assert loaded.price_range == PriceRange.MEDIUM


def test_product_knowledge_roundtrip(storage):
    storage.save_product_knowledge(
        ProductKnowledge(
            id="pk1",
            product_name="真丝衬衫",
            category="女装",
            price=299.0,
            selling_points=["透气", "亲肤"],
            material="真丝",
        )
    )
    records = storage.load_product_knowledge()
    assert len(records) == 1
    assert records[0].material == "真丝"
    assert records[0].selling_points == ["透气", "亲肤"]


def test_competitor_knowledge_roundtrip(storage):
    storage.save_competitor_knowledge(
        CompetitorKnowledge(
            id="c1",
            competitor_url="https://c.example.com",
            competitor_title="竞品",
            price=188.0,
            learnable_points=["主图排版"],
        )
    )
    records = storage.load_competitor_knowledge()
    assert len(records) == 1
    assert records[0].learnable_points == ["主图排版"]


def test_keyword_library_roundtrip(storage):
    storage.save_keyword_library(
        KeywordLibrary(id="kw1", core_keywords=["连衣裙"], negative_keywords=["二手"])
    )
    records = storage.load_keyword_library()
    assert len(records) == 1
    assert records[0].core_keywords == ["连衣裙"]
    assert records[0].negative_keywords == ["二手"]


def test_visual_style_library_roundtrip(storage):
    storage.save_visual_style_library(
        VisualStyleLibrary(
            id="v1",
            main_image_style="白底",
            detail_page_style="图文",
            color_tone="莫兰迪",
        )
    )
    records = storage.load_visual_style_library()
    assert len(records) == 1
    assert records[0].color_tone == "莫兰迪"


def test_review_record_v2_roundtrip(storage):
    storage.save_review_record_v2(
        ReviewRecord(
            id="rv1",
            action_type="投放",
            action_content="加大预算",
            action_result="ROI提升",
            roi=3.0,
        )
    )
    records = storage.load_review_records_v2()
    assert len(records) == 1
    assert records[0].roi == 3.0


def test_log_storage(storage):
    log = Log(
        log_id="log1",
        log_type="task",
        source_module="task_service",
        source_id="task-1",
        action="create",
        status="success",
        risk_level=None,
        message="任务创建",
        details={"foo": "bar"},
    )
    storage.save_log(log)
    logs = storage.load_logs()
    assert len(logs) == 1
    assert logs[0]["log_id"] == "log1"
    assert storage.load_log("log1")["message"] == "任务创建"
    assert storage.load_log("missing") is None


def test_save_logs_replaces_all(storage):
    storage.save_logs([{"log_id": "a"}, {"log_id": "b"}])
    assert len(storage.load_logs()) == 2
    storage.save_logs([{"log_id": "c"}])
    logs = storage.load_logs()
    assert len(logs) == 1
    assert logs[0]["log_id"] == "c"


def test_save_json_writes_utf8(storage):
    storage._save_json(storage.knowledge_records_file, [{"title": "中文"}])
    raw = storage.knowledge_records_file.read_text(encoding="utf-8")
    assert "中文" in raw
    assert json.loads(raw) == [{"title": "中文"}]
