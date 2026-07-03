"""
产品B - 本地知识库存储模块
"""

import json
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from models import (
    LinkLearningRecord,
    TextLearningRecord,
    TableLearningRecord,
    ReviewLearningRecord,
    KnowledgeRecord,
    MerchantProfile,
    MerchantProfileV2,
    ProductKnowledge,
    CompetitorKnowledge,
    KeywordLibrary,
    VisualStyleLibrary,
    ReviewRecord
)
from models.merchant import Platform, PriceRange


class KnowledgeStorage:
    """本地知识库存储服务"""

    def __init__(self, base_path: str = None):
        """初始化存储服务"""
        if base_path is None:
            # 默认使用项目根目录下的data目录
            project_root = Path(__file__).parent.parent.parent
            self.base_path = project_root / "data"
        else:
            self.base_path = Path(base_path)

        # 创建data目录
        self.base_path.mkdir(parents=True, exist_ok=True)

        # 文件路径
        self.merchant_profile_file = self.base_path / "merchant_profile.json"
        self.knowledge_records_file = self.base_path / "knowledge_records.json"
        self.link_learning_records_file = self.base_path / "link_learning_records.json"
        self.text_learning_records_file = self.base_path / "text_learning_records.json"
        self.table_learning_records_file = self.base_path / "table_learning_records.json"
        self.review_records_file = self.base_path / "review_records.json"

        # v0.2 新增文件路径
        self.merchant_profile_v2_file = self.base_path / "merchant_profile.json"  # 复用原有文件
        self.product_knowledge_file = self.base_path / "product_knowledge.json"
        self.competitor_knowledge_file = self.base_path / "competitor_knowledge.json"
        self.keyword_library_file = self.base_path / "keyword_library.json"
        self.visual_style_library_file = self.base_path / "visual_style_library.json"
        self.review_records_v2_file = self.base_path / "review_records.json"  # 复用原有文件

        # v0.3 新增文件路径
        self.title_generations_file = self.base_path / "title_generations.json"
        self.keyword_generations_file = self.base_path / "keyword_generations.json"
        self.image_prompt_generations_file = self.base_path / "image_prompt_generations.json"
        self.listing_packages_file = self.base_path / "listing_packages.json"

        # v0.4 新增文件路径
        self.detail_screen_generations_file = self.base_path / "detail_screen_generations.json"
        self.video_script_generations_file = self.base_path / "video_script_generations.json"
        self.xiaohongshu_generations_file = self.base_path / "xiaohongshu_generations.json"

        # v0.5 新增文件路径
        self.task_center_records_file = self.base_path / "task_center_records.json"

        # v0.6 新增文件路径
        self.acceptance_reports_file = self.base_path / "acceptance_reports.json"

    def _load_json(self, file_path: Path) -> List[Dict]:
        """加载JSON文件"""
        if not file_path.exists():
            return []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载文件失败 {file_path}: {e}")
            return []

    def _save_json(self, file_path: Path, data: List[Dict]):
        """保存JSON文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存文件失败 {file_path}: {e}")

    # 商家档案
    def save_merchant_profile(self, profile: MerchantProfile):
        """保存商家档案"""
        data = profile.to_dict()
        self._save_json(self.merchant_profile_file, [data])

    def load_merchant_profile(self) -> Optional[MerchantProfile]:
        """加载商家档案"""
        data_list = self._load_json(self.merchant_profile_file)
        if not data_list:
            return None
        data = data_list[0]
        return MerchantProfile(
            id=data["id"],
            merchant_name=data["merchant_name"],
            main_category=data["main_category"],
            price_range=data["price_range"],
            positioning=data["positioning"],
            target_audience=data["target_audience"],
            platforms=data["platforms"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )

    # 知识库记录
    def save_knowledge_record(self, record: KnowledgeRecord):
        """保存知识库记录"""
        data_list = self._load_json(self.knowledge_records_file)
        data_list.append(record.to_dict())
        self._save_json(self.knowledge_records_file, data_list)

    def load_knowledge_records(self) -> List[KnowledgeRecord]:
        """加载所有知识库记录"""
        data_list = self._load_json(self.knowledge_records_file)
        records = []
        for data in data_list:
            records.append(KnowledgeRecord(
                id=data["id"],
                title=data["title"],
                content=data["content"],
                category=data["category"],
                tags=data["tags"],
                source_type=data["source_type"],
                source_id=data.get("source_id"),
                applicable_scenarios=data["applicable_scenarios"],
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"])
            ))
        return records

    def get_knowledge_by_category(self, category: str) -> List[KnowledgeRecord]:
        """按类别获取知识库记录"""
        records = self.load_knowledge_records()
        return [r for r in records if r.category == category]

    # 链接学习记录
    def save_link_learning_record(self, record: LinkLearningRecord):
        """保存链接学习记录"""
        data_list = self._load_json(self.link_learning_records_file)
        data_list.append(record.to_dict())
        self._save_json(self.link_learning_records_file, data_list)

    def load_link_learning_records(self) -> List[LinkLearningRecord]:
        """加载所有链接学习记录"""
        data_list = self._load_json(self.link_learning_records_file)
        records = []
        for data in data_list:
            records.append(LinkLearningRecord(
                id=data["id"],
                url=data["url"],
                source_platform=data["source_platform"],
                learning_target=data["learning_target"],
                notes=data.get("notes"),
                status=data["status"],
                extracted_title=data.get("extracted_title"),
                extracted_key_points=data.get("extracted_key_points", []),
                extracted_keywords=data.get("extracted_keywords", []),
                extracted_price_info=data.get("extracted_price_info"),
                page_structure=data.get("page_structure"),
                content_summary=data.get("content_summary"),
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"])
            ))
        return records

    def get_link_learning_record(self, record_id: str) -> Optional[LinkLearningRecord]:
        """获取单个链接学习记录"""
        records = self.load_link_learning_records()
        for record in records:
            if record.id == record_id:
                return record
        return None

    def update_link_learning_record(self, record: LinkLearningRecord):
        """更新链接学习记录"""
        data_list = self._load_json(self.link_learning_records_file)
        updated_list = []
        for data in data_list:
            if data["id"] == record.id:
                updated_list.append(record.to_dict())
            else:
                updated_list.append(data)
        self._save_json(self.link_learning_records_file, updated_list)

    # 文本学习记录
    def save_text_learning_record(self, record: TextLearningRecord):
        """保存文本学习记录"""
        data_list = self._load_json(self.text_learning_records_file)
        data_list.append(record.to_dict())
        self._save_json(self.text_learning_records_file, data_list)

    def load_text_learning_records(self) -> List[TextLearningRecord]:
        """加载所有文本学习记录"""
        data_list = self._load_json(self.text_learning_records_file)
        records = []
        for data in data_list:
            records.append(TextLearningRecord(
                id=data["id"],
                title=data["title"],
                content=data["content"],
                category=data["category"],
                tags=data["tags"],
                learning_target=data["learning_target"],
                knowledge_summary=data.get("knowledge_summary"),
                reusable_rules=data.get("reusable_rules", []),
                extracted_keywords=data.get("extracted_keywords", []),
                operation_suggestions=data.get("operation_suggestions", []),
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"])
            ))
        return records

    # 表格学习记录
    def save_table_learning_record(self, record: TableLearningRecord):
        """保存表格学习记录"""
        data_list = self._load_json(self.table_learning_records_file)
        data_list.append(record.to_dict())
        self._save_json(self.table_learning_records_file, data_list)

    def load_table_learning_records(self) -> List[TableLearningRecord]:
        """加载所有表格学习记录"""
        data_list = self._load_json(self.table_learning_records_file)
        records = []
        for data in data_list:
            records.append(TableLearningRecord(
                id=data["id"],
                filename=data["filename"],
                data_type=data["data_type"],
                row_count=data["row_count"],
                data_summary=data.get("data_summary"),
                abnormal_metrics=data.get("abnormal_metrics", []),
                optimization_directions=data.get("optimization_directions", []),
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"])
            ))
        return records

    # 复盘学习记录
    def save_review_learning_record(self, record: ReviewLearningRecord):
        """保存复盘学习记录"""
        data_list = self._load_json(self.review_records_file)
        data_list.append(record.to_dict())
        self._save_json(self.review_records_file, data_list)

    def load_review_learning_records(self) -> List[ReviewLearningRecord]:
        """加载所有复盘学习记录"""
        data_list = self._load_json(self.review_records_file)
        records = []
        for data in data_list:
            records.append(ReviewLearningRecord(
                id=data["id"],
                action=data["action"],
                result=data["result"],
                exposure=data.get("exposure"),
                click_rate=data.get("click_rate"),
                conversion_rate=data.get("conversion_rate"),
                roi=data.get("roi"),
                problems=data["problems"],
                next_action=data.get("next_action"),
                experience_summary=data.get("experience_summary"),
                next_optimization_suggestions=data.get("next_optimization_suggestions", []),
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"])
            ))
        return records

    # 生成唯一ID
    def generate_id(self) -> str:
        """生成唯一ID"""
        return str(uuid.uuid4())

    # v0.2 新增存储方法

    # 商家档案 v2
    def save_merchant_profile_v2(self, profile: MerchantProfileV2):
        """保存商家档案 v2"""
        data = profile.to_dict()
        self._save_json(self.merchant_profile_v2_file, [data])

    def load_merchant_profile_v2(self) -> Optional[MerchantProfileV2]:
        """加载商家档案 v2"""
        data_list = self._load_json(self.merchant_profile_v2_file)
        if not data_list:
            return None
        data = data_list[0]
        return MerchantProfileV2(
            id=data["id"],
            merchant_name=data["merchant_name"],
            platforms=[Platform(p) for p in data["platforms"]],
            main_category=data["main_category"],
            price_range=PriceRange(data["price_range"]),
            target_audience=data["target_audience"],
            positioning=data["positioning"],
            visual_style=data["visual_style"],
            operation_goal=data["operation_goal"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )

    # 产品知识库
    def save_product_knowledge(self, knowledge: ProductKnowledge):
        """保存产品知识"""
        data_list = self._load_json(self.product_knowledge_file)
        data_list.append(knowledge.to_dict())
        self._save_json(self.product_knowledge_file, data_list)

    def load_product_knowledge(self) -> List[ProductKnowledge]:
        """加载所有产品知识"""
        data_list = self._load_json(self.product_knowledge_file)
        records = []
        for data in data_list:
            records.append(ProductKnowledge(
                id=data["id"],
                product_name=data["product_name"],
                category=data["category"],
                sku=data.get("sku"),
                price=data["price"],
                selling_points=data.get("selling_points", []),
                material=data.get("material"),
                target_audience=data.get("target_audience"),
                style=data.get("style"),
                notes=data.get("notes"),
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"])
            ))
        return records

    # 竞品知识库
    def save_competitor_knowledge(self, knowledge: CompetitorKnowledge):
        """保存竞品知识"""
        data_list = self._load_json(self.competitor_knowledge_file)
        data_list.append(knowledge.to_dict())
        self._save_json(self.competitor_knowledge_file, data_list)

    def load_competitor_knowledge(self) -> List[CompetitorKnowledge]:
        """加载所有竞品知识"""
        data_list = self._load_json(self.competitor_knowledge_file)
        records = []
        for data in data_list:
            records.append(CompetitorKnowledge(
                id=data["id"],
                competitor_url=data["competitor_url"],
                competitor_title=data["competitor_title"],
                price=data["price"],
                selling_points=data.get("selling_points", []),
                main_image_style=data.get("main_image_style"),
                detail_page_structure=data.get("detail_page_structure"),
                learnable_points=data.get("learnable_points", []),
                differentiation_opportunity=data.get("differentiation_opportunity"),
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"])
            ))
        return records

    # 关键词库
    def save_keyword_library(self, library: KeywordLibrary):
        """保存关键词库"""
        data_list = self._load_json(self.keyword_library_file)
        data_list.append(library.to_dict())
        self._save_json(self.keyword_library_file, data_list)

    def load_keyword_library(self) -> List[KeywordLibrary]:
        """加载所有关键词库"""
        data_list = self._load_json(self.keyword_library_file)
        records = []
        for data in data_list:
            records.append(KeywordLibrary(
                id=data["id"],
                core_keywords=data.get("core_keywords", []),
                long_tail_keywords=data.get("long_tail_keywords", []),
                audience_keywords=data.get("audience_keywords", []),
                scenario_keywords=data.get("scenario_keywords", []),
                selling_point_keywords=data.get("selling_point_keywords", []),
                ad_keywords=data.get("ad_keywords", []),
                negative_keywords=data.get("negative_keywords", []),
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"])
            ))
        return records

    # 视觉风格库
    def save_visual_style_library(self, library: VisualStyleLibrary):
        """保存视觉风格库"""
        data_list = self._load_json(self.visual_style_library_file)
        data_list.append(library.to_dict())
        self._save_json(self.visual_style_library_file, data_list)

    def load_visual_style_library(self) -> List[VisualStyleLibrary]:
        """加载所有视觉风格库"""
        data_list = self._load_json(self.visual_style_library_file)
        records = []
        for data in data_list:
            records.append(VisualStyleLibrary(
                id=data["id"],
                main_image_style=data["main_image_style"],
                detail_page_style=data["detail_page_style"],
                model_style=data.get("model_style"),
                scenario_style=data.get("scenario_style"),
                color_tone=data.get("color_tone"),
                composition_method=data.get("composition_method"),
                ai_image_prompt_template=data.get("ai_image_prompt_template"),
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"])
            ))
        return records

    # 复盘记录库 v2
    def save_review_record_v2(self, record: ReviewRecord):
        """保存复盘记录 v2"""
        data_list = self._load_json(self.review_records_v2_file)
        data_list.append(record.to_dict())
        self._save_json(self.review_records_v2_file, data_list)

    def load_review_records_v2(self) -> List[ReviewRecord]:
        """加载所有复盘记录 v2"""
        data_list = self._load_json(self.review_records_v2_file)
        records = []
        for data in data_list:
            records.append(ReviewRecord(
                id=data["id"],
                action_type=data["action_type"],
                action_content=data["action_content"],
                action_result=data["action_result"],
                exposure=data.get("exposure"),
                click_rate=data.get("click_rate"),
                conversion_rate=data.get("conversion_rate"),
                roi=data.get("roi"),
                problem_judgment=data.get("problem_judgment"),
                next_step_suggestion=data.get("next_step_suggestion"),
                created_at=datetime.fromisoformat(data["created_at"]),
                updated_at=datetime.fromisoformat(data["updated_at"])
            ))
        return records

    # v0.3 新增存储方法

    # 标题生成记录
    def save_title_generation(self, generation):
        """保存标题生成记录"""
        data_list = self._load_json(self.title_generations_file)
        data_list.append(generation.to_dict())
        self._save_json(self.title_generations_file, data_list)

    def load_title_generations(self):
        """加载所有标题生成记录"""
        data_list = self._load_json(self.title_generations_file)
        return data_list

    # 关键词生成记录
    def save_keyword_generation(self, generation):
        """保存关键词生成记录"""
        data_list = self._load_json(self.keyword_generations_file)
        data_list.append(generation.to_dict())
        self._save_json(self.keyword_generations_file, data_list)

    def load_keyword_generations(self):
        """加载所有关键词生成记录"""
        data_list = self._load_json(self.keyword_generations_file)
        return data_list

    # 主图提示词生成记录
    def save_image_prompt_generation(self, generation):
        """保存主图提示词生成记录"""
        data_list = self._load_json(self.image_prompt_generations_file)
        data_list.append(generation.to_dict())
        self._save_json(self.image_prompt_generations_file, data_list)

    def load_image_prompt_generations(self):
        """加载所有主图提示词生成记录"""
        data_list = self._load_json(self.image_prompt_generations_file)
        return data_list

    # 上架包
    def save_listing_package(self, package):
        """保存上架包"""
        data_list = self._load_json(self.listing_packages_file)
        data_list.append(package.to_dict())
        self._save_json(self.listing_packages_file, data_list)

    def load_listing_packages(self):
        """加载所有上架包"""
        data_list = self._load_json(self.listing_packages_file)
        return data_list

    def load_listing_package(self, package_id: str):
        """根据ID加载指定上架包"""
        data_list = self._load_json(self.listing_packages_file)
        for data in data_list:
            if data.get("id") == package_id:
                return data
        return None

    # v0.4 新增存储方法

    # 详情页生成记录
    def save_detail_screen_generation(self, generation):
        """保存详情页生成记录"""
        data_list = self._load_json(self.detail_screen_generations_file)
        data_list.append(generation.to_dict())
        self._save_json(self.detail_screen_generations_file, data_list)

    def load_detail_screen_generations(self):
        """加载所有详情页生成记录"""
        data_list = self._load_json(self.detail_screen_generations_file)
        return data_list

    def load_detail_screen_generation(self, generation_id: str):
        """根据ID加载指定详情页生成记录"""
        data_list = self._load_json(self.detail_screen_generations_file)
        for data in data_list:
            if data.get("id") == generation_id:
                return data
        return None

    # v0.4 phase 2 新增存储方法

    # 短视频脚本生成记录
    def save_video_script_generation(self, generation):
        """保存短视频脚本生成记录"""
        data_list = self._load_json(self.video_script_generations_file)
        data_list.append(generation.to_dict())
        self._save_json(self.video_script_generations_file, data_list)

    def load_video_script_generations(self):
        """加载所有短视频脚本生成记录"""
        data_list = self._load_json(self.video_script_generations_file)
        return data_list

    def load_video_script_generation(self, generation_id: str):
        """根据ID加载指定短视频脚本生成记录"""
        data_list = self._load_json(self.video_script_generations_file)
        for data in data_list:
            if data.get("generation_id") == generation_id:
                return data
        return None

    # 小红书文案生成记录
    def save_xiaohongshu_generation(self, generation):
        """保存小红书文案生成记录"""
        data_list = self._load_json(self.xiaohongshu_generations_file)
        data_list.append(generation.to_dict())
        self._save_json(self.xiaohongshu_generations_file, data_list)

    def load_xiaohongshu_generations(self):
        """加载所有小红书文案生成记录"""
        data_list = self._load_json(self.xiaohongshu_generations_file)
        return data_list

    def load_xiaohongshu_generation(self, generation_id: str):
        """根据ID加载指定小红书文案生成记录"""
        data_list = self._load_json(self.xiaohongshu_generations_file)
        for data in data_list:
            if data.get("generation_id") == generation_id:
                return data
        return None

    # v0.5 新增存储方法

    # 任务中心记录
    def save_task(self, task):
        """保存任务记录"""
        data_list = self._load_json(self.task_center_records_file)
        data_list.append(task.to_dict())
        self._save_json(self.task_center_records_file, data_list)

    def load_tasks(self):
        """加载所有任务记录"""
        data_list = self._load_json(self.task_center_records_file)
        return data_list

    def load_task(self, task_id: str):
        """根据ID加载指定任务记录"""
        data_list = self._load_json(self.task_center_records_file)
        for data in data_list:
            if data.get("task_id") == task_id:
                return data
        return None

    def update_task_status(self, task_id: str, status: str):
        """更新任务状态"""
        data_list = self._load_json(self.task_center_records_file)
        for data in data_list:
            if data.get("task_id") == task_id:
                data["status"] = status
                data["updated_at"] = datetime.now().isoformat()
                self._save_json(self.task_center_records_file, data_list)
                return True
        return False

    def record_human_confirmation(self, task_id: str, confirmed: bool, notes: str = None):
        """记录人工确认"""
        data_list = self._load_json(self.task_center_records_file)
        for data in data_list:
            if data.get("task_id") == task_id:
                if notes:
                    data["final_summary"] = notes
                self._save_json(self.task_center_records_file, data_list)
                return True
        return False

    # v0.6 新增存储方法

    # 验收报告记录
    def save_acceptance_report(self, report):
        """保存验收报告"""
        data_list = self._load_json(self.acceptance_reports_file)
        data_list.append(report.to_dict())
        self._save_json(self.acceptance_reports_file, data_list)

    def load_acceptance_reports(self):
        """加载所有验收报告"""
        data_list = self._load_json(self.acceptance_reports_file)
        return data_list

    def load_acceptance_report(self, report_id: str):
        """根据ID加载指定验收报告"""
        data_list = self._load_json(self.acceptance_reports_file)
        for data in data_list:
            if data.get("report_id") == report_id:
                return data
        return None
