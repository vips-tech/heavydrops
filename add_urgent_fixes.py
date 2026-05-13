#!/usr/bin/env python3
"""
Add urgent-fixes.css to all HTML pages
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
    'public/dashboard.html'
]

css_link = '<link rel="stylesheet" href="/css/urgent-fixes.css">'

for html_file in html_files:
    if not os.path.exists(html_file):
        print(f"⚠️  File not found: {html_file}")
        continue
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if urgent-fixes.css is already included
    if 'urgent-fixes.css' in content:
        print(f"✓ {html_file} - Already has urgent-fixes.css")
        continue
    
    # Add the CSS link before </head>
    if '</head>' in content:
        content = content.replace('</head>', f'    {css_link}\n</head>')
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {html_file} - Added urgent-fixes.css")
    else:
        print(f"⚠️  {html_file} - No </head> tag found")

print("\n✅ All files updated!")
