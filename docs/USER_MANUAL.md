# 产品B电商自动化系统 使用说明书

## 目录
1. [产品介绍](#产品介绍)
2. [系统要求](#系统要求)
3. [安装部署](#安装部署)
4. [配置说明](#配置说明)
5. [快速开始](#快速开始)
6. [功能使用](#功能使用)
7. [API接口](#api接口)
8. [常见问题](#常见问题)

---

## 产品介绍

产品B电商自动化系统是一款面向天猫、抖音商家的电商智能自动化平台，提供智能产品规划、代码生成、数据分析等核心能力。

**核心功能：**
- 🤖 **智能产品规划** - AI辅助生成电商平台产品规划
- 💻 **代码生成** - 自动生成API、业务逻辑代码
- 📊 **数据分析** - 销售数据分析、热销商品统计、平台表现分析
- 🛒 **商品管理** - 商品CRUD、搜索、分类管理
- 📦 **订单管理** - 订单创建、状态跟踪、查询统计
- 🎯 **智能编排** - 多任务智能编排和执行

**技术架构：**
- AI模块：CognitiveOrchestrator、StrategyEngine、CodeCrafter
- 业务服务：商品服务、订单服务、分析服务
- API接口：RESTful API（FastAPI）
- LLM集成：支持OpenAI、Anthropic、Mock

---

## 系统要求

### 软件要求
- Python 3.8+
- pip3 包管理器

### 硬件要求
- CPU: 2核及以上
- 内存: 4GB及以上
- 磁盘: 500MB可用空间

### 依赖要求
- 产品A模块（autonomous-ai-agent）需在同级目录

---

## 安装部署

### 方式一：一键安装（推荐）

```bash
# 进入项目目录
cd product-b-ecommerce

# 运行安装脚本
./install.sh
```

安装脚本会自动完成：
1. 检查Python版本
2. 安装所有依赖包
3. 创建环境变量配置文件
4. 检查产品A模块路径

### 方式二：手动安装

```bash
# 1. 进入项目目录
cd product-b-ecommerce

# 2. 安装依赖
pip3 install -r requirements.txt

# 3. 复制环境变量模板
cp .env.example .env

# 4. 编辑.env文件配置LLM API（可选）
vim .env
```

### 依赖说明

**必需依赖：**
- fastapi - Web框架
- uvicorn - ASGI服务器
- pydantic - 数据验证

**可选依赖：**
- openai - OpenAI API客户端
- anthropic - Anthropic API客户端
- sqlalchemy - ORM框架
- pymysql - MySQL驱动

---

## 配置说明

### 环境变量配置

编辑`.env`文件：

```bash
# LLM提供商: openai, anthropic, mock
LLM_PROVIDER=mock

# LLM API密钥（使用真实API时需要）
LLM_API_KEY=your_api_key_here

# LLM模型名称
# OpenAI: gpt-4, gpt-3.5-turbo
# Anthropic: claude-3-opus-20240229, claude-3-sonnet-20240229
LLM_MODEL=

# LLM参数
LLM_MAX_TOKENS=2048
LLM_TEMPERATURE=0.7
LLM_TIMEOUT=30
```

### LLM提供商选择

**Mock模式（默认）**
- 无需API密钥
- 适用于测试和演示
- 返回模拟响应

**OpenAI模式**
```bash
LLM_PROVIDER=openai
LLM_API_KEY=sk-xxx...
LLM_MODEL=gpt-4
```

**Anthropic模式**
```bash
LLM_PROVIDER=anthropic
LLM_API_KEY=sk-ant-xxx...
LLM_MODEL=claude-3-opus-20240229
```

---

## 快速开始

### 运行主应用

```bash
python3 src/main.py
```

运行后会演示完整工作流：
1. 智能产品规划
2. 代码生成
3. 智能任务执行
4. 业务服务演示（商品、订单、数据分析）

### 启动API服务器

```bash
python3 src/api/server.py
```

服务器启动后访问：
- API文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

---

## 功能使用

### 1. 商品管理

#### 创建商品
```bash
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "智能手表",
    "description": "多功能智能手表，支持健康监测",
    "price": 299.99,
    "stock": 100,
    "category": "数码",
    "platform": "taobao"
  }'
```

#### 搜索商品
```bash
curl "http://localhost:8000/api/products?keyword=智能&limit=10"
```

#### 更新商品
```bash
curl -X PUT http://localhost:8000/api/products/{product_id} \
  -H "Content-Type: application/json" \
  -d '{"price": 199.99, "stock": 50}'
```

#### 删除商品
```bash
curl -X DELETE http://localhost:8000/api/products/{product_id}
```

### 2. 订单管理

#### 创建订单
```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user001",
    "items": [
      {
        "product_id": "xxx",
        "product_name": "智能手表",
        "quantity": 2,
        "price": 299.99
      }
    ],
    "shipping_address": "北京市朝阳区",
    "payment_method": "alipay",
    "platform": "taobao"
  }'
```

#### 查询订单
```bash
curl "http://localhost:8000/api/orders?user_id=user001"
```

#### 更新订单状态
```bash
curl -X PUT http://localhost:8000/api/orders/{order_id}/status \
  -H "Content-Type: application/json" \
  -d '{"status": "paid"}'
```

### 3. 数据分析

#### 获取销售摘要
```bash
curl "http://localhost:8000/api/analytics/sales-summary?days=7"
```

#### 获取热销商品
```bash
curl "http://localhost:8000/api/analytics/top-products?limit=10"
```

#### 获取平台表现
```bash
curl "http://localhost:8000/api/analytics/platform-performance?days=30"
```

#### 生成日报
```bash
curl "http://localhost:8000/api/analytics/report?days=7"
```

---

## API接口

### 基础信息
- **Base URL**: `http://localhost:8000`
- **数据格式**: JSON
- **字符编码**: UTF-8

### 端点列表

#### 健康检查
- `GET /health` - 服务健康状态

#### 商品API
- `POST /api/products` - 创建商品
- `GET /api/products/{product_id}` - 获取商品详情
- `PUT /api/products/{product_id}` - 更新商品
- `DELETE /api/products/{product_id}` - 删除商品
- `GET /api/products` - 搜索商品

#### 订单API
- `POST /api/orders` - 创建订单
- `GET /api/orders/{order_id}` - 获取订单详情
- `PUT /api/orders/{order_id}/status` - 更新订单状态
- `GET /api/orders` - 查询订单列表

#### 数据分析API
- `GET /api/analytics/sales-summary` - 销售摘要
- `GET /api/analytics/top-products` - 热销商品
- `GET /api/analytics/platform-performance` - 平台表现
- `GET /api/analytics/report` - 生成日报

### 交互式文档
访问 http://localhost:8000/docs 查看完整的API文档和在线测试工具。

---

## 常见问题

### Q1: 安装时提示找不到产品A模块？
**A**: 确保产品A（autonomous-ai-agent）项目在产品B的上级目录：
```
CascadeProjects/
├── autonomous-ai-agent/
└── product-b-ecommerce/
```

### Q2: 如何切换到真实的LLM API？
**A**: 编辑`.env`文件，设置`LLM_PROVIDER`为`openai`或`anthropic`，并配置相应的API密钥。

### Q3: API服务器启动失败？
**A**: 检查端口8000是否被占用，或修改`src/api/server.py`中的端口号。

### Q4: 数据存储在哪里？
**A**: 当前版本使用内存存储，重启后数据会丢失。生产环境建议接入数据库。

### Q5: 如何部署到生产环境？
**A**: 
1. 配置真实LLM API
2. 接入数据库（MySQL/PostgreSQL）
3. 使用进程管理器（如supervisor）
4. 配置Nginx反向代理
5. 启用HTTPS

### Q6: 支持哪些电商平台？
**A**: 当前支持天猫、抖音等平台，可通过`platform`参数扩展。

### Q7: 如何自定义AI提示词？
**A**: 修改`src/main.py`中的LLM调用参数，或扩展相应的服务类。

---

## 技术支持

- **项目地址**: https://github.com/1010958075a-eng/crispy-couscous
- **问题反馈**: 通过GitHub Issues提交
- **更新日志**: 参考项目README.md

---

## 版本信息

- **当前版本**: 1.0.0
- **发布日期**: 2026-07-01
- **Python版本**: 3.8+

---

## 许可证

产品A专有
