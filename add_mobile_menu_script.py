#!/usr/bin/env python3
"""
Add mobile-menu.js script to all HTML pages
Ensures consistent mobile menu functionality across all pages
"""

import os
import re

# List of HTML files to update
html_files = [
    'public/about.html',
    'public/collection.html',
    'public/dashboard.html',
    'public/detail.html',
    'public/how-it-works.html',
    'public/index.html',
    'public/login.html',
    'public/pay-sim.html',
    'public/philosophy.html',
    'public/privacy-policy.html',
    'public/problem.html',
    'public/scheduling.html',
    'public/security.html',
    'public/seller-agreement.html',
    'public/seller-dashboard.html',
    'public/seller-register.html',
    'public/seller.html',
    'public/terms.html',
    'public/wallet-policy.html',
    'public/wallet.html'
]

mobile_menu_script = '<script src="/js/mobile-menu.js"></script>'

def add_mobile_menu_script(filepath):
    """Add mobile-menu.js script to HTML file if not already present"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if script is already added
        if 'mobile-menu.js' in content:
            print(f"✓ {filepath} - Already has mobile-menu.js")
            return False
        
        # Find the head section and add the script before </head>
        if '</head>' in content:
            content = content.replace('</head>', f'    {mobile_menu_script}\n</head>')
        # Or add before </body> if no </head> found
        elif '</body>' in content:
            content = content.replace('</body>', f'    {mobile_menu_script}\n</body>')
        else:
            print(f"✗ {filepath} - Could not find </head> or </body> tag")
            return False
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {filepath} - Added mobile-menu.js")
        return True
        
    except Exception as e:
        print(f"✗ {filepath} - Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Adding mobile-menu.js to all HTML pages")
    print("=" * 60)
    
    updated = 0
    skipped = 0
    errors = 0
    
    for filepath in html_files:
        if os.path.exists(filepath):
            result = add_mobile_menu_script(filepath)
            if result:
                updated += 1
            elif result is False and 'Already has' in str(result):
                skipped += 1
        else:
            print(f"✗ {filepath} - File not found")
            errors += 1
    
    print("=" * 60)
    print(f"Summary:")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")
    print("=" * 60)

if __name__ == '__main__':
    main()
