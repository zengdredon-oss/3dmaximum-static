#!/usr/bin/env python3
"""Revert jQuery, jquery-ui-core, jquery.tablesorter defer to fix TBT 560ms.
Deferred jQuery causes all scripts to execute in burst after DOM parse,
creating long tasks. TBT has 30% weight in Lighthouse - biggest factor."""
import os, glob

BASE = r'C:\Users\Zeng\Desktop\3dmaximum-static'
stats = {'jquery': 0, 'tablesorter': 0, 'ui_core': 0}

html_files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
html_files = [f for f in html_files if os.sep + 'ar' + os.sep not in f]

for filepath in sorted(html_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Revert jQuery defer (single-quote, ver=3.5.1)
    content = content.replace(
        "id='jquery-core-js' defer></script>",
        "id='jquery-core-js'></script>"
    )
    # Revert jQuery defer (double-quote, ver=3.7.1)
    content = content.replace(
        'id="jquery-core-js" defer></script>',
        'id="jquery-core-js"></script>'
    )

    # Revert jquery.tablesorter defer
    content = content.replace(
        "id='essential_addons_elementor-data-table-js-js' defer></script>",
        "id='essential_addons_elementor-data-table-js-js'></script>"
    )
    content = content.replace(
        'id="essential_addons_elementor-data-table-js-js" defer></script>',
        'id="essential_addons_elementor-data-table-js-js"></script>'
    )

    # Revert jquery-ui-core defer
    content = content.replace(
        "id='jquery-ui-core-js' defer></script>",
        "id='jquery-ui-core-js'></script>"
    )
    content = content.replace(
        'id="jquery-ui-core-js" defer></script>',
        'id="jquery-ui-core-js"></script>'
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        stats['jquery'] += 1

print(f'Reverted jQuery/plugins defer in {stats["jquery"]} files')
