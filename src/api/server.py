"""
产品B - REST API服务器
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
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
from models import Platform, PriceRange, MerchantProfileV2, ProductKnowledge, CompetitorKnowledge, KeywordLibrary, VisualStyleLibrary, ReviewRecord
from models import TitleGeneration, KeywordGeneration, ImagePromptGeneration, ListingPackage
from models import DetailScreen, DetailScreenGeneration
from models import VideoScriptScene, VideoScriptGeneration, XiaohongshuNote
from models import Task, TaskStep, TaskStatus, RiskLevel
from models import AcceptanceReport, AcceptanceIssue, AcceptanceStatus, TargetType
from models import Tool, ToolPlan, ExecutionStep, ToolType, ToolCategory, PlanStatus
from models import Workflow, WorkflowStep, WorkflowStatus, StepStatus, StepType
from models import Log, LogType, LogLevel, LogStatus
from models import ApiProvider, ApiCallRecord, ApiQuotaRecord, ProviderType, CostLevel, RiskLevel, CallStatus
from services import ProductService, OrderService, AnalyticsService, LearningService, TaskPlanner, KnowledgeStorage
from services import TitleService, KeywordService, ImagePromptService, PackageService, DetailService, ContentService, TaskService, AcceptanceService, ToolService, WorkflowService, LogService, ApiProviderService

# 导入枚举类型
from models.merchant import Platform as PlatformEnum, PriceRange as PriceRangeEnum

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
knowledge_storage = KnowledgeStorage()
title_service = TitleService(knowledge_storage)
keyword_service = KeywordService(knowledge_storage)
image_prompt_service = ImagePromptService(knowledge_storage)
package_service = PackageService(knowledge_storage)
detail_service = DetailService(knowledge_storage)
content_service = ContentService(knowledge_storage)
task_service = TaskService(knowledge_storage)
acceptance_service = AcceptanceService(knowledge_storage)
tool_service = ToolService(knowledge_storage)
log_service = LogService(knowledge_storage)
workflow_service = WorkflowService(knowledge_storage, task_service, tool_service, log_service)
api_provider_service = ApiProviderService(knowledge_storage)


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


# v0.2 商家数据喂养 API端点

# 商家档案请求模型
class MerchantProfileV2Request(BaseModel):
    merchant_name: str
    platforms: List[str]
    main_category: str
    price_range: str
    target_audience: str
    positioning: str
    visual_style: str
    operation_goal: str


class ProductKnowledgeRequest(BaseModel):
    product_name: str
    category: str
    sku: Optional[str] = None
    price: float = 0.0
    selling_points: List[str] = []
    material: Optional[str] = None
    target_audience: Optional[str] = None
    style: Optional[str] = None
    notes: Optional[str] = None


class CompetitorKnowledgeRequest(BaseModel):
    competitor_url: str
    competitor_title: str
    price: float = 0.0
    selling_points: List[str] = []
    main_image_style: Optional[str] = None
    detail_page_structure: Optional[str] = None
    learnable_points: List[str] = []
    differentiation_opportunity: Optional[str] = None


class KeywordLibraryRequest(BaseModel):
    core_keywords: List[str] = []
    long_tail_keywords: List[str] = []
    audience_keywords: List[str] = []
    scenario_keywords: List[str] = []
    selling_point_keywords: List[str] = []
    ad_keywords: List[str] = []
    negative_keywords: List[str] = []


class VisualStyleLibraryRequest(BaseModel):
    main_image_style: str
    detail_page_style: str
    model_style: Optional[str] = None
    scenario_style: Optional[str] = None
    color_tone: Optional[str] = None
    composition_method: Optional[str] = None
    ai_image_prompt_template: Optional[str] = None


class ReviewRecordRequest(BaseModel):
    action_type: str
    action_content: str
    action_result: str
    exposure: Optional[int] = None
    click_rate: Optional[float] = None
    conversion_rate: Optional[float] = None
    roi: Optional[float] = None
    problem_judgment: Optional[str] = None
    next_step_suggestion: Optional[str] = None


# 商家档案API
@app.post("/api/merchant/profile")
async def save_merchant_profile(request: MerchantProfileV2Request):
    """保存商家档案"""
    try:
        profile = MerchantProfileV2(
            id=knowledge_storage.generate_id(),
            merchant_name=request.merchant_name,
            platforms=[PlatformEnum(p) for p in request.platforms],
            main_category=request.main_category,
            price_range=PriceRangeEnum(request.price_range),
            target_audience=request.target_audience,
            positioning=request.positioning,
            visual_style=request.visual_style,
            operation_goal=request.operation_goal
        )
        knowledge_storage.save_merchant_profile_v2(profile)
        return profile.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"无效的参数: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存商家档案失败: {e}")


@app.get("/api/merchant/profile")
async def get_merchant_profile():
    """获取商家档案"""
    try:
        profile = knowledge_storage.load_merchant_profile_v2()
        if profile:
            return profile.to_dict()
        else:
            return {"message": "商家档案不存在"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取商家档案失败: {e}")


# 产品知识库API
@app.post("/api/knowledge/product")
async def save_product_knowledge(request: ProductKnowledgeRequest):
    """保存产品知识"""
    try:
        knowledge = ProductKnowledge(
            id=knowledge_storage.generate_id(),
            product_name=request.product_name,
            category=request.category,
            sku=request.sku,
            price=request.price,
            selling_points=request.selling_points,
            material=request.material,
            target_audience=request.target_audience,
            style=request.style,
            notes=request.notes
        )
        knowledge_storage.save_product_knowledge(knowledge)
        return knowledge.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存产品知识失败: {e}")


@app.get("/api/knowledge/product")
async def get_product_knowledge():
    """获取产品知识库"""
    try:
        records = knowledge_storage.load_product_knowledge()
        return [r.to_dict() for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取产品知识库失败: {e}")


# 竞品知识库API
@app.post("/api/knowledge/competitor")
async def save_competitor_knowledge(request: CompetitorKnowledgeRequest):
    """保存竞品知识"""
    try:
        knowledge = CompetitorKnowledge(
            id=knowledge_storage.generate_id(),
            competitor_url=request.competitor_url,
            competitor_title=request.competitor_title,
            price=request.price,
            selling_points=request.selling_points,
            main_image_style=request.main_image_style,
            detail_page_structure=request.detail_page_structure,
            learnable_points=request.learnable_points,
            differentiation_opportunity=request.differentiation_opportunity
        )
        knowledge_storage.save_competitor_knowledge(knowledge)
        return knowledge.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存竞品知识失败: {e}")


@app.get("/api/knowledge/competitor")
async def get_competitor_knowledge():
    """获取竞品知识库"""
    try:
        records = knowledge_storage.load_competitor_knowledge()
        return [r.to_dict() for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取竞品知识库失败: {e}")


# 关键词库API
@app.post("/api/knowledge/keywords")
async def save_keyword_library(request: KeywordLibraryRequest):
    """保存关键词库"""
    try:
        library = KeywordLibrary(
            id=knowledge_storage.generate_id(),
            core_keywords=request.core_keywords,
            long_tail_keywords=request.long_tail_keywords,
            audience_keywords=request.audience_keywords,
            scenario_keywords=request.scenario_keywords,
            selling_point_keywords=request.selling_point_keywords,
            ad_keywords=request.ad_keywords,
            negative_keywords=request.negative_keywords
        )
        knowledge_storage.save_keyword_library(library)
        return library.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存关键词库失败: {e}")


@app.get("/api/knowledge/keywords")
async def get_keyword_library():
    """获取关键词库"""
    try:
        records = knowledge_storage.load_keyword_library()
        return [r.to_dict() for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取关键词库失败: {e}")


# 视觉风格库API
@app.post("/api/knowledge/visual-style")
async def save_visual_style_library(request: VisualStyleLibraryRequest):
    """保存视觉风格库"""
    try:
        library = VisualStyleLibrary(
            id=knowledge_storage.generate_id(),
            main_image_style=request.main_image_style,
            detail_page_style=request.detail_page_style,
            model_style=request.model_style,
            scenario_style=request.scenario_style,
            color_tone=request.color_tone,
            composition_method=request.composition_method,
            ai_image_prompt_template=request.ai_image_prompt_template
        )
        knowledge_storage.save_visual_style_library(library)
        return library.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存视觉风格库失败: {e}")


@app.get("/api/knowledge/visual-style")
async def get_visual_style_library():
    """获取视觉风格库"""
    try:
        records = knowledge_storage.load_visual_style_library()
        return [r.to_dict() for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取视觉风格库失败: {e}")


# 复盘记录库API
@app.post("/api/review/record")
async def save_review_record(request: ReviewRecordRequest):
    """保存复盘记录"""
    try:
        record = ReviewRecord(
            id=knowledge_storage.generate_id(),
            action_type=request.action_type,
            action_content=request.action_content,
            action_result=request.action_result,
            exposure=request.exposure,
            click_rate=request.click_rate,
            conversion_rate=request.conversion_rate,
            roi=request.roi,
            problem_judgment=request.problem_judgment,
            next_step_suggestion=request.next_step_suggestion
        )
        knowledge_storage.save_review_record_v2(record)
        return record.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存复盘记录失败: {e}")


@app.get("/api/review/record")
async def get_review_records():
    """获取复盘记录库"""
    try:
        records = knowledge_storage.load_review_records_v2()
        return [r.to_dict() for r in records]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取复盘记录库失败: {e}")


# v0.3 上架包生成 API端点

# 标题生成请求模型
class TitleGenerationRequest(BaseModel):
    product_id: str
    product_info: Optional[Dict[str, Any]] = None
    merchant_profile_id: Optional[str] = None
    keyword_library_id: Optional[str] = None
    visual_style_id: Optional[str] = None


# 关键词生成请求模型
class KeywordGenerationRequest(BaseModel):
    product_id: str
    product_info: Optional[Dict[str, Any]] = None
    keyword_library_id: Optional[str] = None


# 主图提示词生成请求模型
class ImagePromptGenerationRequest(BaseModel):
    product_id: str
    product_info: Optional[Dict[str, Any]] = None
    visual_style_id: Optional[str] = None


# 上架包生成请求模型
class PackageGenerationRequest(BaseModel):
    product_id: str
    product_info: Optional[Dict[str, Any]] = None


# 标题生成API
@app.post("/api/listing/generate-title")
async def generate_title(request: TitleGenerationRequest):
    """生成20个标题"""
    try:
        generation = title_service.generate_titles(
            product_id=request.product_id,
            product_info=request.product_info,
            merchant_profile_id=request.merchant_profile_id,
            keyword_library_id=request.keyword_library_id,
            visual_style_id=request.visual_style_id
        )
        knowledge_storage.save_title_generation(generation)
        return generation.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成标题失败: {e}")


# 关键词生成API
@app.post("/api/listing/generate-keywords")
async def generate_keywords(request: KeywordGenerationRequest):
    """生成关键词包"""
    try:
        generation = keyword_service.generate_keywords(
            product_id=request.product_id,
            product_info=request.product_info,
            keyword_library_id=request.keyword_library_id
        )
        knowledge_storage.save_keyword_generation(generation)
        return generation.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成关键词失败: {e}")


# 主图提示词生成API
@app.post("/api/listing/generate-main-image-prompts")
async def generate_main_image_prompts(request: ImagePromptGenerationRequest):
    """生成主图九宫格提示词"""
    try:
        generation = image_prompt_service.generate_image_prompts(
            product_id=request.product_id,
            product_info=request.product_info,
            visual_style_id=request.visual_style_id
        )
        knowledge_storage.save_image_prompt_generation(generation)
        return generation.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成主图提示词失败: {e}")


# 上架包生成API
@app.post("/api/listing/generate-package")
async def generate_package(request: PackageGenerationRequest):
    """生成完整上架包"""
    try:
        package = package_service.generate_package(
            product_id=request.product_id,
            product_info=request.product_info
        )
        knowledge_storage.save_listing_package(package)
        return package.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成上架包失败: {e}")


# 获取所有上架包API
@app.get("/api/listing/packages")
async def get_listing_packages():
    """获取所有上架包"""
    try:
        packages = knowledge_storage.load_listing_packages()
        return packages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取上架包列表失败: {e}")


# 获取指定上架包API
@app.get("/api/listing/package/{package_id}")
async def get_listing_package(package_id: str):
    """获取指定上架包"""
    try:
        package = knowledge_storage.load_listing_package(package_id)
        if package:
            return package
        else:
            raise HTTPException(status_code=404, detail="上架包不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取上架包失败: {e}")


# v0.4 详情页生成 API端点

# 详情页生成请求模型
class DetailScreenGenerationRequest(BaseModel):
    product_id: str
    product_info: Optional[Dict[str, Any]] = None


# 详情页生成API
@app.post("/api/detail/generate-9screens")
async def generate_9screens(request: DetailScreenGenerationRequest):
    """生成详情页9屏内容"""
    try:
        generation = detail_service.generate_9screens(
            product_id=request.product_id,
            product_info=request.product_info
        )
        knowledge_storage.save_detail_screen_generation(generation)
        return generation.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成详情页9屏失败: {e}")


# 获取所有详情页生成记录API
@app.get("/api/detail/9screens")
async def get_detail_screen_generations():
    """获取所有详情页生成记录"""
    try:
        generations = knowledge_storage.load_detail_screen_generations()
        return generations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取详情页生成记录列表失败: {e}")


# 获取指定详情页生成记录API
@app.get("/api/detail/9screen/{generation_id}")
async def get_detail_screen_generation(generation_id: str):
    """获取指定详情页生成记录"""
    try:
        generation = knowledge_storage.load_detail_screen_generation(generation_id)
        if generation:
            return generation
        else:
            raise HTTPException(status_code=404, detail="详情页生成记录不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取详情页生成记录失败: {e}")


# v0.4 phase 2: 内容生成API

# 短视频脚本生成请求模型
class VideoScriptGenerationRequest(BaseModel):
    product_id: str
    package_id: Optional[str] = None
    detail_generation_id: Optional[str] = None
    product_info: Optional[Dict[str, Any]] = None
    platform: str = "douyin"
    duration_seconds: int = 30


# 生成短视频脚本API
@app.post("/api/content/generate-video-script")
async def generate_video_script(request: VideoScriptGenerationRequest):
    """生成短视频脚本"""
    try:
        generation = content_service.generate_video_script(
            product_id=request.product_id,
            platform=request.platform,
            duration_seconds=request.duration_seconds,
            package_id=request.package_id,
            detail_generation_id=request.detail_generation_id,
            product_info=request.product_info
        )
        knowledge_storage.save_video_script_generation(generation)
        return generation.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成短视频脚本失败: {e}")


# 获取所有短视频脚本生成记录API
@app.get("/api/content/video-scripts")
async def get_video_script_generations():
    """获取所有短视频脚本生成记录"""
    try:
        generations = knowledge_storage.load_video_script_generations()
        return generations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取短视频脚本生成记录列表失败: {e}")


# 获取指定短视频脚本生成记录API
@app.get("/api/content/video-script/{generation_id}")
async def get_video_script_generation(generation_id: str):
    """获取指定短视频脚本生成记录"""
    try:
        generation = knowledge_storage.load_video_script_generation(generation_id)
        if generation:
            return generation
        else:
            raise HTTPException(status_code=404, detail="短视频脚本生成记录不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取短视频脚本生成记录失败: {e}")


# 小红书文案生成请求模型
class XiaohongshuGenerationRequest(BaseModel):
    product_id: str
    package_id: Optional[str] = None
    detail_generation_id: Optional[str] = None
    product_info: Optional[Dict[str, Any]] = None
    style: str = "种草风"


# 生成小红书文案API
@app.post("/api/content/generate-xiaohongshu")
async def generate_xiaohongshu_note(request: XiaohongshuGenerationRequest):
    """生成小红书文案"""
    try:
        generation = content_service.generate_xiaohongshu_note(
            product_id=request.product_id,
            style=request.style,
            package_id=request.package_id,
            detail_generation_id=request.detail_generation_id,
            product_info=request.product_info
        )
        knowledge_storage.save_xiaohongshu_generation(generation)
        return generation.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成小红书文案失败: {e}")


# 获取所有小红书文案生成记录API
@app.get("/api/content/xiaohongshu-notes")
async def get_xiaohongshu_generations():
    """获取所有小红书文案生成记录"""
    try:
        generations = knowledge_storage.load_xiaohongshu_generations()
        return generations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取小红书文案生成记录列表失败: {e}")


# 获取指定小红书文案生成记录API
@app.get("/api/content/xiaohongshu-note/{generation_id}")
async def get_xiaohongshu_generation(generation_id: str):
    """获取指定小红书文案生成记录"""
    try:
        generation = knowledge_storage.load_xiaohongshu_generation(generation_id)
        if generation:
            return generation
        else:
            raise HTTPException(status_code=404, detail="小红书文案生成记录不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取小红书文案生成记录失败: {e}")


# v0.5: Agent任务中心API

# 任务创建请求模型
class TaskCreateRequest(BaseModel):
    original_request: str
    product_id: Optional[str] = None
    related_package_id: Optional[str] = None
    priority: str = "medium"


# 创建任务API
@app.post("/api/tasks/create")
async def create_task(request: TaskCreateRequest):
    """创建任务并自动拆解步骤"""
    try:
        task = task_service.create_task(
            original_request=request.original_request,
            product_id=request.product_id,
            related_package_id=request.related_package_id,
            priority=request.priority
        )
        knowledge_storage.save_task(task)
        return task.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建任务失败: {e}")


# 获取所有任务API
@app.get("/api/tasks")
async def get_tasks():
    """获取所有任务历史"""
    try:
        tasks = knowledge_storage.load_tasks()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务列表失败: {e}")


# 获取指定任务API
@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    """获取指定任务"""
    try:
        task = knowledge_storage.load_task(task_id)
        if task:
            return task
        else:
            raise HTTPException(status_code=404, detail="任务不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务失败: {e}")


# 任务状态更新请求模型
class TaskStatusUpdateRequest(BaseModel):
    status: str


# 更新任务状态API
@app.post("/api/tasks/{task_id}/status")
async def update_task_status(task_id: str, request: TaskStatusUpdateRequest):
    """更新任务状态"""
    try:
        # 验证状态合法性
        if not task_service.validate_task_status(request.status):
            raise HTTPException(status_code=400, detail=f"非法任务状态: {request.status}")
        success = knowledge_storage.update_task_status(task_id, request.status)
        if success:
            return {"success": True, "message": "任务状态更新成功"}
        else:
            raise HTTPException(status_code=404, detail="任务不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新任务状态失败: {e}")


# 人工确认请求模型
class TaskConfirmationRequest(BaseModel):
    confirmed: bool
    notes: Optional[str] = None


# 记录人工确认API
@app.post("/api/tasks/{task_id}/confirm")
async def confirm_task(task_id: str, request: TaskConfirmationRequest):
    """记录人工确认"""
    try:
        success = knowledge_storage.record_human_confirmation(
            task_id=task_id,
            confirmed=request.confirmed,
            notes=request.notes
        )
        if success:
            return {"success": True, "message": "人工确认记录成功"}
        else:
            raise HTTPException(status_code=404, detail="任务不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"记录人工确认失败: {e}")


# v0.6: 验收中心API

# 任务检查请求模型
class TaskCheckRequest(BaseModel):
    task_data: Dict[str, Any]


# 检查任务API
@app.post("/api/acceptance/check-task")
async def check_task(request: TaskCheckRequest):
    """检查指定任务是否合规"""
    try:
        report = acceptance_service.check_task(request.task_data)
        knowledge_storage.save_acceptance_report(report)
        return report.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检查任务失败: {e}")


# 上架包检查请求模型
class PackageCheckRequest(BaseModel):
    package_data: Dict[str, Any]


# 检查上架包API
@app.post("/api/acceptance/check-package")
async def check_package(request: PackageCheckRequest):
    """检查指定上架包是否字段完整"""
    try:
        report = acceptance_service.check_package(request.package_data)
        knowledge_storage.save_acceptance_report(report)
        return report.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检查上架包失败: {e}")


# 风险检查请求模型
class RiskCheckRequest(BaseModel):
    text: str


# 检查高风险动作API
@app.post("/api/acceptance/check-risk")
async def check_risk(request: RiskCheckRequest):
    """检查文本或任务内容是否包含高风险动作"""
    try:
        result = acceptance_service.check_risk(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检查高风险动作失败: {e}")


# 获取所有验收报告API
@app.get("/api/acceptance/reports")
async def get_acceptance_reports():
    """读取历史验收报告"""
    try:
        reports = knowledge_storage.load_acceptance_reports()
        return reports
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取验收报告列表失败: {e}")


# 获取指定验收报告API
@app.get("/api/acceptance/report/{report_id}")
async def get_acceptance_report(report_id: str):
    """读取指定验收报告"""
    try:
        report = knowledge_storage.load_acceptance_report(report_id)
        if report:
            return report
        else:
            raise HTTPException(status_code=404, detail="验收报告不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取验收报告失败: {e}")


# v0.7: 工具中心API

# 获取所有工具API
@app.get("/api/tools")
async def get_tools():
    """读取所有工具"""
    try:
        tools = tool_service.get_tools()
        return tools
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工具列表失败: {e}")


# 获取所有工具计划API (必须在 /api/tools/{tool_id} 之前)
@app.get("/api/tools/plans")
async def get_tool_plans():
    """读取历史工具计划"""
    try:
        plans = knowledge_storage.load_tool_plans()
        return plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工具计划列表失败: {e}")


# 获取指定工具API
@app.get("/api/tools/{tool_id}")
async def get_tool(tool_id: str):
    """读取指定工具"""
    try:
        tool = tool_service.get_tool(tool_id)
        if tool:
            return tool
        else:
            raise HTTPException(status_code=404, detail="工具不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工具失败: {e}")


# 工具推荐请求模型
class ToolSuggestRequest(BaseModel):
    request: str


# 一句话任务推荐工具API
@app.post("/api/tools/suggest")
async def suggest_tools(request: ToolSuggestRequest):
    """根据一句话任务推荐工具"""
    try:
        tools = tool_service.suggest_tools(request.request)
        return tools
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推荐工具失败: {e}")


# 根据任务推荐工具请求模型
class ToolSuggestForTaskRequest(BaseModel):
    task_id: str


# 根据任务推荐工具API
@app.post("/api/tools/suggest-for-task")
async def suggest_tools_for_task(request: ToolSuggestForTaskRequest):
    """根据task_id推荐工具"""
    try:
        tools = tool_service.suggest_tools_for_task(request.task_id)
        return tools
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推荐工具失败: {e}")


# 工具计划生成请求模型
class ToolPlanRequest(BaseModel):
    original_request: str
    task_id: Optional[str] = None


# 生成工具调用计划API
@app.post("/api/tools/plan")
async def generate_tool_plan(request: ToolPlanRequest):
    """生成工具调用计划"""
    try:
        plan = tool_service.generate_tool_plan(request.original_request, request.task_id)
        knowledge_storage.save_tool_plan(plan)
        return plan.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成工具计划失败: {e}")


# 获取所有工具计划API
@app.get("/api/tools/plans")
async def get_tool_plans():
    """读取历史工具计划"""
    try:
        plans = knowledge_storage.load_tool_plans()
        return plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工具计划列表失败: {e}")


# 获取指定工具计划API
@app.get("/api/tools/plan/{plan_id}")
async def get_tool_plan(plan_id: str):
    """读取指定工具计划"""
    try:
        plan = knowledge_storage.load_tool_plan(plan_id)
        if plan:
            return plan
        else:
            raise HTTPException(status_code=404, detail="工具计划不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工具计划失败: {e}")


# ============ 工作流中心API (v0.8) ============

# Pydantic模型
class WorkflowCreateRequest(BaseModel):
    original_request: str

class WorkflowStatusUpdateRequest(BaseModel):
    status: str

class StepStatusUpdateRequest(BaseModel):
    status: str
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class WorkflowConfirmRequest(BaseModel):
    confirmed_by: str


# 创建工作流API
@app.post("/api/workflows/create")
async def create_workflow(request: WorkflowCreateRequest):
    """创建工作流"""
    try:
        workflow = workflow_service.create_workflow(request.original_request)
        return workflow.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建工作流失败: {e}")


# 获取所有工作流API
@app.get("/api/workflows")
async def get_workflows():
    """读取所有工作流"""
    try:
        workflows = workflow_service.get_workflows()
        return workflows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工作流列表失败: {e}")


# 获取指定工作流API
@app.get("/api/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    """读取指定工作流"""
    try:
        workflow = workflow_service.get_workflow(workflow_id)
        if workflow:
            return workflow
        else:
            raise HTTPException(status_code=404, detail="工作流不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取工作流失败: {e}")


# 更新工作流状态API
@app.post("/api/workflows/{workflow_id}/status")
async def update_workflow_status(workflow_id: str, request: WorkflowStatusUpdateRequest):
    """更新工作流状态"""
    try:
        workflow = workflow_service.update_workflow_status(workflow_id, request.status)
        if workflow:
            return workflow
        else:
            raise HTTPException(status_code=404, detail="工作流不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新工作流状态失败: {e}")


# 更新步骤状态API
@app.post("/api/workflows/{workflow_id}/step/{step_number}/status")
async def update_step_status(workflow_id: str, step_number: int, request: StepStatusUpdateRequest):
    """更新步骤状态"""
    try:
        workflow = workflow_service.update_step_status(
            workflow_id,
            step_number,
            request.status,
            request.result,
            request.error_message
        )
        if workflow:
            return workflow
        else:
            raise HTTPException(status_code=404, detail="工作流不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新步骤状态失败: {e}")


# 确认工作流API
@app.post("/api/workflows/{workflow_id}/confirm")
async def confirm_workflow(workflow_id: str, request: WorkflowConfirmRequest):
    """确认工作流（人工确认）"""
    try:
        workflow = workflow_service.confirm_workflow(workflow_id, request.confirmed_by)
        if workflow:
            return workflow
        else:
            raise HTTPException(status_code=404, detail="工作流不存在或不需要确认")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"确认工作流失败: {e}")


# ============ 日志中心API (v0.9) ============

# Pydantic模型
class LogCreateRequest(BaseModel):
    log_type: str
    source_module: str
    source_id: Optional[str] = None
    action: str
    status: str
    message: str
    risk_level: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


# 创建日志API
@app.post("/api/logs/create")
async def create_log(request: LogCreateRequest):
    """创建日志"""
    try:
        log = log_service.create_log(
            log_type=request.log_type,
            source_module=request.source_module,
            source_id=request.source_id,
            action=request.action,
            status=request.status,
            message=request.message,
            risk_level=request.risk_level,
            details=request.details
        )
        return log.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建日志失败: {e}")


# 获取所有日志API
@app.get("/api/logs")
async def get_logs():
    """读取所有日志"""
    try:
        logs = log_service.get_logs()
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取日志列表失败: {e}")


# 获取指定日志API
@app.get("/api/logs/{log_id}")
async def get_log(log_id: str):
    """读取指定日志"""
    try:
        log = log_service.get_log(log_id)
        if log:
            return log
        else:
            raise HTTPException(status_code=404, detail="日志不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取日志失败: {e}")


# 按类型获取日志API
@app.get("/api/logs/type/{log_type}")
async def get_logs_by_type(log_type: str):
    """按类型读取日志"""
    try:
        logs = log_service.get_logs_by_type(log_type)
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"按类型获取日志失败: {e}")


# ============ API供应商中心API (v1.1) ============

# Pydantic模型
class ProviderCreateRequest(BaseModel):
    provider_name: str
    provider_type: str
    model_name: Optional[str] = None
    api_base_url: Optional[str] = None
    api_key_placeholder: Optional[str] = None
    cost_level: str
    risk_level: str
    daily_limit: int
    monthly_limit: int
    unit_cost_estimate: float
    supported_features: List[str]
    fallback_provider_id: Optional[str] = None


class ProviderQuotaRequest(BaseModel):
    daily_limit: int
    monthly_limit: int


class ProviderEstimateCostRequest(BaseModel):
    provider_id: str
    feature_name: str
    estimated_units: int


class ProviderCheckQuotaRequest(BaseModel):
    provider_id: str
    estimated_units: int


class ProviderMockCallRequest(BaseModel):
    provider_id: str
    feature_name: str
    request_summary: str
    estimated_units: int


# 获取所有供应商API
@app.get("/api/providers")
async def get_providers():
    """读取所有API供应商"""
    try:
        providers = api_provider_service.get_providers()
        return providers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取供应商列表失败: {e}")


# 获取调用记录API
@app.get("/api/providers/calls")
async def get_call_records():
    """读取调用记录"""
    try:
        call_records = api_provider_service.get_call_records()
        return call_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取调用记录失败: {e}")


# 获取指定调用记录API
@app.get("/api/providers/calls/{call_id}")
async def get_call_record(call_id: str):
    """读取指定调用记录"""
    try:
        call_record = api_provider_service.get_call_record(call_id)
        if call_record:
            return call_record
        else:
            raise HTTPException(status_code=404, detail="调用记录不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取调用记录失败: {e}")


# 创建供应商API
@app.post("/api/providers/create")
async def create_provider(request: ProviderCreateRequest):
    """创建供应商配置"""
    try:
        provider = api_provider_service.create_provider(
            provider_name=request.provider_name,
            provider_type=request.provider_type,
            model_name=request.model_name,
            api_base_url=request.api_base_url,
            api_key_placeholder=request.api_key_placeholder,
            cost_level=request.cost_level,
            risk_level=request.risk_level,
            daily_limit=request.daily_limit,
            monthly_limit=request.monthly_limit,
            unit_cost_estimate=request.unit_cost_estimate,
            supported_features=request.supported_features,
            fallback_provider_id=request.fallback_provider_id
        )
        return provider
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建供应商失败: {e}")


# 估算成本API
@app.post("/api/providers/estimate-cost")
async def estimate_cost(request: ProviderEstimateCostRequest):
    """估算调用成本"""
    try:
        result = api_provider_service.estimate_cost(
            provider_id=request.provider_id,
            feature_name=request.feature_name,
            estimated_units=request.estimated_units
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"估算成本失败: {e}")


# 检查额度API
@app.post("/api/providers/check-quota")
async def check_quota(request: ProviderCheckQuotaRequest):
    """检查某个调用是否超出额度"""
    try:
        result = api_provider_service.check_quota(
            provider_id=request.provider_id,
            estimated_units=request.estimated_units
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检查额度失败: {e}")


# 模拟调用API
@app.post("/api/providers/mock-call")
async def mock_call(request: ProviderMockCallRequest):
    """模拟一次API调用（不真实调用外部API）"""
    try:
        result = api_provider_service.mock_call(
            provider_id=request.provider_id,
            feature_name=request.feature_name,
            request_summary=request.request_summary,
            estimated_units=request.estimated_units
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模拟调用失败: {e}")


# 获取指定供应商API
@app.get("/api/providers/{provider_id}")
async def get_provider(provider_id: str):
    """读取指定供应商"""
    try:
        provider = api_provider_service.get_provider(provider_id)
        if provider:
            return provider
        else:
            raise HTTPException(status_code=404, detail="供应商不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取供应商失败: {e}")


# 启用供应商API
@app.post("/api/providers/{provider_id}/enable")
async def enable_provider(provider_id: str):
    """启用供应商"""
    try:
        provider = api_provider_service.enable_provider(provider_id)
        if provider:
            return provider
        else:
            raise HTTPException(status_code=404, detail="供应商不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启用供应商失败: {e}")


# 禁用供应商API
@app.post("/api/providers/{provider_id}/disable")
async def disable_provider(provider_id: str):
    """禁用供应商"""
    try:
        provider = api_provider_service.disable_provider(provider_id)
        if provider:
            return provider
        else:
            raise HTTPException(status_code=404, detail="供应商不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"禁用供应商失败: {e}")


# 设置额度API
@app.post("/api/providers/{provider_id}/quota")
async def set_provider_quota(provider_id: str, request: ProviderQuotaRequest):
    """设置每日/月度额度"""
    try:
        provider = api_provider_service.set_quota(
            provider_id=provider_id,
            daily_limit=request.daily_limit,
            monthly_limit=request.monthly_limit
        )
        if provider:
            return provider
        else:
            raise HTTPException(status_code=404, detail="供应商不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"设置额度失败: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
