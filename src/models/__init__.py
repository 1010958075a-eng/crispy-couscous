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
from .merchant import (
    Platform,
    PriceRange,
    MerchantProfile as MerchantProfileV2,
    ProductKnowledge,
    CompetitorKnowledge,
    KeywordLibrary,
    VisualStyleLibrary,
    ReviewRecord
)
from .listing import (
    TitleGeneration,
    KeywordGeneration,
    ImagePrompt,
    ImagePromptGeneration,
    ListingPackage
)
from .detail import (
    DetailScreen,
    DetailScreenGeneration
)
from .content import (
    VideoScriptScene,
    VideoScriptGeneration,
    XiaohongshuNote
)
from .task import (
    Task,
    TaskStep,
    TaskStatus,
    RiskLevel
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
    "LinkLearningStatus",
    # Merchant models (v0.2)
    "Platform",
    "PriceRange",
    "MerchantProfileV2",
    "ProductKnowledge",
    "CompetitorKnowledge",
    "KeywordLibrary",
    "VisualStyleLibrary",
    "ReviewRecord",
    # Listing models (v0.3)
    "TitleGeneration",
    "KeywordGeneration",
    "ImagePrompt",
    "ImagePromptGeneration",
    "ListingPackage",
    # Detail models (v0.4)
    "DetailScreen",
    "DetailScreenGeneration",
    # Content models (v0.4 phase 2)
    "VideoScriptScene",
    "VideoScriptGeneration",
    "XiaohongshuNote",
    # Task models (v0.5)
    "Task",
    "TaskStep",
    "TaskStatus",
    "RiskLevel"
]
