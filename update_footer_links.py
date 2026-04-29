"""
Update Footer Links - Replace anchor links with separate pages
Updates all HTML files to use separate Privacy Policy and Security pages
"""

import os
import re

def update_footer_links():
    # List of HTML files to update
    html_files = [
        'public/about.html',
        'public/how-it-works.html',
        'public/index.html',
        'public/philosophy.html',
        'public/seller-agreement.html',
        'public/problem.html',
        'public/profile/likes.html',
        'public/terms.html',
        'public/wallet-policy.html',
        'public/collection.html',
        'public/detail.html',
        'public/dashboard.html',
        'public/appointments.html',
        'public/wallet.html',
    ]
    
    updated_count = 0
    
    for file_path in html_files:
        if not os.path.exists(file_path):
            print(f"⚠️  Skipping {file_path} (not found)")
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Replace Privacy Policy link
            content = re.sub(
                r'<a href="/terms#privacy">Privacy Policy</a>',
                '<a href="/privacy-policy">Privacy Policy</a>',
                content
            )
            
            # Replace Security link
            content = re.sub(
                r'<a href="/terms#security">Security</a>',
                '<a href="/security">Security</a>',
                content
            )
            
            # Only write if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Updated {file_path}")
                updated_count += 1
            else:
                print(f"ℹ️  No changes needed for {file_path}")
                
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")
    
    print(f"\n{'='*50}")
    print(f"✅ Updated {updated_count} files")
    print(f"{'='*50}")
    print("\nFooter links now point to:")
    print("  • /privacy-policy (separate page)")
    print("  • /security (separate page)")
    print("\nInstead of:")
    print("  • /terms#privacy (anchor link)")
    print("  • /terms#security (anchor link)")

if __name__ == "__main__":
    update_footer_links()
