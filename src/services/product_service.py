"""
产品B - 商品管理服务
"""

from typing import List, Optional
from datetime import datetime
import uuid

from models.product import Product, ProductStatus, ProductSearchQuery


class ProductService:
    """商品管理服务"""
    
    def __init__(self):
        self.products: dict[str, Product] = {}
    
    def create_product(
        self,
        name: str,
        description: str,
        price: float,
        stock: int,
        category: str,
        platform: str,
        images: List[str] = None,
        tags: List[str] = None
    ) -> Product:
        """
        创建商品
        
        Args:
            name: 商品名称
            description: 商品描述
            price: 价格
            stock: 库存
            category: 分类
            platform: 平台
            images: 图片列表
            tags: 标签列表
            
        Returns:
            商品对象
        """
        product = Product(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            status=ProductStatus.DRAFT,
            images=images or [],
            tags=tags or [],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            platform=platform
        )
        self.products[product.id] = product
        return product
    
    def get_product(self, product_id: str) -> Optional[Product]:
        """
        获取商品
        
        Args:
            product_id: 商品ID
            
        Returns:
            商品对象
        """
        return self.products.get(product_id)
    
    def update_product(
        self,
        product_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        stock: Optional[int] = None,
        status: Optional[ProductStatus] = None
    ) -> Optional[Product]:
        """
        更新商品
        
        Args:
            product_id: 商品ID
            name: 商品名称
            description: 商品描述
            price: 价格
            stock: 库存
            status: 状态
            
        Returns:
            更新后的商品对象
        """
        product = self.products.get(product_id)
        if not product:
            return None
        
        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if stock is not None:
            product.stock = stock
        if status is not None:
            product.status = status
        
        product.updated_at = datetime.now()
        return product
    
    def delete_product(self, product_id: str) -> bool:
        """
        删除商品
        
        Args:
            product_id: 商品ID
            
        Returns:
            是否成功
        """
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False
    
    def search_products(self, query: ProductSearchQuery) -> List[Product]:
        """
        搜索商品
        
        Args:
            query: 搜索查询
            
        Returns:
            商品列表
        """
        results = list(self.products.values())
        
        # 关键词过滤
        if query.keyword:
            results = [
                p for p in results
                if query.keyword.lower() in p.name.lower()
                or query.keyword.lower() in p.description.lower()
            ]
        
        # 分类过滤
        if query.category:
            results = [p for p in results if p.category == query.category]
        
        # 价格过滤
        if query.min_price:
            results = [p for p in results if p.price >= query.min_price]
        if query.max_price:
            results = [p for p in results if p.price <= query.max_price]
        
        # 状态过滤
        if query.status:
            results = [p for p in results if p.status == query.status]
        
        # 平台过滤
        if query.platform:
            results = [p for p in results if p.platform == query.platform]
        
        # 分页
        start = (query.page - 1) * query.limit
        end = start + query.limit
        return results[start:end]
    
    def get_products_by_platform(self, platform: str) -> List[Product]:
        """
        获取指定平台的商品
        
        Args:
            platform: 平台名称
            
        Returns:
            商品列表
        """
        return [p for p in self.products.values() if p.platform == platform]
    
    def get_total_products(self) -> int:
        """获取商品总数"""
        return len(self.products)
