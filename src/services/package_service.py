"""
产品B v0.3 - 上架包服务
"""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from models.listing import ListingPackage
from services import KnowledgeStorage
from services.title_service import TitleService
from services.keyword_service import KeywordService
from services.image_prompt_service import ImagePromptService


class PackageService:
    """上架包服务"""

    def __init__(self, knowledge_storage: KnowledgeStorage = None):
        """初始化上架包服务"""
        self.knowledge_storage = knowledge_storage or KnowledgeStorage()
        self.title_service = TitleService(knowledge_storage)
        self.keyword_service = KeywordService(knowledge_storage)
        self.image_prompt_service = ImagePromptService(knowledge_storage)

    def generate_package(
        self,
        product_id: str,
        product_info: Optional[Dict[str, Any]] = None
    ) -> ListingPackage:
        """生成完整上架包"""

        # 从知识库获取数据
        product_knowledge = self._get_product_knowledge(product_id)
        merchant_profile = self.knowledge_storage.load_merchant_profile_v2()
        visual_style_library = self.knowledge_storage.load_visual_style_library()

        # 使用产品信息或从知识库获取
        if product_info is None and product_knowledge:
            product_info = product_knowledge.to_dict()

        # 生成标题
        title_generation = self.title_service.generate_titles(
            product_id=product_id,
            product_info=product_info
        )

        # 生成关键词
        keyword_generation = self.keyword_service.generate_keywords(
            product_id=product_id,
            product_info=product_info
        )

        # 生成主图提示词
        image_prompt_generation = self.image_prompt_service.generate_image_prompts(
            product_id=product_id,
            product_info=product_info
        )

        # 提取商家档案和视觉风格
        merchant_profile_dict = None
        if merchant_profile:
            merchant_profile_dict = merchant_profile.to_dict()

        visual_style_dict = None
        if visual_style_library:
            visual_style_dict = visual_style_library[0].to_dict() if visual_style_library else None

        # 生成待确认事项
        pending_review = [
            "确认标题是否符合平台规范",
            "确认关键词是否准确",
            "确认主图提示词是否需要调整",
            "确认产品信息是否完整",
            "确认视觉风格是否符合品牌调性"
        ]

        # 创建上架包
        package = ListingPackage(
            id=str(uuid.uuid4()),
            product_id=product_id,
            product_info=product_info,
            titles=title_generation.titles,
            keywords={
                "core_keywords": keyword_generation.core_keywords,
                "long_tail_keywords": keyword_generation.long_tail_keywords,
                "audience_keywords": keyword_generation.audience_keywords,
                "scenario_keywords": keyword_generation.scenario_keywords,
                "selling_point_keywords": keyword_generation.selling_point_keywords,
                "ad_keywords": keyword_generation.ad_keywords,
                "negative_keywords": keyword_generation.negative_keywords
            },
            image_prompts=image_prompt_generation.to_dict()["prompts"],
            merchant_profile=merchant_profile_dict,
            visual_style=visual_style_dict,
            pending_review=pending_review,
            created_at=datetime.now()
        )

        return package

    def _get_product_knowledge(self, product_id: str):
        """从产品知识库获取产品信息"""
        products = self.knowledge_storage.load_product_knowledge()
        for product in products:
            if product.id == product_id:
                return product
        return None
