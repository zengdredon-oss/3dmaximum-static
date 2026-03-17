#!/usr/bin/env python3
"""Comprehensive optimization script for 3dmaximum-static site."""
import os, re, glob

BASE = r'C:\Users\Zeng\Desktop\3dmaximum-static'
DOMAIN = 'https://3dmaximum.com'

# Meta descriptions for each page (based on titles and content)
META_DESCS = {
    'index.html': '3D Maximum — студия компьютерной графики. 3D визуализация интерьеров, экстерьеров, анимация, моделирование и виртуальные туры.',
    '3d-visualization-services': '3D visualization services by 3D Maximum studio. Interior, exterior, product visualization, animation and 3D modeling.',
    '3d-vizualizatsiya-mebeli-novyie-vozmozhnosti-sozdaniya-individualnogo-interera': '3D визуализация мебели — новые возможности создания индивидуального интерьера. Реалистичные рендеры мебели от студии 3D Maximum.',
    'vizualizatsiya-interera-v-kieve-chto-neobhodimo-sdelat-do-nachala-remonta': 'Визуализация интерьера в Киеве: что необходимо сделать до начала ремонта. Советы от студии 3D Maximum.',
    'blog': 'Блог студии 3D Maximum — статьи о 3D визуализации, моделировании, анимации и компьютерной графике.',
    'kontakty': 'Контакты студии 3D Maximum. Свяжитесь с нами для заказа 3D визуализации, анимации или моделирования.',
    'portfolio': 'Портфолио студии 3D Maximum — примеры работ: 3D визуализация интерьеров, экстерьеров, предметная визуализация.',
    'uslugi': 'Услуги студии 3D Maximum — визуализация проектов, 3D анимация, моделирование, виртуальные туры и VR/AR.',
    'uslugi/sozdaniye-3d-animatsii': 'Создание 3D анимации на заказ. Архитектурная анимация, рекламные ролики, визуализация процессов от студии 3D Maximum.',
    'uslugi/sozdaniye-3d-modeley': 'Создание 3D моделей на заказ — от простых объектов до сложных промышленных изделий. Студия 3D Maximum.',
    'uslugi/vr-ar-prilozheniya': 'Разработка VR и AR приложений. Виртуальная и дополненная реальность от студии 3D Maximum.',
    'uslugi/3d-tury': '3D туры и виртуальные прогулки. Интерактивные панорамы 360° для недвижимости и бизнеса.',
    'uslugi/3d-tury/panorama-360': 'Панорама 360° — интерактивные сферические фотографии для виртуальных туров. Студия 3D Maximum.',
    'uslugi/3d-tury/virtualnyie-progulki': 'Виртуальные прогулки — интерактивные 3D туры по интерьерам и экстерьерам. Студия 3D Maximum.',
    '3d-vizualizatsiya': '3D визуализация — фотореалистичные рендеры интерьеров, экстерьеров и объектов от студии 3D Maximum.',
    '3d-vizualizatsiya/3d-vizualizatsiya-interyera': '3D визуализация интерьера — реалистичные рендеры жилых и коммерческих помещений. Студия 3D Maximum.',
    '3d-vizualizatsiya/vizualizatsiya-eksteryera': 'Визуализация экстерьера — 3D рендеры фасадов, ландшафтов и архитектурных объектов.',
    '3d-vizualizatsiya/arkhitekturnaya-3d-vizualizatsiya': 'Архитектурная 3D визуализация — реалистичные рендеры зданий и сооружений. Стиль и качество от 3D Maximum.',
    '3d-vizualizatsiya/predmetnaya-vizualizatsiya': 'Предметная визуализация — от декора до промышленных механизмов. 3D рендеры продуктов для каталогов и рекламы.',
    '3d-vizualizatsiya-tsena': '3D визуализация: цены и сроки выполнения. Таблица стоимости услуг студии 3D Maximum.',
    '3d-vizualizatsiya-tsena/vizualizatsiya-interyera-tsena': 'Стоимость визуализации интерьера. Цены на 3D рендеры помещений от студии 3D Maximum.',
    '3d-vizualizatsiya-tsena/vizualizatsiya-eksterera-tsena': 'Визуализация экстерьера — минимальные цены на 3D рендеры фасадов и архитектуры.',
    '3d-vizualizatsiya-tsena/arhitekturnaja-vizualizacija-tsena': 'Архитектурная визуализация — цены и сроки выполнения. Студия 3D Maximum.',
    '3d-vizualizatsiya-tsena/predmetnaja-tsena': 'Предметная визуализация — цены на 3D рендеры продуктов и объектов.',
    '3d-vizualizatsiya-tsena/3d-tury-panoramy-tsena': '3D туры и панорамы 360° — стоимость создания виртуальных туров. Студия 3D Maximum.',
    '3d-vizualizatsiya-tsena/zakazat-3d-animaciju': 'Заказать 3D анимацию — стоимость и сроки создания анимационных роликов.',
    '3d-vizualizatsiya-tsena/zakazat-3d-model': 'Заказать 3D модель — стоимость создания 3D моделей на заказ. Студия 3D Maximum.',
    'zakazat-3d-vizualizatsiyu': 'Заказать 3D визуализацию в студии 3D Maximum. Быстро, качественно, по доступной цене.',
}

