#!/usr/bin/env python3
"""Mobile performance optimization: defer jQuery, remaining JS, CSS, add preconnects."""
import os, re, glob

BASE = r'C:\Users\Zeng\Desktop\3dmaximum-static'

stats = {
    'files': 0,
    'jquery_deferred': 0,
    'tablesorter_deferred': 0,
    'jquery_ui_deferred': 0,
    'frontend_css_deferred': 0,
    'preconnect_ytimg': 0,
    'preconnect_kuula_fix': 0,
}

html_files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
html_files = [f for f in html_files if os.sep + 'ar' + os.sep not in f]

for filepath in sorted(html_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # === 1. Defer jQuery (biggest win: ~1750ms on mobile) ===
    # jQuery is in <head> without defer. Add defer attribute.
    # Inline scripts only define config vars (no jQuery calls), so safe to defer.
    old_jquery = "<script src='/wp-includes/js/jquery/jquery.min.js?ver=3.5.1' id='jquery-core-js'></script>"
    new_jquery = "<script src='/wp-includes/js/jquery/jquery.min.js?ver=3.5.1' id='jquery-core-js' defer></script>"
    if old_jquery in content:
        content = content.replace(old_jquery, new_jquery)
        stats['jquery_deferred'] += 1

    # === 2. Defer jquery.tablesorter.min.js ===
    old_ts = "id='essential_addons_elementor-data-table-js-js'></script>"
    new_ts = "id='essential_addons_elementor-data-table-js-js' defer></script>"
    if old_ts in content and 'data-table-js-js' in content and 'data-table-js-js' + "' defer" not in content:
        content = content.replace(old_ts, new_ts)
        stats['tablesorter_deferred'] += 1

    # === 3. Defer jquery-ui-core.min.js (~480ms on mobile) ===
    old_ui = "id='jquery-ui-core-js'></script>"
    new_ui = "id='jquery-ui-core-js' defer></script>"
    if old_ui in content and "jquery-ui-core-js' defer" not in content:
        content = content.replace(old_ui, new_ui)
        stats['jquery_ui_deferred'] += 1

    # === 4. Defer frontend.min.css (~640ms on mobile) ===
    # Convert render-blocking <link> to preload/onload pattern
    old_frontend_css = "<link rel='stylesheet' id='elementor-frontend-css'  href='/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=3.1.1' media='all' />"
    new_frontend_css = '<link rel="preload" href="/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=3.1.1" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=3.1.1"></noscript>'
    if old_frontend_css in content:
        content = content.replace(old_frontend_css, new_frontend_css)
        stats['frontend_css_deferred'] += 1

    # === 5. Add preconnect for i.ytimg.com (YouTube thumbnails, ~300ms savings) ===
    # Only add on pages that have YouTube content
    if 'ytimg.com' in content and 'preconnect' in content and 'i.ytimg.com' not in content.split('</head>')[0]:
        preconnect_yt = '<link rel="preconnect" href="https://i.ytimg.com">\n'
        content = content.replace('</head>', preconnect_yt + '</head>')
        stats['preconnect_ytimg'] += 1

    # === 6. Fix kuula preconnect: remove crossorigin (not CORS requests) ===
    # The iframes load normally (not CORS), so crossorigin creates unused connection
    old_kuula = '<link rel="preconnect" href="https://kuula.co" crossorigin>'
    new_kuula = '<link rel="preconnect" href="https://kuula.co">'
    if old_kuula in content:
        content = content.replace(old_kuula, new_kuula)
        # Also fix static.kuula.io and files.kuula.io
        content = content.replace(
            '<link rel="preconnect" href="https://static.kuula.io" crossorigin>',
            '<link rel="preconnect" href="https://static.kuula.io">'
        )
        content = content.replace(
            '<link rel="preconnect" href="https://files.kuula.io" crossorigin>',
            '<link rel="preconnect" href="https://files.kuula.io">'
        )
        stats['preconnect_kuula_fix'] += 1

    # Write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        stats['files'] += 1
        rel = os.path.relpath(filepath, BASE).replace('\\', '/')
        print(f'  Updated: {rel}')

print(f'\n=== MOBILE OPTIMIZATION RESULTS ===')
for k, v in stats.items():
    print(f'  {k}: {v}')
