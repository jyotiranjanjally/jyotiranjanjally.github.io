"""Check the deployable static site and content contracts without dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import ast
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'_site'
errors=[]
class Document(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.ids=set(); self.links=[]; self.canonical=[]; self.h1=0; self.jsonld=[]; self.capture=False; self.data=''
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: errors.append('Duplicate ID: '+a['id'])
            self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        if tag in ['a','link'] and a.get('href'): self.links.append(a['href'])
        if tag in ['script','img'] and a.get('src'): self.links.append(a['src'])
        if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a['href'])
        if tag=='script' and a.get('type')=='application/ld+json': self.capture=True; self.data=''
    def handle_data(self,data):
        if self.capture: self.data+=data
    def handle_endtag(self,tag):
        if tag=='script' and self.capture:
            self.jsonld.append(json.loads(self.data)); self.capture=False

assert SITE.is_dir(), 'Run python3 scripts/build.py --stage first'
pages={p:Document(p.read_text()) for p in SITE.rglob('*.html')}
for path,doc in pages.items():
    if doc.h1!=1: errors.append(f'{path}: expected one h1, got {doc.h1}')
    if len(doc.canonical)!=1: errors.append(f'{path}: expected one canonical')
    for link in doc.links:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        target=(SITE/unquote(u.path).lstrip('/')) if u.path.startswith('/') else (path.parent/unquote(u.path) if u.path else path)
        if target.is_dir(): target/= 'index.html'
        target=target.resolve()
        if not target.exists(): errors.append(f'{path.relative_to(SITE)}: broken link {link}'); continue
        if u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f'{path.relative_to(SITE)}: missing fragment {link}')
items=json.loads((ROOT/'content/articles.json').read_text())
assert len([a for a in items if a.get('series')=='Regression'])==12
assert len({a['slug'] for a in items})==12
for a in items:
    slug=a['slug']; content=(ROOT/a['content']).read_text()
    required=['slug','title','summary','category','subcategory','topicPath','tags','difficulty','date','related']
    if any(not a.get(k) for k in required): errors.append(f'{slug}: metadata missing')
    if len(re.findall('<details>',content))<8: errors.append(f'{slug}: fewer than 8 interview questions')
    if a.get('example'):
        if '<!-- PYTHON -->' not in content: errors.append(f'{slug}: missing code component')
        ast.parse((ROOT/a['example']).read_text())
    if a.get('chart') and '<!-- CHART -->' not in content: errors.append(f'{slug}: missing chart component')
    doc=pages[SITE/f'articles/{slug}/index.html']
    if len(doc.jsonld)!=1 or doc.jsonld[0].get('@type')!='TechArticle': errors.append(f'{slug}: schema missing')
    if any(s not in {i['slug'] for i in items} for s in a['related']): errors.append(f'{slug}: invalid related article')
    if doc.canonical!=[f'https://jyotiranjanjally.github.io/articles/{slug}/']: errors.append(f'{slug}: wrong canonical')
# Vendored font URLs must resolve as well as HTML assets.
css=SITE/'assets/hub/vendor/katex/katex.min.css'
for link in re.findall(r'url\(([^)]+)\)',css.read_text()):
    if not (css.parent/link.strip('"\'')).exists(): errors.append('Missing math font '+link)
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'Validated {len(pages)} pages, internal links/fragments, metadata, schemas, 12 scripts, interview sections, and math fonts.')
