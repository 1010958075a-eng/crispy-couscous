"""
产品B v0.4 - 详情页生成服务
"""

from typing import List, Dict, Any, Optional
import uuid
from models.detail import DetailScreen, DetailScreenGeneration
from services import KnowledgeStorage


class DetailService:
    """详情页生成服务"""

    def __init__(self, knowledge_storage: KnowledgeStorage = None):
        """初始化详情页生成服务"""
        self.knowledge_storage = knowledge_storage or KnowledgeStorage()

    def generate_9screens(
        self,
        product_id: str,
        product_info: Optional[Dict[str, Any]] = None
    ) -> DetailScreenGeneration:
        """生成详情页9屏内容"""

        # 从知识库获取数据
        product_knowledge = self._get_product_knowledge(product_id)
        keyword_library = self.knowledge_storage.load_keyword_library()
        visual_style_library = self.knowledge_storage.load_visual_style_library()

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

        # 提取关键词
        core_keywords = []
        if keyword_library:
            for lib in keyword_library:
                core_keywords.extend(lib.core_keywords)

        # 提取视觉风格
        color_tone = ""
        composition_method = ""
        if visual_style_library:
            for vs in visual_style_library:
                color_tone = vs.color_tone
                composition_method = vs.composition_method
                break

        # 生成9屏内容
        screens = self._generate_9_screens(
            product_name=product_name,
            category=category,
            selling_points=selling_points,
            material=material,
            target_audience=target_audience,
            style=style,
            core_keywords=core_keywords,
            color_tone=color_tone,
            composition_method=composition_method
        )

        # 创建生成记录
        generation = DetailScreenGeneration(
            id=str(uuid.uuid4()),
            product_id=product_id,
            screens=screens,
            generation_method="template"
        )

        return generation

    def _get_product_knowledge(self, product_id: str):
        """从产品知识库获取产品信息"""
        products = self.knowledge_storage.load_product_knowledge()
        for product in products:
            if product.id == product_id:
                return product
        return None

    def _generate_9_screens(
        self,
        product_name: str,
        category: str,
        selling_points: List[str],
        material: str,
        target_audience: str,
        style: str,
        core_keywords: List[str],
        color_tone: str,
        composition_method: str
    ) -> List[DetailScreen]:
        """生成9屏内容"""

        screens = []

        # 1. 首屏主视觉
        screens.append(DetailScreen(
            screen_number=1,
            screen_title="首屏主视觉",
            core_purpose="吸引眼球，展示产品核心卖点",
            copywriting=f"{product_name}·{style}风格\n{selling_points[0] if selling_points else ''}",
            layout_suggestion="产品居中，背景简洁，突出产品主体",
            ai_image_prompt_cn=f"{product_name}首屏主视觉，{category}，{style}风格，{color_tone}色调，居中构图，高清细节",
            ecommerce_design_notes="首屏3秒抓眼球，避免信息过载"
        ))

        # 2. 用户痛点
        screens.append(DetailScreen(
            screen_number=2,
            screen_title="用户痛点",
            core_purpose="击中用户痛点，引发共鸣",
            copywriting=f"{target_audience}的烦恼\n传统{category}存在的问题",
            layout_suggestion="痛点图标+文字说明，左右分栏或上下分屏",
            ai_image_prompt_cn=f"{category}用户痛点场景图，{target_audience}，{style}风格，{color_tone}色调",
            ecommerce_design_notes="痛点真实可信，不要夸大"
        ))

        # 3. 核心卖点
        screens.append(DetailScreen(
            screen_number=3,
            screen_title="核心卖点",
            core_purpose="突出产品核心优势",
            copywriting=f"核心卖点：{'、'.join(selling_points[:3])}",
            layout_suggestion="卖点图标+文字说明，网格布局",
            ai_image_prompt_cn=f"{product_name}核心卖点展示，{category}，{selling_points[0] if selling_points else ''}，{style}风格",
            ecommerce_design_notes="卖点清晰易懂，图文结合"
        ))

        # 4. 材质结构
        screens.append(DetailScreen(
            screen_number=4,
            screen_title="材质结构",
            core_purpose="展示产品材质和工艺",
            copywriting=f"精选{material}材质\n优质工艺，品质保证",
            layout_suggestion="材质特写+结构图解，突出材质优势",
            ai_image_prompt_cn=f"{product_name}材质结构图，{material}材质，{category}，特写镜头，高清细节",
            ecommerce_design_notes="真实展示材质，避免过度美化"
        ))

        # 5. 功能支撑
        screens.append(DetailScreen(
            screen_number=5,
            screen_title="功能支撑",
            core_purpose="展示产品功能特点",
            copywriting=f"功能特点\n{selling_points[0] if selling_points else ''}",
            layout_suggestion="功能场景化展示，图文结合",
            ai_image_prompt_cn=f"{product_name}功能展示图，{category}，{selling_points[0] if selling_points else ''}，{style}风格",
            ecommerce_design_notes="功能清晰，场景真实"
        ))

        # 6. 舒适体验
        screens.append(DetailScreen(
            screen_number=6,
            screen_title="舒适体验",
            core_purpose="展示产品使用体验",
            copywriting=f"舒适体验\n{selling_points[1] if len(selling_points) > 1 else selling_points[0] if selling_points else ''}",
            layout_suggestion="使用场景图+体验描述，生活化场景",
            ai_image_prompt_cn=f"{product_name}舒适体验图，{category}，{target_audience}，{style}风格，生活场景",
            ecommerce_design_notes="体验真实，场景贴近目标人群"
        ))

        # 7. 穿搭/使用场景
        screens.append(DetailScreen(
            screen_number=7,
            screen_title="穿搭/使用场景",
            core_purpose="展示产品使用场景",
            copywriting=f"穿搭建议\n{category}搭配指南",
            layout_suggestion="多场景展示，网格布局或滑动效果",
            ai_image_prompt_cn=f"{product_name}穿搭场景图，{category}，{target_audience}，{style}风格，多场景",
            ecommerce_design_notes="场景贴近目标人群生活"
        ))

        # 8. 色卡/尺码
        screens.append(DetailScreen(
            screen_number=8,
            screen_title="色卡/尺码",
            core_purpose="展示产品颜色和尺码选择",
            copywriting=f"颜色选择\n尺码信息",
            layout_suggestion="色卡式排列，尺码表清晰展示",
            ai_image_prompt_cn=f"{product_name}色卡尺码图，{category}，{color_tone}色调，清晰展示",
            ecommerce_design_notes="颜色真实准确，尺码信息清晰"
        ))

        # 9. 品牌/售后/信任背书
        screens.append(DetailScreen(
            screen_number=9,
            screen_title="品牌/售后/信任背书",
            core_purpose="建立信任，促进转化",
            copywriting=f"品质保证\n售后无忧",
            layout_suggestion="品牌Logo+售后保障+用户评价，信任背书",
            ai_image_prompt_cn=f"{category}品牌售后图，信任背书，{style}风格，{color_tone}色调",
            ecommerce_design_notes="信任背书真实可信"
        ))

        return screens
