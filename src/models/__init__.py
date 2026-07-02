"""
产品B - 数据模型
"""

from .product import Product, ProductStatus, ProductSearchQuery
from .order import Order, OrderStatus, OrderItem, OrderQuery
from .learning import (
    LinkLearningRecord,
    TextLearningRecord,
    TableLearningRecord,
    ReviewLearningRecord,
    KnowledgeRecord,
    MerchantProfile,
    LearningTarget,
    DataType,
    LinkLearningStatus
)

__all__ = [
    # Product models
    "Product",
    "ProductStatus",
    "ProductSearchQuery",
    # Order models
    "Order",
    "OrderStatus",
    "OrderItem",
    "OrderQuery",
    # Learning models
    "LinkLearningRecord",
    "TextLearningRecord",
    "TableLearningRecord",
    "ReviewLearningRecord",
    "KnowledgeRecord",
    "MerchantProfile",
    "LearningTarget",
    "DataType",
    "LinkLearningStatus"
]
