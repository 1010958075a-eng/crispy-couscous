# 产品B接口说明

## 接口概览

产品B提供完整的后端Agent OS基础闭环接口，涵盖学习中心、商家知识库、上架包、详情页、内容生成、任务中心、验收中心、工具中心、工作流中心、日志中心等模块。

## 学习中心

### 创建学习目标
```
POST /api/learning/targets/create
```
请求体：
```json
{
  "target_type": "link",
  "url": "https://example.com",
  "description": "学习目标描述"
}
```

### 获取学习目标列表
```
GET /api/learning/targets
```

### 获取指定学习目标
```
GET /api/learning/targets/{target_id}
```

### 执行学习
```
POST /api/learning/learn
```
请求体：
```json
{
  "target_id": "uuid",
  "data_type": "link"
}
```

## 商家知识库

### 创建商家档案
```
POST /api/knowledge/merchant-profile/create
```
请求体：
```json
{
  "merchant_id": "uuid",
  "platform": "tmall",
  "shop_name": "店铺名称",
  "price_range": "low"
}
```

### 获取商家档案列表
```
GET /api/knowledge/merchant-profiles
```

### 创建商品知识
```
POST /api/knowledge/product-knowledge/create
```
请求体：
```json
{
  "product_id": "uuid",
  "product_name": "商品名称",
  "category": "分类",
  "platform": "tmall"
}
```

### 获取商品知识列表
```
GET /api/knowledge/product-knowledge
```

## 上架包

### 创建上架包
```
POST /api/packages/create
```
请求体：
```json
{
  "product_id": "uuid",
  "title": "商品标题",
  "keywords": ["关键词1", "关键词2"],
  "image_prompts": ["提示词1", "提示词2"]
}
```

### 获取上架包列表
```
GET /api/packages
```

### 获取指定上架包
```
GET /api/packages/{package_id}
```

## 详情页

### 生成详情页
```
POST /api/detail-screens/generate
```
请求体：
```json
{
  "product_id": "uuid",
  "product_name": "商品名称",
  "platform": "tmall"
}
```

### 获取详情页生成记录
```
GET /api/detail-screens
```

### 获取指定详情页
```
GET /api/detail-screens/{generation_id}
```

## 内容生成

### 生成标题
```
POST /api/content/titles/generate
```
请求体：
```json
{
  "product_name": "商品名称",
  "platform": "tmall"
}
```

### 生成关键词
```
POST /api/content/keywords/generate
```
请求体：
```json
{
  "product_name": "商品名称",
  "platform": "tmall"
}
```

### 生成图像提示词
```
POST /api/content/image-prompts/generate
```
请求体：
```json
{
  "product_name": "商品名称",
  "platform": "tmall"
}
```

## 任务中心（v0.5）

### 创建任务
```
POST /api/tasks/create
```
请求体：
```json
{
  "original_request": "生成一个标题和关键词",
  "priority": "medium"
}
```

### 获取任务列表
```
GET /api/tasks
```

### 获取指定任务
```
GET /api/tasks/{task_id}
```

### 更新任务状态
```
POST /api/tasks/{task_id}/status
```
请求体：
```json
{
  "status": "completed"
}
```

## 验收中心（v0.6）

### 创建验收报告
```
POST /api/acceptance/create
```
请求体：
```json
{
  "target_type": "task",
  "target_id": "uuid",
  "acceptance_criteria": ["验收标准1", "验收标准2"]
}
```

### 获取验收报告列表
```
GET /api/acceptance
```

### 获取指定验收报告
```
GET /api/acceptance/{report_id}
```

## 工具中心（v0.7）

### 获取工具列表
```
GET /api/tools
```

### 推荐工具
```
POST /api/tools/suggest
```
请求体：
```json
{
  "original_request": "生成一个标题和关键词"
}
```

### 生成工具计划
```
POST /api/tools/plan/generate
```
请求体：
```json
{
  "original_request": "生成一个标题和关键词",
  "task_id": "uuid"
}
```

## 工作流中心（v0.8）

### 创建工作流
```
POST /api/workflows/create
```
请求体：
```json
{
  "original_request": "生成一个标题和关键词"
}
```

### 获取工作流列表
```
GET /api/workflows
```

### 获取指定工作流
```
GET /api/workflows/{workflow_id}
```

### 更新工作流状态
```
POST /api/workflows/{workflow_id}/status
```
请求体：
```json
{
  "status": "running"
}
```

### 更新步骤状态
```
POST /api/workflows/{workflow_id}/step/{step_number}/status
```
请求体：
```json
{
  "status": "completed"
}
```

### 确认工作流
```
POST /api/workflows/{workflow_id}/confirm
```
请求体：
```json
{
  "confirmed_by": "admin"
}
```

## 日志中心（v0.9）

### 创建日志
```
POST /api/logs/create
```
请求体：
```json
{
  "log_type": "workflow",
  "source_module": "workflow_service",
  "source_id": "uuid",
  "action": "create_workflow",
  "status": "success",
  "message": "创建工作流",
  "risk_level": "low",
  "details": {}
}
```

### 获取所有日志
```
GET /api/logs
```

### 获取指定日志
```
GET /api/logs/{log_id}
```

### 按类型获取日志
```
GET /api/logs/type/{log_type}
```
支持的类型：task, tool, acceptance, workflow, risk, system

## 通用接口

### 健康检查
```
GET /health
```
响应：
```json
{
  "status": "healthy",
  "service": "product-b-ecommerce-api"
}
```

### API文档
```
GET /docs
```
提供Swagger UI交互式API文档

## 错误响应

所有接口在出错时返回统一格式：
```json
{
  "detail": "错误描述"
}
```

常见HTTP状态码：
- 200: 成功
- 404: 资源不存在
- 500: 服务器内部错误

## 安全说明

所有接口均遵循以下安全原则：
- 不保存账号密码
- 不自动登录商家后台
- 不自动执行高风险操作
- 高风险动作需要人工确认
- 所有操作记录日志
