"""Build the static portfolio with Python's standard library. No server build required."""
import json
import hashlib
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://salmanhaider.pro/'
EMAIL = 'salman12haider13@gmail.com'
LINKEDIN = 'https://www.linkedin.com/in/salman12haider13'
GITHUB = 'https://github.com/salman12haider13'
RESUME = 'assets/docs/Salman-Haider-GIS-Analyst-Resume.pdf'
PORTRAIT = 'assets/images/profile/salman-headshot.webp'
SIZES = json.loads((ROOT / 'content/image-sizes.json').read_text(encoding='utf-8'))
MAPS = json.loads((ROOT / 'content/maps.json').read_text(encoding='utf-8'))
TOOLS = json.loads((ROOT / 'content/tools.json').read_text(encoding='utf-8'))
PROFILE = json.loads((ROOT / 'content/profile.json').read_text(encoding='utf-8'))
ARTICLES = json.loads((ROOT / 'content/articles.json').read_text(encoding='utf-8'))
SEO = PROFILE['seo']
PROJECTS = MAPS + TOOLS
BY_SLUG = {p['slug']: p for p in PROJECTS}
LABELS = {'analysis': 'Spatial analysis', 'cartography': 'Cartography', 'tools': 'Code & tools'}
CSS_VERSION = hashlib.sha256((ROOT/'portfolio.css').read_bytes()).hexdigest()[:10]
JS_VERSION = hashlib.sha256((ROOT/'portfolio.js').read_bytes()).hexdigest()[:10]

def e(text):
    return escape(str(text), quote=True)

def paras(items, cls=''):
    return '\n'.join(f'<p{f" class={e(cls)}" if cls else ""}>{e(p)}</p>' for p in items)

def image(src, alt, prefix='', lazy=True, cls=''):
    dims = SIZES.get(src)
    size = f' width="{dims[0]}" height="{dims[1]}"' if dims else ''
    return f'<img src="{prefix}{e(src)}" alt="{e(alt)}"{size} loading="{"lazy" if lazy else "eager"}" decoding="async"{f" class={e(cls)}" if cls else ""}>'

def display(src):
    if '/maps/full/' in src:
        return str(Path(src.replace('/full/', '/display/')).with_suffix('.webp')).replace('\\', '/')
    return src

def ext_link(url, label):
    return f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)}<span class="sr-only"> (opens in a new tab)</span></a>'

def header(active, prefix):
    links = [('index.html', 'Home', 'home'), ('work.html', 'Work', 'work'), ('about.html', 'About', 'about'), ('articles/', 'Articles', 'articles')]
    nav = ''.join(f'<a href="{prefix}{url}"{chr(32) + "aria-current=page" if active == key else ""}>{label}</a>' for url, label, key in links)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap site-nav"><a class="wordmark" href="{prefix}index.html">Salman Haider</a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" hidden>Menu</button>
<nav id="primary-nav" class="primary-nav" aria-label="Main navigation">{nav}<a href="{prefix}index.html#contact">Contact</a><a href="{prefix}{RESUME}">Resume <span aria-hidden="true">↗</span><span class="sr-only"> (PDF)</span></a></nav></div></header>'''

def footer(prefix):
    return f'''<section class="contact" id="contact" aria-labelledby="contact-title"><div class="wrap contact-inner"><div><h2 id="contact-title">Get in touch</h2><p>I’m looking for GIS opportunities across Canada. You can reach me by email or on LinkedIn.</p></div><div class="actions"><a class="button" href="mailto:{EMAIL}">Email me</a>{ext_link(LINKEDIN, 'LinkedIn')}</div></div></section>
