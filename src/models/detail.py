"""
产品B v0.4 - 详情页数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class DetailScreen:
    """详情页单屏内容"""
    screen_number: int
    screen_title: str
    core_purpose: str
    copywriting: str
    layout_suggestion: str
    ai_image_prompt_cn: str
    ecommerce_design_notes: str


@dataclass
class DetailScreenGeneration:
    """详情页9屏生成记录"""
    id: str
    product_id: str
    screens: List[DetailScreen]
    generation_method: str
    merchant_profile_id: Optional[str] = None
    keyword_library_id: Optional[str] = None
    visual_style_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "screens": [self._screen_to_dict(screen) for screen in self.screens],
            "generation_method": self.generation_method,
            "merchant_profile_id": self.merchant_profile_id,
            "keyword_library_id": self.keyword_library_id,
            "visual_style_id": self.visual_style_id,
            "created_at": self.created_at.isoformat()
        }

    def _screen_to_dict(self, screen: DetailScreen):
        """屏幕转换为字典"""
        return {
            "screen_number": screen.screen_number,
            "screen_title": screen.screen_title,
            "core_purpose": screen.core_purpose,
            "copywriting": screen.copywriting,
            "layout_suggestion": screen.layout_suggestion,
            "ai_image_prompt_cn": screen.ai_image_prompt_cn,
            "ecommerce_design_notes": screen.ecommerce_design_notes
        }
