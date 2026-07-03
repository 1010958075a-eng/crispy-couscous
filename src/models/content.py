"""
产品B v0.4 - 内容生成数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class VideoScriptScene:
    """短视频脚本场景"""
    scene_number: int
    duration: str
    shot_type: str
    visual_content: str
    voiceover: str
    subtitle: str
    product_focus: str
    shooting_notes: str


@dataclass
class VideoScriptGeneration:
    """短视频脚本生成记录"""
    generation_id: str
    product_id: str
    platform: str
    duration_seconds: int
    script_title: str
    target_audience: str
    core_selling_points: List[str]
    scenes: List[VideoScriptScene]
    package_id: Optional[str] = None
    detail_generation_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "generation_id": self.generation_id,
            "product_id": self.product_id,
            "platform": self.platform,
            "duration_seconds": self.duration_seconds,
            "script_title": self.script_title,
            "target_audience": self.target_audience,
            "core_selling_points": self.core_selling_points,
            "scenes": [self._scene_to_dict(scene) for scene in self.scenes],
            "package_id": self.package_id,
            "detail_generation_id": self.detail_generation_id,
            "created_at": self.created_at.isoformat()
        }

    def _scene_to_dict(self, scene: VideoScriptScene):
        """场景转换为字典"""
        return {
            "scene_number": scene.scene_number,
            "duration": scene.duration,
            "shot_type": scene.shot_type,
            "visual_content": scene.visual_content,
            "voiceover": scene.voiceover,
            "subtitle": scene.subtitle,
            "product_focus": scene.product_focus,
            "shooting_notes": scene.shooting_notes
        }


@dataclass
class XiaohongshuNote:
    """小红书文案"""
    generation_id: str
    product_id: str
    note_title: str
    opening_hook: str
    content: str
    selling_points: List[str]
    user_pain_points: List[str]
    scene_recommendations: List[str]
    tags: List[str]
    compliance_notes: str
    package_id: Optional[str] = None
    detail_generation_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "generation_id": self.generation_id,
            "product_id": self.product_id,
            "note_title": self.note_title,
            "opening_hook": self.opening_hook,
            "content": self.content,
            "selling_points": self.selling_points,
            "user_pain_points": self.user_pain_points,
            "scene_recommendations": self.scene_recommendations,
            "tags": self.tags,
            "compliance_notes": self.compliance_notes,
            "package_id": self.package_id,
            "detail_generation_id": self.detail_generation_id,
            "created_at": self.created_at.isoformat()
        }
