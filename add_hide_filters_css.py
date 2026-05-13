#!/usr/bin/env python3
"""
Add hide-inline-filters.css to all HTML pages
"""

import os
import glob

html_files = glob.glob('public/*.html')
hide_filters_css = '<link rel="stylesheet" href="/css/hide-inline-filters.css">'

def add_hide_filters_css(filepath):
    """Add hide-inline-filters.css to HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already added
        if 'hide-inline-filters.css' in content:
            print(f"✓ {filepath} - Already has hide-inline-filters.css")
            return False
        
        # Add before </head>
        if '</head>' in content:
            content = content.replace('</head>', f'    {hide_filters_css}\n</head>')
        else:
            print(f"✗ {filepath} - Could not find </head> tag")
            return False
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {filepath} - Added hide-inline-filters.css")
        return True
        
    except Exception as e:
        print(f"✗ {filepath} - Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Hiding inline filters - accessible only via sidebar")
    print("=" * 60)
    
    updated = 0
    skipped = 0
    
    for filepath in sorted(html_files):
        if os.path.exists(filepath):
            result = add_hide_filters_css(filepath)
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
    print("\n✅ Filters now hidden from main page")
    print("  - Only accessible via FILTERS button")
    print("  - Cleaner page layout")
    print("  - Less clutter")

if __name__ == '__main__':
    main()
