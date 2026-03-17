#!/usr/bin/env python3
"""Revert tablesorter + jquery-ui-core defer (increased TBT 390→490ms).
Keep fonts.css deferred and image width/height — those are net positive."""
import os, glob

BASE = r'C:\Users\Zeng\Desktop\3dmaximum-static'
stats = {'tablesorter': 0, 'ui_core': 0}

html_files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
html_files = [f for f in html_files if os.sep + 'ar' + os.sep not in f]

for filepath in sorted(html_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Revert tablesorter defer (single-quote)
    content = content.replace(
        "id='essential_addons_elementor-data-table-js-js' defer></script>",
        "id='essential_addons_elementor-data-table-js-js'></script>"
    )
    # Revert tablesorter defer (double-quote)
    content = content.replace(
        'id="essential_addons_elementor-data-table-js-js" defer></script>',
        'id="essential_addons_elementor-data-table-js-js"></script>'
    )

    # Revert jquery-ui-core defer (single-quote)
    content = content.replace(
        "id='jquery-ui-core-js' defer></script>",
        "id='jquery-ui-core-js'></script>"
    )
    # Revert jquery-ui-core defer (double-quote)
    content = content.replace(
        'id="jquery-ui-core-js" defer></script>',
        'id="jquery-ui-core-js"></script>'
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        rel = os.path.relpath(filepath, BASE).replace('\\', '/')
        print(f'  Reverted: {rel}')

        if "data-table-js-js'></script>" in content or 'data-table-js-js"></script>' in content:
            stats['tablesorter'] += 1
        if "ui-core-js'></script>" in content or 'ui-core-js"></script>' in content:
            stats['ui_core'] += 1

print(f'\nReverted tablesorter in {stats["tablesorter"]} files')
print(f'Reverted ui-core in {stats["ui_core"]} files')
