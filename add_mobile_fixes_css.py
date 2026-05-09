#!/usr/bin/env python3
"""
Add mobile-fixes.css to all HTML pages
Ensures text visibility and proper mobile layout across all pages
"""

import os
import glob

# Find all HTML files
html_files = glob.glob('public/*.html')

mobile_fixes_css = '<link rel="stylesheet" href="/css/mobile-fixes.css">'

def add_mobile_fixes_css(filepath):
    """Add mobile-fixes.css to HTML file if not already present"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if CSS is already added
        if 'mobile-fixes.css' in content:
            print(f"✓ {filepath} - Already has mobile-fixes.css")
            return False
        
        # Find design-system.css and add mobile-fixes.css after it
        if 'design-system.css' in content:
            content = content.replace(
                '<link rel="stylesheet" href="/css/design-system.css">',
                '<link rel="stylesheet" href="/css/design-system.css">\n    ' + mobile_fixes_css
            )
        # Or add before </head> if design-system.css not found
        elif '</head>' in content:
            content = content.replace('</head>', f'    {mobile_fixes_css}\n</head>')
        else:
            print(f"✗ {filepath} - Could not find insertion point")
            return False
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {filepath} - Added mobile-fixes.css")
        return True
        
    except Exception as e:
        print(f"✗ {filepath} - Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Adding mobile-fixes.css to all HTML pages")
    print("=" * 60)
    
    updated = 0
    skipped = 0
    errors = 0
    
    for filepath in sorted(html_files):
        result = add_mobile_fixes_css(filepath)
        if result:
            updated += 1
        elif result is False:
            skipped += 1
    
    print("=" * 60)
    print(f"Summary:")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")
    print(f"  Total files: {len(html_files)}")
    print("=" * 60)

if __name__ == '__main__':
    main()
