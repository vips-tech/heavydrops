#!/usr/bin/env python3
"""
Fix footer and add legal-pages-fix.css to all HTML pages
"""

import os
import re

# List of all HTML files
html_files = [
    'public/index.html',
    'public/collection.html',
    'public/detail.html',
    'public/seller.html',
    'public/wallet.html',
    'public/seller-dashboard.html',
    'public/seller-register.html',
    'public/admin.html',
    'public/login.html',
    'public/scheduling.html',
    'public/how-it-works.html',
    'public/problem.html',
    'public/about.html',
    'public/philosophy.html',
    'public/profile/likes.html',
    'public/terms.html',
    'public/wallet-policy.html',
    'public/seller-agreement.html',
    'public/privacy-policy.html',
    'public/security.html',
    'public/appointments.html',
    'public/dashboard.html',
    'public/pay-sim.html'
]

css_link = '<link rel="stylesheet" href="/css/legal-pages-fix.css">'

for html_file in html_files:
    if not os.path.exists(html_file):
        print(f"⚠️  File not found: {html_file}")
        continue
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # Remove "Discover Collection" line from footer
    if 'Discover Collection' in content:
        # Remove the entire line with Discover Collection
        content = re.sub(
            r'\s*<li><a href="[^"]*">Discover Collection</a></li>\s*\n',
            '',
            content
        )
        modified = True
        print(f"✓ {html_file} - Removed 'Discover Collection' from footer")
    
    # Add legal-pages-fix.css if not already present
    if 'legal-pages-fix.css' not in content:
        if '</head>' in content:
            content = content.replace('</head>', f'    {css_link}\n</head>')
            modified = True
            print(f"✓ {html_file} - Added legal-pages-fix.css")
    
    # Write back if modified
    if modified:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

print("\n✅ All files updated!")
print("- Removed 'Discover Collection' from all footers")
print("- Added legal-pages-fix.css to all pages")
