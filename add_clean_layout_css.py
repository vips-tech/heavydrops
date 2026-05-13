#!/usr/bin/env python3
"""
Add clean-layout-fix.css to all HTML pages
Fixes white space and text visibility issues
"""

import os
import glob

html_files = glob.glob('public/*.html')
clean_layout_css = '<link rel="stylesheet" href="/css/clean-layout-fix.css">'

def add_clean_layout_css(filepath):
    """Add clean-layout-fix.css to HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already added
        if 'clean-layout-fix.css' in content:
            print(f"✓ {filepath} - Already has clean-layout-fix.css")
            return False
        
        # Add before </head>
        if '</head>' in content:
            content = content.replace('</head>', f'    {clean_layout_css}\n</head>')
        else:
            print(f"✗ {filepath} - Could not find </head> tag")
            return False
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {filepath} - Added clean-layout-fix.css")
        return True
        
    except Exception as e:
        print(f"✗ {filepath} - Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Adding clean layout fixes")
    print("=" * 60)
    
    updated = 0
    skipped = 0
    
    for filepath in sorted(html_files):
        if os.path.exists(filepath):
            result = add_clean_layout_css(filepath)
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
    print("\n✅ Clean layout fixes applied:")
    print("  - Removed white space above hero")
    print("  - Fixed text visibility")
    print("  - Maximum contrast")
    print("  - Clean professional layout")

if __name__ == '__main__':
    main()
