#!/bin/bash

echo "🚀 QUICK API START"
echo "=================="

# Kill existing processes
echo "🔄 Stopping existing servers..."
pkill -f "uvicorn" 2>/dev/null
pkill -f "python" 2>/dev/null
sleep 2

# Start API
echo "🎯 Starting Connected Business API..."
cd /data/data/com.termux/files/home/fastapi-clean
source venv/bin/activate
uvicorn main_connected_fixed:app --host 0.0.0.0 --port 8000 --reload &

# Wait for startup
echo "⏳ Waiting for API to start..."
sleep 5

# Test connection
echo "🧪 Testing API..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ SUCCESS! API is running on http://localhost:8000"
    echo "📚 Docs: http://localhost:8000/docs"
    echo "📊 Dashboard: http://localhost:8000/dashboard"
else
    echo "❌ FAILED! API did not start properly"
    echo "💡 Check the logs in the other terminal"
fi
