#!/usr/bin/env python3
"""Revert frontend.min.css deferral - it's Elementor's base layout CSS causing CLS 0.345."""
import os, glob

BASE = r'C:\Users\Zeng\Desktop\3dmaximum-static'
count = 0

html_files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
html_files = [f for f in html_files if os.sep + 'ar' + os.sep not in f]

for filepath in sorted(html_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Revert deferred frontend.min.css (single-quote version from older pages)
    deferred = '<link rel="preload" href="/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=3.1.1" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=3.1.1"></noscript>'
    blocking = "<link rel='stylesheet' id='elementor-frontend-css' href='/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=3.1.1' media='all' />"
    if deferred in content:
        content = content.replace(deferred, blocking)
        count += 1

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print(f'Reverted frontend.min.css in {count} files')
