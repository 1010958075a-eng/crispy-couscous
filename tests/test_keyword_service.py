"""Unit tests for KeywordService."""

import pytest

from models.merchant import KeywordLibrary, ProductKnowledge
from services.knowledge_storage import KnowledgeStorage
from services.keyword_service import KeywordService


@pytest.fixture
def storage(tmp_path):
    return KnowledgeStorage(base_path=str(tmp_path / "data"))


@pytest.fixture
def service(storage):
    return KeywordService(knowledge_storage=storage)


def test_generate_keywords_from_product_info(service):
    gen = service.generate_keywords(
        product_id="p1",
        product_info={
            "product_name": "连衣裙",
            "category": "女装",
            "material": "棉",
            "style": "复古",
        },
    )
    assert gen.product_id == "p1"
    assert gen.generation_method == "template"
    assert "连衣裙" in gen.core_keywords
    assert "女装" in gen.core_keywords
    assert "女装连衣裙" in gen.long_tail_keywords
    assert "棉" in gen.selling_point_keywords
    assert "复古" in gen.selling_point_keywords


def test_generate_keywords_merges_library(storage, service):
    storage.save_keyword_library(
        KeywordLibrary(
            id="kw1",
            core_keywords=["夏季"],
            long_tail_keywords=["夏季新款"],
            negative_keywords=["二手"],
        )
    )
    gen = service.generate_keywords(
        product_id="p1", product_info={"product_name": "裙子", "category": "女装"}
    )
    assert "夏季" in gen.core_keywords
    assert "夏季新款" in gen.long_tail_keywords
    assert "二手" in gen.negative_keywords


def test_generate_keywords_deduplicates(storage, service):
    storage.save_keyword_library(KeywordLibrary(id="kw1", core_keywords=["女装", "女装"]))
    gen = service.generate_keywords(
        product_id="p1", product_info={"product_name": "裙子", "category": "女装"}
    )
    assert gen.core_keywords.count("女装") == 1


def test_generate_keywords_uses_stored_product_knowledge(storage, service):
    storage.save_product_knowledge(
        ProductKnowledge(
            id="p1",
            product_name="真丝衬衫",
            category="女装",
            material="真丝",
        )
    )
    gen = service.generate_keywords(product_id="p1")
    assert "真丝衬衫" in gen.core_keywords
    assert "真丝" in gen.selling_point_keywords


def test_get_product_knowledge_missing_returns_none(service):
    assert service._get_product_knowledge("nope") is None
