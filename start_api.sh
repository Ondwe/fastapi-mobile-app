#!/bin/bash

# Kill any existing uvicorn processes
echo "🔄 Stopping any existing API servers..."
pkill -f "uvicorn" 2>/dev/null
sleep 2

# Find available port
find_available_port() {
    for port in {8000..8010}; do
        if ! lsof -i :$port > /dev/null 2>&1; then
            echo $port
            return
        fi
    done
    echo 8000
}

PORT=$(find_available_port)
API_FILE="main_mobile.py"

# Check which API file exists
if [ -f "main_unified.py" ]; then
    API_FILE="main_unified.py"
    echo "🎯 Using Unified API"
elif [ -f "main_connected.py" ]; then
    API_FILE="main_connected.py" 
    echo "🎯 Using Connected API"
elif [ -f "main_mobile.py" ]; then
    API_FILE="main_mobile.py"
    echo "🎯 Using Mobile Business API"
else
    echo "❌ No API file found. Using simple API."
    API_FILE="simple_api.py"
fi

echo "🚀 Starting $API_FILE on port $PORT..."
uvicorn ${API_FILE%.py}:app --host 0.0.0.0 --port $PORT --reload &

# Wait for server to start
sleep 3

# Test the server
echo "🧪 Testing API..."
if curl -s http://localhost:$PORT/health > /dev/null; then
    echo "✅ API is running successfully!"
    echo "📚 Documentation: http://localhost:$PORT/docs"
    echo "🌐 Local URL: http://localhost:$PORT"
    echo "📱 Network URL: http://$(hostname -I | awk '{print $1}'):$PORT"
    
    # Save the port for other scripts
    echo $PORT > ~/.api_port
else
    echo "❌ API failed to start. Check logs above."
fi
