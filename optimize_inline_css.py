#!/usr/bin/env python3
"""Inline 3 small CSS files into index.html to eliminate render-blocking requests.

Replaces <link> tags for post-2798.css, global.css, and post-22.css with
inline <style> blocks. This saves 3 HTTP round-trips (~480ms on slow 4G)
without any CLS risk since the same CSS is applied, just inline.
"""
import os

BASE = r'C:\Users\Zeng\Desktop\3dmaximum-static'
INDEX = os.path.join(BASE, 'index.html')

# Read CSS file contents
css_files = {
    'post-2798': os.path.join(BASE, 'wp-content', 'uploads', 'elementor', 'css', 'post-2798.css'),
    'global': os.path.join(BASE, 'wp-content', 'uploads', 'elementor', 'css', 'global.css'),
    'post-22': os.path.join(BASE, 'wp-content', 'uploads', 'elementor', 'css', 'post-22.css'),
}

css_contents = {}
for name, path in css_files.items():
    with open(path, 'r', encoding='utf-8') as f:
        css_contents[name] = f.read().strip()
    print(f'  Read {name}: {len(css_contents[name])} chars')

# Read index.html
with open(INDEX, 'r', encoding='utf-8') as f:
    html = f.read()

original = html

# Replace post-2798.css link with inline style
old_2798 = "<link rel='stylesheet' id='elementor-post-2798-css' href='/wp-content/uploads/elementor/css/post-2798.css?ver=1612127884' media='all' />"
new_2798 = f"<style id='elementor-post-2798-inline'>{css_contents['post-2798']}</style>"
html = html.replace(old_2798, new_2798)

# Replace global.css link with inline style
old_global = "<link rel='stylesheet' id='elementor-global-css' href='/wp-content/uploads/elementor/css/global.css?ver=1612127884' media='all' />"
new_global = f"<style id='elementor-global-inline'>{css_contents['global']}</style>"
html = html.replace(old_global, new_global)

# Replace post-22.css link with inline style
old_22 = "<link rel='stylesheet' id='elementor-post-22-css' href='/wp-content/uploads/elementor/css/post-22.css?ver=1697629354' media='all' />"
new_22 = f"<style id='elementor-post-22-inline'>{css_contents['post-22']}</style>"
html = html.replace(old_22, new_22)

if html != original:
    with open(INDEX, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'\n  Updated index.html')
    print(f'  Replaced 3 <link> tags with inline <style> blocks')
    print(f'  Eliminated 3 render-blocking HTTP requests')
else:
    print('\n  ERROR: No replacements made!')
