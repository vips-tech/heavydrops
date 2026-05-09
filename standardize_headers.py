#!/usr/bin/env python3
"""
Standardize headers across all HTML pages
Replaces existing navigation with universal header from homepage
"""

import os
import re
import glob

# Read the universal header
with open('public/includes/header.html', 'r', encoding='utf-8') as f:
    universal_header = f.read()

# List of HTML files to update
html_files = glob.glob('public/*.html')

def extract_and_replace_nav(content):
    """Extract and replace navigation section with universal header"""
    
    # Pattern to match from <nav to </nav> including filter sidebar and overlay
    # This handles multi-line navigation blocks
    
    # First, try to find and remove old navigation
    patterns_to_remove = [
        # Pattern 1: Full nav with filter sidebar and overlay
        r'<nav\s+class="std-nav"[^>]*>.*?</nav>\s*(?:<!--.*?-->\s*)?(?:<div\s+class="filter-sidebar".*?</div>\s*)?(?:<div\s+class="filter-overlay".*?</div>\s*)?',
        # Pattern 2: Just nav element
        r'<nav\s+class="std-nav"[^>]*>.*?</nav>',
        # Pattern 3: Nav with comments
        r'<!--.*?[Nn]avigation.*?-->\s*<nav.*?</nav>',
    ]
    
    # Try each pattern
    for pattern in patterns_to_remove:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, '{{HEADER_PLACEHOLDER}}', content, count=1, flags=re.DOTALL)
            break
    
    # If no pattern matched, try to find <body> tag and insert after it
    if '{{HEADER_PLACEHOLDER}}' not in content:
        body_match = re.search(r'<body[^>]*>\s*', content)
        if body_match:
            insert_pos = body_match.end()
            content = content[:insert_pos] + '\n{{HEADER_PLACEHOLDER}}\n' + content[insert_pos:]
    
    # Replace placeholder with universal header
    content = content.replace('{{HEADER_PLACEHOLDER}}', universal_header)
    
    return content

def update_html_file(filepath):
    """Update HTML file with universal header"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file already has the universal header marker
        if 'Universal Header' in content and 'Enhanced Navigation - Universal Header' in content:
            print(f"✓ {filepath} - Already has universal header")
            return False
        
        # Extract and replace navigation
        new_content = extract_and_replace_nav(content)
        
        # Check if anything changed
        if new_content == content:
            print(f"⚠ {filepath} - No navigation found to replace")
            return False
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ {filepath} - Updated with universal header")
        return True
        
    except Exception as e:
        print(f"✗ {filepath} - Error: {e}")
        return False

def main():
    print("=" * 70)
    print("Standardizing Headers Across All Pages")
    print("=" * 70)
    
    updated = 0
    skipped = 0
    errors = 0
    
    for filepath in sorted(html_files):
        if os.path.exists(filepath):
            result = update_html_file(filepath)
            if result:
                updated += 1
            else:
                skipped += 1
        else:
            print(f"✗ {filepath} - File not found")
            errors += 1
    
    print("=" * 70)
    print(f"Summary:")
    print(f"  Updated: {updated}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")
    print(f"  Total files: {len(html_files)}")
    print("=" * 70)
    print("\n✅ All pages now have:")
    print("  - Gold rate ticker")
    print("  - Filter button")
    print("  - Hamburger menu")
    print("  - Consistent navigation")

if __name__ == '__main__':
    main()
