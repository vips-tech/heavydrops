#!/usr/bin/env python3
"""
Heavy Drops Website Testing Script
Tests all enhanced features and functionality
"""

import requests
import json
import time
from pathlib import Path

class WebsiteTester:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.test_results = []

    def test_endpoint(self, endpoint, expected_status=200, description=""):
        """Test a single endpoint"""
        try:
            response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            success = response.status_code == expected_status
            
            result = {
                "endpoint": endpoint,
                "status_code": response.status_code,
                "expected": expected_status,
                "success": success,
                "description": description,
                "response_time": response.elapsed.total_seconds()
            }
            
            self.test_results.append(result)
            
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {endpoint} - {response.status_code} ({response.elapsed.total_seconds():.3f}s)")
            
            return success
            
        except Exception as e:
            result = {
                "endpoint": endpoint,
                "status_code": "ERROR",
                "expected": expected_status,
                "success": False,
                "description": description,
                "error": str(e)
            }
            
            self.test_results.append(result)
            print(f"❌ {endpoint} - ERROR: {e}")
            return False

    def test_static_files(self):
        """Test static file serving"""
        print("\n🎨 Testing Static Files...")
        
        static_files = [
            "/css/design-system.css",
            "/css/components-enhanced.css", 
            "/css/mobile-nav.css",
            "/js/enhanced-features.js",
            "/js/jewelry-images.js",
            "/js/session.js",
            "/assets/logo.png"
        ]
        
        for file_path in static_files:
            self.test_endpoint(file_path, 200, f"Static file: {file_path}")

    def test_html_pages(self):
        """Test HTML page serving"""
        print("\n📄 Testing HTML Pages...")
        
        pages = [
            ("/", "Home page"),
            ("/collection", "Collection page"),
            ("/how-it-works", "How it works page"),
            ("/about", "About page"),
            ("/login", "Login page"),
            ("/terms", "Terms page"),
            ("/wallet", "Wallet page"),
            ("/seller-register", "Seller registration"),
            ("/admin", "Admin page")
        ]
        
        for endpoint, description in pages:
            self.test_endpoint(endpoint, 200, description)

    def test_api_endpoints(self):
        """Test API endpoints"""
        print("\n🔌 Testing API Endpoints...")
        
        api_endpoints = [
            ("/api/health/config", "System configuration"),
            ("/api/designs", "Design discovery"),
            ("/api/designs?category=Necklace", "Filtered designs"),
            ("/api/designs?max_price=100000", "Price filtered designs")
        ]
        
        for endpoint, description in api_endpoints:
            self.test_endpoint(endpoint, 200, description)

    def test_responsive_design(self):
        """Test responsive design elements"""
        print("\n📱 Testing Responsive Design...")
        
        # Test that CSS files contain responsive breakpoints
        css_files = [
            "public/css/design-system.css",
            "public/css/components-enhanced.css"
        ]
        
        for css_file in css_files:
            if Path(css_file).exists():
                with open(css_file, 'r') as f:
                    content = f.read()
                    
                has_mobile = "@media (max-width: 768px)" in content
                has_tablet = "@media (max-width: 1024px)" in content
                
                print(f"✅ {css_file} - Mobile breakpoints: {has_mobile}")
                print(f"✅ {css_file} - Tablet breakpoints: {has_tablet}")

    def test_javascript_features(self):
        """Test JavaScript functionality"""
        print("\n⚡ Testing JavaScript Features...")
        
        js_files = [
            "public/js/enhanced-features.js",
            "public/js/jewelry-images.js"
        ]
        
        for js_file in js_files:
            if Path(js_file).exists():
                with open(js_file, 'r') as f:
                    content = f.read()
                    
                # Check for key features
                features = {
                    "Gold Rate Updates": "goldRate" in content,
                    "Animation System": "animation" in content.lower(),
                    "Mobile Navigation": "toggleMobileMenu" in content,
                    "Image Management": "JewelryImages" in content,
                    "Intersection Observer": "IntersectionObserver" in content
                }
                
                for feature, present in features.items():
                    status = "✅" if present else "❌"
                    print(f"{status} {feature} in {js_file}")

    def test_image_resources(self):
        """Test image resource availability"""
        print("\n🖼️ Testing Image Resources...")
        
        # Test some sample jewelry images
        sample_images = [
            "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?q=80&w=600&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?q=80&w=600&auto=format&fit=crop",
            "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?q=80&w=600&auto=format&fit=crop"
        ]
        
        for img_url in sample_images:
            try:
                response = requests.head(img_url, timeout=5)
                success = response.status_code == 200
                status = "✅" if success else "❌"
                print(f"{status} Image resource: {img_url[:50]}...")
            except Exception as e:
                print(f"❌ Image resource error: {e}")

    def generate_report(self):
        """Generate test report"""
        print("\n📊 Test Report Summary")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['endpoint']} - {result.get('error', result['status_code'])}")
        
        # Calculate average response time
        response_times = [r["response_time"] for r in self.test_results if "response_time" in r]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            print(f"\nAverage Response Time: {avg_response_time:.3f}s")
        
        return passed_tests == total_tests

    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Heavy Drops Website Tests...")
        print(f"Testing against: {self.base_url}")
        
        # Run all test suites
        self.test_static_files()
        self.test_html_pages()
        self.test_api_endpoints()
        self.test_responsive_design()
        self.test_javascript_features()
        self.test_image_resources()
        
        # Generate final report
        success = self.generate_report()
        
        if success:
            print("\n🎉 All tests passed! Website is ready for production.")
        else:
            print("\n⚠️ Some tests failed. Please review and fix issues.")
        
        return success

if __name__ == "__main__":
    tester = WebsiteTester()
    tester.run_all_tests()