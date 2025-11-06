from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse as urlparse
from payment_handlers import PaymentAPI
from admin import HumbuAdmin
from crm import HumbuCRM
from sms_notifications import HumbuSMS
from sms_templates import SMSTemplates

class HumbuAPIHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.db = HumbuDatabase()
        self.payment_api = PaymentAPI(self.db)
        self.admin = HumbuAdmin(self.db)
        self.crm = HumbuCRM(self.db)
        self.sms = HumbuSMS(self.db)
        super().__init__(*args, **kwargs)
    
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers(200)
    
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        path_parts = parsed_path.path.split('/')
        
        # API Routes
        if parsed_path.path == '/api/products':
            self.get_products()
        elif parsed_path.path.startswith('/api/products/') and len(path_parts) >= 4:
            product_id = path_parts[3]
            self.get_product(product_id)
        elif parsed_path.path == '/api/orders':
            self.get_orders()
        elif parsed_path.path == '/api/payment/methods':
            self.get_payment_methods()
        elif parsed_path.path.startswith('/api/payment/status/') and len(path_parts) >= 5:
            order_id = path_parts[4]
            self.get_payment_status(order_id)
        elif parsed_path.path == '/api/admin/analytics':
            self.get_admin_analytics()
        elif parsed_path.path == '/api/admin/orders':
            self.get_admin_orders()
        elif parsed_path.path == '/api/admin/payments':
            self.get_admin_payments()
        elif parsed_path.path == '/api/admin/products':
            self.get_admin_products()
        elif parsed_path.path == '/api/crm/analytics':
            self.get_crm_analytics()
        elif parsed_path.path == '/api/crm/top-customers':
            self.get_top_customers()
        elif parsed_path.path == '/api/crm/customers':
            self.get_all_customers()
        elif parsed_path.path.startswith('/api/crm/customer/') and len(path_parts) >= 5:
            customer_phone = path_parts[4]
            self.get_customer_details(customer_phone)
        elif parsed_path.path == '/api/sms/analytics':
            self.get_sms_analytics()
        elif parsed_path.path == '/api/sms/test':
            self.test_sms()
        elif parsed_path.path == '/crm':
            self.serve_crm_dashboard()
        elif parsed_path.path == '/admin':
            self.serve_admin_dashboard()
        elif parsed_path.path == '/api/health':
            self.health_check()
        elif parsed_path.path == '/':
            self.serve_homepage()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        parsed_path = urlparse.urlparse(self.path)
        
        if parsed_path.path == '/api/orders':
            self.create_order(post_data)
        elif parsed_path.path == '/api/products':
            self.create_product(post_data)
        elif parsed_path.path == '/api/payment/process':
            self.process_payment(post_data)
        elif parsed_path.path == '/api/admin/orders/update':
            self.update_order_status(post_data)
        elif parsed_path.path == '/api/crm/sync':
            self.sync_customers()
        elif parsed_path.path == '/api/crm/customer/note':
            self.add_customer_note(post_data)
        elif parsed_path.path == '/api/sms/send':
            self.send_sms_notification(post_data)
        elif parsed_path.path == '/api/sms/broadcast':
            self.send_broadcast_sms(post_data)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
    
    def get_sms_analytics(self):
        """Get SMS analytics"""
        try:
            analytics = self.sms.get_sms_analytics()
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "data": analytics
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def test_sms(self):
        """Test SMS functionality"""
        try:
            # Send a test SMS
            result = self.sms.send_sms("0794658481", "📱 Test SMS from Humbu Platform - SMS system is working!")
            
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "message": "Test SMS sent",
                "result": result
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def send_sms_notification(self, post_data):
        """Send SMS notification"""
        try:
            data = json.loads(post_data.decode())
            
            required_fields = ['phone_number', 'message']
            for field in required_fields:
                if field not in data:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": f"Missing field: {field}"}).encode())
                    return
            
            result = self.sms.send_sms(
                data['phone_number'], 
                data['message'],
                data.get('provider', 'simulated')
            )
            
            self._set_headers(200 if result['success'] else 400)
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def send_broadcast_sms(self, post_data):
        """Send broadcast SMS to multiple customers"""
        try:
            data = json.loads(post_data.decode())
            
            if 'message' not in data:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Missing message"}).encode())
                return
            
            # Get phone numbers from different sources
            phone_numbers = []
            
            if data.get('send_to_all_customers'):
                customers = self.crm.get_all_customers()
                phone_numbers = [customer['phone'] for customer in customers if customer['phone']]
            
            elif data.get('customer_phones'):
                phone_numbers = data['customer_phones']
            
            elif data.get('customer_type'):
                customers = self.crm.get_all_customers(data['customer_type'])
                phone_numbers = [customer['phone'] for customer in customers if customer['phone']]
            
            if not phone_numbers:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "No phone numbers found"}).encode())
                return
            
            # Send SMS to each phone number
            results = []
            for phone in phone_numbers[:10]:  # Limit to 10 for demo
                result = self.sms.send_sms(phone, data['message'])
                results.append({
                    'phone': phone,
                    'success': result['success'],
                    'message_id': result.get('message_id')
                })
            
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "message": f"SMS sent to {len(results)} customers",
                "results": results
            }).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def serve_crm_dashboard(self):
        """Serve the CRM dashboard"""
        try:
            with open('customer_management.html', 'r') as f:
                html_content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())
        except:
            self._set_headers(404)
            self.wfile.write(b'CRM dashboard not found')
    
    def get_crm_analytics(self):
        """Get CRM analytics"""
        try:
            analytics = self.crm.get_customer_analytics()
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "data": analytics
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def get_top_customers(self):
        """Get top customers"""
        try:
            analytics = self.crm.get_customer_analytics()
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "top_customers": analytics['top_customers']
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def get_all_customers(self):
        """Get all customers with optional filter"""
        try:
            query_params = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            customer_type = query_params.get('type', [None])[0]
            
            customers = self.crm.get_all_customers(customer_type)
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "customers": customers
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def get_customer_details(self, customer_phone):
        """Get customer details with orders and interactions"""
        try:
            customer = self.crm.get_customer_by_phone(customer_phone)
            if not customer:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Customer not found"}).encode())
                return
            
            orders = self.crm.get_customer_orders(customer_phone)
            interactions = self.crm.get_customer_interactions(customer['id'])
            
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "details": customer,
                "orders": orders,
                "interactions": interactions
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def sync_customers(self):
        """Sync customers from existing orders"""
        try:
            synced_count = self.crm.sync_customers_from_orders()
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "message": "Customers synced successfully",
                "synced_count": synced_count
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def add_customer_note(self, post_data):
        """Add note to customer"""
        try:
            data = json.loads(post_data.decode())
            self.crm.add_customer_note(data['customer_id'], data['note'])
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "message": "Note added successfully"
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def serve_admin_dashboard(self):
        """Serve the admin dashboard"""
        try:
            with open('admin_dashboard.html', 'r') as f:
                html_content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode())
        except:
            self._set_headers(404)
            self.wfile.write(b'Admin dashboard not found')
    
    def get_admin_analytics(self):
        """Get business analytics for admin dashboard"""
        try:
            analytics = self.admin.get_business_analytics()
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "data": analytics
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def get_admin_orders(self):
        """Get all orders for admin"""
        try:
            orders = self.admin.get_all_orders()
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "data": orders
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def get_admin_payments(self):
        """Get payment data for admin"""
        try:
            analytics = self.admin.get_business_analytics()
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "recent_transactions": analytics['recent_transactions'],
                "payment_breakdown": analytics['payment_breakdown']
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def get_admin_products(self):
        """Get product analytics for admin"""
        try:
            products = self.admin.get_product_analytics()
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "data": products
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def update_order_status(self, post_data):
        """Update order status"""
        try:
            data = json.loads(post_data.decode())
            result = self.admin.update_order_status(data['order_id'], data['status'])
            self._set_headers(200)
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def get_payment_methods(self):
        """Get available payment methods"""
        result = self.payment_api.handle_payment_methods()
        self._set_headers(result['status'])
        self.wfile.write(json.dumps(result['body']).encode())
    
    def process_payment(self, post_data):
        """Process payment for an order"""
        result = self.payment_api.handle_process_payment(post_data)
        self._set_headers(result['status'])
        self.wfile.write(json.dumps(result['body']).encode())
    
    def get_payment_status(self, order_id):
        """Get payment status for an order"""
        result = self.payment_api.handle_payment_status(order_id)
        self._set_headers(result['status'])
        self.wfile.write(json.dumps(result['body']).encode())
    
    def get_products(self):
        """Get all products"""
        try:
            products = self.db.execute_query('''
                SELECT * FROM products WHERE is_active = 1 ORDER BY created_at DESC
            ''')
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "data": products,
                "business": "Humbu Wandeme Trading Enterprise"
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def get_product(self, product_id):
        """Get single product by ID"""
        try:
            products = self.db.execute_query(
                'SELECT * FROM products WHERE id = ? AND is_active = 1',
                (product_id,)
            )
            if products:
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    "success": True,
                    "data": products[0]
                }).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Product not found"}).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def create_order(self, post_data):
        """Create new order and send SMS notification"""
        try:
            data = json.loads(post_data.decode())
            
            # Validate required fields
            required_fields = ['customer_name', 'customer_phone', 'items']
            for field in required_fields:
                if field not in data:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": f"Missing field: {field}"}).encode())
                    return
            
            # Calculate total amount
            total_amount = 0
            for item in data['items']:
                product = self.db.execute_query(
                    'SELECT price FROM products WHERE id = ?',
                    (item['product_id'],)
                )
                if product:
                    total_amount += product[0]['price'] * item['quantity']
            
            # Create order
            result = self.db.execute_query('''
                INSERT INTO orders (customer_name, customer_email, customer_phone, total_amount)
                VALUES (?, ?, ?, ?)
            ''', (data['customer_name'], data.get('customer_email'), data['customer_phone'], total_amount))
            
            order_id = result['lastrowid']
            
            # Add order items
            for item in data['items']:
                product = self.db.execute_query(
                    'SELECT price FROM products WHERE id = ?',
                    (item['product_id'],)
                )
                if product:
                    self.db.execute_query('''
                        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                        VALUES (?, ?, ?, ?)
                    ''', (order_id, item['product_id'], item['quantity'], product[0]['price']))
            
            # Sync customer to CRM
            self.crm.create_or_update_customer(
                name=data['customer_name'],
                phone=data['customer_phone'],
                email=data.get('customer_email'),
                source='order_creation'
            )
            
            # Update customer stats
            self.crm.update_customer_stats(data['customer_phone'])
            
            # Send order confirmation SMS
            order_data = {
                'customer_name': data['customer_name'],
                'customer_phone': data['customer_phone'],
                'order_id': order_id,
                'total_amount': total_amount
            }
            sms_result = self.sms.send_order_notification(order_data, 'order_confirm')
            
            self._set_headers(201)
            self.wfile.write(json.dumps({
                "success": True,
                "message": "Order created successfully",
                "order_id": order_id,
                "total_amount": total_amount,
                "business": "Humbu Wandeme Trading Enterprise",
                "sms_sent": sms_result['success'],
                "next_step": "Use /api/payment/process to complete payment"
            }).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def create_product(self, post_data):
        """Create new product (admin function)"""
        try:
            data = json.loads(post_data.decode())
            
            result = self.db.execute_query('''
                INSERT INTO products (name, description, price, category, stock_quantity, image_url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                data['name'],
                data.get('description', ''),
                data['price'],
                data.get('category', 'general'),
                data.get('stock_quantity', 0),
                data.get('image_url', '')
            ))
            
            self._set_headers(201)
            self.wfile.write(json.dumps({
                "success": True,
                "message": "Product created successfully"
            }).encode())
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def get_orders(self):
        """Get all orders"""
        try:
            orders = self.db.execute_query('''
                SELECT o.*, 
                       GROUP_CONCAT(p.name || ' (x' || oi.quantity || ')') as items
                FROM orders o
                LEFT JOIN order_items oi ON o.id = oi.order_id
                LEFT JOIN products p ON oi.product_id = p.id
                GROUP BY o.id
                ORDER BY o.created_at DESC
            ''')
            self._set_headers(200)
            self.wfile.write(json.dumps({
                "success": True,
                "data": orders
            }).encode())
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def health_check(self):
        """Health check endpoint"""
        self._set_headers(200)
        self.wfile.write(json.dumps({
            "status": "healthy",
            "service": "Humbu Platform API with SMS",
            "business": "Humbu Wandeme Trading Enterprise",
            "version": "4.0.0",
            "contact": "079 465 8481",
            "website": "https://humbu.store",
            "features": ["e-commerce", "payment processing", "order management", "CRM", "SMS notifications"]
        }).encode())
    
    def serve_homepage(self):
        """Serve enhanced homepage with SMS features"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Humbu Wandeme Trading Enterprise</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #1a2a6c; border-bottom: 2px solid #fdbb2d; padding-bottom: 10px; }
                .btn { background: #1a2a6c; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; text-decoration: none; display: inline-block; }
                .admin-btn { background: #1976d2; }
                .crm-btn { background: #28a745; }
                .sms-btn { background: #ff6b35; }
                .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
                .feature-card { background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #1a2a6c; }
                .sms-demo { background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 15px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛍️ Humbu Platform API</h1>
                <p><strong>Business:</strong> Humbu Wandeme Trading Enterprise</p>
                <p><strong>Contact:</strong> 079 465 8481 | humbulani@humbu.store</p>
                <p><strong>Location:</strong> Thohoyandou, Limpopo 0950</p>
                
                <div style="margin: 20px 0;">
                    <a href="/admin" class="btn admin-btn">🚀 Admin Dashboard</a>
                    <a href="/crm" class="btn crm-btn">👥 CRM System</a>
                    <button class="btn sms-btn" onclick="testSMS()">📱 Test SMS</button>
                </div>
                
                <div class="sms-demo">
                    <h3>📱 SMS Notifications Active!</h3>
                    <p>Your platform now automatically sends SMS notifications for:</p>
                    <ul>
                        <li>✅ Order confirmations</li>
                        <li>✅ Payment updates</li>
                        <li>✅ Order status changes</li>
                        <li>✅ Promotional messages</li>
                    </ul>
                    <p><small>Currently using simulated SMS for testing. Ready for AfricasTalking/Twilio integration.</small></p>
                </div>
                
                <h2>🌟 Platform Features</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3>🛍️ E-commerce</h3>
                        <p>Product catalog & order management</p>
                    </div>
                    <div class="feature-card">
                        <h3>💳 Payments</h3>
                        <p>Mobile money, bank transfer & cash</p>
                    </div>
                    <div class="feature-card">
                        <h3>👥 CRM</h3>
                        <p>Customer relationship management</p>
                    </div>
                    <div class="feature-card">
                        <h3>📱 SMS</h3>
                        <p>Automated customer notifications</p>
                    </div>
                    <div class="feature-card">
                        <h3>📊 Analytics</h3>
                        <p>Business intelligence & reporting</p>
                    </div>
                </div>
                
                <h2>Quick Links</h2>
                <p>
                    <a href="/api/health">Health Check</a> | 
                    <a href="/api/products">Products API</a> | 
                    <a href="/api/sms/test">Test SMS</a>
                </p>
            </div>

            <script>
                async function testSMS() {
                    try {
                        const response = await fetch('/api/sms/test');
                        const result = await response.json();
                        
                        if (result.success) {
                            alert('✅ Test SMS sent successfully! Check the server logs.');
                        } else {
                            alert('❌ Failed to send test SMS');
                        }
                    } catch (error) {
                        alert('❌ Error sending test SMS');
                    }
                }
            </script>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())

def run_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, HumbuAPIHandler)
    print('')
    print('🚀 HUMBU PLATFORM WITH SMS STARTED!')
    print('='*50)
    print('📱 SMS NOTIFICATIONS INTEGRATED')
    print('📊 Business: Humbu Wandeme Trading Enterprise')
    print('📞 Contact: 079 465 8481')
    print('📧 Email: humbulani@humbu.store')
    print('🌐 Website: https://humbu.store')
    print('📍 Location: Thohoyandou, Limpopo 0950')
    print('='*50)
    print('🌐 Server running on: http://localhost:8080')
    print('')
    print('📋 NEW SMS ENDPOINTS:')
    print('   GET  /api/sms/test      - Test SMS system')
    print('   POST /api/sms/send      - Send custom SMS')
    print('   POST /api/sms/broadcast - Broadcast to customers')
    print('   GET  /api/sms/analytics - SMS performance')
    print('')
    print('💡 TEST SMS SYSTEM:')
    print('   curl http://localhost:8080/api/sms/test')
    print('   curl -X POST http://localhost:8080/api/sms/send \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"phone_number": "0794658481", "message": "Test SMS"}\'')
    print('')
    print('Press Ctrl+C to stop the server')
    print('='*50)
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
