#!/usr/bin/env python3
"""Fix the 3 remaining HTML files with different quote style / jQuery version."""
import os, re

BASE = r'C:\Users\Zeng\Desktop\3dmaximum-static'

files = [
    os.path.join(BASE, 'zakazat-3d-vizualizatsiyu', 'index.html'),
    os.path.join(BASE, '3d-vizualizatsiya-tsena', '3d-tury-panoramy-tsena', 'index.html'),
    os.path.join(BASE, '3d-vizualizatsiya-tsena', 'predmetnaja-tsena', 'index.html'),
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # 1. Defer jQuery 3.7.1
    content = content.replace(
        'id="jquery-core-js"></script>',
        'id="jquery-core-js" defer></script>'
    )

    # 2. Defer jquery.tablesorter
    content = content.replace(
        'id="essential_addons_elementor-data-table-js-js"></script>',
        'id="essential_addons_elementor-data-table-js-js" defer></script>'
    )

    # 3. Defer jquery-ui-core
    content = content.replace(
        'id="jquery-ui-core-js"></script>',
        'id="jquery-ui-core-js" defer></script>'
    )

    # 4. Defer frontend.min.css (double-quote version)
    old_css = '<link rel="stylesheet" id="elementor-frontend-css" href="/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=3.1.1" media="all">'
    new_css = '<link rel="preload" href="/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=3.1.1" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="/wp-content/plugins/elementor/assets/css/frontend.min.css?ver=3.1.1"></noscript>'
    content = content.replace(old_css, new_css)

    # 5. Add preconnect for i.ytimg.com if page has YouTube content
    if 'ytimg.com' in content and 'i.ytimg.com' not in content.split('</head>')[0]:
        content = content.replace('</head>', '<link rel="preconnect" href="https://i.ytimg.com">\n</head>')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  Fixed: {os.path.relpath(filepath, BASE)}')

print('Done!')
