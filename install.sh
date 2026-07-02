#!/bin/bash
# 产品B电商自动化系统 - 一键安装脚本

echo "=========================================="
echo "产品B电商自动化系统"
echo "=========================================="
echo ""

# 检查Python版本
echo "[1] 检查Python版本..."
python3 --version
if [ $? -ne 0 ]; then
    echo "错误: 未找到Python3，请先安装Python 3.8+"
    exit 1
fi
echo "✓ Python检查通过"
echo ""

# 安装依赖
echo "[2] 安装依赖..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误: 依赖安装失败"
    exit 1
fi
echo "✓ 依赖安装完成"
echo ""

# 创建环境变量文件
echo "[3] 配置环境变量..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ 已创建.env文件，请编辑配置API密钥"
else
    echo "✓ .env文件已存在"
fi
echo ""

# 检查产品A模块路径
echo "[4] 检查产品A模块路径..."
PRODUCT_A_PATH="../autonomous-ai-agent"
if [ -d "$PRODUCT_A_PATH" ]; then
    echo "✓ 产品A模块路径存在"
else
    echo "⚠ 警告: 产品A模块路径不存在: $PRODUCT_A_PATH"
    echo "  请确保产品A项目在正确位置"
fi
echo ""

echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "使用方法:"
echo "1. 编辑 .env 文件配置LLM API密钥（可选，默认使用Mock）"
echo "2. 运行主应用: python3 src/main.py"
echo "3. 启动API服务器: python3 src/api/server.py"
echo ""
echo "API文档: http://localhost:8000/docs"
echo ""
