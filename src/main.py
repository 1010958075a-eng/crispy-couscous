"""
产品B - 电商智能自动化平台
主应用入口
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

# 导入产品B业务服务
from models import Product, Order, ProductStatus, OrderStatus, OrderItem
from services import ProductService, OrderService, AnalyticsService

# 导入LLM客户端（可选依赖）
try:
    from llm import create_llm_client
    from config.llm_config import LLMConfig
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("警告：LLM模块不可用，将使用基础模式")


class ECommercePlatform:
    """电商平台核心类"""

    def __init__(self, llm_config: LLMConfig = None):
        # 初始化LLM（可选）
        if LLM_AVAILABLE:
            if llm_config:
                self.llm = create_llm_client(llm_config)
            else:
                self.llm = create_llm_client()
            self.llm_enabled = True
        else:
            self.llm = None
            self.llm_enabled = False

        # 初始化业务服务
        self.product_service = ProductService()
        self.order_service = OrderService()
        self.analytics_service = AnalyticsService(self.order_service, self.product_service)
    
    def run_basic_demo(self):
        """运行基础业务服务演示"""
        print("=" * 60)
        print("产品B电商自动化系统 - 基础演示")
        print("=" * 60)
        print(f"LLM状态: {'启用' if self.llm_enabled else '禁用（基础模式）'}")
        print(f"LLM模块: {'可用' if LLM_AVAILABLE else '不可用'}")

        # 演示业务服务
        self._demo_business_services()

        print("\n" + "=" * 60)
        print("基础演示完成")
        print("=" * 60)
    
    def _demo_business_services(self):
        """演示业务服务"""
        print("\n" + "=" * 60)
        print("业务服务演示")
        print("=" * 60)
        
        # 创建示例商品
        print("\n[1] 创建商品")
        product1 = self.product_service.create_product(
            name="智能手表",
            description="多功能智能手表，支持健康监测",
            price=299.0,
            stock=100,
            category="数码",
            platform="taobao",
            tags=["智能", "健康"]
        )
        product2 = self.product_service.create_product(
            name="蓝牙耳机",
            description="无线蓝牙耳机，降噪功能",
            price=199.0,
            stock=200,
            category="数码",
            platform="douyin",
            tags=["无线", "降噪"]
        )
        print(f"  ✓ 创建商品: {product1.name} (¥{product1.price})")
        print(f"  ✓ 创建商品: {product2.name} (¥{product2.price})")
        
        # 创建示例订单
        print("\n[2] 创建订单")
        order1 = self.order_service.create_order(
            user_id="user001",
            items=[
                OrderItem(
                    product_id=product1.id,
                    product_name=product1.name,
                    quantity=2,
                    price=product1.price
                )
            ],
            shipping_address="北京市朝阳区",
            payment_method="alipay",
            platform="taobao"
        )
        order1.status = OrderStatus.PAID
        print(f"  ✓ 创建订单: {order1.id} (¥{order1.total_amount})")
        
        # 搜索商品
        print("\n[3] 搜索商品")
        from models.product import ProductSearchQuery
        results = self.product_service.search_products(
            ProductSearchQuery(keyword="智能", limit=10)
        )
        print(f"  ✓ 找到 {len(results)} 个商品")
        for p in results:
            print(f"    - {p.name}: ¥{p.price}")
        
        # 数据分析
        print("\n[4] 数据分析")
        summary = self.analytics_service.get_sales_summary(days=7)
        print(f"  ✓ 总订单数: {summary['total_orders']}")
        print(f"  ✓ 总收入: ¥{summary['total_revenue']:,.2f}")
        
        # 生成报告
        print("\n[5] 生成日报")
        report = self.analytics_service.generate_daily_report(days=7)
        print(f"  ✓ 报告生成完成（前200字符）:")
        print(f"    {report[:200]}...")


async def main():
    """主函数"""
    platform = ECommercePlatform()

    # 运行基础演示
    platform.run_basic_demo()

    print("\n✓ 产品B基础演示完成")
    print("\n下一步:")
    print("1. 集成学习中心功能")
    print("2. 实现数据喂养能力")
    print("3. 添加本地知识库")
    print("4. 实现一句话任务拆解")


if __name__ == "__main__":
    asyncio.run(main())
