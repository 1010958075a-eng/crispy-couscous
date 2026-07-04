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

        # v0.7 新增文件路径
        self.tool_registry_file = self.base_path / "tool_registry.json"
        self.tool_plan_records_file = self.base_path / "tool_plan_records.json"

        # v0.8 新增文件路径
        self.workflow_records_file = self.base_path / "workflow_records.json"

        # v0.9 新增文件路径
        self.log_records_file = self.base_path / "log_records.json"

        # v1.1 新增文件路径
        self.api_providers_file = self.base_path / "api_providers.json"
        self.api_call_records_file = self.base_path / "api_call_records.json"
        self.api_quota_records_file = self.base_path / "api_quota_records.json"

        # v1.2 新增文件路径
        self.subscription_plans_file = self.base_path / "subscription_plans.json"
        self.customer_quota_accounts_file = self.base_path / "customer_quota_accounts.json"
        self.feature_point_rules_file = self.base_path / "feature_point_rules.json"
        self.usage_records_file = self.base_path / "usage_records.json"

        # v1.3 新增文件路径
        self.model_profiles_file = self.base_path / "model_profiles.json"
        self.business_experts_file = self.base_path / "business_experts.json"
        self.model_route_rules_file = self.base_path / "model_route_rules.json"
        self.model_route_decisions_file = self.base_path / "model_route_decisions.json"

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

    # v0.7 新增存储方法

    # 工具注册表记录
    def save_tool_registry(self, tools):
        """保存工具注册表"""
        data_list = [tool.to_dict() for tool in tools]
        self._save_json(self.tool_registry_file, data_list)

    def load_tool_registry(self):
        """加载工具注册表"""
        data_list = self._load_json(self.tool_registry_file)
        return data_list

    # 工具计划记录
    def save_tool_plan(self, plan):
        """保存工具计划"""
        data_list = self._load_json(self.tool_plan_records_file)
        data_list.append(plan.to_dict())
        self._save_json(self.tool_plan_records_file, data_list)

    def load_tool_plans(self):
        """加载所有工具计划"""
        data_list = self._load_json(self.tool_plan_records_file)
        return data_list

    def load_tool_plan(self, plan_id: str):
        """根据ID加载指定工具计划"""
        data_list = self._load_json(self.tool_plan_records_file)
        for data in data_list:
            if data.get("plan_id") == plan_id:
                return data
        return None

    # v0.8 新增存储方法

    # 工作流记录
    def save_workflow(self, workflow):
        """保存工作流"""
        data_list = self._load_json(self.workflow_records_file)
        data_list.append(workflow.to_dict())
        self._save_json(self.workflow_records_file, data_list)

    def save_workflows(self, workflows):
        """保存工作流列表"""
        self._save_json(self.workflow_records_file, workflows)

    def load_workflows(self):
        """加载所有工作流"""
        data_list = self._load_json(self.workflow_records_file)
        return data_list

    def load_workflow(self, workflow_id: str):
        """加载指定工作流"""
        data_list = self._load_json(self.workflow_records_file)
        for data in data_list:
            if data.get("workflow_id") == workflow_id:
                return data
        return None

    # v0.9 新增存储方法

    # 日志记录
    def save_log(self, log):
        """保存日志"""
        data_list = self._load_json(self.log_records_file)
        data_list.append(log.to_dict())
        self._save_json(self.log_records_file, data_list)

    def save_logs(self, logs):
        """保存日志列表"""
        self._save_json(self.log_records_file, logs)

    def load_logs(self):
        """加载所有日志"""
        data_list = self._load_json(self.log_records_file)
        return data_list

    def load_log(self, log_id: str):
        """加载指定日志"""
        data_list = self._load_json(self.log_records_file)
        for data in data_list:
            if data.get("log_id") == log_id:
                return data
        return None

    # v1.1 新增存储方法

    # API供应商
    def save_api_providers(self, providers):
        """保存API供应商列表"""
        provider_dicts = [p.to_dict() for p in providers]
        self._save_json(self.api_providers_file, provider_dicts)

    def load_api_providers(self):
        """加载API供应商列表"""
        data_list = self._load_json(self.api_providers_file)
        if data_list:
            # 从存储恢复供应商对象
            providers = []
            for provider_dict in data_list:
                from models.api_provider import ApiProvider
                provider = ApiProvider(
                    provider_id=provider_dict["provider_id"],
                    provider_name=provider_dict["provider_name"],
                    provider_type=provider_dict["provider_type"],
                    model_name=provider_dict["model_name"],
                    api_base_url=provider_dict["api_base_url"],
                    api_key_placeholder=provider_dict["api_key_placeholder"],
                    cost_level=provider_dict["cost_level"],
                    risk_level=provider_dict["risk_level"],
                    enabled=provider_dict["enabled"],
                    daily_limit=provider_dict["daily_limit"],
                    monthly_limit=provider_dict["monthly_limit"],
                    used_today=provider_dict["used_today"],
                    used_this_month=provider_dict["used_this_month"],
                    unit_cost_estimate=provider_dict["unit_cost_estimate"],
                    supported_features=provider_dict["supported_features"],
                    fallback_provider_id=provider_dict["fallback_provider_id"]
                )
                providers.append(provider)
            return providers
        else:
            return []

    def load_api_provider(self, provider_id: str):
        """加载指定API供应商"""
        providers = self.load_api_providers()
        for provider in providers:
            if provider.provider_id == provider_id:
                return provider
        return None

    # API调用记录
    def save_api_call_records(self, call_records):
        """保存API调用记录列表"""
        call_record_dicts = [c.to_dict() for c in call_records]
        self._save_json(self.api_call_records_file, call_record_dicts)

    def load_api_call_records(self):
        """加载API调用记录列表"""
        data_list = self._load_json(self.api_call_records_file)
        if data_list:
            # 从存储恢复调用记录对象
            call_records = []
            for record_dict in data_list:
                from models.api_provider import ApiCallRecord
                call_record = ApiCallRecord(
                    call_id=record_dict["call_id"],
                    provider_id=record_dict["provider_id"],
                    provider_name=record_dict["provider_name"],
                    provider_type=record_dict["provider_type"],
                    feature_name=record_dict["feature_name"],
                    request_summary=record_dict["request_summary"],
                    estimated_units=record_dict["estimated_units"],
                    estimated_cost=record_dict["estimated_cost"],
                    status=record_dict["status"],
                    blocked_reason=record_dict["blocked_reason"]
                )
                call_records.append(call_record)
            return call_records
        else:
            return []

    def load_api_call_record(self, call_id: str):
        """加载指定API调用记录"""
        call_records = self.load_api_call_records()
        for record in call_records:
            if record.call_id == call_id:
                return record
        return None

    # API额度记录
    def save_api_quota_records(self, quota_records):
        """保存API额度记录列表"""
        quota_record_dicts = [q.to_dict() for q in quota_records]
        self._save_json(self.api_quota_records_file, quota_record_dicts)

    def load_api_quota_records(self):
        """加载API额度记录列表"""
        data_list = self._load_json(self.api_quota_records_file)
        if data_list:
            # 从存储恢复额度记录对象
            quota_records = []
            for record_dict in data_list:
                from models.api_provider import ApiQuotaRecord
                quota_record = ApiQuotaRecord(
                    quota_id=record_dict["quota_id"],
                    provider_id=record_dict["provider_id"],
                    daily_limit=record_dict["daily_limit"],
                    monthly_limit=record_dict["monthly_limit"],
                    used_today=record_dict["used_today"],
                    used_this_month=record_dict["used_this_month"],
                    remaining_today=record_dict["remaining_today"],
                    remaining_this_month=record_dict["remaining_this_month"]
                )
                quota_records.append(quota_record)
            return quota_records
        else:
            return []

    def load_api_quota_record(self, quota_id: str):
        """加载指定API额度记录"""
        quota_records = self.load_api_quota_records()
        for record in quota_records:
            if record.quota_id == quota_id:
                return record
        return None

    # v1.2 新增存储方法

    # 订阅套餐
    def save_subscription_plans(self, plans):
        """保存订阅套餐列表"""
        plan_dicts = [p.to_dict() for p in plans]
        self._save_json(self.subscription_plans_file, plan_dicts)

    def load_subscription_plans(self):
        """加载订阅套餐列表"""
        data_list = self._load_json(self.subscription_plans_file)
        if data_list:
            # 从存储恢复套餐对象
            plans = []
            for plan_dict in data_list:
                from models.subscription import SubscriptionPlan
                plan = SubscriptionPlan(
                    plan_id=plan_dict["plan_id"],
                    plan_name=plan_dict["plan_name"],
                    plan_level=plan_dict["plan_level"],
                    monthly_price=plan_dict["monthly_price"],
                    included_points=plan_dict["included_points"],
                    daily_point_limit=plan_dict["daily_point_limit"],
                    monthly_point_limit=plan_dict["monthly_point_limit"],
                    image_generation_limit=plan_dict["image_generation_limit"],
                    remove_bg_limit=plan_dict["remove_bg_limit"],
                    workflow_limit=plan_dict["workflow_limit"],
                    knowledge_base_limit=plan_dict["knowledge_base_limit"],
                    advanced_model_enabled=plan_dict["advanced_model_enabled"],
                    team_member_limit=plan_dict["team_member_limit"],
                    private_deployment_enabled=plan_dict["private_deployment_enabled"],
                    enabled=plan_dict["enabled"]
                )
                plans.append(plan)
            return plans
        else:
            return []

    def load_subscription_plan(self, plan_id: str):
        """加载指定订阅套餐"""
        plans = self.load_subscription_plans()
        for plan in plans:
            if plan.plan_id == plan_id:
                return plan
        return None

    # 客户额度账户
    def save_customer_quota_accounts(self, accounts):
        """保存客户额度账户列表"""
        account_dicts = [a.to_dict() for a in accounts]
        self._save_json(self.customer_quota_accounts_file, account_dicts)

    def load_customer_quota_accounts(self):
        """加载客户额度账户列表"""
        data_list = self._load_json(self.customer_quota_accounts_file)
        if data_list:
            # 从存储恢复账户对象
            accounts = []
            for account_dict in data_list:
                from models.subscription import CustomerQuotaAccount
                account = CustomerQuotaAccount(
                    account_id=account_dict["account_id"],
                    customer_id=account_dict["customer_id"],
                    plan_id=account_dict["plan_id"],
                    total_points=account_dict["total_points"],
                    used_points=account_dict["used_points"],
                    remaining_points=account_dict["remaining_points"],
                    daily_used_points=account_dict["daily_used_points"],
                    monthly_used_points=account_dict["monthly_used_points"],
                    status=account_dict["status"]
                )
                accounts.append(account)
            return accounts
        else:
            return []

    def load_customer_quota_account(self, account_id: str):
        """加载指定客户额度账户"""
        accounts = self.load_customer_quota_accounts()
        for account in accounts:
            if account.account_id == account_id:
                return account
        return None

    # 功能扣点规则
    def save_feature_point_rules(self, rules):
        """保存功能扣点规则列表"""
        rule_dicts = [r.to_dict() for r in rules]
        self._save_json(self.feature_point_rules_file, rule_dicts)

    def load_feature_point_rules(self):
        """加载功能扣点规则列表"""
        data_list = self._load_json(self.feature_point_rules_file)
        if data_list:
            # 从存储恢复规则对象
            rules = []
            for rule_dict in data_list:
                from models.subscription import FeaturePointRule
                rule = FeaturePointRule(
                    rule_id=rule_dict["rule_id"],
                    feature_name=rule_dict["feature_name"],
                    points_required=rule_dict["points_required"],
                    feature_type=rule_dict["feature_type"],
                    risk_level=rule_dict["risk_level"],
                    enabled=rule_dict["enabled"]
                )
                rules.append(rule)
            return rules
        else:
            return []

    def load_feature_point_rule(self, rule_id: str):
        """加载指定功能扣点规则"""
        rules = self.load_feature_point_rules()
        for rule in rules:
            if rule.rule_id == rule_id:
                return rule
        return None

    # 消费记录
    def save_usage_records(self, usage_records):
        """保存消费记录列表"""
        usage_record_dicts = [u.to_dict() for u in usage_records]
        self._save_json(self.usage_records_file, usage_record_dicts)

    def load_usage_records(self):
        """加载消费记录列表"""
        data_list = self._load_json(self.usage_records_file)
        if data_list:
            # 从存储恢复消费记录对象
            usage_records = []
            for record_dict in data_list:
                from models.subscription import UsageRecord
                usage_record = UsageRecord(
                    usage_id=record_dict["usage_id"],
                    customer_id=record_dict["customer_id"],
                    account_id=record_dict["account_id"],
                    plan_id=record_dict["plan_id"],
                    feature_name=record_dict["feature_name"],
                    points_used=record_dict["points_used"],
                    status=record_dict["status"],
                    blocked_reason=record_dict["blocked_reason"],
                    before_remaining_points=record_dict["before_remaining_points"],
                    after_remaining_points=record_dict["after_remaining_points"]
                )
                usage_records.append(usage_record)
            return usage_records
        else:
            return []

    def load_usage_record(self, usage_id: str):
        """加载指定消费记录"""
        usage_records = self.load_usage_records()
        for record in usage_records:
            if record.usage_id == usage_id:
                return record
        return None

    # v1.3 新增存储方法

    # 模型档案
    def save_model_profiles(self, models):
        """保存模型档案列表"""
        model_dicts = [m.to_dict() for m in models]
        self._save_json(self.model_profiles_file, model_dicts)

    def load_model_profiles(self):
        """加载模型档案列表"""
        data_list = self._load_json(self.model_profiles_file)
        if data_list:
            # 从存储恢复模型对象
            models = []
            for model_dict in data_list:
                from models.model_router import ModelProfile
                model = ModelProfile(
                    model_id=model_dict["model_id"],
                    provider_id=model_dict["provider_id"],
                    model_name=model_dict["model_name"],
                    provider_type=model_dict["provider_type"],
                    model_tier=model_dict["model_tier"],
                    capability_tags=model_dict["capability_tags"],
                    supported_task_types=model_dict["supported_task_types"],
                    cost_level=model_dict["cost_level"],
                    quality_level=model_dict["quality_level"],
                    speed_level=model_dict["speed_level"],
                    privacy_level=model_dict["privacy_level"],
                    supports_local_only=model_dict["supports_local_only"],
                    supports_streaming=model_dict["supports_streaming"],
                    supports_batch=model_dict["supports_batch"],
                    supports_rag=model_dict["supports_rag"],
                    supports_image=model_dict["supports_image"],
                    supports_text=model_dict["supports_text"],
                    enabled=model_dict["enabled"]
                )
                models.append(model)
            return models
        else:
            return []

    def load_model_profile(self, model_id: str):
        """加载指定模型档案"""
        models = self.load_model_profiles()
        for model in models:
            if model.model_id == model_id:
                return model
        return None

    # 业务专家
    def save_business_experts(self, experts):
        """保存业务专家列表"""
        expert_dicts = [e.to_dict() for e in experts]
        self._save_json(self.business_experts_file, expert_dicts)

    def load_business_experts(self):
        """加载业务专家列表"""
        data_list = self._load_json(self.business_experts_file)
        if data_list:
            # 从存储恢复专家对象
            experts = []
            for expert_dict in data_list:
                from models.model_router import BusinessExpert
                expert = BusinessExpert(
                    expert_id=expert_dict["expert_id"],
                    expert_name=expert_dict["expert_name"],
                    expert_type=expert_dict["expert_type"],
                    supported_task_types=expert_dict["supported_task_types"],
                    capability_tags=expert_dict["capability_tags"],
                    risk_level=expert_dict["risk_level"],
                    default_priority=expert_dict["default_priority"],
                    enabled=expert_dict["enabled"]
                )
                experts.append(expert)
            return experts
        else:
            return []

    def load_business_expert(self, expert_id: str):
        """加载指定业务专家"""
        experts = self.load_business_experts()
        for expert in experts:
            if expert.expert_id == expert_id:
                return expert
        return None

    # 路由规则
    def save_model_route_rules(self, rules):
        """保存路由规则列表"""
        rule_dicts = [r.to_dict() for r in rules]
        self._save_json(self.model_route_rules_file, rule_dicts)

    def load_model_route_rules(self):
        """加载路由规则列表"""
        data_list = self._load_json(self.model_route_rules_file)
        if data_list:
            # 从存储恢复规则对象
            rules = []
            for rule_dict in data_list:
                from models.model_router import ModelRouteRule
                rule = ModelRouteRule(
                    rule_id=rule_dict["rule_id"],
                    task_type=rule_dict["task_type"],
                    feature_name=rule_dict["feature_name"],
                    route_policy=rule_dict["route_policy"],
                    preferred_expert_ids=rule_dict["preferred_expert_ids"],
                    preferred_model_ids=rule_dict["preferred_model_ids"],
                    fallback_model_ids=rule_dict["fallback_model_ids"],
                    min_quality_level=rule_dict["min_quality_level"],
                    max_cost_level=rule_dict["max_cost_level"],
                    local_only_required=rule_dict["local_only_required"],
                    human_approval_required=rule_dict["human_approval_required"],
                    enabled=rule_dict["enabled"]
                )
                rules.append(rule)
            return rules
        else:
            return []

    def load_model_route_rule(self, rule_id: str):
        """加载指定路由规则"""
        rules = self.load_model_route_rules()
        for rule in rules:
            if rule.rule_id == rule_id:
                return rule
        return None

    # 路由决策记录
    def save_model_route_decisions(self, decisions):
        """保存路由决策记录列表"""
        decision_dicts = [d.to_dict() for d in decisions]
        self._save_json(self.model_route_decisions_file, decision_dicts)

    def load_model_route_decisions(self):
        """加载路由决策记录列表"""
        data_list = self._load_json(self.model_route_decisions_file)
        if data_list:
            # 从存储恢复决策对象
            decisions = []
            for decision_dict in data_list:
                from models.model_router import ModelRouteDecision
                decision = ModelRouteDecision(
                    decision_id=decision_dict["decision_id"],
                    task_text=decision_dict["task_text"],
                    task_type=decision_dict["task_type"],
                    feature_name=decision_dict["feature_name"],
                    customer_id=decision_dict["customer_id"],
                    account_id=decision_dict["account_id"],
                    route_policy=decision_dict["route_policy"],
                    selected_expert_ids=decision_dict["selected_expert_ids"],
                    candidate_model_ids=decision_dict["candidate_model_ids"],
                    selected_model_id=decision_dict["selected_model_id"],
                    fallback_model_ids=decision_dict["fallback_model_ids"],
                    estimated_points=decision_dict["estimated_points"],
                    estimated_cost_level=decision_dict["estimated_cost_level"],
                    requires_human_approval=decision_dict["requires_human_approval"],
                    status=decision_dict["status"],
                    blocked_reason=decision_dict["blocked_reason"],
                    decision_reason=decision_dict["decision_reason"]
                )
                decisions.append(decision)
            return decisions
        else:
            return []

    def load_model_route_decision(self, decision_id: str):
        """加载指定路由决策记录"""
        decisions = self.load_model_route_decisions()
        for decision in decisions:
            if decision.decision_id == decision_id:
                return decision
        return None
