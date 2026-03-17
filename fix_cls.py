#!/usr/bin/env python3
"""Revert CSS deferrals that cause CLS: style.min.css, global.css, post-2798.css, post-22.css.
These base layout CSS files must be render-blocking to prevent layout shifts."""
import os, re, glob

BASE = r'C:\Users\Zeng\Desktop\3dmaximum-static'
stats = {'files': 0, 'style_reverted': 0, 'global_reverted': 0, 'p2798_reverted': 0, 'p22_reverted': 0}

html_files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
html_files = [f for f in html_files if os.sep + 'ar' + os.sep not in f]

for filepath in sorted(html_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # === 1. Revert style.min.css back to render-blocking ===
    deferred_style = '<link rel="preload" href="/wp-content/themes/astra/assets/css/minified/style.min.css?ver=3.1.2" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="/wp-content/themes/astra/assets/css/minified/style.min.css?ver=3.1.2"></noscript>'
    blocking_style = "<link rel='stylesheet' id='astra-theme-css-css' href='/wp-content/themes/astra/assets/css/minified/style.min.css?ver=3.1.2' media='all' />"
    if deferred_style in content:
        content = content.replace(deferred_style, blocking_style)
        stats['style_reverted'] += 1

    # === 2. Revert global.css back to render-blocking ===
    deferred_global = '<link rel="preload" href="/wp-content/uploads/elementor/css/global.css?ver=1612127884" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="/wp-content/uploads/elementor/css/global.css?ver=1612127884"></noscript>'
    blocking_global = "<link rel='stylesheet' id='elementor-global-css' href='/wp-content/uploads/elementor/css/global.css?ver=1612127884' media='all' />"
    if deferred_global in content:
        content = content.replace(deferred_global, blocking_global)
        stats['global_reverted'] += 1

    # === 3. Revert post-2798.css back to render-blocking ===
    deferred_p2798 = '<link rel="preload" href="/wp-content/uploads/elementor/css/post-2798.css?ver=1612127884" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="/wp-content/uploads/elementor/css/post-2798.css?ver=1612127884"></noscript>'
    blocking_p2798 = "<link rel='stylesheet' id='elementor-post-2798-css' href='/wp-content/uploads/elementor/css/post-2798.css?ver=1612127884' media='all' />"
    if deferred_p2798 in content:
        content = content.replace(deferred_p2798, blocking_p2798)
        stats['p2798_reverted'] += 1

    # === 4. Revert post-22.css back to render-blocking (homepage only) ===
    deferred_p22 = '<link rel="preload" href="/wp-content/uploads/elementor/css/post-22.css?ver=1697629354" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="/wp-content/uploads/elementor/css/post-22.css?ver=1697629354"></noscript>'
    blocking_p22 = "<link rel='stylesheet' id='elementor-post-22-css' href='/wp-content/uploads/elementor/css/post-22.css?ver=1697629354' media='all' />"
    if deferred_p22 in content:
        content = content.replace(deferred_p22, blocking_p22)
        stats['p22_reverted'] += 1

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        stats['files'] += 1

print(f'=== CLS FIX RESULTS ===')
for k, v in stats.items():
    print(f'  {k}: {v}')
