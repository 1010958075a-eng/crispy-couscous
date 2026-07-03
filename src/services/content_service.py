"""
产品B v0.4 - 内容生成服务
"""

import uuid
from typing import List, Optional, Dict, Any
from models.content import (
    VideoScriptScene,
    VideoScriptGeneration,
    XiaohongshuNote
)
from .knowledge_storage import KnowledgeStorage


class ContentService:
    """内容生成服务"""
    
    def __init__(self, knowledge_storage: KnowledgeStorage):
        self.knowledge_storage = knowledge_storage
    
    def generate_video_script(
        self,
        product_id: str,
        platform: str = "douyin",
        duration_seconds: int = 30,
        package_id: Optional[str] = None,
        detail_generation_id: Optional[str] = None,
        product_info: Optional[Dict[str, Any]] = None
    ) -> VideoScriptGeneration:
        """生成短视频脚本"""
        
        # 获取产品信息
        product_knowledge = self._get_product_knowledge(product_id)
        
        # 如果提供了package_id，优先使用上架包信息
        if package_id:
            package = self._get_listing_package(package_id)
            if package:
                product_info = self._extract_product_info_from_package(package)
        
        # 如果提供了detail_generation_id，结合详情页内容
        detail_content = None
        if detail_generation_id:
            detail_content = self._get_detail_generation(detail_generation_id)
        
        # 提取基础信息
        product_name = product_info.get("product_name", product_knowledge.product_name if product_knowledge else "产品")
        category = product_info.get("category", product_knowledge.category if product_knowledge else "服装")
        selling_points = product_info.get("selling_points", product_knowledge.selling_points if product_knowledge else [])
        target_audience = product_info.get("target_audience", product_knowledge.target_audience if product_knowledge else "25-35岁")
        material = product_info.get("material", product_knowledge.material if product_knowledge else "优质材质")
        style = product_info.get("style", product_knowledge.style if product_knowledge else "简约")
        
        # 生成脚本
        script_title = f"{product_name}·{platform}短视频"
        core_selling_points = selling_points[:3] if len(selling_points) > 3 else selling_points
        
        # 生成场景
        scenes = self._generate_video_scenes(
            product_name=product_name,
            category=category,
            selling_points=selling_points,
            target_audience=target_audience,
            material=material,
            style=style,
            platform=platform,
            detail_content=detail_content
        )
        
        return VideoScriptGeneration(
            generation_id=str(uuid.uuid4()),
            product_id=product_id,
            platform=platform,
            duration_seconds=duration_seconds,
            script_title=script_title,
            target_audience=target_audience,
            core_selling_points=core_selling_points,
            scenes=scenes,
            package_id=package_id,
            detail_generation_id=detail_generation_id
        )
    
    def _generate_video_scenes(
        self,
        product_name: str,
        category: str,
        selling_points: List[str],
        target_audience: str,
        material: str,
        style: str,
        platform: str,
        detail_content: Optional[Any] = None
    ) -> List[VideoScriptScene]:
        """生成短视频场景"""
        
        scenes = []
        
        # 场景1: 0-3秒 痛点/吸引注意
        scenes.append(VideoScriptScene(
            scene_number=1,
            duration="0-3秒",
            shot_type="特写",
            visual_content=f"{target_audience}使用{category}的痛点场景，快速切换",
            voiceover=f"{target_audience}的烦恼找到了吗？",
            subtitle="还在为这些问题烦恼吗？",
            product_focus="产品尚未出现",
            shooting_notes="快节奏，抓住注意力"
        ))
        
        # 场景2: 3-8秒 产品出现
        scenes.append(VideoScriptScene(
            scene_number=2,
            duration="3-8秒",
            shot_type="中景",
            visual_content=f"{product_name}产品特写，{style}风格，产品居中",
            voiceover=f"这款{product_name}来了！",
            subtitle=f"{product_name}登场",
            product_focus="产品主体",
            shooting_notes="清晰展示产品，突出质感"
        ))
        
        # 场景3: 8-15秒 核心卖点
        scenes.append(VideoScriptScene(
            scene_number=3,
            duration="8-15秒",
            shot_type="近景+特写",
            visual_content=f"快速展示{selling_points[0] if selling_points else '核心卖点'}功能特写",
            voiceover=f"{'、'.join(selling_points[:2])}，让你心动不已",
            subtitle=f"{'、'.join(selling_points[:2])}",
            product_focus="产品功能点",
            shooting_notes="突出核心卖点，节奏紧凑"
        ))
        
        # 场景4: 15-22秒 使用场景
        scenes.append(VideoScriptScene(
            scene_number=4,
            duration="15-22秒",
            shot_type="全景",
            visual_content=f"{target_audience}在生活场景中使用{product_name}，{style}风格",
            voiceover=f"{target_audience}日常使用，舒适自在",
            subtitle="日常使用场景",
            product_focus="产品与用户互动",
            shooting_notes="真实场景，贴近生活"
        ))
        
        # 场景5: 22-27秒 信任/对比
        scenes.append(VideoScriptScene(
            scene_number=5,
            duration="22-27秒",
            shot_type="中景",
            visual_content=f"{material}材质特写，品质展示",
            voiceover=f"精选{material}，品质保证",
            subtitle="品质保证",
            product_focus="产品材质细节",
            shooting_notes="展示材质细节，建立信任"
        ))
        
        # 场景6: 27-30秒 行动引导
        scenes.append(VideoScriptScene(
            scene_number=6,
            duration="27-30秒",
            shot_type="特写",
            visual_content=f"{product_name}产品特写+品牌Logo",
            voiceover=f"立即下单，体验{product_name}！",
            subtitle="立即下单",
            product_focus="产品+品牌",
            shooting_notes="行动引导，促进转化"
        ))
        
        return scenes
    
    def generate_xiaohongshu_note(
        self,
        product_id: str,
        style: str = "种草风",
        package_id: Optional[str] = None,
        detail_generation_id: Optional[str] = None,
        product_info: Optional[Dict[str, Any]] = None
    ) -> XiaohongshuNote:
        """生成小红书文案"""
        
        # 获取产品信息
        product_knowledge = self._get_product_knowledge(product_id)
        
        # 如果提供了package_id，优先使用上架包信息
        if package_id:
            package = self._get_listing_package(package_id)
            if package:
                product_info = self._extract_product_info_from_package(package)
        
        # 如果提供了detail_generation_id，结合详情页内容
        detail_content = None
        if detail_generation_id:
            detail_content = self._get_detail_generation(detail_generation_id)
        
        # 提取基础信息
        product_name = product_info.get("product_name", product_knowledge.product_name if product_knowledge else "产品")
        category = product_info.get("category", product_knowledge.category if product_knowledge else "服装")
        selling_points = product_info.get("selling_points", product_knowledge.selling_points if product_knowledge else [])
        target_audience = product_info.get("target_audience", product_knowledge.target_audience if product_knowledge else "25-35岁")
        material = product_info.get("material", product_knowledge.material if product_knowledge else "优质材质")
        style_desc = product_info.get("style", product_knowledge.style if product_knowledge else "简约")
        
        # 生成文案
        note_title = f"{product_name}，{target_audience}必备！"
        opening_hook = f"{target_audience}姐妹们，这款{product_name}真的太好用了！"
        
        # 生成内容
        content = self._generate_xiaohongshu_content(
            product_name=product_name,
            category=category,
            selling_points=selling_points,
            target_audience=target_audience,
            material=material,
            style_desc=style_desc
        )
        
        # 用户痛点
        user_pain_points = self._generate_user_pain_points(category, target_audience)
        
        # 场景推荐
        scene_recommendations = self._generate_scene_recommendations(category, style_desc)
        
        # 标签
        tags = self._generate_tags(category, style_desc, target_audience)
        
        # 合规说明
        compliance_notes = "本内容为产品推荐，不构成医疗建议，使用前请仔细阅读产品说明"
        
        return XiaohongshuNote(
            generation_id=str(uuid.uuid4()),
            product_id=product_id,
            note_title=note_title,
            opening_hook=opening_hook,
            content=content,
            selling_points=selling_points,
            user_pain_points=user_pain_points,
            scene_recommendations=scene_recommendations,
            tags=tags,
            compliance_notes=compliance_notes,
            package_id=package_id,
            detail_generation_id=detail_generation_id
        )
    
    def _generate_xiaohongshu_content(
        self,
        product_name: str,
        category: str,
        selling_points: List[str],
        target_audience: str,
        material: str,
        style_desc: str
    ) -> str:
        """生成小红书正文内容"""
        
        content = f"""
姐妹们，今天要给你们推荐一款超赞的{product_name}！✨

作为一个{target_audience}，我一直在找一款合适的{category}，直到遇到了它。

{selling_points[0] if selling_points else '使用体验'}真的太棒了！{selling_points[1] if len(selling_points) > 1 else '整体设计'}也很贴心。

精选{material}材质，{style_desc}风格，日常穿着很舒适。

不管是上班通勤还是周末休闲，都能轻松驾驭。

真心推荐给需要的姐妹们！💕
"""
        return content.strip()
    
    def _generate_user_pain_points(self, category: str, target_audience: str) -> List[str]:
        """生成用户痛点"""
        return [
            f"{target_audience}在选择{category}时的困扰",
            f"传统{category}存在的问题",
            f"日常使用中的不便"
        ]
    
    def _generate_scene_recommendations(self, category: str, style_desc: str) -> List[str]:
        """生成场景推荐"""
        return [
            f"日常通勤，{style_desc}风格",
            f"周末休闲，轻松搭配",
            f"约会聚会，气质出众"
        ]
    
    def _generate_tags(self, category: str, style_desc: str, target_audience: str) -> List[str]:
        """生成标签"""
        return [
            f"#{category}",
            f"#{style_desc}",
            f"#{target_audience}",
            "#好物推荐",
            "#种草"
        ]
    
    def _get_product_knowledge(self, product_id: str):
        """从产品知识库获取产品信息"""
        products = self.knowledge_storage.load_product_knowledge()
        for product in products:
            if product.id == product_id:
                return product
        return None
    
    def _get_listing_package(self, package_id: str):
        """从上架包库获取上架包信息"""
        packages = self.knowledge_storage.load_listing_packages()
        for package in packages:
            if package.id == package_id:
                return package
        return None
    
    def _get_detail_generation(self, generation_id: str):
        """从详情页生成记录获取详情页内容"""
        generations = self.knowledge_storage.load_detail_screen_generations()
        for generation in generations:
            if generation.id == generation_id:
                return generation
        return None
    
    def _extract_product_info_from_package(self, package) -> Dict[str, Any]:
        """从上架包提取产品信息"""
        return {
            "product_name": package.product_name,
            "category": package.category,
            "selling_points": package.selling_points,
            "target_audience": package.target_audience,
            "material": package.material,
            "style": package.style
        }
