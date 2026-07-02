"""
产品B - REST API服务器
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import sys
from pathlib import Path

# 添加项目根目录和src目录到路径
project_root = Path(__file__).parent.parent.parent
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))

from models import Product, Order, ProductStatus, OrderStatus, OrderItem, ProductSearchQuery
from models import LearningTarget, DataType
from services import ProductService, OrderService, AnalyticsService, LearningService, TaskPlanner

# 创建FastAPI应用
app = FastAPI(
    title="产品B电商自动化系统 API",
    description="面向天猫、抖音商家的电商智能自动化平台",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
product_service = ProductService()
order_service = OrderService()
analytics_service = AnalyticsService(order_service, product_service)
learning_service = LearningService()
task_planner = TaskPlanner()


# Pydantic模型
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str
    platform: str
    images: Optional[List[str]] = []
    tags: Optional[List[str]] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    status: Optional[str] = None


class OrderItemCreate(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float


class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItemCreate]
    shipping_address: str
    payment_method: str
    platform: str


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "product-b-ecommerce-api"}


# 商品API
@app.post("/api/products", response_model=dict)
async def create_product(product_data: ProductCreate):
    """创建商品"""
    product = product_service.create_product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        category=product_data.category,
        platform=product_data.platform,
        images=product_data.images,
        tags=product_data.tags
    )
    return product.to_dict()


@app.get("/api/products/{product_id}", response_model=dict)
async def get_product(product_id: str):
    """获取商品"""
    product = product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product.to_dict()


@app.put("/api/products/{product_id}", response_model=dict)
async def update_product(product_id: str, product_data: ProductUpdate):
    """更新商品"""
    status = None
    if product_data.status:
        status = ProductStatus(product_data.status)
    
    product = product_service.update_product(
        product_id=product_id,
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        status=status
    )
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product.to_dict()


@app.delete("/api/products/{product_id}")
async def delete_product(product_id: str):
    """删除商品"""
    success = product_service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="商品不存在")
    return {"message": "商品已删除"}


@app.get("/api/products", response_model=List[dict])
async def search_products(
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    platform: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    """搜索商品"""
    query = ProductSearchQuery(
        keyword=keyword,
        category=category,
        min_price=min_price,
        max_price=max_price,
        platform=platform,
        page=page,
        limit=limit
    )
    products = product_service.search_products(query)
    return [p.to_dict() for p in products]


# 订单API
@app.post("/api/orders", response_model=dict)
async def create_order(order_data: OrderCreate):
    """创建订单"""
    items = [
        OrderItem(
            product_id=item.product_id,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price
        )
        for item in order_data.items
    ]
    
    order = order_service.create_order(
        user_id=order_data.user_id,
        items=items,
        shipping_address=order_data.shipping_address,
        payment_method=order_data.payment_method,
        platform=order_data.platform
    )
    return order.to_dict()


@app.get("/api/orders/{order_id}", response_model=dict)
async def get_order(order_id: str):
    """获取订单"""
    order = order_service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order.to_dict()


@app.put("/api/orders/{order_id}/status")
async def update_order_status(order_id: str, status: str):
    """更新订单状态"""
    order_status = OrderStatus(status)
    order = order_service.update_order_status(order_id, order_status)
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order.to_dict()


@app.get("/api/orders", response_model=List[dict])
async def get_orders(
    user_id: Optional[str] = None,
    status: Optional[str] = None,
    platform: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    """获取订单列表"""
    from models.order import OrderQuery
    order_status = OrderStatus(status) if status else None
    
    query = OrderQuery(
        user_id=user_id,
        status=order_status,
        platform=platform,
        page=page,
        limit=limit
    )
    orders = order_service.query_orders(query)
    return [o.to_dict() for o in orders]


# 数据分析API
@app.get("/api/analytics/sales-summary")
async def get_sales_summary(days: int = 7):
    """获取销售摘要"""
    summary = analytics_service.get_sales_summary(days=days)
    return summary


@app.get("/api/analytics/top-products")
async def get_top_products(limit: int = 10):
    """获取热销商品"""
    products = analytics_service.get_top_products(limit=limit)
    return products


@app.get("/api/analytics/platform-performance")
async def get_platform_performance(days: int = 30):
    """获取平台表现"""
    performance = analytics_service.get_platform_performance(days=days)
    return performance


@app.get("/api/analytics/report")
async def generate_report(days: int = 7):
    """生成日报"""
    report = analytics_service.generate_daily_report(days=days)
    return {"report": report}


# 学习中心API端点

# 学习中心请求模型
class LinkLearningRequest(BaseModel):
    url: str
    source_platform: str
    learning_target: str
    notes: Optional[str] = None
    manual_content: Optional[str] = None


class TextLearningRequest(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str] = []
    learning_target: str = "other"


class TableLearningRequest(BaseModel):
    filename: str
    data_type: str
    row_count: int


class ReviewLearningRequest(BaseModel):
    action: str
    result: str
    exposure: Optional[int] = None
    click_rate: Optional[float] = None
    conversion_rate: Optional[float] = None
    roi: Optional[float] = None
    problems: List[str] = []
    next_action: Optional[str] = None


class TaskPlanningRequest(BaseModel):
    user_input: str


# 学习中心端点
@app.post("/api/learning/link")
async def learn_from_link(request: LinkLearningRequest):
    """链接学习"""
    try:
        learning_target = LearningTarget(request.learning_target)
        record = learning_service.learn_from_link(
            url=request.url,
            source_platform=request.source_platform,
            learning_target=learning_target,
            notes=request.notes,
            manual_content=request.manual_content
        )
        return record.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"无效的学习目标: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"链接学习失败: {e}")


@app.post("/api/learning/text")
async def learn_from_text(request: TextLearningRequest):
    """文本学习"""
    try:
        learning_target = LearningTarget(request.learning_target)
        record = learning_service.learn_from_text(
            title=request.title,
            content=request.content,
            category=request.category,
            tags=request.tags,
            learning_target=learning_target
        )
        return record.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"无效的学习目标: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文本学习失败: {e}")


@app.post("/api/learning/table")
async def learn_from_table(request: TableLearningRequest):
    """表格学习"""
    try:
        data_type = DataType(request.data_type)
        record = learning_service.learn_from_table(
            filename=request.filename,
            data_type=data_type,
            row_count=request.row_count
        )
        return record.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"无效的数据类型: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"表格学习失败: {e}")


@app.post("/api/learning/review")
async def learn_from_review(request: ReviewLearningRequest):
    """复盘学习"""
    try:
        record = learning_service.learn_from_review(
            action=request.action,
            result=request.result,
            exposure=request.exposure,
            click_rate=request.click_rate,
            conversion_rate=request.conversion_rate,
            roi=request.roi,
            problems=request.problems,
            next_action=request.next_action
        )
        return record.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"复盘学习失败: {e}")


@app.get("/api/learning/records")
async def get_learning_records(record_type: str = "all"):
    """获取学习记录"""
    try:
        if record_type == "link":
            records = learning_service.get_link_learning_records()
        elif record_type == "text":
            records = learning_service.get_text_learning_records()
        elif record_type == "table":
            records = learning_service.get_table_learning_records()
        elif record_type == "review":
            records = learning_service.get_review_learning_records()
        else:
            # 返回所有记录
            return {
                "link": [r.to_dict() for r in learning_service.get_link_learning_records()],
                "text": [r.to_dict() for r in learning_service.get_text_learning_records()],
                "table": [r.to_dict() for r in learning_service.get_table_learning_records()],
                "review": [r.to_dict() for r in learning_service.get_review_learning_records()]
            }

        return [r.to_dict() for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取学习记录失败: {e}")


@app.get("/api/learning/knowledge")
async def get_knowledge_records(category: Optional[str] = None):
    """获取知识库记录"""
    try:
        if category:
            records = learning_service.get_knowledge_by_category(category)
        else:
            records = learning_service.get_knowledge_records()
        return [r.to_dict() for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取知识库记录失败: {e}")


@app.get("/api/learning/health")
async def learning_health_check():
    """学习中心健康检查"""
    return {
        "status": "healthy",
        "service": "product-b-learning-center",
        "features": {
            "link_learning": True,
            "text_learning": True,
            "table_learning": True,
            "review_learning": True,
            "knowledge_base": True
        }
    }


# 任务拆解端点
@app.post("/api/task/plan")
async def plan_task(request: TaskPlanningRequest):
    """一句话任务拆解"""
    try:
        task_plan = task_planner.parse_task(request.user_input)
        return task_plan.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"任务拆解失败: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
