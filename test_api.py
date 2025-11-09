import requests

# Test the dashboard endpoint
response = requests.get("http://localhost:8000/dashboard")
data = response.json()

print("📊 BUSINESS DASHBOARD DATA")
print("==========================")
print(f"💰 Revenue: ${data['dashboard']['total_revenue']:,.2f}")
print(f"👥 Customers: {data['dashboard']['active_customers']}")
print(f"🛒 Transactions Today: {data['dashboard']['today_transactions']}")
print(f"📦 Pending Orders: {data['dashboard']['pending_orders']}")
print(f"🎯 Conversion Rate: {data['dashboard']['conversion_rate'] * 100:.1f}%")
print(f"🚀 Status: {data['dashboard']['business_status']}")

# Test customers endpoint
print("\n👥 CUSTOMER ANALYTICS")
print("====================")
cust_response = requests.get("http://localhost:8000/customers")
cust_data = cust_response.json()
print(f"Total Customers: {cust_data['analytics']['total_customers']}")
print(f"Satisfaction: {cust_data['analytics']['satisfaction_score']}")
print(f"AI Enhanced: {cust_data['render_enhanced']}")

# Test status
print("\n🌐 SYSTEM STATUS")
print("================")
status_response = requests.get("http://localhost:8000/status")
status_data = status_response.json()
print(f"Local API: {status_data['local_api']}")
print(f"Render API: {status_data['render_api']}")
