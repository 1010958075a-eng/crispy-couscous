# 产品B电商自动化系统 - 快速操作指南（完整闭环）

本指南将引导你完成从安装到业务闭环的完整操作流程。

---

## 步骤1：安装部署

```bash
# 进入项目目录
cd /Users/linguanghai/CascadeProjects/product-b-ecommerce

# 运行一键安装脚本
./install.sh
```

**预期输出：**
```
==========================================
产品B电商自动化系统
==========================================

[1] 检查Python版本...
Python 3.9.6
✓ Python检查通过

[2] 安装依赖...
✓ 依赖安装完成

[3] 配置环境变量...
✓ .env文件已存在

[4] 检查产品A模块路径...
✓ 产品A模块路径存在

==========================================
安装完成！
==========================================
```

---

## 步骤2：启动API服务器

```bash
# 启动API服务器
python3 src/api/server.py
```

**预期输出：**
```
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**验证服务：**
```bash
# 新开一个终端窗口，测试健康检查
curl http://localhost:8000/health
```

**预期输出：**
```json
{"status":"healthy","service":"product-b-api"}
```

---

## 步骤3：创建商品（上架）

### 3.1 创建第一个商品

```bash
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "智能手表Pro",
    "description": "2024新款智能手表，支持心率监测、GPS定位、防水功能",
    "price": 599.00,
    "stock": 100,
    "category": "数码",
    "platform": "taobao",
    "tags": ["智能", "健康", "运动"]
  }'
```

**预期输出：**
```json
{
  "id": "xxx-xxx-xxx",
  "name": "智能手表Pro",
  "description": "2024新款智能手表，支持心率监测、GPS定位、防水功能",
  "price": 599.0,
  "stock": 100,
  "category": "数码",
  "status": "draft",
  "images": [],
  "tags": ["智能", "健康", "运动"],
  "created_at": "2026-07-01T21:00:00",
  "updated_at": "2026-07-01T21:00:00",
  "platform": "taobao"
}
```

**记录商品ID：** `xxx-xxx-xxx`（后续创建订单时需要）

### 3.2 创建第二个商品

```bash
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "蓝牙降噪耳机",
    "description": "主动降噪蓝牙耳机，30小时续航",
    "price": 299.00,
    "stock": 200,
    "category": "数码",
    "platform": "douyin",
    "tags": ["无线", "降噪", "音乐"]
  }'
```

**记录商品ID：** `yyy-yyy-yyy`

### 3.3 将商品上架

```bash
# 将第一个商品上架
curl -X PUT http://localhost:8000/api/products/xxx-xxx-xxx \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

---

## 步骤4：创建订单（销售）

### 4.1 创建第一个订单

```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "customer_001",
    "items": [
      {
        "product_id": "xxx-xxx-xxx",
        "product_name": "智能手表Pro",
        "quantity": 2,
        "price": 599.00
      }
    ],
    "shipping_address": "北京市朝阳区望京SOHO",
    "payment_method": "alipay",
    "platform": "taobao"
  }'
```

**预期输出：**
```json
{
  "id": "order-001",
  "user_id": "customer_001",
  "items": [
    {
      "product_id": "xxx-xxx-xxx",
      "product_name": "智能手表Pro",
      "quantity": 2,
      "price": 599.0
    }
  ],
  "total_amount": 1198.0,
  "status": "pending",
  "shipping_address": "北京市朝阳区望京SOHO",
  "payment_method": "alipay",
  "platform": "taobao",
  "created_at": "2026-07-01T21:05:00",
  "updated_at": "2026-07-01T21:05:00"
}
```

**记录订单ID：** `order-001`

### 4.2 订单支付

```bash
curl -X PUT http://localhost:8000/api/orders/order-001/status \
  -H "Content-Type: application/json" \
  -d '{"status": "paid"}'
```

### 4.3 创建第二个订单（抖音平台）

```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "customer_002",
    "items": [
      {
        "product_id": "yyy-yyy-yyy",
        "product_name": "蓝牙降噪耳机",
        "quantity": 3,
        "price": 299.00
      }
    ],
    "shipping_address": "上海市浦东新区陆家嘴",
    "payment_method": "wechat",
    "platform": "douyin"
  }'
```

**记录订单ID：** `order-002`

---

## 步骤5：订单发货

