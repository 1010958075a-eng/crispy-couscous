"""Unit tests for OrderService."""

from datetime import datetime, timedelta

import pytest

from models.order import OrderItem, OrderQuery, OrderStatus
from services.order_service import OrderService


@pytest.fixture
def service():
    return OrderService()


def _items():
    return [
        OrderItem(product_id="p1", product_name="A", quantity=2, price=50.0),
        OrderItem(product_id="p2", product_name="B", quantity=1, price=30.0),
    ]


def _make(service, **overrides):
    params = dict(
        user_id="u1",
        items=_items(),
        shipping_address="北京市",
        payment_method="alipay",
        platform="taobao",
    )
    params.update(overrides)
    return service.create_order(**params)


def test_create_order_computes_total(service):
    order = _make(service)
    assert order.total_amount == 130.0
    assert order.status == OrderStatus.PENDING
    assert service.get_total_orders() == 1
    assert service.get_order(order.id) is order


def test_get_order_missing(service):
    assert service.get_order("nope") is None


def test_update_order_status(service):
    order = _make(service)
    updated = service.update_order_status(order.id, OrderStatus.PAID)
    assert updated.status == OrderStatus.PAID


def test_update_order_status_missing(service):
    assert service.update_order_status("nope", OrderStatus.PAID) is None


def test_cancel_pending_order(service):
    order = _make(service)
    assert service.cancel_order(order.id) is True
    assert service.get_order(order.id).status == OrderStatus.CANCELLED


def test_cannot_cancel_paid_order(service):
    order = _make(service)
    service.update_order_status(order.id, OrderStatus.PAID)
    assert service.cancel_order(order.id) is False


def test_cancel_missing_order(service):
    assert service.cancel_order("nope") is False


def test_query_by_user_status_platform(service):
    o1 = _make(service, user_id="u1", platform="taobao")
    _make(service, user_id="u2", platform="douyin")
    service.update_order_status(o1.id, OrderStatus.PAID)

    assert len(service.query_orders(OrderQuery(user_id="u1"))) == 1
    assert len(service.query_orders(OrderQuery(status=OrderStatus.PAID))) == 1
    assert len(service.query_orders(OrderQuery(platform="douyin"))) == 1


def test_query_by_date_range(service):
    order = _make(service)
    past = datetime.now() - timedelta(days=1)
    future = datetime.now() + timedelta(days=1)
    assert len(service.query_orders(OrderQuery(start_date=past, end_date=future))) == 1
    assert len(service.query_orders(OrderQuery(start_date=future))) == 0
    assert order.id


def test_query_pagination(service):
    for _ in range(5):
        _make(service)
    assert len(service.query_orders(OrderQuery(page=1, limit=2))) == 2
    assert len(service.query_orders(OrderQuery(page=3, limit=2))) == 1


def test_get_orders_by_user(service):
    _make(service, user_id="u1")
    _make(service, user_id="u1")
    _make(service, user_id="u2")
    assert len(service.get_orders_by_user("u1")) == 2
    assert service.get_orders_by_user("nope") == []


def test_get_total_revenue_counts_only_fulfilled(service):
    o_paid = _make(service)
    o_shipped = _make(service)
    o_delivered = _make(service)
    _make(service)  # pending, excluded
    service.update_order_status(o_paid.id, OrderStatus.PAID)
    service.update_order_status(o_shipped.id, OrderStatus.SHIPPED)
    service.update_order_status(o_delivered.id, OrderStatus.DELIVERED)
    assert service.get_total_revenue() == 390.0
