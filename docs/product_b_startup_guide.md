# 产品B启动说明

## 项目路径
```
/Users/linguanghai/CascadeProjects/product-b-ecommerce
```

## 启动方式

### 1. 安装依赖
```bash
cd /Users/linguanghai/CascadeProjects/product-b-ecommerce
pip install -r requirements.txt
```

### 2. 启动API服务器
```bash
cd /Users/linguanghai/CascadeProjects/product-b-ecommerce
python3 -m src.api.server
```

服务器将在 `http://localhost:8000` 启动

### 3. 验证启动
```bash
# 健康检查
curl http://localhost:8000/health

# API文档
curl http://localhost:8000/docs
```

## 无 OPENAI_API_KEY 启动支持

产品B支持无 OPENAI_API_KEY 启动，基础功能可正常运行：

```bash
# 无Key启动
unset OPENAI_API_KEY
python3 -m src.api.server
```

无Key启动时，系统会提供基础功能：
- 学习中心基础接口
- 本地知识库查询
- 任务中心基础功能
- 验收中心基础功能
- 工具中心基础功能
- 工作流中心基础功能
- 日志中心基础功能

## 本地 data 文件说明

产品B使用本地JSON文件存储，首次运行时会自动生成以下文件：

```
data/
├── learning_targets.json          # 学习目标记录
├── merchant_profiles.json         # 商家档案
├── product_knowledge.json         # 商品知识库
├── competitor_knowledge.json      # 竞品知识库
├── keyword_library.json           # 关键词库
├── visual_style_library.json      # 视觉风格库
├── review_records.json            # 复盘记录
├── title_generations.json         # 标题生成记录
├── keyword_generations.json       # 关键词生成记录
├── image_prompt_generations.json  # 图像提示词生成记录
├── listing_packages.json          # 上架包记录
├── detail_screen_generations.json # 详情页生成记录
├── video_script_generations.json  # 视频脚本生成记录
├── xiaohongshu_notes.json         # 小红书笔记记录
├── task_records.json              # 任务记录
├── acceptance_reports.json        # 验收报告
├── tool_registry.json             # 工具注册表
├── tool_plan_records.json         # 工具计划记录
├── workflow_records.json          # 工作流记录
└── log_records.json               # 日志记录
```

## 核心接口

### 健康检查
- `GET /health` - 系统健康检查
- `GET /docs` - API文档（Swagger UI）

### 学习中心
- `POST /api/learning/targets/create` - 创建学习目标
- `GET /api/learning/targets` - 获取学习目标列表
- `GET /api/learning/targets/{target_id}` - 获取指定学习目标
- `POST /api/learning/learn` - 执行学习

### 商家知识库
- `POST /api/knowledge/merchant-profile/create` - 创建商家档案
- `GET /api/knowledge/merchant-profiles` - 获取商家档案列表
- `POST /api/knowledge/product-knowledge/create` - 创建商品知识
- `GET /api/knowledge/product-knowledge` - 获取商品知识列表

### 上架包
- `POST /api/packages/create` - 创建上架包
- `GET /api/packages` - 获取上架包列表
- `GET /api/packages/{package_id}` - 获取指定上架包

### 详情页
- `POST /api/detail-screens/generate` - 生成详情页
- `GET /api/detail-screens` - 获取详情页生成记录
- `GET /api/detail-screens/{generation_id}` - 获取指定详情页

### 内容生成
- `POST /api/content/titles/generate` - 生成标题
- `POST /api/content/keywords/generate` - 生成关键词
- `POST /api/content/image-prompts/generate` - 生成图像提示词

### 任务中心（v0.5）
- `POST /api/tasks/create` - 创建任务
- `GET /api/tasks` - 获取任务列表
- `GET /api/tasks/{task_id}` - 获取指定任务
- `POST /api/tasks/{task_id}/status` - 更新任务状态

### 验收中心（v0.6）
- `POST /api/acceptance/create` - 创建验收报告
- `GET /api/acceptance` - 获取验收报告列表
- `GET /api/acceptance/{report_id}` - 获取指定验收报告

### 工具中心（v0.7）
- `GET /api/tools` - 获取工具列表
- `POST /api/tools/suggest` - 推荐工具
- `POST /api/tools/plan/generate` - 生成工具计划

### 工作流中心（v0.8）
- `POST /api/workflows/create` - 创建工作流
- `GET /api/workflows` - 获取工作流列表
- `GET /api/workflows/{workflow_id}` - 获取指定工作流
- `POST /api/workflows/{workflow_id}/status` - 更新工作流状态
- `POST /api/workflows/{workflow_id}/confirm` - 确认工作流

### 日志中心（v0.9）
- `POST /api/logs/create` - 创建日志
- `GET /api/logs` - 获取所有日志
- `GET /api/logs/{log_id}` - 获取指定日志
- `GET /api/logs/type/{log_type}` - 按类型获取日志

## 安全边界

**禁止真实执行：**
- ❌ 自动登录淘宝/天猫
- ❌ 自动上架商品
- ❌ 自动改价
- ❌ 自动开车投放
- ❌ 自动投放
- ❌ 自动扣费
- ❌ 保存账号密码
- ❌ 真实调用外部API

**安全策略：**
- ✅ 只生成建议和待确认任务
- ✅ 高风险动作自动阻断
- ✅ 需要人工确认才能执行高风险操作
- ✅ 所有操作记录日志
- ✅ 本地数据存储，不上传云端

## 故障排查

### 端口占用
如果8000端口被占用，可以修改启动端口：
```bash
python3 -m src.api.server --port 8001
```

### 权限问题
确保data目录有写入权限：
```bash
chmod -R 755 data/
```
