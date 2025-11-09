import requests
import json
from datetime import datetime

class ProductionBusinessClient:
    def __init__(self, base_url="https://fastapi-mobile-app.onrender.com"):
        self.base_url = base_url
    
    def get_business_overview(self):
        """Get complete business overview from production API"""
        try:
            print("🏢 PRODUCTION BUSINESS DASHBOARD")
            print("================================")
            print(f"API: {self.base_url}")
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print()
            
            # Test connection
            health_response = requests.get(f"{self.base_url}/health", timeout=10)
            print("🔗 Connection Status:")
            print(f"   Health: ✅ ({health_response.status_code})")
            if health_response.status_code == 200:
                health_data = health_response.json()
                print(f"   Version: {health_data.get('version', 'Unknown')}")
                print(f"   Service: {health_data.get('service', health_data.get('message', 'Unknown'))}")
            print()
            
            # Get dashboard data
            print("📊 BUSINESS INTELLIGENCE:")
            dash_response = requests.get(f"{self.base_url}/dashboard", timeout=10)
            if dash_response.status_code == 200:
                dash_data = dash_response.json()
                dashboard = dash_data['dashboard']
                
                print(f"   💰 Revenue: ${dashboard['total_revenue']:,.2f}")
                print(f"   👥 Customers: {dashboard['active_customers']}")
                print(f"   🛒 Transactions Today: {dashboard['today_transactions']}")
                print(f"   📦 Pending Orders: {dashboard['pending_orders']}")
                print(f"   🎯 Conversion Rate: {dashboard['conversion_rate'] * 100:.1f}%")
                print(f"   🚀 Business Status: {dashboard['business_status']}")
                print(f"   🤖 AI Enhanced: {dash_data['render_enhanced']}")
            else:
                print("   ❌ Could not fetch dashboard")
            print()
            
            # Get customer data
            print("👥 CUSTOMER ANALYTICS:")
            cust_response = requests.get(f"{self.base_url}/customers", timeout=10)
            if cust_response.status_code == 200:
                cust_data = cust_response.json()
                analytics = cust_data['analytics']
                
                print(f"   Total Customers: {analytics['total_customers']}")
                print(f"   Satisfaction: {analytics['satisfaction_score']}")
                print(f"   🤖 AI Enhanced: {cust_data['render_enhanced']}")
            else:
                print("   ❌ Could not fetch customer data")
            print()
            
            print("🌐 API ENDPOINTS AVAILABLE:")
            print("   /dashboard  - Business metrics")
            print("   /customers  - Customer analytics") 
            print("   /health     - System status")
            print("   /docs       - API documentation")
            
        except Exception as e:
            print(f"❌ Error: {e}")

# Run the production client
client = ProductionBusinessClient()
client.get_business_overview()
