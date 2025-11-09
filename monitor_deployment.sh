#!/bin/bash

RENDER_URL="https://fastapi-mobile-app.onrender.com"
echo "🔍 MONITORING RENDER DEPLOYMENT"
echo "================================"

for i in {1..10}; do
    echo ""
    echo "🔄 Check #$i - $(date '+%H:%M:%S')"
    
    # Test health endpoint
    health_response=$(curl -s --max-time 10 "$RENDER_URL/health")
    if [ $? -eq 0 ]; then
        echo "✅ Health endpoint responding"
        
        # Check if it's the new API
        if echo "$health_response" | grep -q "Connected Business API"; then
            echo "🎯 NEW CONNECTED API DETECTED!"
            echo "🚀 Deployment successful!"
            
            # Test new endpoints
            echo ""
            echo "🧪 Testing new endpoints:"
            for endpoint in "/dashboard" "/customers" "/status"; do
                echo -n "🔍 $endpoint: "
                if curl -s --max-time 5 "$RENDER_URL$endpoint" > /dev/null; then
                    echo "✅ WORKING"
                else
                    echo "❌ FAILED"
                fi
            done
            break
        else
            echo "🔄 Old API still running - waiting for deployment..."
        fi
    else
        echo "❌ Health endpoint not responding - deployment in progress"
    fi
    
    sleep 30
done

echo ""
echo "📊 Final deployment status:"
curl -s "$RENDER_URL/health" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print('Service:', data.get('service', 'Unknown'))
    print('Version:', data.get('version', 'Unknown'))
    print('Status:', data.get('status', 'Unknown'))
except:
    print('Could not parse response')
"
