#!/bin/bash

# AI Harmonizer 快速测试脚本
# 使用方法: ./test-ai.sh

echo "🤖 AI Harmonizer 测试脚本"
echo "=========================="
echo ""

# 1. 检查端口占用
echo "📍 Step 1: 检查端口 3000..."
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "   ⚠️  端口 3000 已被占用，尝试 kill..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    sleep 1
fi

# 2. 启动服务器
echo ""
echo "🚀 Step 2: 启动开发服务器..."
echo "   使用: npx serve . -p 3000"
echo ""

npx serve . -p 3000 &
SERVER_PID=$!

echo "   ✓ 服务器已启动 (PID: $SERVER_PID)"

# 等待服务器启动
sleep 3

# 3. 打开浏览器
echo ""
echo "🌐 Step 3: 打开浏览器..."
TEST_URL="http://localhost:3000/test-ai-harmonizer.html"

if command -v open &> /dev/null; then
    # macOS
    open "$TEST_URL"
    echo "   ✓ 已打开 Safari/Chrome"
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open "$TEST_URL"
    echo "   ✓ 已打开默认浏览器"
elif command -v start &> /dev/null; then
    # Windows Git Bash
    start "$TEST_URL"
    echo "   ✓ 已打开默认浏览器"
else
    echo "   ⚠️  无法自动打开浏览器"
    echo "   请手动访问: $TEST_URL"
fi

echo ""
echo "=========================="
echo "✅ 准备完成！"
echo ""
echo "📋 测试步骤:"
echo "   1. 在浏览器中打开 F12 (开发者工具)"
echo "   2. 切换到 Console 标签"
echo "   3. 依次点击 4 个按钮："
echo "      - Step 1: Check Dependencies"
echo "      - Step 2: Load Model"
echo "      - Step 3: Generate Harmony"
echo "      - Step 4: Play Audio"
echo ""
echo "📖 详细文档: docs/AI_VERIFICATION_RESULTS.md"
echo ""
echo "🛑 停止服务器: Ctrl+C 或运行 'kill $SERVER_PID'"
echo ""

# 保持脚本运行
wait $SERVER_PID
