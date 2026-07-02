"""
产品B - 商品模型
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ProductStatus(Enum):
    """商品状态"""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"


@dataclass
class Product:
    """商品模型"""
    id: str
    name: str
    description: str
    price: float
    stock: int
    category: str
    status: ProductStatus
    images: List[str]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    platform: str  # "taobao", "douyin", etc.
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "status": self.status.value,
            "images": self.images,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "platform": self.platform
        }


@dataclass
class ProductSearchQuery:
    """商品搜索查询"""
    keyword: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    status: Optional[ProductStatus] = None
    platform: Optional[str] = None
    page: int = 1
    limit: int = 10
