import requests
import json
from datetime import datetime

class BusinessAPIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def get_dashboard(self):
        """Get business dashboard data"""
        response = requests.get(f"{self.base_url}/dashboard")
        return response.json()
    
    def get_customers(self):
        """Get customer analytics"""
        response = requests.get(f"{self.base_url}/customers")
        return response.json()
    
    def get_transactions(self, limit=5):
        """Get recent transactions"""
        response = requests.get(f"{self.base_url}/transactions?limit={limit}")
        return response.json()
    
    def get_revenue(self, days=7):
        """Get revenue data"""
        response = requests.get(f"{self.base_url}/revenue?days={days}")
        return response.json()
    
    def get_status(self):
        """Get system status"""
        response = requests.get(f"{self.base_url}/status")
        return response.json()
    
    def display_summary(self):
        """Display comprehensive business summary"""
        print("🏢 BUSINESS INTELLIGENCE DASHBOARD")
        print("==================================")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Dashboard data
        dash = self.get_dashboard()
        dashboard = dash['dashboard']
        print("📊 KEY METRICS:")
        print(f"   💰 Revenue: ${dashboard['total_revenue']:,.2f}")
        print(f"   👥 Customers: {dashboard['active_customers']}")
        print(f"   🛒 Transactions Today: {dashboard['today_transactions']}")
        print(f"   📦 Pending Orders: {dashboard['pending_orders']}")
        print(f"   🎯 Conversion: {dashboard['conversion_rate'] * 100:.1f}%")
        print(f"   🚀 Status: {dashboard['business_status']}")
        print()
        
        # Customer data
        cust = self.get_customers()
        analytics = cust['analytics']
        print("👥 CUSTOMER ANALYTICS:")
        print(f"   Total: {analytics['total_customers']}")
        print(f"   New Today: {analytics['new_customers_today']}")
        print(f"   Repeat: {analytics['repeat_customers']}")
        print(f"   Satisfaction: {analytics['satisfaction_score']}")
        print(f"   🤖 AI Enhanced: {cust['render_enhanced']}")
        print()
        
        # System status
        status = self.get_status()
        print("🌐 SYSTEM STATUS:")
        print(f"   Local API: {status['local_api']}")
        print(f"   Render API: {status['render_api']}")
        print(f"   Connected System: {status['connected_system']}")

# Create client and display summary
client = BusinessAPIClient()
client.display_summary()
