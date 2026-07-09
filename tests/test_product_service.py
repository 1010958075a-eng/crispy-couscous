"""Unit tests for ProductService."""

import pytest

from models.product import ProductStatus, ProductSearchQuery
from services.product_service import ProductService


@pytest.fixture
def service():
    return ProductService()


def _make(service, **overrides):
    params = dict(
        name="连衣裙",
        description="夏季新款连衣裙",
        price=199.0,
        stock=100,
        category="女装",
        platform="taobao",
    )
    params.update(overrides)
    return service.create_product(**params)


def test_create_product_defaults(service):
    product = _make(service)
    assert product.id
    assert product.status == ProductStatus.DRAFT
    assert product.images == []
    assert product.tags == []
    assert service.get_total_products() == 1
    assert service.get_product(product.id) is product


def test_create_product_with_images_and_tags(service):
    product = _make(service, images=["a.jpg"], tags=["新品"])
    assert product.images == ["a.jpg"]
    assert product.tags == ["新品"]


def test_get_product_missing_returns_none(service):
    assert service.get_product("nope") is None


def test_update_product_fields(service):
    product = _make(service)
    updated = service.update_product(
        product.id,
        name="新名称",
        description="新描述",
        price=88.0,
        stock=5,
        status=ProductStatus.ACTIVE,
    )
    assert updated is not None
    assert updated.name == "新名称"
    assert updated.description == "新描述"
    assert updated.price == 88.0
    assert updated.stock == 5
    assert updated.status == ProductStatus.ACTIVE


def test_update_product_partial_keeps_other_fields(service):
    product = _make(service, name="原名")
    updated = service.update_product(product.id, price=50.0)
    assert updated.name == "原名"
    assert updated.price == 50.0


def test_update_product_missing_returns_none(service):
    assert service.update_product("nope", name="x") is None


def test_delete_product(service):
    product = _make(service)
    assert service.delete_product(product.id) is True
    assert service.get_product(product.id) is None
    assert service.delete_product(product.id) is False


def test_search_by_keyword_matches_name_and_description(service):
    _make(service, name="红色连衣裙", description="优雅")
    _make(service, name="蓝色衬衫", description="含连衣裙元素")
    _make(service, name="牛仔裤", description="经典")
    results = service.search_products(ProductSearchQuery(keyword="连衣裙", limit=10))
    assert len(results) == 2


def test_search_by_category_and_platform(service):
    _make(service, category="女装", platform="taobao")
    _make(service, category="男装", platform="douyin")
    results = service.search_products(ProductSearchQuery(category="女装"))
    assert len(results) == 1 and results[0].category == "女装"
    results = service.search_products(ProductSearchQuery(platform="douyin"))
    assert len(results) == 1 and results[0].platform == "douyin"


def test_search_by_price_range(service):
    _make(service, price=30.0)
    _make(service, price=150.0)
    _make(service, price=600.0)
    results = service.search_products(
        ProductSearchQuery(min_price=100.0, max_price=500.0)
    )
    assert len(results) == 1
    assert results[0].price == 150.0


def test_search_by_status(service):
    p1 = _make(service)
    _make(service)
    service.update_product(p1.id, status=ProductStatus.ACTIVE)
    results = service.search_products(ProductSearchQuery(status=ProductStatus.ACTIVE))
    assert len(results) == 1
    assert results[0].id == p1.id


def test_search_pagination(service):
    for i in range(5):
        _make(service, name=f"商品{i}")
    page1 = service.search_products(ProductSearchQuery(page=1, limit=2))
    page2 = service.search_products(ProductSearchQuery(page=2, limit=2))
    page3 = service.search_products(ProductSearchQuery(page=3, limit=2))
    assert len(page1) == 2
    assert len(page2) == 2
    assert len(page3) == 1


def test_get_products_by_platform(service):
    _make(service, platform="taobao")
    _make(service, platform="taobao")
    _make(service, platform="douyin")
    assert len(service.get_products_by_platform("taobao")) == 2
    assert len(service.get_products_by_platform("douyin")) == 1
    assert service.get_products_by_platform("unknown") == []
