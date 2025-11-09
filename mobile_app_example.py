import requests
import time

class MobileBusinessApp:
    def __init__(self):
        self.api_url = "http://localhost:8000"
    
    def refresh_dashboard(self):
        """Refresh mobile dashboard data"""
        try:
            response = requests.get(f"{self.api_url}/dashboard")
            data = response.json()
            
            print("📱 MOBILE BUSINESS APP")
            print("======================")
            print(f"🕒 Last update: {time.strftime('%H:%M:%S')}")
            print()
            
            dash = data['dashboard']
            print(f"💰 Revenue: ${dash['total_revenue']:,.2f}")
            print(f"👥 Customers: {dash['active_customers']}")
            print(f"🛒 Today's Sales: {dash['today_transactions']}")
            print(f"📦 Orders: {dash['pending_orders']} pending")
            print(f"🎯 Conversion: {dash['conversion_rate'] * 100:.1f}%")
            print(f"🚀 Status: {dash['business_status']}")
            
            # Check AI status
            if data['render_enhanced']:
                print("\n🤖 AI Insights: Available")
            else:
                print("\nℹ️  AI Insights: Local data")
                
        except Exception as e:
            print(f"❌ Error: {e}")

# Simulate mobile app
app = MobileBusinessApp()
app.refresh_dashboard()
