"""Unit tests for TitleService."""

import pytest

from models.merchant import (
    KeywordLibrary,
    MerchantProfile as MerchantProfileV2,
    Platform,
    PriceRange,
    ProductKnowledge,
)
from services.knowledge_storage import KnowledgeStorage
from services.title_service import TitleService


@pytest.fixture
def storage(tmp_path):
    return KnowledgeStorage(base_path=str(tmp_path / "data"))


@pytest.fixture
def service(storage):
    return TitleService(knowledge_storage=storage)


def test_generate_titles_returns_at_most_20_unique(service):
    gen = service.generate_titles(
        product_id="p1",
        product_info={
            "product_name": "连衣裙",
            "category": "女装",
            "selling_points": ["显瘦", "百搭"],
            "material": "棉麻",
            "target_audience": "轻熟女",
            "style": "法式",
        },
    )
    assert gen.product_id == "p1"
    assert gen.generation_method == "template"
    assert 0 < len(gen.titles) <= 20
    assert len(gen.titles) == len(set(gen.titles))


def test_generate_titles_incorporate_fields(service):
    gen = service.generate_titles(
        product_id="p1",
        product_info={
            "product_name": "衬衫",
            "category": "女装",
            "target_audience": "职场",
            "style": "简约",
        },
    )
    joined = "".join(gen.titles)
    assert "衬衫" in joined
    assert "女装" in joined
    assert "职场" in joined
    assert "简约" in joined


def test_generate_titles_minimal_info_still_produces_titles(service):
    gen = service.generate_titles(
        product_id="p1", product_info={"product_name": "商品X", "category": "类目Y"}
    )
    assert len(gen.titles) >= 1


def test_generate_titles_uses_stored_product_knowledge(storage, service):
    storage.save_product_knowledge(
        ProductKnowledge(
            id="p1",
            product_name="真丝裙",
            category="女装",
            style="优雅",
        )
    )
    gen = service.generate_titles(product_id="p1")
    joined = "".join(gen.titles)
    assert "真丝裙" in joined


def test_generate_titles_uses_keyword_library_and_merchant_profile(storage, service):
    storage.save_keyword_library(KeywordLibrary(id="kw1", core_keywords=["夏季爆款"]))
    storage.save_merchant_profile_v2(
        MerchantProfileV2(
            id="m1",
            merchant_name="店",
            platforms=[Platform.TAOBAO],
            main_category="女装",
            price_range=PriceRange.MEDIUM,
            target_audience="都市白领",
            positioning="轻奢",
            visual_style="简约",
            operation_goal="GMV",
        )
    )
    gen = service.generate_titles(
        product_id="p1", product_info={"product_name": "裙", "category": "女装"}
    )
    joined = "".join(gen.titles)
    assert "夏季爆款" in joined
    assert "都市白领" in joined


def test_generate_20_titles_helper_dedup_and_cap(service):
    titles = service._generate_20_titles(
        product_name="裙",
        category="女装",
        selling_points=["显瘦"],
        material="棉",
        target_audience="女生",
        style="甜美",
        core_keywords=["夏季", "新款"],
    )
    assert len(titles) <= 20
    assert len(titles) == len(set(titles))