<footer class="site-footer"><div class="wrap footer-inner"><p>© 2026 Salman Haider</p><div class="footer-links">{ext_link(GITHUB, 'GitHub')}<a href="{prefix}{RESUME}">Resume (PDF)</a><a href="mailto:{EMAIL}">Email</a></div></div></footer>'''

VIEWER = '''<dialog class="map-dialog" aria-labelledby="viewer-title"><div class="viewer-head"><h2 id="viewer-title">Image</h2><div class="viewer-controls"><button type="button" data-zoom="out" aria-label="Zoom out">−</button><button type="button" data-zoom="in" aria-label="Zoom in">+</button><button type="button" data-zoom="fit">Fit</button><button type="button" data-close autofocus>Close</button></div></div><div class="map-stage" tabindex="0" aria-label="Image viewer. Use plus and minus to zoom, arrow keys to pan, and Escape to close."><img alt="" hidden draggable="false"><p class="viewer-status" role="status">Loading image…</p></div><div class="viewer-foot"><span>Zoom to read details. Drag to move around.</span><a data-original target="_blank" rel="noopener">Open original image</a></div></dialog>'''

def page_url(path):
    return BASE + (path[:-10] if path.endswith('index.html') else path)

def write_page(path, title, description, body, active='', viewer=False, social=None, project=None, article=None, noindex=False):
    prefix = '../' * (len(Path(path).parts) - 1)
    if path == '404.html':
        prefix = '/'
    canonical = page_url(path)
    social_path = social or 'assets/images/social/portfolio-preview.png'
    # Link previews have much broader raster support than SVG.
    if social_path.endswith('.svg'):
        raster = str(Path(social_path).with_suffix('.png')).replace('\\', '/')
        social_path = raster if (ROOT/raster).exists() else 'assets/images/social/portfolio-preview.png'
    social = BASE + social_path
    person = {'@type': 'Person', '@id': BASE+'#person', 'name': 'Salman Haider', 'url': BASE+'about.html', 'jobTitle': 'GIS Professional', 'image': BASE+PORTRAIT, 'sameAs': [LINKEDIN, GITHUB], 'description': SEO['description'], 'homeLocation': {'@type': 'Country', 'name': 'Canada'}, 'alumniOf': {'@type': 'CollegeOrUniversity', 'name': 'University of Calgary', 'url': 'https://www.ucalgary.ca/'}, 'hasCredential': {'@type': 'EducationalOccupationalCredential', 'name': 'Master of Geographic Information Systems', 'credentialCategory': 'Master’s degree', 'recognizedBy': {'@type': 'CollegeOrUniversity', 'name': 'University of Calgary'}}, 'knowsAbout': ['Geographic Information Systems (GIS)', 'Spatial analysis', 'Cartography', 'Python and ArcPy automation', 'ArcGIS Pro', 'PostGIS', 'Web GIS', 'Remote sensing']}
    website = {'@type': 'WebSite', '@id': BASE+'#website', 'url': BASE, 'name': 'Salman Haider GIS Portfolio', 'inLanguage': 'en-CA', 'publisher': {'@id': BASE+'#person'}}
    page_type = 'ProfilePage' if active == 'about' else 'CollectionPage' if path in ('work.html', 'articles/index.html') else 'WebPage'
    webpage = {'@type': page_type, '@id': canonical+'#webpage', 'url': canonical, 'name': title, 'description': description, 'inLanguage': 'en-CA', 'isPartOf': {'@id': BASE+'#website'}, 'about': {'@id': BASE+'#person'}}
    nodes = [person, website, webpage]
    if active == 'about':
        webpage['mainEntity'] = {'@id': BASE+'#person'}
    if project:
        creative = {'@type': 'SoftwareSourceCode' if project['kind'] == 'tool' else 'CreativeWork', '@id': canonical+'#project', 'url': canonical, 'name': project['title'], 'description': description, 'author': {'@id': BASE+'#person'}, 'mainEntityOfPage': {'@id': canonical+'#webpage'}, 'genre': LABELS[project['category']]}
        if project.get('repo'):
            creative['codeRepository'] = project['repo']
            creative['programmingLanguage'] = [t for t in project['tools'] if t in ('Python','JavaScript','SQL','R','HTML','CSS')]
        if project['figures']:
            creative['image'] = [BASE+f['src'] for f in project['figures']]
            creative['hasPart'] = [{'@type': 'ImageObject', 'contentUrl': BASE+f['src'], 'name': f['title'], 'caption': f['caption']} for f in project['figures']]
        webpage['mainEntity'] = {'@id': canonical+'#project'}
        nodes.append(creative)
    if path == 'work.html':
        nodes.append({'@type': 'ItemList', '@id': canonical+'#projects', 'numberOfItems': len(PROJECTS), 'itemListElement': [{'@type': 'ListItem', 'position': i+1, 'url': BASE+'projects/'+p['slug']+'.html', 'name': p['title']} for i,p in enumerate(PROJECTS)]})
        webpage['mainEntity'] = {'@id': canonical+'#projects'}
    if article:
        story = {'@type': 'BlogPosting', '@id': canonical+'#article', 'headline': article['title'], 'description': description, 'datePublished': article['date'], 'author': {'@id': BASE+'#person'}, 'mainEntityOfPage': {'@id': canonical+'#webpage'}, 'image': social}
        if article.get('modified'):
            story['dateModified'] = article['modified']
        webpage['mainEntity'] = {'@id': canonical+'#article'}
        nodes.append(story)
    if project or article:
        section_url = BASE + ('work.html' if project else 'articles/')
        section_name = 'Work' if project else 'Articles'
        nodes.append({'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem','position': 1,'name': 'Home','item': BASE}, {'@type': 'ListItem','position': 2,'name': section_name,'item': section_url}, {'@type': 'ListItem','position': 3,'name': project['title'] if project else article['title'],'item': canonical}]})
    schema = {'@context': 'https://schema.org', '@graph': nodes}
    indexing = 'noindex, follow' if noindex else 'index, follow, max-image-preview:large'
    social_dims = SIZES.get(social_path)
    image_meta = (f'<meta property="og:image:width" content="{social_dims[0]}"><meta property="og:image:height" content="{social_dims[1]}">' if social_dims else '')
    extra_meta = f'<meta name="robots" content="{indexing}"><meta name="author" content="Salman Haider"><meta property="og:site_name" content="Salman Haider GIS Portfolio"><meta property="og:locale" content="en_CA"><meta property="og:image:alt" content="{e(title)}"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{social}">{image_meta}'
    page = f'''<!doctype html>
