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
    MerchantProfile
)


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
