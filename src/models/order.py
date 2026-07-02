"""
产品B - 订单模型
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    """订单状态"""
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


@dataclass
class OrderItem:
    """订单项"""
    product_id: str
    product_name: str
    quantity: int
    price: float


@dataclass
class Order:
    """订单模型"""
    id: str
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus
    shipping_address: str
    payment_method: str
    platform: str
    created_at: datetime
    updated_at: datetime
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "price": item.price
                }
                for item in self.items
            ],
            "total_amount": self.total_amount,
            "status": self.status.value,
            "shipping_address": self.shipping_address,
            "payment_method": self.payment_method,
            "platform": self.platform,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class OrderQuery:
    """订单查询"""
    user_id: Optional[str] = None
    status: Optional[OrderStatus] = None
    platform: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    page: int = 1
    limit: int = 10
