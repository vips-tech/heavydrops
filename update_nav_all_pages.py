import os
import re

# List of HTML files to update
html_files = [
    'public/wallet.html',
    'public/scheduling.html',
    'public/profile/likes.html',
    'public/login.html',
    'public/about.html',
    'public/how-it-works.html',
    'public/philosophy.html',
    'public/problem.html',
    'public/terms.html',
    'public/wallet-policy.html',
    'public/seller-agreement.html',
    'public/seller.html',
    'public/seller-register.html',
    'public/pay-sim.html'
]

for file_path in html_files:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path} - file not found")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add onclick to mobile menu button
    content = re.sub(
        r'<button class="mobile-menu-btn" aria-label="Toggle menu">',
        r'<button class="mobile-menu-btn" aria-label="Toggle menu" onclick="toggleMobileMenu()">',
        content
    )
    
    # Add id to nav-center
    content = re.sub(
        r'<div class="nav-center">',
        r'<div class="nav-center" id="navCenter">',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {file_path}")

print("\nAll pages updated successfully!")
