#!/bin/bash

echo "📱 BUSINESS DASHBOARD - LIVE TERMINAL VIEW"
echo "==========================================="
echo "Refreshing every 5 seconds... (Ctrl+C to stop)"
echo ""

while true; do
    # Clear screen and show header
    clear
    echo "📱 BUSINESS DASHBOARD - LIVE TERMINAL VIEW"
    echo "==========================================="
    echo "Last updated: $(date '+%H:%M:%S')"
    echo ""
    
    # Get dashboard data
    DATA=$(curl -s http://localhost:8001/dashboard)
    
    if [ $? -eq 0 ]; then
        # Extract and display data
        revenue=$(echo $DATA | grep -o '"total_revenue":[0-9]*[.]?[0-9]*' | cut -d: -f2)
        customers=$(echo $DATA | grep -o '"active_customers":[0-9]*' | cut -d: -f2)
        transactions=$(echo $DATA | grep -o '"today_transactions":[0-9]*' | cut -d: -f2)
        pending=$(echo $DATA | grep -o '"pending_orders":[0-9]*' | cut -d: -f2)
        conversion=$(echo $DATA | grep -o '"conversion_rate":[0-9]*[.]?[0-9]*' | cut -d: -f2)
        status=$(echo $DATA | grep -o '"business_status":"[^"]*' | cut -d\" -f4)
        
        echo "💰  Revenue:        \$$revenue"
        echo "👥  Customers:      $customers"
        echo "🛒  Transactions:   $transactions"
        echo "📦  Pending Orders: $pending"
        echo "🎯  Conversion:     $(echo "scale=1; $conversion * 100" | bc)%"
        echo "🚀  Status:         $status"
        
        # Show quick stats
        quick_stats=$(curl -s http://localhost:8001/dashboard | grep -o '"quick_stats":[^}]*')
        target_progress=$(echo $quick_stats | grep -o '"target_progress":[0-9]*[.]?[0-9]*' | cut -d: -f2)
        active_sessions=$(echo $quick_stats | grep -o '"active_sessions":[0-9]*' | cut -d: -f2)
        
        echo ""
        echo "📈 QUICK STATS:"
        echo "   Daily Target Progress: ${target_progress}%"
        echo "   Active Sessions: $active_sessions"
        
    else
        echo "❌ Could not connect to API server"
        echo "   Make sure your FastAPI app is running:"
        echo "   uvicorn main_mobile:app --host 0.0.0.0 --port 8001 --reload"
    fi
    
    echo ""
    echo "⏳ Refreshing in 5 seconds..."
    sleep 5
done
