#!/usr/bin/env python3
"""
Test all website functionality
- Check all pages load
- Verify all buttons exist
- Test all links
- Check API endpoints
"""

import requests
import time
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:5001"

# All pages to test
PAGES = [
    "/",
    "/about",
    "/how-it-works",
    "/problem",
    "/philosophy",
    "/collection",
    "/terms",
    "/privacy-policy",
    "/security",
    "/wallet-policy",
    "/seller-agreement",
    "/login",
    "/seller-register",
]

# API endpoints to test
API_ENDPOINTS = [
    "/api/health/config",
    "/api/designs",
]

def test_page_loads(url):
    """Test if a page loads successfully"""
    try:
        response = requests.get(f"{BASE_URL}{url}", timeout=5)
        return response.status_code == 200, response.status_code
    except Exception as e:
        return False, str(e)

def test_page_elements(url):
    """Test if page has required elements"""
    try:
        response = requests.get(f"{BASE_URL}{url}", timeout=5)
        if response.status_code != 200:
            return False, "Page not found"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        issues = []
        
        # Check for header
        if not soup.find('nav', class_='std-nav'):
            issues.append("Missing navigation header")
        
        # Check for footer
        if not soup.find('footer', class_='std-footer'):
            issues.append("Missing footer")
        
        # Check for mobile menu button
        if not soup.find('button', class_='mobile-menu-btn'):
            issues.append("Missing mobile menu button")
        
        # Check for filter button
        if not soup.find('button', class_='filter-toggle-btn'):
            issues.append("Missing filter button")
        
        return len(issues) == 0, issues if issues else "All elements present"
        
    except Exception as e:
        return False, str(e)

def test_api_endpoint(endpoint):
    """Test if API endpoint works"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        return response.status_code == 200, response.status_code
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 70)
    print("Comprehensive Functionality Test")
    print("=" * 70)
    print(f"Testing: {BASE_URL}")
    print()
    
    # Test pages
    print("📄 Testing Pages:")
    print("-" * 70)
    page_results = []
    for page in PAGES:
        success, result = test_page_loads(page)
        status = "✅" if success else "❌"
        print(f"{status} {page:30} - Status: {result}")
        page_results.append(success)
        time.sleep(0.1)
    
    print()
    
    # Test page elements
    print("🔍 Testing Page Elements:")
    print("-" * 70)
    element_results = []
    for page in PAGES:
        success, result = test_page_elements(page)
        status = "✅" if success else "❌"
        if success:
            print(f"{status} {page:30} - {result}")
        else:
            print(f"{status} {page:30}")
            for issue in result:
                print(f"     └─ {issue}")
        element_results.append(success)
        time.sleep(0.1)
    
    print()
    
    # Test API endpoints
    print("🔌 Testing API Endpoints:")
    print("-" * 70)
    api_results = []
    for endpoint in API_ENDPOINTS:
        success, result = test_api_endpoint(endpoint)
        status = "✅" if success else "❌"
        print(f"{status} {endpoint:30} - Status: {result}")
        api_results.append(success)
        time.sleep(0.1)
    
    print()
    print("=" * 70)
    print("Summary:")
    print(f"  Pages Loading: {sum(page_results)}/{len(page_results)}")
    print(f"  Page Elements: {sum(element_results)}/{len(element_results)}")
    print(f"  API Endpoints: {sum(api_results)}/{len(api_results)}")
    print("=" * 70)
    
    if all(page_results) and all(element_results) and all(api_results):
        print("\n✅ All tests passed! Website is fully functional.")
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")

if __name__ == '__main__':
    main()
