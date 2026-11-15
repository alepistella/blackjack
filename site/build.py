#!/usr/bin/env python3
"""Small static publisher, Python standard library only. HTML fragments are trusted source."""
from pathlib import Path
from string import Template
from html import escape
from datetime import date, datetime, timezone
from urllib.parse import urlparse
import argparse, json, math, re, shutil
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
OUT=HERE/'dist'
def esc(s): return escape(str(s), quote=True)
def load(name): return json.loads((HERE/name).read_text())
def template(filename,**values): return Template((HERE/'templates'/filename).read_text()).substitute(values)
def root_for(path): return '../' * len(Path(path).parent.parts)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--production',action='store_true');args=parser.parse_args()
    cfg=load('site.json');allposts=load('content/posts.json')
    if cfg['theme'] not in ('tactical-dark','field-light'): raise ValueError('Unknown theme')
    u=urlparse(cfg['url'])
    if u.scheme!='https' or not u.netloc or u.query or u.fragment:raise ValueError('site.url must be an HTTPS origin plus optional path')
    cfg['url']=cfg['url'].rstrip('/')
    required=('slug','title','date','category','status','summary','tags','body','draft','demo')
    slugs=set()
    for post in allposts:
        for field in required:
            if field not in post:raise ValueError(f'Missing {field}: {post}')
        slug=post['slug']
        if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',slug) or slug in slugs:raise ValueError('Invalid/duplicate slug: '+slug)
        slugs.add(slug);date.fromisoformat(post['date'])
        if 'work_date' in post:
            if date.fromisoformat(post['work_date']) > date.fromisoformat(post['date']):raise ValueError('work_date follows publication')
        if not isinstance(post['draft'],bool) or not isinstance(post['demo'],bool):raise ValueError('draft/demo must be booleans')
        body=(HERE/'content/posts'/post['body']).resolve()
        if not body.is_relative_to((HERE/'content/posts').resolve()) or not body.is_file():raise ValueError('Invalid body file')
        post['html']=body.read_text().replace('{{thermal-lab}}', (HERE/'templates/thermal-lab.html').read_text())
        headings=re.findall(r'<h2\s+id="([a-z0-9-]+)">(.+?)</h2>',post['html'])
        if not headings:raise ValueError('Each article needs h2 headings with stable IDs')
        post['headings']=headings
        if 'updated' in post:
            if date.fromisoformat(post['updated']) < date.fromisoformat(post['date']):raise ValueError('updated precedes publication')
        if args.production and not post['draft'] and (post['demo'] or 'Template example' in post['status'] or re.search(r'\b(TODO|TBD|lorem ipsum)\b',post['html'],re.I)):
            raise ValueError(f'Replace demo/placeholder content before publishing: {slug}. Or keep draft=true.')
    posts=sorted((p for p in allposts if not p['draft']),key=lambda p:(p.get('work_date',p['date']),p['slug']),reverse=True)
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir();shutil.copytree(HERE/'assets',OUT/'assets')
    (OUT/'.nojekyll').touch()
    urls=[]
    def rows(chosen,root):
        if not chosen:return '<p class="empty">No notes published yet.</p>'
        result=[]
        for p in chosen:
            journal_date=p.get('work_date',p['date']);journal_label=esc(p.get('work_label','Published'))
            tags=''.join(f'<span class="tag">{esc(t)}</span>' for t in p['tags'])
            search=esc(' '.join([p['title'],p['summary'],p['category'],*p['tags']]).lower())
            result.append(f'<article class="post-row" data-post data-search="{search}" data-category="{esc(p["category"])}"><div class="post-meta"><time datetime="{journal_date}">{date.fromisoformat(journal_date).strftime("%d %b %Y")}</time><br>{journal_label}<br>{esc(p["category"])}<br>{"DEMO / " if p["demo"] else ""}{esc(p["status"])}</div><div><h3><a href="{root}blog/{p["slug"]}/index.html">{esc(p["title"])}</a></h3><p>{esc(p["summary"])}</p>{tags}</div><span class="post-arrow" aria-hidden="true">↗</span></article>')
        return ''.join(result)
    def write(path,content,title,description,article=None):
        root=root_for(path);canonical=cfg['url']+'/'+('' if path=='index.html' else path.replace('index.html',''))
        urls.append(canonical)
        author={'@type':'Person','@id':cfg['url']+'/#author','name':cfg['author'],'url':cfg['linkedin'],'sameAs':[cfg['author_github'],cfg['linkedin']]}
        structured={'@context':'https://schema.org','@type':'Article' if article else ('CollectionPage' if path=='blog/index.html' else 'WebPage'),'@id':canonical+('#article' if article else '#page'),'headline':article['title'] if article else title,'name':article['title'] if article else title,'description':description,'url':canonical,'inLanguage':'en','author':author,'image':cfg['url']+'/'+cfg['hero_image'],'about':[{'@type':'Thing','name':t['name'],'url':t['url']} for t in cfg['topics']],'isPartOf':{'@type':'WebSite','@id':cfg['url']+'/#website','name':cfg['name']+' / Robotics engineering notebook','url':cfg['url']+'/'}}
        if article:
            structured.update(datePublished=article['date'],dateModified=article.get('updated',article['date']),mainEntityOfPage={'@type':'WebPage','@id':canonical+'#page','url':canonical})
            structured['mainEntityOfPage']['breadcrumb']={'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':cfg['name'],'item':cfg['url']+'/'},{'@type':'ListItem','position':2,'name':'Engineering notebook','item':cfg['url']+'/blog/'},{'@type':'ListItem','position':3,'name':article['title'],'item':canonical}]}
        values={key:esc(cfg[key]) for key in ('name','author','repository','linkedin','theme')}
        values['brand_markup']=(f'<img class="brand-image" src="{root}{esc(cfg["wordmark_image"])}" alt="{esc(cfg.get("wordmark_alt",cfg["name"]))}" width="2172" height="724">' if cfg.get('wordmark_image') else esc(cfg['name']))
        values.update(root=root,title=esc(title),description=esc(description),canonical=esc(canonical),color_scheme='dark' if cfg['theme']=='tactical-dark' else 'light',theme_color='#111714' if cfg['theme']=='tactical-dark' else '#fafbf5',og_type='article' if article else 'website',social_image=esc(cfg['url']+'/'+cfg['hero_image']),social_alt=esc(cfg['hero_alt']),structured_data='<script type="application/ld+json">'+json.dumps(structured).replace('<','\\u003c')+'</script>',content=content,preview_banner='' if args.production else ('<div class="demo-banner"><strong>LOCAL REVIEW</strong> / Episode 01 and proposed timeline. Awaiting editorial approval.</div>' if cfg.get('review_preview') else '<div class="demo-banner"><strong>LOCAL TEMPLATE PREVIEW</strong> / Example notes are not project results. Production builds reject demo content.</div>'),reference_link='' if args.production else f'<a href="{root}styleguide.html">Design system</a>',related=''.join(f'<a href="{esc(r["url"])}">{esc(r["name"])} ↗</a><span class="caption">{esc(r["description"])}</span>' for r in cfg['related']))
        values['interactive_assets'] = (f'<link rel="stylesheet" href="{root}assets/thermal-lab.css?v=1"><script defer src="{root}assets/thermal-model.js?v=1"></script><script defer src="{root}assets/thermal-lab.js?v=1"></script>' if 'data-thermal-lab' in content else '')
        output=OUT/path;output.parent.mkdir(parents=True,exist_ok=True);output.write_text(template('base.html',**values))
    homevalues={key:esc(cfg[key]) for key in ('eyebrow','intro','description','hero_image','hero_alt','hero_caption','name','status','author','about','bio','repository','linkedin')}
    homevalues.update(headline='<br>'.join(esc(cfg['headline']).split('\n')),posts=rows(sorted(sorted(posts,key=lambda p:p['slug'])[:3],key=lambda p:(p.get('work_date',p['date']),p['slug']),reverse=True),''))
    write('index.html',template('home.html',**homevalues),cfg.get('seo_title',cfg['name']+' / Engineering notebook'),cfg['description'])
    categories=sorted({p['category'] for p in posts})
    filters='<div class="filters" hidden><label>Search notes<input id="search" type="search" placeholder="A topic, component or question"></label><label>Category<select id="category"><option value="">All categories</option>'+''.join(f'<option value="{esc(cat)}">{esc(cat)}</option>' for cat in categories)+'</select></label></div><p class="result-count" id="result-count" role="status" aria-live="polite"></p>'
    archive='<header class="page-intro"><div class="eyebrow"><span class="dot" aria-hidden="true"></span>THE NOTEBOOK</div><h1>Decisions, tests<br>and field notes.</h1><p class="standfirst">The work behind the rover, one question at a time.</p></header>'+filters+rows(posts,'../')+'<p id="empty" class="empty" hidden>No matching notes. Try another term or category.</p>'
    write('blog/index.html',archive,cfg['name']+' / Notes','Design decisions, methods and integration notes from '+cfg['name']+'.')
    for p in posts:
        path=f'blog/{p["slug"]}/index.html';root=root_for(path)
        body=p['html'].replace('{{root}}',root)
        content=template('article.html',root=root,category=esc(p['category']),status=esc(p['status']),post_title=esc(p['title']),summary=esc(p['summary']),author=esc(cfg['author']),date=p.get('work_date',p['date']),display_date=date.fromisoformat(p.get('work_date',p['date'])).strftime('%d %B %Y'),date_label=esc(p.get('work_label','Published')),publication_note=(f'<p class="caption">Published {date.fromisoformat(p["date"]).strftime("%d %B %Y")}. The date above identifies the project milestone described in this note.</p>' if 'work_date' in p else ''),reading_time=str(max(1,math.ceil(len(re.findall(r'\w+',re.sub('<[^>]+>',' ',body)))/220))),updated=f'<span>Updated {esc(p["updated"])}</span>' if 'updated' in p else '',demo_label='<p class="caption">Demonstration content. Not a published engineering result.</p>' if p['demo'] else '',toc=''.join(f'<li><a href="#{i}">{re.sub("<[^>]+>","",t)}</a></li>' for i,t in p['headings']),body=body,repository=esc(cfg['repository']))
        write(path,content,p.get('seo_title',p['title']+' / '+cfg['name']),p['summary'],p)
    if not args.production:
        swatches=''.join(f'<div class="swatch"><i style="--sample:var(--{name})"></i><code>--{name}</code></div>' for name in ['bg','surface','text','muted','accent','signal'])
        styleguide='<header class="page-intro"><div class="eyebrow"><span class="dot"></span>SHARED SYSTEM / LOCAL REFERENCE</div><h1>One signature.<br>Two environments.</h1><p class="standfirst">Editorial clarity stays the same. Blackjack keeps its dark, tactical character.</p></header><div class="theme-control" role="group" aria-label="Preview theme"><button data-set-theme="tactical-dark" aria-pressed="true">Tactical dark / Blackjack</button><button data-set-theme="field-light" aria-pressed="false">Field light / dum-e family</button></div><section class="component-panel"><div class="kicker">01 / Colour roles</div><h2>A restrained palette.</h2><div class="swatches">'+swatches+'</div><p class="caption">Semantic tokens keep the same meaning across both themes. Muted text remains readable; orange is an accent, not a wall of colour.</p></section><section class="component-panel"><div class="kicker">02 / Type</div><h2>A question worth testing.</h2><p class="standfirst">An editorial headline, then a concrete explanation.</p><p class="lede">Body copy uses the system sans stack. Metadata uses a small, readable monospace. The serif is reserved for editorial headings.</p><pre><code>input → component → observation</code></pre></section><section class="component-panel"><div class="kicker">03 / Evidence</div><div class="callout"><strong>State the boundary.</strong><p>Analysis, simulation and physical measurements carry different meanings. Label each one.</p></div><div class="link-row"><a class="button" href="blog/index.html">Read the notes ↗</a><a class="button secondary" href="index.html">Project home</a></div></section>'
        write('styleguide.html',styleguide,'Shared editorial system / Reference','Typography, colour roles and reusable components.')
    # XML is generated with ElementTree so project names and summaries are escaped.
    rss=ET.Element('rss',version='2.0');channel=ET.SubElement(rss,'channel')
    for k,v in [('title',cfg['name']+' / Notes'),('link',cfg['url']+'/'),('description',cfg['description'])]:ET.SubElement(channel,k).text=v
    for p in posts:
        item=ET.SubElement(channel,'item');link=cfg['url']+'/blog/'+p['slug']+'/'
        for k,v in [('title',p['title']),('link',link),('guid',link),('description',p['summary']),('pubDate',datetime.fromisoformat(p['date']).replace(tzinfo=timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT'))]:ET.SubElement(item,k).text=v
    ET.ElementTree(rss).write(OUT/'feed.xml',encoding='utf-8',xml_declaration=True)
    ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns);sitemap=ET.Element('{'+ns+'}urlset')
    for url in urls:
        entry=ET.SubElement(sitemap,'{'+ns+'}url');ET.SubElement(entry,'{'+ns+'}loc').text=url
    ET.ElementTree(sitemap).write(OUT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+cfg['url']+'/sitemap.xml\n')
    print(f'Built {len(urls)} pages / {len(posts)} notes / {cfg["theme"]} / '+('PRODUCTION' if args.production else 'PREVIEW'))
if __name__=='__main__':main()