```bash
# 将第一个订单改为已发货状态
curl -X PUT http://localhost:8000/api/orders/order-001/status \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped"}'

# 将第二个订单改为已支付状态
curl -X PUT http://localhost:8000/api/orders/order-002/status \
  -H "Content-Type: application/json" \
  -d '{"status": "paid"}'
```

---

## 步骤6：数据分析（业务闭环）

### 6.1 查看销售摘要

```bash
curl "http://localhost:8000/api/analytics/sales-summary?days=7"
```

**预期输出：**
```json
{
  "period_days": 7,
  "start_date": "2026-06-24T21:00:00",
  "end_date": "2026-07-01T21:00:00",
  "total_orders": 2,
  "total_revenue": 2095.0,
  "avg_order_value": 1047.5,
  "status_breakdown": {
    "paid": 1,
    "shipped": 1
  }
}
```

### 6.2 查看热销商品

```bash
curl "http://localhost:8000/api/analytics/top-products?limit=10"
```

**预期输出：**
```json
[
  {
    "product_id": "xxx-xxx-xxx",
    "product_name": "智能手表Pro",
    "category": "数码",
    "sales": 2,
    "revenue": 1198.0
  },
  {
    "product_id": "yyy-yyy-yyy",
    "product_name": "蓝牙降噪耳机",
    "category": "数码",
    "sales": 3,
    "revenue": 897.0
  }
]
```

### 6.3 查看平台表现

```bash
curl "http://localhost:8000/api/analytics/platform-performance?days=30"
```

**预期输出：**
```json
{
  "taobao": {
    "orders": 1,
    "revenue": 1198.0,
    "products": 1
  },
  "douyin": {
    "orders": 1,
    "revenue": 897.0,
    "products": 1
  }
}
```

### 6.4 生成日报

```bash
curl "http://localhost:8000/api/analytics/report?days=7"
```

**预期输出：**
```json
{
  "report": "# 电商数据分析日报\n\n## 时间范围\n...\n## 销售概览\n- 总订单数: 2\n- 总收入: ¥2095.00\n..."
}
```

---

## 步骤7：业务验证（闭环确认）

### 7.1 查询所有订单

```bash
curl "http://localhost:8000/api/orders"
```

### 7.2 搜索商品

```bash
curl "http://localhost:8000/api/products?keyword=智能&limit=10"
```

### 7.3 查看特定订单详情

```bash
curl "http://localhost:8000/api/orders/order-001"
```

---

## 完整业务闭环总结

**业务流程：**
1. ✅ **商品上架** - 创建商品并上架销售
2. ✅ **订单创建** - 客户下单购买
3. ✅ **订单支付** - 订单状态更新为已支付
4. ✅ **订单发货** - 订单状态更新为已发货
5. ✅ **数据分析** - 查看销售数据和业务表现
6. ✅ **业务优化** - 根据数据优化商品和营销策略

**数据流转：**
- 商品 → 订单 → 支付 → 发货 → 数据分析 → 业务优化

---

## 常用操作命令速查

```bash
# 健康检查
curl http://localhost:8000/health

# 创建商品
curl -X POST http://localhost:8000/api/products -H "Content-Type: application/json" -d '{...}'

# 搜索商品
curl "http://localhost:8000/api/products?keyword=xxx"

# 创建订单
curl -X POST http://localhost:8000/api/orders -H "Content-Type: application/json" -d '{...}'

# 更新订单状态
curl -X PUT http://localhost:8000/api/orders/{order_id}/status -H "Content-Type: application/json" -d '{"status":"paid"}'

# 销售摘要
curl "http://localhost:8000/api/analytics/sales-summary?days=7"

# 热销商品
curl "http://localhost:8000/api/analytics/top-products?limit=10"
```

---

## 下一步建议

完成基础闭环后，可以：

1. **配置真实LLM** - 编辑`.env`文件，使用OpenAI或Anthropic API
2. **接入数据库** - 添加MySQL/PostgreSQL持久化存储
3. **部署生产环境** - 使用Docker、Kubernetes等容器化部署
4. **扩展功能** - 添加用户管理、权限控制、支付集成等

---

## 技术支持

- **API文档**: http://localhost:8000/docs
- **详细说明书**: docs/USER_MANUAL.md
- **问题反馈**: GitHub Issues
