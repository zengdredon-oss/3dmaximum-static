#!/usr/bin/env python3
"""Round 4: Defer tablesorter+ui-core (save 640ms render-blocking),
add width/height to images, defer fonts.css."""
import os, re, glob

BASE = r'C:\Users\Zeng\Desktop\3dmaximum-static'

stats = {
    'files': 0,
    'tablesorter_deferred': 0,
    'ui_core_deferred': 0,
    'fonts_deferred': 0,
    'images_fixed': 0,
}

html_files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
html_files = [f for f in html_files if os.sep + 'ar' + os.sep not in f]

# === Image dimensions for homepage ===
# Images without width/height on homepage - data-lazy-src filenames and their dimensions
IMG_DIMS = {
    '105_1-p26980lxhhc3l7g5s9hazgtq1yxcdyinfcjxfsu4d6.jpg': (137, 137),
    '76_2-p269uc9xstw9bt0sfevbpc0tyew67655huc2rdqil6.jpg': (137, 137),
    '56_1-p26a4xwevkeo9hmgiztutnpz4un70a86ab77lq0oey.jpg': (137, 137),
    '360-city-min-ns8vdn1zlkbr9o7r829zj58stw8csj4vnhlql3k13u.jpg': (137, 137),
    'Ikonka_79_18-min-ns8ujtmasriayzizc6a1fo4efv76m6revwl8j3rmhm.jpg': (137, 137),
    '102_1-p2699sj419j5cv5xhg5qf1vgok6cdfht6kkf3e2cgw.jpg': (600, 400),
    '106_1-nrwpdjyzpirrhkj8u50s5p732n4cphutl58dlswyao.jpg': (600, 400),
    '105_1-p26980m34j3nfdqruoj3pi04acxdu0g29s7egkp480.jpg': (600, 400),
    '56_1-p26a4xwkim683nx2levnjowdd8n8gc5l4quomhvo9s.jpg': (600, 400),
    '58_1-p26a1oeqsbpdsenqni3ae0jr42qcq6750lazmwpvvk.jpg': (600, 400),
    '44_8-p26a8fuxyeynbeu45xbntt44yvef3s1ma29qxkox40.jpg': (600, 400),
}

for filepath in sorted(html_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # === 1. Defer jquery.tablesorter (save 320ms render-blocking) ===
    # jQuery is still blocking, so tablesorter can safely use $ after DOM parse
    # Single-quote version (25 older pages)
    content = content.replace(
        "id='essential_addons_elementor-data-table-js-js'></script>",
        "id='essential_addons_elementor-data-table-js-js' defer></script>"
    )
    # Double-quote version (3 newer pages)
    content = content.replace(
        'id="essential_addons_elementor-data-table-js-js"></script>',
        'id="essential_addons_elementor-data-table-js-js" defer></script>'
    )
    if "data-table-js-js' defer>" in content or 'data-table-js-js" defer>' in content:
        if "data-table-js-js'></script>" not in original and 'data-table-js-js"></script>' not in original:
            pass  # Already deferred
        else:
            stats['tablesorter_deferred'] += 1

    # === 2. Defer jquery-ui-core (save 320ms render-blocking) ===
    # Single-quote version
    content = content.replace(
        "id='jquery-ui-core-js'></script>",
        "id='jquery-ui-core-js' defer></script>"
    )
    # Double-quote version
    content = content.replace(
        'id="jquery-ui-core-js"></script>',
        'id="jquery-ui-core-js" defer></script>'
    )
    if "ui-core-js' defer>" in content or 'ui-core-js" defer>' in content:
        if "ui-core-js'></script>" not in original and 'ui-core-js"></script>' not in original:
            pass
        else:
            stats['ui_core_deferred'] += 1

    # === 3. Defer fonts.css (save 160ms render-blocking) ===
    # The inline @font-face in <style> already provides the Astra icon font
    # fonts.css only provides Open Sans/Montserrat WOFF2 - safe to defer
    old_fonts = '<link rel="stylesheet" href="/fonts.css?v=2">'
    new_fonts = '<link rel="preload" href="/fonts.css?v=2" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<noscript><link rel="stylesheet" href="/fonts.css?v=2"></noscript>'
    if old_fonts in content:
        content = content.replace(old_fonts, new_fonts)
        stats['fonts_deferred'] += 1

    # === 4. Add width/height to images without them (homepage only) ===
    # Fix lazy-loaded images that have viewBox='0 0 0 0' placeholder
    for img_name, (w, h) in IMG_DIMS.items():
        # Match the img tag with this specific data-lazy-src filename
        # Pattern: <img src="data:image/svg+xml,..." ... data-lazy-src="/wp-content/.../FILENAME" />
        if img_name in content:
            # Find img tags containing this filename that don't have width attribute
            pattern = r'(<img\s+src="data:image/svg\+xml[^"]*")\s+((?:(?!width)[^/])*?data-lazy-src="[^"]*' + re.escape(img_name) + r'[^"]*")\s*(/?>)'
            def add_dims(m):
                stats['images_fixed'] += 1
                return f'{m.group(1)} width="{w}" height="{h}" {m.group(2)} {m.group(3)}'
            content = re.sub(pattern, add_dims, content)

            # Also fix the noscript version of same images
            pattern_noscript = r'(<img\s+src="/wp-content/uploads/elementor/thumbs/' + re.escape(img_name) + r'")\s+((?:(?!width)[^/])*?)(/?>)'
            def add_dims_noscript(m):
                return f'{m.group(1)} width="{w}" height="{h}" {m.group(2)}{m.group(3)}'
            content = re.sub(pattern_noscript, add_dims_noscript, content)

    # Write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        stats['files'] += 1
        rel = os.path.relpath(filepath, BASE).replace('\\', '/')
        print(f'  Updated: {rel}')

print(f'\n=== ROUND 4 RESULTS ===')
for k, v in stats.items():
    print(f'  {k}: {v}')
