"""
产品B v0.3 - 主图提示词生成服务
"""

from typing import List, Dict, Any, Optional
import uuid
from models.listing import ImagePrompt, ImagePromptGeneration
from services import KnowledgeStorage
from utils import find_by_id, extract_product_fields


class ImagePromptService:
    """主图提示词生成服务"""

    def __init__(self, knowledge_storage: KnowledgeStorage = None):
        """初始化主图提示词生成服务"""
        self.knowledge_storage = knowledge_storage or KnowledgeStorage()

    def generate_image_prompts(
        self,
        product_id: str,
        product_info: Optional[Dict[str, Any]] = None,
        visual_style_id: Optional[str] = None
    ) -> ImagePromptGeneration:
        """生成主图九宫格提示词"""

        # 从知识库获取数据
        product_knowledge = self._get_product_knowledge(product_id)
        visual_style_library = self.knowledge_storage.load_visual_style_library()

        # 使用产品信息或从知识库获取
        if product_info is None and product_knowledge:
            product_info = product_knowledge.to_dict()

        # 提取基础信息
        fields = extract_product_fields(product_info)
        product_name = fields["product_name"]
        category = fields["category"]
        material = fields["material"]
        style = fields["style"]
        selling_points = fields["selling_points"]

        # 提取视觉风格
        main_image_style = ""
        detail_page_style = ""
        color_tone = ""
        composition_method = ""
        ai_prompt_template = ""

        if visual_style_library:
            for vs in visual_style_library:
                main_image_style = vs.main_image_style
                detail_page_style = vs.detail_page_style
                color_tone = vs.color_tone
                composition_method = vs.composition_method
                ai_prompt_template = vs.ai_image_prompt_template
                break

        # 生成9张主图提示词
        prompts = self._generate_9_prompts(
            product_name=product_name,
            category=category,
            material=material,
            style=style,
            selling_points=selling_points,
            main_image_style=main_image_style,
            color_tone=color_tone,
            composition_method=composition_method,
            ai_prompt_template=ai_prompt_template
        )

        # 创建生成记录
        generation = ImagePromptGeneration(
            id=str(uuid.uuid4()),
            product_id=product_id,
            prompts=prompts,
            generation_method="template",
            visual_style_id=visual_style_id
        )

        return generation

    def _get_product_knowledge(self, product_id: str):
        """从产品知识库获取产品信息"""
        return find_by_id(self.knowledge_storage.load_product_knowledge(), product_id)

    def _generate_9_prompts(
        self,
        product_name: str,
        category: str,
        material: str,
        style: str,
        selling_points: List[str],
        main_image_style: str,
        color_tone: str,
        composition_method: str,
        ai_prompt_template: str
    ) -> List[ImagePrompt]:
        """生成9张主图提示词"""

        prompts = []

        # 1. 白底主图
        prompts.append(ImagePrompt(
            image_type="白底主图",
            purpose="展示产品整体外观，用于搜索主图",
            structure="纯色背景，产品居中，完整展示",
            focus="产品整体形态和核心特征",
            ai_prompt_cn=f"{product_name}白底主图，{category}，{style}风格，{color_tone}色调，居中构图，高清细节",
            ai_prompt_en=f"{product_name} white background main image, {category}, {style} style, {color_tone} tone, centered composition, high definition details",
            notes="保持产品真实质感，不要过度美化，背景干净整洁"
        ))

        # 2. 模特上身图
        prompts.append(ImagePrompt(
            image_type="模特上身图",
            purpose="展示产品上身效果，增强购买欲望",
            structure="模特上身展示，自然姿态，生活化场景",
            focus="产品上身效果和穿着舒适度",
            ai_prompt_cn=f"{product_name}模特上身图，{category}，{style}风格，自然姿态，生活场景，{color_tone}色调",
            ai_prompt_en=f"{product_name} model wearing, {category}, {style} style, natural pose, lifestyle scene, {color_tone} tone",
            notes="模特选择符合目标人群，展示真实穿着效果"
        ))

        # 3. 高级质感图
        prompts.append(ImagePrompt(
            image_type="高级质感图",
            purpose="展示产品材质和工艺细节",
            structure="特写镜头，光影效果突出质感",
            focus="材质纹理和工艺细节",
            ai_prompt_cn=f"{product_name}质感特写，{material}材质，{category}，高级质感，光影效果，细节清晰",
            ai_prompt_en=f"{product_name} texture close-up, {material} material, {category}, premium texture, lighting effects, clear details",
            notes="突出材质优势，避免过度修图"
        ))

        # 4. 材质特写图
        prompts.append(ImagePrompt(
            image_type="材质特写图",
            purpose="展示产品材质细节",
            structure="局部特写，清晰展示材质纹理",
            focus="材质纹理和触感",
            ai_prompt_cn=f"{product_name}材质特写，{material}，{category}，纹理清晰，细节丰富",
            ai_prompt_en=f"{product_name} material close-up, {material}, {category}, clear texture, rich details",
            notes="真实展示材质，不要模糊处理"
        ))

        # 5. 功能卖点图
        prompts.append(ImagePrompt(
            image_type="功能卖点图",
            purpose="突出产品核心卖点",
            structure="卖点场景化展示，图文结合",
            focus="核心功能和使用场景",
            ai_prompt_cn=f"{product_name}功能展示，{selling_points[0] if selling_points else ''}，{category}，使用场景，{style}风格",
            ai_prompt_en=f"{product_name} function display, {selling_points[0] if selling_points else ''}, {category}, usage scenario, {style} style",
            notes="卖点清晰易懂，场景真实可信"
        ))

        # 6. 对比图
        prompts.append(ImagePrompt(
            image_type="对比图",
            purpose="展示产品优势对比",
            structure="前后对比或与其他产品对比",
            focus="产品优势明显",
            ai_prompt_cn=f"{product_name}对比图，{category}，优势展示，{style}风格",
            ai_prompt_en=f"{product_name} comparison image, {category}, advantage display, {style} style",
            notes="对比真实可信，不要夸大"
        ))

        # 7. 场景生活图
        prompts.append(ImagePrompt(
            image_type="场景生活图",
            purpose="展示产品在生活中的应用",
            structure="生活场景，产品融入环境",
            focus="产品使用场景和生活方式",
            ai_prompt_cn=f"{product_name}生活场景，{category}，{style}风格，{color_tone}色调，生活化",
            ai_prompt_en=f"{product_name} lifestyle scene, {category}, {style} style, {color_tone} tone, lifestyle",
            notes="场景贴近目标人群生活"
        ))

        # 8. 色卡图
        prompts.append(ImagePrompt(
            image_type="色卡图",
            purpose="展示产品颜色选择",
            structure="产品多色展示，色卡式排列",
            focus="颜色选择和搭配",
            ai_prompt_cn=f"{product_name}色卡图，{category}，多色展示，{color_tone}色调",
            ai_prompt_en=f"{product_name} color card, {category}, multi-color display, {color_tone} tone",
            notes="颜色真实准确"
        ))

        # 9. 尺码/洗护图
        prompts.append(ImagePrompt(
            image_type="尺码/洗护图",
            purpose="展示尺码信息和洗护建议",
            structure="尺码表或洗护图标示",
            focus="尺码准确性和洗护方法",
            ai_prompt_cn=f"{product_name}尺码洗护图，{category}，尺码信息，洗护建议",
            ai_prompt_en=f"{product_name} size care image, {category}, size information, care instructions",
            notes="信息清晰准确"
        ))

        return prompts
