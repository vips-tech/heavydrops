#!/usr/bin/env python3
"""
Add universal-header.js script to all HTML pages
"""

import os
import glob

html_files = glob.glob('public/*.html')
universal_header_script = '<script src="/js/universal-header.js"></script>'

def add_universal_header_script(filepath):
    """Add universal-header.js to HTML file if not already present"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if script is already added
        if 'universal-header.js' in content:
            print(f"✓ {filepath} - Already has universal-header.js")
            return False
        
        # Add before </head> tag
        if '</head>' in content:
            content = content.replace('</head>', f'    {universal_header_script}\n</head>')
        else:
            print(f"✗ {filepath} - Could not find </head> tag")
            return False
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {filepath} - Added universal-header.js")
        return True
        
    except Exception as e:
        print(f"✗ {filepath} - Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Adding universal-header.js to all HTML pages")
    print("=" * 60)
    
    updated = 0
    skipped = 0
    
    for filepath in sorted(html_files):
        if os.path.exists(filepath):
            result = add_universal_header_script(filepath)
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

if __name__ == '__main__':
    main()
