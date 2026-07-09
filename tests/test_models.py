"""Unit tests for data-model serialization (to_dict)."""

from datetime import datetime

from models.order import Order, OrderItem, OrderStatus
from models.product import Product, ProductStatus
from models.log import Log, LogLevel, LogStatus, LogType
from models.listing import (
    ImagePrompt,
    ImagePromptGeneration,
    KeywordGeneration,
    ListingPackage,
    TitleGeneration,
)
from models.merchant import (
    MerchantProfile as MerchantProfileV2,
    Platform,
    PriceRange,
    ProductKnowledge,
)


def test_product_to_dict():
    now = datetime(2026, 1, 1, 12, 0, 0)
    product = Product(
        id="p1",
        name="连衣裙",
        description="描述",
        price=199.0,
        stock=10,
        category="女装",
        status=ProductStatus.ACTIVE,
        images=["a.jpg"],
        tags=["新品"],
        created_at=now,
        updated_at=now,
        platform="taobao",
    )
    d = product.to_dict()
    assert d["status"] == "active"
    assert d["created_at"] == now.isoformat()
    assert d["images"] == ["a.jpg"]


def test_order_to_dict_nested_items():
    now = datetime(2026, 1, 1)
    order = Order(
        id="o1",
        user_id="u1",
        items=[OrderItem(product_id="p1", product_name="A", quantity=2, price=50.0)],
        total_amount=100.0,
        status=OrderStatus.PAID,
        shipping_address="北京",
        payment_method="alipay",
        platform="taobao",
        created_at=now,
        updated_at=now,
    )
    d = order.to_dict()
    assert d["status"] == "paid"
    assert d["items"][0]["product_name"] == "A"
    assert d["items"][0]["quantity"] == 2


def test_log_to_dict_and_enums():
    log = Log(
        log_id="l1",
        log_type=LogType.TASK.value,
        source_module="m",
        source_id=None,
        action="create",
        status=LogStatus.SUCCESS.value,
        risk_level=None,
        message="msg",
        details={"a": 1},
    )
    d = log.to_dict()
    assert d["log_type"] == "task"
    assert d["status"] == "success"
    assert d["details"] == {"a": 1}
    assert "created_at" in d
    assert LogLevel.ERROR.value == "error"


def test_title_generation_to_dict():
    gen = TitleGeneration(
        id="t1",
        product_id="p1",
        titles=["标题1", "标题2"],
        generation_method="template",
    )
    d = gen.to_dict()
    assert d["titles"] == ["标题1", "标题2"]
    assert d["generation_method"] == "template"


def test_keyword_generation_to_dict():
    gen = KeywordGeneration(
        id="k1",
        product_id="p1",
        core_keywords=["a"],
        long_tail_keywords=["b"],
        audience_keywords=[],
        scenario_keywords=[],
        selling_point_keywords=[],
        ad_keywords=[],
        negative_keywords=["x"],
        generation_method="template",
    )
    d = gen.to_dict()
    assert d["core_keywords"] == ["a"]
    assert d["negative_keywords"] == ["x"]


def test_image_prompt_generation_to_dict_nested():
    prompt = ImagePrompt(
        image_type="白底主图",
        purpose="展示",
        structure="居中",
        focus="正面",
        ai_prompt_cn="中文提示",
        ai_prompt_en="english prompt",
        notes="注意",
    )
    gen = ImagePromptGeneration(
        id="i1", product_id="p1", prompts=[prompt], generation_method="template"
    )
    d = gen.to_dict()
    assert d["prompts"][0]["image_type"] == "白底主图"
    assert d["prompts"][0]["ai_prompt_en"] == "english prompt"


def test_listing_package_to_dict_defaults():
    pkg = ListingPackage(
        id="lp1",
        product_id="p1",
        product_info={"name": "x"},
        titles=["t"],
        keywords={"core": ["a"]},
        image_prompts=[{"image_type": "白底"}],
    )
    d = pkg.to_dict()
    assert d["pending_review"] == []
    assert d["merchant_profile"] is None
    assert d["keywords"] == {"core": ["a"]}


def test_merchant_profile_v2_to_dict_enum_values():
    profile = MerchantProfileV2(
        id="m1",
        merchant_name="店",
        platforms=[Platform.TAOBAO, Platform.TMALL],
        main_category="女装",
        price_range=PriceRange.HIGH,
        target_audience="白领",
        positioning="轻奢",
        visual_style="简约",
        operation_goal="GMV",
    )
    d = profile.to_dict()
    assert d["platforms"] == ["淘宝", "天猫"]
    assert d["price_range"] == "高价（500-1000元）"


def test_product_knowledge_to_dict_defaults():
    pk = ProductKnowledge(id="pk1", product_name="裙", category="女装")
    d = pk.to_dict()
    assert d["selling_points"] == []
    assert d["price"] == 0.0
    assert d["sku"] is None
