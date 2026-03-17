#!/usr/bin/env python3
"""Round 3 optimization: fix font cache, defer more CSS, fix preconnects, astra font-display."""
import os, re, glob

BASE = r'C:\Users\Zeng\Desktop\3dmaximum-static'

stats = {
    'files': 0,
    'fonts_versioned': 0,
    'style_css_deferred': 0,
    'post22_css_deferred': 0,
    'post2798_css_deferred': 0,
    'global_css_deferred': 0,
    'kuula_preconnect_removed': 0,
    'astra_font_display': 0,
}

html_files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
html_files = [f for f in html_files if os.sep + 'ar' + os.sep not in f]

for filepath in sorted(html_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # === 1. Version fonts.css to bust Cloudflare cache ===
    # Replace /fonts.css with /fonts.css?v=2 (both quote styles)
    if '"/fonts.css"' in content or "'/fonts.css'" in content or 'href="/fonts.css"' in content:
        content = content.replace('href="/fonts.css"', 'href="/fonts.css?v=2"')
        content = content.replace("href='/fonts.css'", "href='/fonts.css?v=2'")
        stats['fonts_versioned'] += 1

    # === 2. Defer style.min.css (Astra theme, 13.7KB, 640ms on mobile) ===
    # The inline CSS already contains all critical Astra styles, so deferring is safe
    # Handle single-quote version
    old_style = "<link rel='stylesheet' id='astra-theme-css-css'  href='/wp-content/themes/astra/assets/css/minified/style.min.css?ver=3.1.2' media='all' />"
    new_style = '<link rel="preload" href="/wp-content/themes/astra/assets/css/minified/style.min.css?ver=3.1.2" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="/wp-content/themes/astra/assets/css/minified/style.min.css?ver=3.1.2"></noscript>'
    if old_style in content:
        content = content.replace(old_style, new_style)
        stats['style_css_deferred'] += 1
    # Handle double-quote version (3 newer pages)
    old_style2 = '<link rel="stylesheet" id="astra-theme-css-css" href="/wp-content/themes/astra/assets/css/minified/style.min.css?ver=3.1.2" media="all">'
    if old_style2 in content:
        content = content.replace(old_style2, new_style)
        stats['style_css_deferred'] += 1

    # === 3. Defer post-22.css (4.4KB, 320ms on mobile) ===
    # This is homepage-specific Elementor CSS
    old_p22 = "<link rel='stylesheet' id='elementor-post-22-css'  href='/wp-content/uploads/elementor/css/post-22.css?ver=1697629354' media='all' />"
    new_p22 = '<link rel="preload" href="/wp-content/uploads/elementor/css/post-22.css?ver=1697629354" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="/wp-content/uploads/elementor/css/post-22.css?ver=1697629354"></noscript>'
    if old_p22 in content:
        content = content.replace(old_p22, new_p22)
        stats['post22_css_deferred'] += 1

    # === 4. Defer post-2798.css (1.1KB, 160ms) - Elementor kit CSS ===
    old_p2798 = "<link rel='stylesheet' id='elementor-post-2798-css'  href='/wp-content/uploads/elementor/css/post-2798.css?ver=1612127884' media='all' />"
    new_p2798 = '<link rel="preload" href="/wp-content/uploads/elementor/css/post-2798.css?ver=1612127884" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="/wp-content/uploads/elementor/css/post-2798.css?ver=1612127884"></noscript>'
    if old_p2798 in content:
        content = content.replace(old_p2798, new_p2798)
        stats['post2798_css_deferred'] += 1

    # === 5. Defer global.css (1.4KB, 160ms) - Elementor global CSS ===
    old_global = "<link rel='stylesheet' id='elementor-global-css'  href='/wp-content/uploads/elementor/css/global.css?ver=1612127884' media='all' />"
    new_global = '<link rel="preload" href="/wp-content/uploads/elementor/css/global.css?ver=1612127884" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="/wp-content/uploads/elementor/css/global.css?ver=1612127884"></noscript>'
    if old_global in content:
        content = content.replace(old_global, new_global)
        stats['global_css_deferred'] += 1

    # === 6. Remove kuula preconnects from pages where kuula iframe is lazy-loaded ===
    # PageSpeed warns about >4 preconnects. Kuula iframes are loading="lazy"
    # so preconnect fires too early and wastes connection.
    # Keep only i.ytimg.com preconnect (YouTube thumbnails load immediately)
    kuula_block = '<link rel="preconnect" href="https://kuula.co">\n<link rel="preconnect" href="https://static.kuula.io">\n<link rel="preconnect" href="https://files.kuula.io">\n'
    if kuula_block in content:
        content = content.replace(kuula_block, '')
        stats['kuula_preconnect_removed'] += 1

    # === 7. Add font-display: swap to Astra icon font ===
    # The inline @font-face for "Astra" uses font-display: fallback which causes 538ms delay
    if 'font-family: "Astra"' in content and 'font-display: fallback' in content:
        content = content.replace(
            'font-display: fallback;',
            'font-display: swap;'
        )
        stats['astra_font_display'] += 1

    # Write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        stats['files'] += 1
        rel = os.path.relpath(filepath, BASE).replace('\\', '/')
        print(f'  Updated: {rel}')

print(f'\n=== ROUND 3 RESULTS ===')
for k, v in stats.items():
    print(f'  {k}: {v}')
