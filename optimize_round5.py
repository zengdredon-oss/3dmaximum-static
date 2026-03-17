#!/usr/bin/env python3
"""Round 5: Lazy-load JivoChat (saves ~3s CPU) and kuula.io iframes (saves ~1.7s CPU).

JivoChat: Replace immediate async load with delayed load (5s after page load).
  This lets the page fully render before JivoChat starts parsing its heavy bundle.

Kuula.io iframes: Replace src with data-src, load only when user scrolls near them.
  Uses IntersectionObserver for efficient lazy-loading.
"""
import os, glob, re

BASE = r'C:\Users\Zeng\Desktop\3dmaximum-static'
stats = {'jivo_lazy': 0, 'kuula_lazy': 0}

html_files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
html_files = [f for f in html_files if os.sep + 'ar' + os.sep not in f]

# === JivoChat lazy-load snippet ===
# Instead of loading immediately with async, we delay 5 seconds after page load
# This ensures the page is fully interactive before JivoChat starts
JIVO_OLD = '<script src="//code.jivosite.com/widget/oThUZaNuyK" async></script>'
JIVO_NEW = """<script>
(function(){var d=5000;window.addEventListener('load',function(){setTimeout(function(){var s=document.createElement('script');s.src='//code.jivosite.com/widget/oThUZaNuyK';s.async=true;document.body.appendChild(s);},d);});})();
</script>"""

for filepath in sorted(html_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # === 1. Lazy-load JivoChat ===
    if JIVO_OLD in content:
        content = content.replace(JIVO_OLD, JIVO_NEW)
        stats['jivo_lazy'] += 1

    # === 2. Lazy-load kuula.io iframes with IntersectionObserver ===
    # Replace src= with data-src= on kuula iframes, add observer script
    if 'kuula.co' in content:
        # Replace src with data-src on kuula iframes
        content = content.replace(
            'class="ku-embed" frameborder="0" allow="xr-spatial-tracking; gyroscope; accelerometer" allowfullscreen scrolling="no" src="https://kuula.co/',
            'class="ku-embed" frameborder="0" allow="xr-spatial-tracking; gyroscope; accelerometer" allowfullscreen scrolling="no" data-src="https://kuula.co/'
        )

        # Add IntersectionObserver script before </body> if not already present
        if 'ku-embed-observer' not in content:
            observer_script = """<script id="ku-embed-observer">
(function(){var io=new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){var f=e.target;f.src=f.getAttribute('data-src');io.unobserve(f);}});},{rootMargin:'200px'});document.querySelectorAll('iframe.ku-embed[data-src]').forEach(function(f){io.observe(f);});})();
</script>"""
            content = content.replace('</body>', observer_script + '\n</body>')
            stats['kuula_lazy'] += 1

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        rel = os.path.relpath(filepath, BASE).replace('\\', '/')
        print(f'  Updated: {rel}')

print(f'\n=== ROUND 5 RESULTS ===')
for k, v in stats.items():
    print(f'  {k}: {v}')
