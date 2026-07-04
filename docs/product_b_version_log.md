# 产品B版本记录

## v1.0 内部可用总体验收版
**发布日期：** 2026-07-04

### 新增功能
- 完成内部可用总体验收
- 新增启动说明文档
- 新增接口说明文档
- 新增总体验收报告
- 新增版本记录文档

### 已完成模块
- v0.5 任务中心
- v0.6 验收中心
- v0.7 工具中心
- v0.8 工作流中心
- v0.9 日志中心

### 核心能力
- 会拆任务
- 会选工具
- 会跑流程
- 会验收
- 会阻断风险
- 会记录过程

### 安全边界
- 无自动登录淘宝/天猫
- 无自动上架商品
- 无自动改价
- 无自动开车投放
- 无自动扣费
- 无账号密码保存
- 无真实外部API调用

### 已知问题
- task_service 和 tool_service 暂未写入日志（P2）

---

## v0.9 日志中心
**发布日期：** 2026-07-04

### 新增功能
- 日志数据模型（Log）
- 日志服务（LogService）
- 日志存储（log_records.json）
- 日志API接口
  - POST /api/logs/create
  - GET /api/logs
  - GET /api/logs/{log_id}
  - GET /api/logs/type/{log_type}

### 日志类型
- task
- tool
- acceptance
- workflow
- risk
- system

### 集成
- workflow_service 集成日志写入
- 创建工作流时写入日志
- 人工确认时写入风险日志

### 数据文件
- data/log_records.json

---

## v0.8 工作流中心
**发布日期：** 2026-07-04

### 新增功能
- 工作流数据模型（Workflow, WorkflowStep）
- 工作流服务（WorkflowService）
- 工作流存储（workflow_records.json）
- 工作流API接口
  - POST /api/workflows/create
  - GET /api/workflows
  - GET /api/workflows/{workflow_id}
  - POST /api/workflows/{workflow_id}/status
  - POST /api/workflows/{workflow_id}/step/{step_number}/status
  - POST /api/workflows/{workflow_id}/confirm

### 工作流步骤
- 任务创建
- 工具推荐
- 工具计划生成
- 内容生成
- 验收检查
- 风险检查
- 人工确认
- 归档

### 集成
- 集成任务中心（TaskService）
- 集成工具中心（ToolService）
- 高风险动作自动阻断
- 人工确认机制

### 数据文件
- data/workflow_records.json

---

## v0.7 工具中心
**发布日期：** 2026-07-04

### 新增功能
- 工具数据模型（Tool, ToolPlan, ExecutionStep）
- 工具服务（ToolService）
- 工具注册表（tool_registry.json）
- 工具计划存储（tool_plan_records.json）
- 工具API接口
  - GET /api/tools
  - POST /api/tools/suggest
  - POST /api/tools/plan/generate

### 内置工具
- title_generator - 标题生成器
- main_image_prompt_generator - 主图提示词生成器
- detail_screen_generator - 详情页生成器
- task_center - 任务中心
- acceptance_checker - 验收检查器

### 高风险动作阻断
- 自动登录
- 自动上架
- 自动改价
- 自动开车
- 开车投放
- 自动投放
- 自动改预算
- 自动扣费

### 数据文件
- data/tool_registry.json
- data/tool_plan_records.json

---

## v0.6 验收中心
**发布日期：** 2026-07-04

### 新增功能
- 验收报告数据模型（AcceptanceReport, AcceptanceIssue）
- 验收服务（AcceptanceService）
- 验收报告存储（acceptance_reports.json）
- 验收API接口
  - POST /api/acceptance/create
  - GET /api/acceptance
  - GET /api/acceptance/{report_id}

### 验收类型
- task - 任务验收
- tool_plan - 工具计划验收
- workflow - 工作流验收
- content - 内容生成验收

### 验收状态
- pending - 待验收
- passed - 通过
- failed - 未通过
- blocked - 阻断

### 数据文件
- data/acceptance_reports.json

---

## v0.5 任务中心
**发布日期：** 2026-07-04

### 新增功能
- 任务数据模型（Task, TaskStep）
- 任务服务（TaskService）
- 任务存储（task_records.json）
- 任务API接口
  - POST /api/tasks/create
  - GET /api/tasks
  - GET /api/tasks/{task_id}
  - POST /api/tasks/{task_id}/status

### 任务类型
- title_generation - 标题生成
- keyword_generation - 关键词生成
- image_prompt_generation - 图像提示词生成
- detail_screen_generation - 详情页生成
- listing_package_creation - 上架包创建
- content_creation - 内容创建
- product_optimization - 商品优化

### 任务步骤
- 自动拆解为执行步骤
- 步骤状态追踪
- 高风险步骤识别
- 人工确认机制

### 数据文件
- data/task_records.json

---

## v0.1 学习中心骨架版
**发布日期：** 2026-07-02

### 新增功能
- 学习中心基础接口
- 本地知识库存储
- 一句话任务拆解
- 无OPENAI_API_KEY启动

### 学习类型
- link - 链接学习
- text - 文本学习
- table - 表格学习
- review - 复盘学习

### 数据文件
- data/learning_targets.json
- data/merchant_profiles.json
- data/product_knowledge.json
- data/competitor_knowledge.json
- data/keyword_library.json
- data/visual_style_library.json
- data/review_records.json

### 依赖状态
- 已移除产品A硬依赖
- 可独立运行
