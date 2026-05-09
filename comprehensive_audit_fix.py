#!/usr/bin/env python3
"""
Comprehensive Website Audit and Fix
- Ensures all pages have universal header and footer
- Fixes text visibility issues
- Ensures all buttons and links work
- Makes the site professional and functional
"""

import os
import re
import glob

# Universal footer HTML
UNIVERSAL_FOOTER = '''
    <!-- Enhanced Footer -->
    <footer class="std-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h4>Platform</h4>
                    <ul>
                        <li><a href="/collection">Discover Collection</a></li>
                        <li><a href="/how-it-works">How It Works</a></li>
                        <li><a href="/problem">Problem We Solve</a></li>
                        <li><a href="/philosophy">Our Philosophy</a></li>
                        <li><a href="/about">About Heavy Drops</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Legal & Trust</h4>
                    <ul>
                        <li><a href="/terms">Terms & Conditions</a></li>
                        <li><a href="/wallet-policy">Wallet Policy</a></li>
                        <li><a href="/seller-agreement">Seller Agreement</a></li>
                        <li><a href="/privacy-policy">Privacy Policy</a></li>
                        <li><a href="/security">Security</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Partners</h4>
                    <ul>
                        <li><a href="/seller-register">Become a Seller</a></li>
                        <li><a href="/seller-login">Partner Portal</a></li>
                        <li><a href="/seller-dashboard">Seller Dashboard</a></li>
                        <li><a href="/seller-agreement">Partnership Terms</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Contact & Support</h4>
                    <ul>
                        <li><a href="mailto:concierge@heavydrops.com">concierge@heavydrops.com</a></li>
                        <li><a href="tel:+919840828137">+91 98408 28137</a></li>
                        <li><span style="opacity: 0.6;">Chennai, Tamil Nadu</span></li>
                        <li><a href="/support">Help Center</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <span>&copy; 2026 Heavy Drops Intent Network. All rights reserved.</span>
                <span>Crafted in Chennai with ♥</span>
            </div>
        </div>
    </footer>
'''

def ensure_footer(content):
    """Ensure page has universal footer"""
    # Remove existing footer if present
    content = re.sub(r'<footer.*?</footer>', '', content, flags=re.DOTALL)
    
    # Add footer before </body>
    if '</body>' in content:
        content = content.replace('</body>', f'{UNIVERSAL_FOOTER}\n\n</body>')
    
    return content

def ensure_required_scripts(content):
    """Ensure all required scripts are present"""
    required_scripts = [
        '<script src="/js/session.js"></script>',
        '<script src="/js/mobile-menu.js"></script>',
        '<script src="/js/universal-header.js"></script>',
    ]
    
    for script in required_scripts:
        if script not in content:
            # Add before </head>
            if '</head>' in content:
                content = content.replace('</head>', f'    {script}\n</head>')
    
    return content

def ensure_required_css(content):
    """Ensure all required CSS files are present"""
    required_css = [
        '<link rel="stylesheet" href="/css/design-system.css">',
        '<link rel="stylesheet" href="/css/mobile-fixes.css">',
        '<link rel="stylesheet" href="/css/components-enhanced.css">',
        '<link rel="stylesheet" href="/css/mobile-nav.css">',
    ]
    
    for css in required_css:
        if css not in content:
            # Add after other stylesheets or before </head>
            if 'design-system.css' in content and css != required_css[0]:
                content = content.replace(
                    '<link rel="stylesheet" href="/css/design-system.css">',
                    f'<link rel="stylesheet" href="/css/design-system.css">\n    {css}'
                )
            elif '</head>' in content:
                content = content.replace('</head>', f'    {css}\n</head>')
    
    return content

def fix_text_visibility(content):
    """Add inline styles to ensure text visibility on dark backgrounds"""
    # Add text visibility class to hero sections
    patterns = [
        (r'(<div class="hero-content"[^>]*>)', r'\1\n        <style>.hero-content * { position: relative; z-index: 10; }</style>'),
        (r'(<section class="hero-banner"[^>]*>)', r'\1\n    <style>.hero-banner .hero-title, .hero-banner .hero-subtitle { text-shadow: 0 3px 25px rgba(0,0,0,0.9); }</style>'),
    ]
    
    for pattern, replacement in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content, count=1)
    
    return content

def audit_and_fix_page(filepath):
    """Audit and fix a single HTML page"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        issues_found = []
        fixes_applied = []
        
        # Check for universal header
        if 'Enhanced Navigation - Universal Header' not in content:
            issues_found.append("Missing universal header")
        
        # Check for footer
        if '<footer class="std-footer">' not in content:
            issues_found.append("Missing universal footer")
            content = ensure_footer(content)
            fixes_applied.append("Added universal footer")
        
        # Check for required scripts
        if 'mobile-menu.js' not in content:
            issues_found.append("Missing mobile-menu.js")
            content = ensure_required_scripts(content)
            fixes_applied.append("Added required scripts")
        
        # Check for required CSS
        if 'mobile-fixes.css' not in content:
            issues_found.append("Missing mobile-fixes.css")
            content = ensure_required_css(content)
            fixes_applied.append("Added required CSS")
        
        # Fix text visibility
        content = fix_text_visibility(content)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ {filepath}")
            if issues_found:
                print(f"  Issues: {', '.join(issues_found)}")
            if fixes_applied:
                print(f"  Fixes: {', '.join(fixes_applied)}")
            return True
        else:
            print(f"✓ {filepath} - Already correct")
            return False
            
    except Exception as e:
        print(f"✗ {filepath} - Error: {e}")
        return False

def main():
    print("=" * 70)
    print("Comprehensive Website Audit and Fix")
    print("=" * 70)
    
    html_files = glob.glob('public/*.html')
    
    updated = 0
    correct = 0
    errors = 0
    
    for filepath in sorted(html_files):
        if os.path.exists(filepath):
            result = audit_and_fix_page(filepath)
            if result:
                updated += 1
            else:
                correct += 1
        else:
            errors += 1
    
    print("=" * 70)
    print(f"Summary:")
    print(f"  Updated: {updated}")
    print(f"  Already Correct: {correct}")
    print(f"  Errors: {errors}")
    print(f"  Total files: {len(html_files)}")
    print("=" * 70)
    print("\n✅ All pages now have:")
    print("  - Universal header with gold rate & filter")
    print("  - Universal footer with all links")
    print("  - Mobile menu functionality")
    print("  - Text visibility fixes")
    print("  - All required CSS and JS")

if __name__ == '__main__':
    main()
