#!/usr/bin/env python3
"""
Add gradient-hero-styles.css to all HTML pages
"""

import os

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

css_link = '<link rel="stylesheet" href="/css/gradient-hero-styles.css">'

for html_file in html_files:
    if not os.path.exists(html_file):
        print(f"⚠️  File not found: {html_file}")
        continue
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add gradient-hero-styles.css if not already present
    if 'gradient-hero-styles.css' not in content:
        if '</head>' in content:
            content = content.replace('</head>', f'    {css_link}\n</head>')
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ {html_file} - Added gradient-hero-styles.css")
        else:
            print(f"⚠️  {html_file} - No </head> tag found")
    else:
        print(f"✓ {html_file} - Already has gradient-hero-styles.css")

print("\n✅ All files updated with gradient-hero-styles.css!")
