"""
产品B - 订单管理服务
"""

from typing import List, Optional
from datetime import datetime
import uuid

from models.order import Order, OrderStatus, OrderItem, OrderQuery
from utils import paginate


class OrderService:
    """订单管理服务"""
    
    def __init__(self):
        self.orders: dict[str, Order] = {}
    
    def create_order(
        self,
        user_id: str,
        items: List[OrderItem],
        shipping_address: str,
        payment_method: str,
        platform: str
    ) -> Order:
        """
        创建订单
        
        Args:
            user_id: 用户ID
            items: 订单项列表
            shipping_address: 收货地址
            payment_method: 支付方式
            platform: 平台
            
        Returns:
            订单对象
        """
        total_amount = sum(item.price * item.quantity for item in items)
        
        order = Order(
            id=str(uuid.uuid4()),
            user_id=user_id,
            items=items,
            total_amount=total_amount,
            status=OrderStatus.PENDING,
            shipping_address=shipping_address,
            payment_method=payment_method,
            platform=platform,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.orders[order.id] = order
        return order
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """
        获取订单
        
        Args:
            order_id: 订单ID
            
        Returns:
            订单对象
        """
        return self.orders.get(order_id)
    
    def update_order_status(
        self,
        order_id: str,
        status: OrderStatus
    ) -> Optional[Order]:
        """
        更新订单状态
        
        Args:
            order_id: 订单ID
            status: 新状态
            
        Returns:
            更新后的订单对象
        """
        order = self.orders.get(order_id)
        if not order:
            return None
        
        order.status = status
        order.updated_at = datetime.now()
        return order
    
    def cancel_order(self, order_id: str) -> bool:
        """
        取消订单
        
        Args:
            order_id: 订单ID
            
        Returns:
            是否成功
        """
        order = self.orders.get(order_id)
        if order and order.status == OrderStatus.PENDING:
            order.status = OrderStatus.CANCELLED
            order.updated_at = datetime.now()
            return True
        return False
    
    def query_orders(self, query: OrderQuery) -> List[Order]:
        """
        查询订单
        
        Args:
            query: 查询条件
            
        Returns:
            订单列表
        """
        results = list(self.orders.values())
        
        # 用户ID过滤
        if query.user_id:
            results = [o for o in results if o.user_id == query.user_id]
        
        # 状态过滤
        if query.status:
            results = [o for o in results if o.status == query.status]
        
        # 平台过滤
        if query.platform:
            results = [o for o in results if o.platform == query.platform]
        
        # 时间范围过滤
        if query.start_date:
            results = [o for o in results if o.created_at >= query.start_date]
        if query.end_date:
            results = [o for o in results if o.created_at <= query.end_date]
        
        # 分页
        return paginate(results, query.page, query.limit)
    
    def get_orders_by_user(self, user_id: str) -> List[Order]:
        """
        获取用户订单
        
        Args:
            user_id: 用户ID
            
        Returns:
            订单列表
        """
        return [o for o in self.orders.values() if o.user_id == user_id]
    
    def get_total_orders(self) -> int:
        """获取订单总数"""
        return len(self.orders)
    
    def get_total_revenue(self) -> float:
        """获取总收入"""
        return sum(
            o.total_amount for o in self.orders.values()
            if o.status in [OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED]
        )