# CSS files to defer (non-critical for first render)
CSS_TO_DEFER = [
    "to-top-public.css",
    "animations.min.css",
    "frontend-legacy.min.css",
    "brands.min.css",
]

stats = {'files': 0, 'canonical': 0, 'meta_desc': 0, 'fonts_moved': 0,
         'preconnect': 0, 'iframe_title': 0, 'yt_alt': 0, 'css_deferred': 0,
         'lcp_preload': 0, 'kuula_lazy': 0}

html_files = glob.glob(os.path.join(BASE, '**', 'index.html'), recursive=True)
# Skip ar/index.html (it's a different kind of page)
html_files = [f for f in html_files if os.sep + 'ar' + os.sep not in f]

for filepath in sorted(html_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    rel_path = os.path.relpath(filepath, BASE).replace('\\', '/')
    # Get page key for meta descriptions
    page_key = os.path.dirname(rel_path).replace('\\', '/')
    if page_key == '.' or page_key == '':
        page_key = 'index.html'

    # === 1. Fix canonical URLs to absolute ===
    def fix_canonical(m):
        href = m.group(1)
        if not href.startswith('http'):
            stats['canonical'] += 1
            return f'<link rel="canonical" href="{DOMAIN}{href}"'
        return m.group(0)
    content = re.sub(r'<link rel="canonical" href="([^"]*)"', fix_canonical, content)

    # === 2. Add meta description if missing ===
    if 'meta name="description"' not in content and page_key in META_DESCS:
        desc = META_DESCS[page_key]
        # Insert after <meta name="viewport"> or after <meta charset>
        if '<meta name="viewport"' in content:
            content = content.replace(
                '<meta name="viewport" content="width=device-width, initial-scale=1">',
                '<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="description" content="' + desc + '" />'
            )
            stats['meta_desc'] += 1
        elif '<meta charset=' in content:
            content = re.sub(
                r'(<meta charset="[^"]*"\s*/?>)',
                r'\1\n<meta name="description" content="' + desc + '" />',
                content, count=1
            )
            stats['meta_desc'] += 1

    # === 3. Move fonts.css from body to head ===
    # Remove fonts.css from wherever it is in body
    fonts_link_pattern = r'\n?<link rel="stylesheet" href="/fonts\.css">\n?'
    if re.search(fonts_link_pattern, content):
        # Check if it's after </head> (i.e., in body)
        head_end = content.find('</head>')
        fonts_match = re.search(fonts_link_pattern, content)
        if fonts_match and fonts_match.start() > head_end:
            # Remove from body
            content = re.sub(fonts_link_pattern, '\n', content)
            # Add to head (before </head>)
            content = content.replace('</head>', '<link rel="stylesheet" href="/fonts.css">\n</head>')
            stats['fonts_moved'] += 1
    # If fonts.css not found at all, add it to head
    elif '/fonts.css' not in content:
        content = content.replace('</head>', '<link rel="stylesheet" href="/fonts.css">\n</head>')
        stats['fonts_moved'] += 1

    # === 4. Add preconnect for kuula.co (on pages with kuula iframes) ===
    if 'kuula.co' in content and 'preconnect' not in content:
        preconnect = '<link rel="preconnect" href="https://kuula.co" crossorigin>\n<link rel="preconnect" href="https://static.kuula.io" crossorigin>\n<link rel="preconnect" href="https://files.kuula.io" crossorigin>\n'
        content = content.replace('</head>', preconnect + '</head>')
        stats['preconnect'] += 1

    # === 5. LCP hero image preload (homepage only) ===
    if page_key == 'index.html' and 'preload' not in content.split('</head>')[0]:
        preload = '<link rel="preload" as="image" href="/wp-content/uploads/2018/05/79_18.jpg">\n'
        content = content.replace('</head>', preload + '</head>')
        stats['lcp_preload'] += 1

    # === 6. Add loading="lazy" to kuula iframes ===
    def add_lazy_kuula(m):
        iframe_tag = m.group(0)
        if 'loading=' not in iframe_tag:
            stats['kuula_lazy'] += 1
            return iframe_tag.replace('<iframe ', '<iframe loading="lazy" ')
        return iframe_tag
    content = re.sub(r'<iframe[^>]*kuula\.co[^>]*>', add_lazy_kuula, content)

    # === 7. Add title to iframes without title ===
    def add_iframe_title(m):
        iframe = m.group(0)
        if 'title=' in iframe:
            return iframe
        stats['iframe_title'] += 1
        if 'kuula.co' in iframe:
            return iframe.replace('<iframe ', '<iframe title="Виртуальный 3D тур" ')
        elif 'youtube' in iframe.lower() or 'youtu.be' in iframe.lower():
            return iframe.replace('<iframe ', '<iframe title="YouTube видео" ')
        elif 'sirv.com' in iframe:
            return iframe.replace('<iframe ', '<iframe title="3D обзор объекта" ')
        else:
            return iframe.replace('<iframe ', '<iframe title="Встроенный контент" ')
        return iframe
    content = re.sub(r'<iframe[^>]*>', add_iframe_title, content)

    # === 8. Add alt to YouTube thumbnail images ===
    def add_yt_alt(m):
        img = m.group(0)
        if 'alt=' in img:
            return img
        stats['yt_alt'] += 1
        return img.replace('<img ', '<img alt="Видео превью" ')
    # Match img tags with ytimg.com sources
    content = re.sub(r'<img[^>]*i\.ytimg\.com[^>]*>', add_yt_alt, content)

    # === 9. Defer non-critical CSS ===
    for css_file in CSS_TO_DEFER:
        # Pattern: <link rel='stylesheet' ... href='...css_file...' media='all' />
        pattern = r"(<link\s+rel='stylesheet'[^>]*" + re.escape(css_file) + r"[^>]*/\s*>)"
        match = re.search(pattern, content)
        if match:
            old_tag = match.group(1)
            # Extract href
            href_match = re.search(r"href='([^']*)'", old_tag)
            if href_match:
                href = href_match.group(1)
                # Replace with preload + noscript pattern
                new_tag = f'<link rel="preload" href="{href}" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">'
                new_tag += f'\n<noscript><link rel="stylesheet" href="{href}"></noscript>'
                content = content.replace(old_tag, new_tag)
                stats['css_deferred'] += 1

    # Write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        stats['files'] += 1
        print(f'  Updated: {rel_path}')

print(f'\n=== RESULTS ===')
for k, v in stats.items():
    print(f'  {k}: {v}')
