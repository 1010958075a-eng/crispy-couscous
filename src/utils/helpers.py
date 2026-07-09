"""
产品B - 通用工具函数

集中存放在多个服务中重复出现的通用逻辑，避免代码重复。
"""

from typing import Any, Dict, List, Optional, Sequence, TypeVar

T = TypeVar("T")


def find_by_attr(items: Sequence[T], attr: str, value: Any) -> Optional[T]:
    """在对象列表中按指定属性查找第一个匹配项。

    Args:
        items: 对象列表
        attr: 用于匹配的属性名
        value: 目标值

    Returns:
        匹配的对象，未找到时返回 None
    """
    for item in items:
        if getattr(item, attr) == value:
            return item
    return None


def find_by_id(items: Sequence[T], item_id: str) -> Optional[T]:
    """在对象列表中按 ``id`` 属性查找第一个匹配项。

    Args:
        items: 含有 ``id`` 属性的对象列表
        item_id: 目标 ID

    Returns:
        匹配的对象，未找到时返回 None
    """
    return find_by_attr(items, "id", item_id)


def find_dict_by_field(
    data_list: List[Dict[str, Any]],
    value: Any,
    field: str = "id",
) -> Optional[Dict[str, Any]]:
    """在字典列表中按指定字段查找第一个匹配项。

    Args:
        data_list: 字典列表
        value: 目标值
        field: 用于匹配的字段名，默认为 ``id``

    Returns:
        匹配的字典，未找到时返回 None
    """
    for data in data_list:
        if data.get(field) == value:
            return data
    return None


def paginate(items: List[T], page: int, limit: int) -> List[T]:
    """对列表进行分页。

    Args:
        items: 待分页的列表
        page: 页码（从 1 开始）
        limit: 每页数量

    Returns:
        当前页的元素列表
    """
    start = (page - 1) * limit
    end = start + limit
    return items[start:end]


def extract_product_fields(product_info: Dict[str, Any]) -> Dict[str, Any]:
    """从产品信息字典中提取标准字段，提供默认值。

    Args:
        product_info: 产品信息字典

    Returns:
        含 product_name / category / selling_points / material /
        target_audience / style 的标准字段字典
    """
    return {
        "product_name": product_info.get("product_name", ""),
        "category": product_info.get("category", ""),
        "selling_points": product_info.get("selling_points", []),
        "material": product_info.get("material", ""),
        "target_audience": product_info.get("target_audience", ""),
        "style": product_info.get("style", ""),
    }
