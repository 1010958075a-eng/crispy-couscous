"""
产品B - 学习中心服务
"""

import re
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime

from models import (
    LinkLearningRecord,
    TextLearningRecord,
    TableLearningRecord,
    ReviewLearningRecord,
    KnowledgeRecord,
    LearningTarget,
    DataType,
    LinkLearningStatus
)
from .knowledge_storage import KnowledgeStorage


class LearningService:
    """学习中心服务"""

    def __init__(self, storage: KnowledgeStorage = None):
        """初始化学习服务"""
        if storage is None:
            self.storage = KnowledgeStorage()
        else:
            self.storage = storage

    # 链接学习功能
    def learn_from_link(
        self,
        url: str,
        source_platform: str,
        learning_target: LearningTarget,
        notes: Optional[str] = None,
        manual_content: Optional[str] = None
    ) -> LinkLearningRecord:
        """
        从链接学习

        Args:
            url: 链接URL
            source_platform: 来源平台
            learning_target: 学习目标
            notes: 备注
            manual_content: 手动输入的内容（如果自动抓取失败）

        Returns:
            链接学习记录
        """
        record_id = self.storage.generate_id()
        record = LinkLearningRecord(
            id=record_id,
            url=url,
            source_platform=source_platform,
            learning_target=learning_target,
            notes=notes,
            status=LinkLearningStatus.PENDING
        )

        # 尝试自动提取（简化版本，不使用复杂爬虫）
        try:
            if manual_content:
                # 使用手动输入的内容
                extracted_data = self._extract_from_content(manual_content)
                record.extracted_title = extracted_data.get("title", "手动输入内容")
                record.extracted_key_points = extracted_data.get("key_points", [])
                record.extracted_keywords = extracted_data.get("keywords", [])
                record.content_summary = manual_content[:500] + "..." if len(manual_content) > 500 else manual_content
                record.status = LinkLearningStatus.SUCCESS
            else:
                # 简化版本：直接标记为需要手动输入
                record.status = LinkLearningStatus.MANUAL_REQUIRED
                record.content_summary = "链接内容需要手动输入"
        except Exception as e:
            # 抓取失败，标记为需要手动输入
            record.status = LinkLearningStatus.MANUAL_REQUIRED
            record.content_summary = f"自动抓取失败，请手动输入页面内容。错误：{str(e)}"

        record.updated_at = datetime.now()
        self.storage.save_link_learning_record(record)

        # 如果成功提取，保存到知识库
        if record.status == LinkLearningStatus.SUCCESS:
            self._save_to_knowledge_from_link(record)

        return record

    def _extract_from_content(self, content: str) -> Dict[str, Any]:
        """从内容中提取关键信息（简化版本）"""
        # 简化版本：使用基本的文本处理
        lines = content.split('\n')
        title = lines[0] if lines else "未知标题"

        # 提取关键词（简化：使用词频统计）
        words = re.findall(r'\w+', content.lower())
        word_freq = {}
        for word in words:
            if len(word) > 2:  # 忽略短词
                word_freq[word] = word_freq.get(word, 0) + 1

        # 取前10个高频词作为关键词
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        keywords_list = [k[0] for k in keywords]

        # 提取关键点（简化：取前5行作为关键点）
        key_points = [line.strip() for line in lines[:5] if line.strip()]

        return {
            "title": title,
            "key_points": key_points,
            "keywords": keywords_list
        }

    def _save_to_knowledge_from_link(self, record: LinkLearningRecord):
        """从链接学习记录保存到知识库"""
        if record.extracted_title and record.extracted_key_points:
            knowledge = KnowledgeRecord(
                id=self.storage.generate_id(),
                title=record.extracted_title,
                content=record.content_summary or "",
                category=record.learning_target.value,
                tags=record.extracted_keywords,
                source_type="link",
                source_id=record.id,
                applicable_scenarios=["竞品分析", "商品优化"]
            )
            self.storage.save_knowledge_record(knowledge)

    # 文本学习功能
    def learn_from_text(
        self,
        title: str,
        content: str,
        category: str,
        tags: List[str],
        learning_target: LearningTarget
    ) -> TextLearningRecord:
        """
        从文本学习

        Args:
            title: 标题
            content: 内容
            category: 类目
            tags: 标签
            learning_target: 学习目标

        Returns:
            文本学习记录
        """
        record_id = self.storage.generate_id()
        record = TextLearningRecord(
            id=record_id,
            title=title,
            content=content,
            category=category,
            tags=tags,
            learning_target=learning_target
        )

        # 简化版本：生成知识摘要
        extracted_data = self._extract_from_content(content)
        record.knowledge_summary = f"{title}的核心要点：{', '.join(extracted_data['key_points'][:3])}"
        record.extracted_keywords = extracted_data['keywords']
        record.reusable_rules = extracted_data['key_points'][:3]
        record.operation_suggestions = [f"基于{title}的建议：优化关键词布局"]

        record.updated_at = datetime.now()
        self.storage.save_text_learning_record(record)

        # 保存到知识库
        self._save_to_knowledge_from_text(record)

        return record

    def _save_to_knowledge_from_text(self, record: TextLearningRecord):
        """从文本学习记录保存到知识库"""
        knowledge = KnowledgeRecord(
            id=self.storage.generate_id(),
            title=record.title,
            content=record.content,
            category=record.category,
            tags=record.tags + record.extracted_keywords,
            source_type="text",
            source_id=record.id,
            applicable_scenarios=["运营优化", "策略制定"]
        )
        self.storage.save_knowledge_record(knowledge)

    # 表格学习功能
    def learn_from_table(
        self,
        filename: str,
        data_type: DataType,
        row_count: int
    ) -> TableLearningRecord:
        """
        从表格学习

        Args:
            filename: 文件名
            data_type: 数据类型
            row_count: 行数

        Returns:
            表格学习记录
        """
        record_id = self.storage.generate_id()
        record = TableLearningRecord(
            id=record_id,
            filename=filename,
            data_type=data_type,
            row_count=row_count
        )

        # 简化版本：生成数据摘要
        record.data_summary = f"已导入{row_count}行{data_type.value}数据"
        record.abnormal_metrics = []
        record.optimization_directions = ["建议分析数据趋势", "关注异常指标"]

        record.updated_at = datetime.now()
        self.storage.save_table_learning_record(record)

        return record

    # 复盘学习功能
    def learn_from_review(
        self,
        action: str,
        result: str,
        exposure: Optional[int] = None,
        click_rate: Optional[float] = None,
        conversion_rate: Optional[float] = None,
        roi: Optional[float] = None,
        problems: List[str] = None,
        next_action: Optional[str] = None
    ) -> ReviewLearningRecord:
        """
        从复盘学习

        Args:
            action: 本次动作
            result: 执行结果
            exposure: 曝光
            click_rate: 点击率
            conversion_rate: 转化率
            roi: ROI
            problems: 问题列表
            next_action: 下一步动作

        Returns:
            复盘学习记录
        """
        record_id = self.storage.generate_id()
        record = ReviewLearningRecord(
            id=record_id,
            action=action,
            result=result,
            exposure=exposure,
            click_rate=click_rate,
            conversion_rate=conversion_rate,
            roi=roi,
            problems=problems or [],
            next_action=next_action
        )

        # 简化版本：生成经验沉淀
        record.experience_summary = f"{action}的执行结果：{result}"
        record.next_optimization_suggestions = [
            "分析失败原因",
            "优化执行策略",
            "关注关键指标"
        ]

        record.updated_at = datetime.now()
        self.storage.save_review_learning_record(record)

        return record

    # 获取学习记录
    def get_link_learning_records(self) -> List[LinkLearningRecord]:
        """获取所有链接学习记录"""
        return self.storage.load_link_learning_records()

    def get_text_learning_records(self) -> List[TextLearningRecord]:
        """获取所有文本学习记录"""
        return self.storage.load_text_learning_records()

    def get_table_learning_records(self) -> List[TableLearningRecord]:
        """获取所有表格学习记录"""
        return self.storage.load_table_learning_records()

    def get_review_learning_records(self) -> List[ReviewLearningRecord]:
        """获取所有复盘学习记录"""
        return self.storage.load_review_learning_records()

    def get_knowledge_records(self) -> List[KnowledgeRecord]:
        """获取所有知识库记录"""
        return self.storage.load_knowledge_records()

    def get_knowledge_by_category(self, category: str) -> List[KnowledgeRecord]:
        """按类别获取知识库记录"""
        return self.storage.get_knowledge_by_category(category)
