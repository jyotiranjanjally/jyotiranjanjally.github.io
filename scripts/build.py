"""Build the static knowledge hub with only the Python standard library."""
from pathlib import Path
import argparse
import html
import json
import math
import re
import shutil
from datetime import date
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://jyotiranjanjally.github.io'
E = html.escape


def read(path):
    return (ROOT / path).read_text()


def page(title, description, path, body, structured=None, detail=False):
    schema_json = json.dumps(structured).replace('<', '\\u003c')
    schema = f'<script type="application/ld+json">{schema_json}</script>' if structured else ''
    math_assets = '''<link rel="stylesheet" href="/assets/hub/vendor/katex/katex.min.css">
<script defer src="/assets/hub/vendor/katex/katex.min.js"></script>''' if detail else ''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | Jyoti Ranjan Jally</title><meta name="description" content="{E(description)}">
<link rel="canonical" href="{BASE}{path}"><meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}"><meta property="og:url" content="{BASE}{path}">
<meta property="og:type" content="{'article' if detail else 'website'}"><meta name="theme-color" content="#f5f4f1">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/assets/hub/hub.css">
<script>try{{document.documentElement.dataset.theme=localStorage.getItem('portfolio-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}}catch(e){{document.documentElement.dataset.theme='light'}}</script>
{math_assets}{schema}<script defer src="/app.js"></script><script defer src="/assets/hub/hub.js"></script>
{'<script defer src="/assets/hub/charts.js"></script>' if detail else ''}</head><body id="top" class="knowledge-hub">
<a class="skip" href="#main">Skip to content</a>{read('content/templates/header.html')}
{body}{read('content/templates/footer.html')}</body></html>'''


def topic_url(category, topic=''):
    return '/articles.html?' + E(urlencode({'category': category, **({'topic': topic} if topic else {})}))


def directory(categories):
    sections = []
    for category, topics in categories.items():
        links = []
        for topic, children in topics.items():
            children_html = ' → ' + ', '.join(f'<a href="{topic_url(category, child)}">{E(child)}</a>' for child in children) if children else ''
            links.append(f'<li><a href="{topic_url(category, topic)}">{E(topic)}</a>{children_html}</li>')
        sections.append(f'<details><summary>{E(category)}</summary><ul>{"".join(links)}</ul></details>')
    return ''.join(sections)


def card(a):
    label = E(a['subcategory'].upper()) + (f" / {a['seriesOrder']:02}" if a.get('series') else '')
    return f'''<article class="hub-card" data-category="{E(a['category'])}" data-topic="{E(a['subcategory'])}" data-search="{E(' '.join([a['title'], a['summary'], *a['tags'], *a['topicPath']]).lower())}">
<div class="card-top"><span class="eyebrow">{label}</span><span class="difficulty">{E(a['difficulty'])}</span></div>
<h3><a href="/articles/{a['slug']}/">{E(a['title'])}</a></h3><p>{E(a['summary'])}</p>
<div class="card-bottom"><span>{a['readingTime']} min read</span><span>Read tutorial ↗</span></div></article>'''


def build():
    items = json.loads(read('content/articles.json'))
    categories = json.loads(read('content/categories.json'))
    bodies = {}
    for a in items:
        raw = read(a["content"])
        # Code lives in executable files, never in a separate untested copy.
        if a.get('example'):
            code = read(a['example'])
            raw = raw.replace('<!-- PYTHON -->', f'<p><a class="download-code" href="/{E(a["example"])}" download>Download the complete Python script ↓</a> · <a href="/examples/requirements.txt">Python requirements</a></p><div class="code-wrap"><button class="copy-code" type="button">Copy code</button><pre><code class="language-python">{E(code)}</code></pre></div>')
        a['readingTime'] = max(1, math.ceil(len(re.sub('<[^>]+>', ' ', raw).split()) / 190))
        bodies[a['slug']] = raw
    lookup = {a['slug']: a for a in items}
    for a in items:
        series = sorted([item for item in items if a.get('series') and item.get('series') == a['series']], key=lambda item: item['seriesOrder'])
        i = series.index(a) if series else 0
        series_label = f"THE {E(a['series'].upper())} SERIES / {i+1:02} OF {len(series):02}" if series else E(a['category'].upper())
        published = date.fromisoformat(a['date']).strftime('%d %B %Y').lstrip('0')
        tags = ''.join(f'<a href="/articles.html?{E(urlencode({"q": tag}))}">{E(tag)}</a>' for tag in a['tags'])
        raw = bodies[a['slug']]
        headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', raw)
        toc = ''.join(f'<li><a href="#{ident}">{E(re.sub(r"^[0-9]+[.] ", "", label))}</a></li>' for ident, label in headings)
        breadcrumbs = '<a href="/articles.html">Knowledge hub</a> / ' + ' / '.join(f'<a href="{topic_url(a["category"], t if level else "")}">{E(t)}</a>' for level, t in enumerate(a['topicPath']))
        chart = f'''<figure class="lab" data-chart="{E(a.get('chart', 'line'))}"><div class="lab-heading"><span class="eyebrow">INTERACTIVE LAB</span><span>Change one variable. Observe the effect.</span></div><div class="lab-controls"></div><svg viewBox="0 0 700 340" role="img" aria-label="Interactive regression diagram"></svg><p class="chart-summary" aria-live="polite"></p><figcaption>Figure 1. A deterministic educational experiment; values are calculated from the displayed model. See the controls and summary for a text interpretation.</figcaption><noscript>Enable JavaScript to explore this diagram. The worked example below provides the numerical explanation.</noscript></figure>'''
        raw = raw.replace('<!-- CHART -->', chart)
        related = ''.join(f'<li><a href="/articles/{s}/">{E(lookup[s]["title"])}</a></li>' for s in a['related'])
        prev = f'<a rel="prev" href="/articles/{series[i-1]["slug"]}/">← Previous<br>{E(series[i-1]["title"])}</a>' if i else '<a href="/articles.html">← All tutorials</a>'
        nxt = f'<a rel="next" href="/articles/{series[i+1]["slug"]}/">Next →<br>{E(series[i+1]["title"])}</a>' if i+1 < len(series) else '<a href="/articles.html">Explore the knowledge hub →</a>'
        body = f'''<div class="reading-progress" aria-hidden="true"></div><main id="main" class="wrap"><nav class="breadcrumbs" aria-label="Breadcrumb">{breadcrumbs}</nav>
<header class="reading-header"><p class="eyebrow">{series_label}</p><h1>{E(a['title'])}</h1><p class="standfirst">{E(a['summary'])}</p><div class="reading-meta"><span class="difficulty">{a['difficulty']}</span><span>{a['readingTime']} min read</span><time datetime="{a['date']}">{published}</time></div><nav class="article-tags" aria-label="Article tags">{tags}</nav></header>
<div class="reading-layout"><aside class="toc"><nav aria-label="Table of contents"><p class="eyebrow">ON THIS PAGE</p><ol>{toc}</ol></nav><a href="{topic_url(a['category'], a['subcategory'])}">Explore this topic ↗</a></aside>
<article class="tutorial">{raw}<section class="related"><h2 id="related">Continue learning</h2><ul>{related}</ul></section><nav class="series-nav" aria-label="Series navigation">{prev}{nxt}</nav></article></div></main>'''
        schema = {'@context':'https://schema.org','@type':'TechArticle','headline':a['title'],'description':a['summary'],'datePublished':a['date'],'author':{'@type':'Person','name':'Jyoti Ranjan Jally','url':BASE},'mainEntityOfPage':BASE+f"/articles/{a['slug']}/",'articleSection':a['topicPath'],'keywords':a['tags'],'proficiencyLevel':a['difficulty'],'inLanguage':'en'}
        dest = ROOT / 'articles' / a['slug']
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'index.html').write_text(page(a['title'],a['summary'],f"/articles/{a['slug']}/",body,schema,True))
    legacy = re.findall(r'<details class="article-entry".*?</details>', read('content/legacy-articles.html'), re.S)
    legacy_count = len(legacy)
    legacy = ''.join(legacy).replace('class="article-entry"','class="article-entry legacy-note"')
    # Retain all original IDs so homepage links and external bookmarks keep working.
    legacy = legacy.replace('data-category="foundations"','data-category="Machine Learning" data-topic="Model Evaluation"').replace('data-category="ai"','data-category="Artificial Intelligence" data-topic="AI Agents"')
    topic_options = sorted(set([topic for sub in categories.values() for topic, children in sub.items() for topic in ([topic]+children)]))
    filters = ''.join(f'<button type="button" data-hub-category="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in categories)
    topics = ''.join(f'<option>{E(t)}</option>' for t in topic_options)
    body = f'''<main id="main" class="wrap"><section class="hub-hero"><div><a class="back-link" href="/index.html">← Back to portfolio</a><p class="eyebrow">THE ENGINEERING NOTEBOOK</p><h1>Understand deeply.<br><span>Build with confidence.</span></h1><p class="standfirst">Mathematics you can follow. Code you can run.<br>A growing library for the curious engineer.</p></div><div class="hub-index"><span>01—12</span><p>A complete path through<br>regression, from first principles.</p><a href="/articles/introduction-to-regression/">Start the series ↗</a></div></section>
<section class="hub-library" aria-labelledby="library-title"><div class="library-heading"><h2 id="library-title">Explore the knowledge hub</h2><span class="eyebrow">{len(items)} TUTORIALS · {legacy_count} ENGINEERING NOTES</span></div>
<form class="hub-search" role="search"><label for="article-search">Search the library<input id="article-search" type="search" placeholder="Try ridge, Python, or gradient descent…" autocomplete="off"></label><label for="topic-select">Topic<select id="topic-select"><option value="">All topics</option>{topics}</select></label><button type="reset">Reset filters</button></form>
<div class="category-tabs" role="group" aria-label="Filter by category"><button type="button" data-hub-category="" aria-pressed="true">All categories</button>{filters}</div>
<p id="hub-results" role="status">{len(items) + legacy_count} articles</p><div class="hub-grid">{''.join(card(a) for a in items)}</div><p id="hub-empty" hidden>No articles match these filters yet. Choose another topic or reset the filters to explore the regression series.</p>
<section class="legacy-notes"><h2>Engineering notes</h2>{legacy}</section></section>
<section class="topic-directory"><h2>A map for your learning</h2><p>Browse the topic hierarchy. Categories without published articles show an honest empty state.</p>{directory(categories)}</section></main>'''
    (ROOT / 'articles.html').write_text(page('Technical Knowledge Hub','Explore regression tutorials, executable Python, mathematical derivations, and engineering notes.','/articles.html',body))
    (ROOT / 'assets/hub/catalog.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
    urls = ['/', '/articles.html'] + [f"/articles/{a['slug']}/" for a in items]
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{u}</loc></url>' for u in urls)+'</urlset>\n')
    (ROOT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
    print(f'Built {len(items)} tutorials and preserved {len(re.findall("<details",legacy))} engineering notes.')


def stage():
    dest = ROOT/'_site'
    if dest.exists(): shutil.rmtree(dest)
    dest.mkdir()
    for name in ['index.html','articles.html','style.css','app.js','favicon.svg','sitemap.xml','robots.txt']:
        shutil.copy2(ROOT/name,dest/name)
    for name in ['assets','articles','examples']:
        shutil.copytree(ROOT/name,dest/name,ignore=shutil.ignore_patterns('__pycache__'))
    (dest/'.nojekyll').touch()
    print('Staged deployable files in _site/')

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--stage',action='store_true')
    args=parser.parse_args()
    build()
    if args.stage: stage()
