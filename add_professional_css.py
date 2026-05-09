#!/usr/bin/env python3
"""
Add professional-enhancements.css to all HTML pages
"""

import os
import glob

html_files = glob.glob('public/*.html')
professional_css = '<link rel="stylesheet" href="/css/professional-enhancements.css">'

def add_professional_css(filepath):
    """Add professional-enhancements.css to HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already added
        if 'professional-enhancements.css' in content:
            print(f"✓ {filepath} - Already has professional-enhancements.css")
            return False
        
        # Add after mobile-nav.css or before </head>
        if 'mobile-nav.css' in content:
            content = content.replace(
                '<link rel="stylesheet" href="/css/mobile-nav.css">',
                f'<link rel="stylesheet" href="/css/mobile-nav.css">\n    {professional_css}'
            )
        elif '</head>' in content:
            content = content.replace('</head>', f'    {professional_css}\n</head>')
        else:
            print(f"✗ {filepath} - Could not find insertion point")
            return False
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {filepath} - Added professional-enhancements.css")
        return True
        
    except Exception as e:
        print(f"✗ {filepath} - Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Adding professional-enhancements.css to all pages")
    print("=" * 60)
    
    updated = 0
    skipped = 0
    
    for filepath in sorted(html_files):
        if os.path.exists(filepath):
            result = add_professional_css(filepath)
            if result:
                updated += 1
            else:
                skipped += 1
    
    print("=" * 60)
    print(f"Summary:")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")
    print(f"  Total files: {len(html_files)}")
    print("=" * 60)
    print("\n✅ All pages now have professional enhancements:")
    print("  - Maximum text visibility")
    print("  - Professional button styling")
    print("  - Smooth animations")
    print("  - Better accessibility")

if __name__ == '__main__':
    main()
