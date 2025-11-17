import requests
import sys
import json
from datetime import datetime

class ApplianceShopAPITester:
    def __init__(self, base_url="https://shop-appliance.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.admin_token = None
        self.user_id = None
        self.admin_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.created_product_id = None
        self.created_order_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, use_admin=False):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        # Use admin token if specified and available
        if use_admin and self.admin_token:
            headers['Authorization'] = f'Bearer {self.admin_token}'
        elif self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            elif method == 'PATCH':
                response = requests.patch(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return True, response.json() if response.content else {}
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Error: {error_detail}")
                except:
                    print(f"   Response: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_user_registration(self):
        """Test user registration"""
        timestamp = datetime.now().strftime('%H%M%S')
        user_data = {
            "name": f"Test User {timestamp}",
            "email": f"testuser{timestamp}@example.com",
            "password": "TestPass123!"
        }
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data=user_data
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_id = response['user']['id']
            print(f"   User ID: {self.user_id}")
            return True
        return False

    def test_admin_login(self):
        """Test admin login"""
        admin_data = {
            "email": "admin@appliancehub.com",
            "password": "admin123"
        }
        
        success, response = self.run_test(
            "Admin Login",
            "POST",
            "auth/login",
            200,
            data=admin_data
        )
        
        if success and 'access_token' in response:
            self.admin_token = response['access_token']
            self.admin_id = response['user']['id']
            print(f"   Admin ID: {self.admin_id}")
            return True
        return False

    def test_get_user_profile(self):
        """Test getting user profile"""
        return self.run_test("Get User Profile", "GET", "auth/me", 200)

    def test_get_products(self):
        """Test getting products"""
        return self.run_test("Get Products", "GET", "products", 200)

    def test_get_categories(self):
        """Test getting categories"""
        return self.run_test("Get Categories", "GET", "categories", 200)

    def test_search_products(self):
        """Test product search"""
        return self.run_test("Search Products", "GET", "products?search=refrigerator", 200)

    def test_filter_by_category(self):
        """Test filtering products by category"""
        return self.run_test("Filter by Category", "GET", "products?category=Refrigerators", 200)

    def test_create_product_admin(self):
        """Test creating a product (admin only)"""
        product_data = {
            "name": "Test Refrigerator",
            "description": "A test refrigerator for API testing",
            "price": 999.99,
            "category": "Refrigerators",
            "image_url": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=500",
            "brand": "TestBrand",
            "stock": 10,
            "features": ["Energy Efficient", "Large Capacity", "Smart Controls"]
        }
        
        success, response = self.run_test(
            "Create Product (Admin)",
            "POST",
            "products",
            200,
            data=product_data,
            use_admin=True
        )
        
        if success and 'id' in response:
            self.created_product_id = response['id']
            print(f"   Created Product ID: {self.created_product_id}")
            return True
        return False

    def test_get_single_product(self):
        """Test getting a single product"""
        if not self.created_product_id:
            print("❌ Skipping - No product ID available")
            return False
        
        return self.run_test(
            "Get Single Product",
            "GET",
            f"products/{self.created_product_id}",
            200
        )

    def test_add_to_cart(self):
        """Test adding item to cart"""
        if not self.created_product_id:
            print("❌ Skipping - No product ID available")
            return False
            
        cart_item = {
            "product_id": self.created_product_id,
            "quantity": 2
        }
        
        return self.run_test(
            "Add to Cart",
            "POST",
            "cart/items",
            200,
            data=cart_item
        )

    def test_get_cart(self):
        """Test getting user's cart"""
        return self.run_test("Get Cart", "GET", "cart", 200)

    def test_update_cart_quantity(self):
        """Test updating cart item quantity"""
        if not self.created_product_id:
            print("❌ Skipping - No product ID available")
            return False
            
        cart_item = {
            "product_id": self.created_product_id,
            "quantity": 3
        }
        
        return self.run_test(
            "Update Cart Quantity",
            "POST",
            "cart/items",
            200,
            data=cart_item
        )

    def test_create_order(self):
        """Test creating an order"""
        success, response = self.run_test(
            "Create Order",
            "POST",
            "orders",
            200
        )
        
        if success and 'id' in response:
            self.created_order_id = response['id']
            print(f"   Created Order ID: {self.created_order_id}")
            return True
        return False

    def test_get_orders(self):
        """Test getting user orders"""
        return self.run_test("Get User Orders", "GET", "orders", 200)

    def test_get_single_order(self):
        """Test getting a single order"""
        if not self.created_order_id:
            print("❌ Skipping - No order ID available")
            return False
        
        return self.run_test(
            "Get Single Order",
            "GET",
            f"orders/{self.created_order_id}",
            200
        )

    def test_create_review(self):
        """Test creating a product review"""
        if not self.created_product_id:
            print("❌ Skipping - No product ID available")
            return False
            
        review_data = {
            "product_id": self.created_product_id,
            "rating": 5,
            "comment": "Great product! Highly recommended."
        }
        
        return self.run_test(
            "Create Review",
            "POST",
            "reviews",
            200,
            data=review_data
        )

    def test_get_reviews(self):
        """Test getting product reviews"""
        if not self.created_product_id:
            print("❌ Skipping - No product ID available")
            return False
        
        return self.run_test(
            "Get Product Reviews",
            "GET",
            f"reviews/{self.created_product_id}",
            200
        )

    def test_get_recommendations(self):
        """Test AI recommendations"""
        return self.run_test(
            "Get AI Recommendations",
            "POST",
            "recommendations",
            200
        )

    def test_admin_get_all_orders(self):
        """Test admin getting all orders"""
        return self.run_test(
            "Admin Get All Orders",
            "GET",
            "admin/orders",
            200,
            use_admin=True
        )

    def test_admin_update_order_status(self):
        """Test admin updating order status"""
        if not self.created_order_id:
            print("❌ Skipping - No order ID available")
            return False
        
        return self.run_test(
            "Admin Update Order Status",
            "PATCH",
            f"admin/orders/{self.created_order_id}?status=processing",
            200,
            use_admin=True
        )

    def test_remove_from_cart(self):
        """Test removing item from cart"""
        if not self.created_product_id:
            print("❌ Skipping - No product ID available")
            return False
        
        return self.run_test(
            "Remove from Cart",
            "DELETE",
            f"cart/items/{self.created_product_id}",
            200
        )

    def test_clear_cart(self):
        """Test clearing entire cart"""
        return self.run_test("Clear Cart", "DELETE", "cart", 200)

    def test_update_product_admin(self):
        """Test updating a product (admin only)"""
        if not self.created_product_id:
            print("❌ Skipping - No product ID available")
            return False
            
        update_data = {
            "name": "Updated Test Refrigerator",
            "description": "An updated test refrigerator",
            "price": 1199.99,
            "category": "Refrigerators",
            "image_url": "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=500",
            "brand": "TestBrand",
            "stock": 15,
            "features": ["Energy Efficient", "Large Capacity", "Smart Controls", "WiFi Enabled"]
        }
        
        return self.run_test(
            "Update Product (Admin)",
            "PUT",
            f"products/{self.created_product_id}",
            200,
            data=update_data,
            use_admin=True
        )

    def test_delete_product_admin(self):
        """Test deleting a product (admin only)"""
        if not self.created_product_id:
            print("❌ Skipping - No product ID available")
            return False
        
        return self.run_test(
            "Delete Product (Admin)",
            "DELETE",
            f"products/{self.created_product_id}",
            200,
            use_admin=True
        )

def main():
    print("🚀 Starting Appliance Shop API Tests")
    print("=" * 50)
    
    tester = ApplianceShopAPITester()
    
    # Test sequence
    test_results = []
    
    # Basic API tests
    test_results.append(("Root API", tester.test_root_endpoint()))
    
    # Authentication tests
    test_results.append(("User Registration", tester.test_user_registration()))
    test_results.append(("Admin Login", tester.test_admin_login()))
    test_results.append(("Get User Profile", tester.test_get_user_profile()))
    
    # Product tests
    test_results.append(("Get Products", tester.test_get_products()))
    test_results.append(("Get Categories", tester.test_get_categories()))
    test_results.append(("Search Products", tester.test_search_products()))
    test_results.append(("Filter by Category", tester.test_filter_by_category()))
    
    # Admin product management
    test_results.append(("Create Product (Admin)", tester.test_create_product_admin()))
    test_results.append(("Get Single Product", tester.test_get_single_product()))
    test_results.append(("Update Product (Admin)", tester.test_update_product_admin()))
    
    # Cart tests
    test_results.append(("Add to Cart", tester.test_add_to_cart()))
    test_results.append(("Get Cart", tester.test_get_cart()))
    test_results.append(("Update Cart Quantity", tester.test_update_cart_quantity()))
    
    # Order tests
    test_results.append(("Create Order", tester.test_create_order()))
    test_results.append(("Get User Orders", tester.test_get_orders()))
    test_results.append(("Get Single Order", tester.test_get_single_order()))
    
    # Review tests
    test_results.append(("Create Review", tester.test_create_review()))
    test_results.append(("Get Product Reviews", tester.test_get_reviews()))
    
    # AI recommendations
    test_results.append(("Get AI Recommendations", tester.test_get_recommendations()))
    
    # Admin tests
    test_results.append(("Admin Get All Orders", tester.test_admin_get_all_orders()))
    test_results.append(("Admin Update Order Status", tester.test_admin_update_order_status()))
    
    # Cart cleanup tests
    test_results.append(("Remove from Cart", tester.test_remove_from_cart()))
    test_results.append(("Clear Cart", tester.test_clear_cart()))
    
    # Cleanup - delete test product
    test_results.append(("Delete Product (Admin)", tester.test_delete_product_admin()))
    
    # Print results summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    failed_tests = []
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            failed_tests.append(test_name)
    
    print(f"\n📈 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    success_rate = (tester.tests_passed / tester.tests_run) * 100 if tester.tests_run > 0 else 0
    print(f"📈 Success rate: {success_rate:.1f}%")
    
    if failed_tests:
        print(f"\n❌ Failed tests: {', '.join(failed_tests)}")
        return 1
    else:
        print("\n🎉 All tests passed!")
        return 0

if __name__ == "__main__":
    sys.exit(main())