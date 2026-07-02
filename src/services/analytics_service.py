"""
产品B - 数据分析服务
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict

from models.order import Order, OrderStatus
from models.product import Product


class AnalyticsService:
    """数据分析服务"""
    
    def __init__(self, order_service, product_service):
        self.order_service = order_service
        self.product_service = product_service
    
    def get_sales_summary(self, days: int = 7) -> Dict[str, Any]:
        """
        获取销售摘要
        
        Args:
            days: 天数
            
        Returns:
            销售摘要数据
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取指定时间范围内的订单
        orders = [
            o for o in self.order_service.orders.values()
            if o.created_at >= start_date and o.created_at <= end_date
        ]
        
        total_orders = len(orders)
        total_revenue = sum(
            o.total_amount for o in orders
            if o.status in [OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED]
        )
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # 按状态统计
        status_counts = defaultdict(int)
        for order in orders:
            status_counts[order.status.value] += 1
        
        return {
            "period_days": days,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "avg_order_value": avg_order_value,
            "status_breakdown": dict(status_counts)
        }
    
    def get_top_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取热销商品
        
        Args:
            limit: 返回数量
            
        Returns:
            商品销量列表
        """
        # 统计每个商品的销售数量
        product_sales = defaultdict(int)
        
        for order in self.order_service.orders.values():
            if order.status in [OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
                for item in order.items:
                    product_sales[item.product_id] += item.quantity
        
        # 获取商品详情并排序
        top_products = []
        for product_id, sales in product_sales.items():
            product = self.product_service.get_product(product_id)
            if product:
                top_products.append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "category": product.category,
                    "sales": sales,
                    "revenue": sales * product.price
                })
        
        # 按销量排序
        top_products.sort(key=lambda x: x["sales"], reverse=True)
        return top_products[:limit]
    
    def get_platform_performance(self, days: int = 30) -> Dict[str, Any]:
        """
        获取平台表现
        
        Args:
            days: 天数
            
        Returns:
            平台表现数据
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 按平台统计
        platform_data = defaultdict(lambda: {
            "orders": 0,
            "revenue": 0.0,
            "products": 0
        })
        
        # 统计订单数据
        for order in self.order_service.orders.values():
            if order.created_at >= start_date and order.created_at <= end_date:
                if order.status in [OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
                    platform_data[order.platform]["orders"] += 1
                    platform_data[order.platform]["revenue"] += order.total_amount
        
        # 统计商品数据
        for product in self.product_service.products.values():
            platform_data[product.platform]["products"] += 1
        
        return dict(platform_data)
    
    def generate_daily_report(self, days: int = 7) -> str:
        """
        生成日报
        
        Args:
            days: 天数
            
        Returns:
            日报文本
        """
        summary = self.get_sales_summary(days)
        top_products = self.get_top_products(5)
        platform_performance = self.get_platform_performance(days)
        
        report = f"""
# 电商数据分析日报

## 时间范围
{summary['start_date']} 至 {summary['end_date']}（{summary['period_days']}天）

## 销售概览
- 总订单数: {summary['total_orders']}
- 总收入: ¥{summary['total_revenue']:,.2f}
- 平均订单价值: ¥{summary['avg_order_value']:,.2f}

## 订单状态分布
"""
        for status, count in summary['status_breakdown'].items():
            report += f"- {status}: {count}\n"
        
        report += "\n## 热销商品 TOP 5\n"
        for i, product in enumerate(top_products, 1):
            report += f"{i}. {product['product_name']}\n"
            report += f"   销量: {product['sales']} | 收入: ¥{product['revenue']:,.2f}\n"
        
        report += "\n## 平台表现\n"
        for platform, data in platform_performance.items():
            report += f"- {platform}:\n"
            report += f"  订单数: {data['orders']} | 收入: ¥{data['revenue']:,.2f} | 商品数: {data['products']}\n"
        
        return report
