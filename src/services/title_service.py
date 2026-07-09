"""
产品B v0.3 - 标题生成服务
"""

from typing import List, Dict, Any, Optional
import uuid
from models.listing import TitleGeneration
from services import KnowledgeStorage
from utils import find_by_id, extract_product_fields


class TitleService:
    """标题生成服务"""

    def __init__(self, knowledge_storage: KnowledgeStorage = None):
        """初始化标题生成服务"""
        self.knowledge_storage = knowledge_storage or KnowledgeStorage()

    def generate_titles(
        self,
        product_id: str,
        product_info: Optional[Dict[str, Any]] = None,
        merchant_profile_id: Optional[str] = None,
        keyword_library_id: Optional[str] = None,
        visual_style_id: Optional[str] = None
    ) -> TitleGeneration:
        """生成20个淘宝/天猫标题"""

        # 从知识库获取数据
        product_knowledge = self._get_product_knowledge(product_id)
        merchant_profile = self.knowledge_storage.load_merchant_profile_v2()
        keyword_library = self.knowledge_storage.load_keyword_library()

        # 使用产品信息或从知识库获取
        if product_info is None and product_knowledge:
            product_info = product_knowledge.to_dict()

        # 提取基础信息
        fields = extract_product_fields(product_info)
        product_name = fields["product_name"]
        category = fields["category"]
        selling_points = fields["selling_points"]
        material = fields["material"]
        target_audience = fields["target_audience"]
        style = fields["style"]

        # 提取关键词
        core_keywords = []
        if keyword_library:
            for lib in keyword_library:
                core_keywords.extend(lib.core_keywords)

        # 提取商家档案信息
        target_audience_from_profile = ""
        if merchant_profile:
            target_audience_from_profile = merchant_profile.target_audience

        # 生成20个标题
        titles = self._generate_20_titles(
            product_name=product_name,
            category=category,
            selling_points=selling_points,
            material=material,
            target_audience=target_audience or target_audience_from_profile,
            style=style,
            core_keywords=core_keywords
        )

        # 创建生成记录
        generation = TitleGeneration(
            id=str(uuid.uuid4()),
            product_id=product_id,
            titles=titles,
            generation_method="template",
            merchant_profile_id=merchant_profile_id,
            keyword_library_id=keyword_library_id,
            visual_style_id=visual_style_id
        )

        return generation

    def _get_product_knowledge(self, product_id: str):
        """从产品知识库获取产品信息"""
        return find_by_id(self.knowledge_storage.load_product_knowledge(), product_id)

    def _generate_20_titles(
        self,
        product_name: str,
        category: str,
        selling_points: List[str],
        material: str,
        target_audience: str,
        style: str,
        core_keywords: List[str]
    ) -> List[str]:
        """生成20个标题（基于模板规则）"""

        titles = []

        # 基础信息
        name = product_name if product_name else "商品"
        cat = category if category else ""
        points = selling_points if selling_points else []
        mat = material if material else ""
        audience = target_audience if target_audience else ""
        sty = style if style else ""
        keywords = core_keywords if core_keywords else []

        # 生成不同类型的标题

        # 1-5: 基础标题（类目+产品+卖点）
        if cat and name:
            titles.append(f"{cat}{name}")
            titles.append(f"{cat}{name}{points[0] if points else ''}")
            titles.append(f"{name}{cat}{points[0] if points else ''}")
            titles.append(f"{cat}{name}{mat}")
            titles.append(f"{name}{cat}{mat}")

        # 6-10: 人群定位标题
        if audience:
            titles.append(f"{audience}{name}")
            titles.append(f"{audience}{name}{points[0] if points else ''}")
            titles.append(f"{audience}{cat}{name}")
            titles.append(f"{audience}{name}{mat}")
            titles.append(f"{audience}{sty}{name}")

        # 11-15: 风格定位标题
        if sty:
            titles.append(f"{sty}{name}")
            titles.append(f"{sty}{name}{points[0] if points else ''}")
            titles.append(f"{sty}{cat}{name}")
            titles.append(f"{sty}{name}{mat}")
            titles.append(f"{name}{sty}")

        # 16-20: 关键词组合标题
        if keywords:
            for i, keyword in enumerate(keywords[:5]):
                titles.append(f"{keyword}{name}")
        else:
            # 如果没有关键词，使用卖点补充
            for i, point in enumerate(points[:5]):
                titles.append(f"{point}{name}")

        # 确保正好20个标题
        while len(titles) < 20:
            titles.append(f"{name}{points[len(titles) % len(points)] if points else ''}")

        # 去重并限制为20个
        titles = list(dict.fromkeys(titles))[:20]

        return titles
