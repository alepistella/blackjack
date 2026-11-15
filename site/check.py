#!/usr/bin/env python3
"""Check generated local links, fragments, metadata, IDs and image alternatives."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json, re, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent/'dist'
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.links=[];self.errors=[];self.h1=0;self.main=0;self.title=0;self.description=False;self.canonical=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:self.errors.append('Duplicate id '+a['id'])
            self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='main':self.main+=1
        if tag=='title':self.title+=1
        if tag=='meta' and a.get('name')=='description':self.description=bool(a.get('content'))
        if tag=='link' and a.get('rel')=='canonical':self.canonical=a.get('href','').startswith('https://')
        if tag=='img':
            if 'alt' not in a:self.errors.append('Missing image alt')
            if not a.get('width') or not a.get('height'):self.errors.append('Missing image dimensions')
        for key in ('href','src','data-portrait-src','data-portrait-poster'):
            if key in a:self.links.append(a[key])

def main():
    pages={};errors=[]
    for f in ROOT.rglob('*.html'):
        text=f.read_text();page=Page();page.feed(text);pages[f.resolve()]=page
        if re.search(r'\$\{?[a-zA-Z_][a-zA-Z_]*\}?|\{\{root\}\}',text):errors.append(f'{f}: unresolved template marker')
        if page.h1!=1 or page.main!=1 or page.title!=1 or not page.description or not page.canonical:page.errors.append('Invalid h1/main/title/description/canonical contract')
        errors.extend(f'{f}: {e}' for e in page.errors)
    for f,page in pages.items():
        for raw in page.links:
            url=urlsplit(raw)
            if url.scheme or url.netloc:continue
            if url.path.startswith('/'):errors.append(f'{f}: root-relative link breaks project portability: {raw}');continue
            target=(f.parent/unquote(url.path)).resolve() if url.path else f
            if target.is_dir():target=target/'index.html'
            if not target.is_relative_to(ROOT.resolve()) or not target.exists():errors.append(f'{f}: missing local target {raw}');continue
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:errors.append(f'{f}: missing fragment {raw}')
    for css in (ROOT/'assets').glob('*.css'):
        for url in re.findall(r"url\(['\"]?([^)'\"]+)",css.read_text()):
            if not urlsplit(url).scheme and not (css.parent/urlsplit(url).path).exists():errors.append(f'{css}: missing stylesheet dependency {url}')
    for name in ('feed.xml','sitemap.xml'):ET.parse(ROOT/name)
    if not pages:errors.append('No built pages')
    if errors:raise SystemExit('\n'.join(errors))
    print(f'PASS / {len(pages)} HTML pages / local links, anchors, image alternatives, dimensions, metadata, CSS imports, RSS and sitemap')
if __name__=='__main__':main()
