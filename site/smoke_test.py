#!/usr/bin/env python3
"""Exercise the adopted notebook publishing contracts in a disposable copy."""
from pathlib import Path
import tempfile, shutil, json, subprocess, sys
SOURCE = Path(__file__).resolve().parent
def run(folder, *args):
    result = subprocess.run([sys.executable, *args], cwd=folder, capture_output=True, text=True)
    return result
with tempfile.TemporaryDirectory(prefix='blackjack-site-check-') as tmp:
    root = Path(tmp) / 'site'
    shutil.copytree(SOURCE, root, ignore=shutil.ignore_patterns('dist', '__pycache__'))
    postfile = root / 'content/posts.json'
    posts = json.loads(postfile.read_text())
    posts[0]['demo'] = True
    postfile.write_text(json.dumps(posts))
    result = run(root, 'build.py', '--production')
    assert result.returncode != 0 and 'Replace demo' in result.stderr
    posts[0]['demo'] = False
    draft = dict(posts[0], slug='unpublished-fixture', draft=True)
    posts.append(draft)
    postfile.write_text(json.dumps(posts))
    cfgfile = root / 'site.json'
    cfg = json.loads(cfgfile.read_text())
    cfg.update(theme='field-light', url='https://example.org/projects/blackjack')
    cfgfile.write_text(json.dumps(cfg))
    result = run(root, 'build.py', '--production')
    assert result.returncode == 0, result.stderr
    result = run(root, 'check.py')
    assert result.returncode == 0, result.stdout + result.stderr
    assert not (root / 'dist/styleguide.html').exists()
    assert not (root / 'dist/blog/unpublished-fixture').exists()
    home = (root / 'dist/index.html').read_text()
    assert 'data-theme="field-light"' in home
    assert 'LOCAL REVIEW' not in home
    article = (root / 'dist/blog/01-a-bigger-question/index.html').read_text()
    assert 'https://example.org/projects/blackjack/blog/01-a-bigger-question/' in article
    assert '../../assets/style.css' in article
    assert '../../assets/video/blackjack-launch-v6.mp4' in article
    assert '../../assets/video/blackjack-launch-v6-portrait.mp4' in article
    assert '../../assets/images/blackjack-launch-v6-portrait-poster.jpg' in article
    assert 'unpublished-fixture' not in (root / 'dist/feed.xml').read_text()
    # Journal milestones must not silently backdate actual publication metadata.
    assert '<time datetime="2026-11-13">13 November 2026</time>' in article
    assert '"datePublished": "2026-11-15"' in article
    assert 'Published 15 November 2026' in article
    assert '13 Nov 2026' in home and '14 Nov 2026' in home and '15 Nov 2026' in home
    assert 'Arduino VENTUNO Q robot, Qualcomm &amp; Waveshare</title>' in home
    home_notes=home[home.index('id="latest"'):]
    assert home_notes.index('blog/03-the-decisions-under-the-skin/') < home_notes.index('blog/02-inside-blackjack/') < home_notes.index('blog/01-a-bigger-question/')
    assert 'id="software-route"' in home and 'Qualcomm AI Hub' in home
    assert home.count('class="architecture-step"')==4
    assert 'Diagram revision 02' in home and 'Evidence feeds the next decision.' in home
    stack_article=(root / 'dist/blog/02-inside-blackjack/index.html').read_text()
    assert 'A finding that earns its own session' in stack_article
    assert 'YOLOX-Small' in stack_article and 'QIR SDK 2.6.1' in stack_article
    assert 'id="essential-bom"' in home
    assert 'Qualcomm Dragonwing IQ8 (QCS8275) + STM32H5F5' in home
    from html.parser import HTMLParser
    class StructuredData(HTMLParser):
        def __init__(self):super().__init__();self.active=False;self.chunks=[]
        def handle_starttag(self,tag,attrs):self.active = tag=='script' and dict(attrs).get('type')=='application/ld+json'
        def handle_endtag(self,tag):
            if tag=='script':self.active=False
        def handle_data(self,data):
            if self.active:self.chunks.append(data)
    parser=StructuredData();parser.feed(article);data=json.loads(''.join(parser.chunks))
    assert data['author']['name']=='Alessandro Pistella'
    assert data['about'][0]['name']=='Arduino VENTUNO Q'
    assert data['mainEntityOfPage']['breadcrumb']['itemListElement'][0]['item']=='https://example.org/projects/blackjack/'
    assert data['datePublished']=='2026-11-15'
    assert data['mainEntityOfPage']['@id']!=data['@id']
    assert data['mainEntityOfPage']['url']==data['url']

    assert '<pubDate>Sun, 15 Nov 2026' in (root / 'dist/feed.xml').read_text()

    posts[0]['work_date'] = '2026-11-16'
    postfile.write_text(json.dumps(posts))
    result = run(root, 'build.py', '--production')
    assert result.returncode != 0 and 'work_date follows publication' in result.stderr
    posts[0]['work_date'] = '2026-11-13'
    posts.append(posts[0].copy())
    postfile.write_text(json.dumps(posts))
    result = run(root, 'build.py')
    assert result.returncode != 0 and 'duplicate slug' in result.stderr
print('PASS / demo gate, draft exclusion, production banner removal, article output, theme, nested canonical, relative media, RSS, duplicate slug rejection')
