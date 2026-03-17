#!/usr/bin/env python3
"""Fix remaining carousel images without width/height on homepage."""
import os

filepath = os.path.join(r'C:\Users\Zeng\Desktop\3dmaximum-static', 'index.html')

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
original = content

# Carousel images: class="swiper-slide-image" src="data:..." alt="X" data-lazy-src="..."
# Need to add width="600" height="400" to each
carousel_imgs = [
    ('102_1-p2699sj419j5cv5xhg5qf1vgok6cdfht6kkf3e2cgw.jpg', 600, 400),
    ('106_1-nrwpdjyzpirrhkj8u50s5p732n4cphutl58dlswyao.jpg', 600, 400),
    ('105_1-p26980m34j3nfdqruoj3pi04acxdu0g29s7egkp480.jpg', 600, 400),
    ('56_1-p26a4xwkim683nx2levnjowdd8n8gc5l4quomhvo9s.jpg', 600, 400),
    ('58_1-p26a1oeqsbpdsenqni3ae0jr42qcq6750lazmwpvvk.jpg', 600, 400),
    ('44_8-p26a8fuxyeynbeu45xbntt44yvef3s1ma29qxkox40.jpg', 600, 400),
]

count = 0
for img_name, w, h in carousel_imgs:
    # Fix lazy-loaded version: <img class="swiper-slide-image" src="data:..." alt="X" data-lazy-src="...IMG..."
    old_marker = f'data-lazy-src="/wp-content/uploads/elementor/thumbs/{img_name}"'
    if old_marker in content and f'width="{w}"' not in content.split(old_marker)[0].split('<img')[-1]:
        # Add width/height before data-lazy-src
        content = content.replace(
            old_marker,
            f'width="{w}" height="{h}" {old_marker}'
        )
        count += 1

    # Fix noscript version: <img class="swiper-slide-image" src="/wp-content/.../IMG"
    noscript_marker = f'src="/wp-content/uploads/elementor/thumbs/{img_name}"'
    # Only fix in noscript context (after </noscript> pattern)
    for old_frag in [f'<img class="swiper-slide-image" {noscript_marker}']:
        if old_frag in content:
            content = content.replace(
                old_frag,
                f'<img class="swiper-slide-image" width="{w}" height="{h}" {noscript_marker}'
            )

if content != original:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Fixed {count} carousel images with width/height')
else:
    print('No changes needed')
