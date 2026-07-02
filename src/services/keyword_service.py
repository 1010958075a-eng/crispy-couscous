"""
产品B v0.3 - 关键词生成服务
"""

from typing import List, Dict, Any, Optional
import uuid
from models.listing import KeywordGeneration
from services import KnowledgeStorage


class KeywordService:
    """关键词生成服务"""

    def __init__(self, knowledge_storage: KnowledgeStorage = None):
        """初始化关键词生成服务"""
        self.knowledge_storage = knowledge_storage or KnowledgeStorage()

    def generate_keywords(
        self,
        product_id: str,
        product_info: Optional[Dict[str, Any]] = None,
        keyword_library_id: Optional[str] = None
    ) -> KeywordGeneration:
        """生成关键词包"""

        # 从知识库获取数据
        product_knowledge = self._get_product_knowledge(product_id)
        keyword_library = self.knowledge_storage.load_keyword_library()

        # 使用产品信息或从知识库获取
        if product_info is None and product_knowledge:
            product_info = product_knowledge.to_dict()

        # 提取基础信息
        product_name = product_info.get("product_name", "")
        category = product_info.get("category", "")
        selling_points = product_info.get("selling_points", [])
        material = product_info.get("material", "")
        target_audience = product_info.get("target_audience", "")
        style = product_info.get("style", "")

        # 从关键词库提取关键词
        core_keywords = []
        long_tail_keywords = []
        audience_keywords = []
        scenario_keywords = []
        selling_point_keywords = []
        ad_keywords = []
        negative_keywords = []

        if keyword_library:
            for lib in keyword_library:
                # KeywordLibrary 是数据类，使用属性访问
                core_keywords.extend(lib.core_keywords)
                long_tail_keywords.extend(lib.long_tail_keywords)
                audience_keywords.extend(lib.audience_keywords)
                scenario_keywords.extend(lib.scenario_keywords)
                selling_point_keywords.extend(lib.selling_point_keywords)
                ad_keywords.extend(lib.ad_keywords)
                negative_keywords.extend(lib.negative_keywords)

        # 基于产品信息补充关键词
        if product_name:
            core_keywords.append(product_name)
        if category:
            core_keywords.append(category)
            long_tail_keywords.append(f"{category}{product_name}")
        if material:
            selling_point_keywords.append(material)
        if style:
            selling_point_keywords.append(style)

        # 去重
        core_keywords = list(set(core_keywords))
        long_tail_keywords = list(set(long_tail_keywords))
        audience_keywords = list(set(audience_keywords))
        scenario_keywords = list(set(scenario_keywords))
        selling_point_keywords = list(set(selling_point_keywords))
        ad_keywords = list(set(ad_keywords))
        negative_keywords = list(set(negative_keywords))

        # 创建生成记录
        generation = KeywordGeneration(
            id=str(uuid.uuid4()),
            product_id=product_id,
            core_keywords=core_keywords,
            long_tail_keywords=long_tail_keywords,
            audience_keywords=audience_keywords,
            scenario_keywords=scenario_keywords,
            selling_point_keywords=selling_point_keywords,
            ad_keywords=ad_keywords,
            negative_keywords=negative_keywords,
            generation_method="template",
            keyword_library_id=keyword_library_id
        )

        return generation

    def _get_product_knowledge(self, product_id: str):
        """从产品知识库获取产品信息"""
        products = self.knowledge_storage.load_product_knowledge()
        for product in products:
            if product.id == product_id:
                return product
        return None