<html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#f5f2eb"><link rel="canonical" href="{canonical}"><meta property="og:type" content="{"article" if article else "website"}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{social}"><meta name="twitter:card" content="summary_large_image">{extra_meta}<link rel="icon" href="{prefix}assets/images/social/favicon.png"><link rel="stylesheet" href="{prefix}portfolio.css?v={CSS_VERSION}"><script src="{prefix}portfolio.js?v={JS_VERSION}" defer></script><script type="application/ld+json">{json.dumps(schema)}</script></head><body>
{header(active, prefix)}
<main id="main" tabindex="-1">{body}</main>
{footer(prefix)}
{VIEWER if viewer else ''}
</body></html>'''
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding='utf-8')

def cover(p, css='feature-visual'):
    href = f'projects/{p["slug"]}.html'
    if p.get('thumbnail'):
        return f'<a class="{css}" href="{href}" tabindex="-1" aria-hidden="true">{image(p["thumbnail"]["src"], "")}</a>'
    if p['figures']:
        f = p['figures'][0]
        src = display(f['src'])
        return f'<a class="{css}" href="{href}" tabindex="-1" aria-hidden="true">{image(src, "")}</a>'
    return ''

def feature(slug, reverse=False, small=False):
    p = BY_SLUG[slug]
    visual = cover(p)
    text = f'<p class="eyebrow">{e(LABELS[p["category"]])}</p><h3><a href="projects/{slug}.html">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p><a class="project-link" href="projects/{slug}.html">Read the project<span class="sr-only">: {e(p["title"])}</span></a>'
    if small:
        return f'<article class="small-feature">{visual}{text}</article>'
    cls = 'feature' + (' feature-reverse' if reverse else '') + (' feature-tool' if p['kind'] == 'tool' else '')
    return f'<article class="{cls}">{visual}<div class="feature-copy">{text}</div></article>'

home = f'''<div class="wrap"><section class="hero" aria-labelledby="home-title"><div class="hero-text"><div class="hero-identity"><p class="eyebrow">Canada</p><h1 id="home-title">Salman Haider</h1><p class="hero-role">GIS Professional</p></div><p class="hero-description">I’ve worked on franchise territories, land records and public transit access, and built Python tools to automate GIS workflows. Here I’ve put together some of my maps and tools, with the questions, decisions and results behind them.</p><div class="actions"><a class="button" href="#work">View my work</a><a href="about.html">About me</a><a href="{RESUME}">Resume (PDF)</a></div></div><figure>{image(PORTRAIT, 'Salman Haider', lazy=False, cls='portrait')}</figure></section><div class="career-note"><span><strong>105+</strong> franchise territory projects</span><span><strong>4+</strong> years of applied GIS experience</span><span>Master of Geographic Information Systems</span></div><section class="section" id="work" aria-labelledby="selected-title"><div class="section-heading"><h2 id="selected-title">Selected work</h2><a href="work.html">All projects →</a></div>{feature('calgary-parks')}{feature('geo-copilot', reverse=True)}<div class="selected-pair">{feature('calgary-housing', small=True)}{feature('forestry-sampling', small=True)}</div></section></div>
<section class="section experience-preview" aria-labelledby="experience-title"><div class="wrap"><div class="section-heading"><h2 id="experience-title">Work experience</h2><a href="about.html#experience">Full experience →</a></div><div class="experience-grid"><article><h3>Franchise Ready</h3><p>I worked on more than 105 territory projects, turning franchise requirements and demographic data into territories, maps and dashboards.</p></article><article><h3>University of Calgary</h3><p>I used transit schedules and network analysis to examine access to fresh food across Calgary.</p></article><article><h3>Greenage Services</h3><p>I worked with scanned land records, georeferencing and digitization, and used Python to help sort the records.</p></article></div></div></section>
<section class="section"><div class="wrap personal-preview"><div><h2>Outside work</h2><p>{e(PROFILE['personal']['text'])}</p><a class="project-link" href="about.html#outside-work">A little more about me</a></div><figure>{image('assets/images/off-the-map/web/1000216467.webp', 'Salman walking along Ogden Point Breakwater in Victoria')}<figcaption>Ogden Point Breakwater, Victoria</figcaption></figure></div></section>'''
write_page('index.html', SEO['title'], SEO['description'], home, 'home')

ordered = [BY_SLUG[s] for s in ['calgary-parks','geo-copilot','calgary-housing','logistics-routing','heathrow-connections','paradise-valley','town-of-olds','drone-route-reporting','forestry-sampling','ndvi-zonal-stats','flood-settlements','prhps-coverage','red-carpet','spatial-reference-checker','csv-survey-points','lidar-metadata','tree-canopy','health-geography']]
cards = ''.join(f'<article class="work-card{chr(32) + 'is-utility' if not p['figures'] else ''}" data-category="{p["category"]}">{cover(p, "work-image")}<p class="eyebrow">{e(LABELS[p["category"]])}</p><h2><a href="projects/{p["slug"]}.html">{e(p["title"])}</a></h2><p>{e(p["summary"])}</p><a class="project-link" href="projects/{p["slug"]}.html">Read the project<span class="sr-only">: {e(p["title"])}</span></a></article>' for p in ordered)
filters = ''.join(f'<button type="button" class="filter-button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{e(label)}</button>' for key, label in [('all','All work'), *LABELS.items()])
write_page('work.html', 'GIS Projects and Python Tools | Salman Haider', 'Explore GIS projects by Salman Haider, a GIS professional in Canada working with spatial analysis, cartography, Python automation and web mapping.', f'<div class="wrap"><header class="page-intro"><h1>Work</h1><p>Maps, analysis and tools I’ve made. Each project includes the approach, the result and what I would keep in mind when using it.</p></header><div class="filters" role="group" aria-label="Filter projects" hidden>{filters}</div><p class="result-count" role="status">18 projects</p><div class="work-grid">{cards}</div></div>', 'work')

def figure(f, lazy=True):
    src = f['src']
    rendered = display(src)
    dims = SIZES.get(src, [1200,800])
    css = 'project-figure is-portrait' if dims[1] / dims[0] > 1.15 else 'project-figure'
    if '/evidence/' in src and src.endswith('.svg'):
        css += ' is-diagram'
    if '/charts/' in src:
        css += ' is-chart'
    title = e(f['title'])
    return f'''<figure class="{css}"><h2>{title}</h2><a class="figure-frame" href="../{e(src)}" data-inspect data-title="{title}" aria-label="Inspect {title}">{image(rendered, f['alt'], '../', lazy=lazy)}</a><figcaption class="figure-caption"><p>{e(f['caption'])}</p><a href="../{e(src)}" data-inspect data-title="{title}">Inspect details<span class="sr-only">: {title}</span></a></figcaption></figure>'''

for n, p in enumerate(ordered):
    facts = p['facts'] + ([{'label': 'Tools', 'value': ', '.join(p['tools'])}] if p['tools'] else [])
    facts_html = ''.join(f'<div{chr(32) + "class=fact-tools" if f["label"] == "Tools" else ""}><dt>{e(f["label"])}</dt><dd>{e(f["value"])}</dd></div>' for f in facts)
    body = f'<article class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../work.html">Work</a> / {e(p["title"])}</nav><header class="project-header"><p class="eyebrow">{e(LABELS[p["category"]])}</p><h1>{e(p["title"])}</h1><div class="intro">{paras(p["intro"])}</div>'
    if p.get('repo'):
        body += f'<div class="actions">{ext_link(p["repo"], "View source on GitHub")}</div>'
    body += f'</header><dl class="project-facts">{facts_html}</dl><div class="case-body">'
    section_ids = [re.sub(r'[^a-z0-9]+', '-', s['title'].lower()).strip('-') for s in p['sections']]
    if len(p['sections']) > 4:
        body += '<nav class="page-outline" aria-label="Project sections"><strong>On this page</strong><ul>' + ''.join(f'<li><a href="#{section_ids[i]}">{e(s["title"])}</a></li>' for i,s in enumerate(p['sections'])) + '</ul></nav>'
    figures = p['figures']
    shown_figures = set()
    lead = p.get('leadFigure', 0)
    if figures and lead is not None:
        body += figure(figures[lead], lazy=False)
        shown_figures.add(lead)
    for i, section in enumerate(p['sections']):
        body += f'<section class="case-text" id="{section_ids[i]}"><h2>{e(section["title"])}</h2>{paras(section["paragraphs"])}</section>'
        indices = section.get('figureIndices', [i+1] if i+1 < len(figures) else [])
        for fig_index in indices:
            if fig_index in shown_figures:
                raise ValueError(f'Duplicate figure placement: {p["slug"]} {fig_index}')
            body += figure(figures[fig_index])
            shown_figures.add(fig_index)
    if len(shown_figures) != len(figures):
        raise ValueError(f'Unplaced figures in {p["slug"]}')
    if p['sources']:
        sources = ''.join(f'<li>{ext_link(s["url"], s["label"]) if s.get("url") else e(s["label"])}</li>' for s in p['sources'])
        body += f'<section class="source-list"><h2>Data and references</h2><ul>{sources}</ul></section>'
    next_p = ordered[(n+1) % len(ordered)]
    body += f'<nav class="project-bottom" aria-label="More projects"><a href="../work.html">← All work</a><a href="{next_p["slug"]}.html">{e(next_p["title"])} →</a></nav></div></article>'
    social = p.get('thumbnail', {}).get('src') or (display(figures[0]['src']) if figures else None)
    write_page(f'projects/{p["slug"]}.html', f'{p["title"]} | Salman Haider', p['summary'], body, 'work', viewer=bool(figures), social=social, project=p)

def institution_logo(r):
    if not r.get('logo'):
        return ''
    return f'<div class="institution-logo">{image(r["logo"], "")}</div>'

experience = ''.join(f'<article class="experience-item"><div class="institution-heading">{institution_logo(r)}<div><time>{e(r["dates"])}</time><h3>{e(r["organization"])}</h3><p class="role">{e(r["title"])}</p></div></div>{paras(r["paragraphs"])}</article>' for r in PROFILE['experience'])
education = ''.join(f'<div class="education-item institution-heading">{institution_logo(r)}<div><h3>{e(r["degree"])}</h3><p>{e(r["institution"])}</p><p>{e(r["dates"])}</p></div></div>' for r in PROFILE['education'])
capabilities = ''.join(f'<div class="capability"><h3>{e(r["title"])}</h3><p>{e(r["text"])}</p></div>' for r in PROFILE['capabilities'])
tool_directory = '<div class="tool-directory">' + ''.join(f'<section class="tool-group"><h3>{e(g["title"])}</h3><p>{e(" · ".join(g["items"]))}</p></section>' for g in PROFILE['toolGroups']) + '</div>'
photos = ''.join(f'<figure>{image(f["src"], f["alt"])}<figcaption>{e(f["caption"])}</figcaption></figure>' for f in PROFILE['personal']['photos'])
about = f'<div class="wrap"><header class="about-intro"><div><h1>About me</h1>{paras(PROFILE["intro"])}<div class="actions"><a class="button" href="{RESUME}">Resume (PDF)</a>{ext_link(LINKEDIN, "LinkedIn")}<a href="#tools">Tools and technologies</a></div></div><figure>{image(PORTRAIT, "Salman Haider", lazy=False)}</figure></header><section class="about-section anchor-target" id="experience"><h2>Experience</h2><div>{experience}</div></section><section class="about-section"><h2>Education</h2><div>{education}</div></section><section class="about-section"><h2>What I work with</h2><div>{capabilities}</div></section><section class="about-section anchor-target" id="tools"><h2>Tools and technologies</h2><div><p class="tools-intro">These are the tools I’ve used across work and projects, with additional training listed separately.</p>{tool_directory}</div></section><section class="section anchor-target" id="outside-work"><h2>Outside work</h2><div class="case-text">{paras([PROFILE["personal"]["text"]])}</div><div class="photo-grid">{photos}</div></section></div>'
write_page('about.html', SEO['aboutTitle'], SEO['aboutDescription'], about, 'about')
write_page('404.html', 'Page not found | Salman Haider', 'This page could not be found.', '<div class="wrap section"><h1>Page not found</h1><p>The page may have moved. You can find all my projects on the Work page.</p><div class="actions"><a class="button" href="/work.html">View work</a><a href="/">Home</a></div></div>', noindex=True)

# Future posts use a small metadata entry and an HTML fragment. No CMS is needed.
article_cards = []
for a in sorted(ARTICLES, key=lambda item: item['date'], reverse=True):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', a['slug']):
        raise ValueError('Article slugs must use lowercase words separated by hyphens.')
    article_body = (ROOT/'content/articles'/f'{a["slug"]}.html').read_text(encoding='utf-8')
    article_path = f'articles/{a["slug"]}.html'
    story_body = f'<article class="wrap article-page"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Articles</a> / {e(a["title"])}</nav><header class="project-header"><h1>{e(a["title"])}</h1><p class="article-byline">By Salman Haider · <time datetime="{e(a["date"])}">{e(a["date"])}</time></p><div class="intro"><p>{e(a["description"])}</p></div></header><div class="article-body">{article_body}</div><nav class="project-bottom"><a href="index.html">← All articles</a><a href="../work.html">View projects →</a></nav></article>'
    write_page(article_path, f'{a["title"]} | Salman Haider', a['description'], story_body, 'articles', social=a.get('image'), article=a)
    article_cards.append(f'<article class="article-list-item"><time datetime="{e(a["date"])}">{e(a["date"])}</time><h2><a href="{a["slug"]}.html">{e(a["title"])}</a></h2><p>{e(a["description"])}</p></article>')
articles_body = '<div class="wrap"><header class="page-intro"><h1>Articles</h1><p>I’ll be writing about GIS projects, scripts and tools, and sharing what I learn as I work on them.</p></header>'
articles_body += ''.join(article_cards) if article_cards else '<section class="articles-empty"><h2>More to come</h2><p>There are no articles here yet. In the meantime, you can read about the projects I’ve already worked on.</p><a class="project-link" href="../work.html">Explore my projects</a></section>'
articles_body += '</div>'
write_page('articles/index.html', 'Articles | Salman Haider', 'Notes on GIS projects, Python scripts, spatial analysis and the tools I build.', articles_body, 'articles', noindex=not ARTICLES)

paths = ['index.html', 'work.html', 'about.html'] + [f'projects/{p["slug"]}.html' for p in ordered]
if ARTICLES:
    paths += ['articles/index.html'] + [f'articles/{a["slug"]}.html' for a in ARTICLES]
sitemap_entries = []
for path in paths:
    image_entries = ''
    if path.startswith('projects/'):
        p = BY_SLUG[Path(path).stem]
        image_entries = ''.join(f'<image:image><image:loc>{e(BASE+f["src"])}</image:loc></image:image>' for f in p['figures'])
    sitemap_entries.append(f'  <url><loc>{e(page_url(path))}</loc>{image_entries}</url>')
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + '\n'.join(sitemap_entries) + '\n</urlset>\n', encoding='utf-8')
print(f'Built {len(paths)} indexable pages, Articles landing page and 404.html.')
