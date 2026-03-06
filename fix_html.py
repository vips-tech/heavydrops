import os

PUBLIC_DIR = os.path.join("d:\\HeavyDrops_Platform_v1.0", "public")
HAMBURGER = '<nav class="std-nav">\n        <button class="mobile-menu-btn" aria-label="Toggle menu"><svg viewBox="0 0 24 24"><path d="M3 12h18M3 6h18M3 18h18"/></svg></button>'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If it already has the button or if it lacks std-nav, skip
    if "mobile-menu-btn" in content:
        return
        
    old_target = '<nav class="std-nav">'
    if old_target in content:
        content = content.replace(old_target, HAMBURGER)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Skipped {filepath} (no target found)")

for root, _, files in os.walk(PUBLIC_DIR):
    for file in files:
        if file.endswith('.html'):
            process_file(os.path.join(root, file))

print("Done")
