#!/usr/bin/env python3
"""Create a draft without overwriting a post. Usage: python3 new_post.py a-new-note"""
from pathlib import Path
from datetime import date
import json,re,sys
root=Path(__file__).resolve().parent
if len(sys.argv)!=2 or not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',sys.argv[1]):raise SystemExit('Usage: python3 new_post.py lowercase-hyphenated-slug')
slug=sys.argv[1];index=root/'content/posts.json';posts=json.loads(index.read_text());body=root/'content/posts'/f'{slug}.html'
if body.exists() or any(p['slug']==slug for p in posts):raise SystemExit('That slug already exists; nothing changed.')
body.write_text('<h2 id="question">The question</h2>\n<p>TODO: state the question and its scope.</p>\n<h2 id="method">Method and boundary</h2>\n<p>TODO: setup, versions, input, controls and evidence.</p>\n<h2 id="result">Result and interpretation</h2>\n<p>TODO: observations with units, limits and sources.</p>\n<h2 id="reproduce">Reproduce</h2>\n<p>TODO: exact revision, commands, raw data and expected output.</p>\n')
posts.append(dict(slug=slug,title='A specific question',date=date.today().isoformat(),category='Engineering',status='Draft',summary='Replace with a concrete one-sentence summary.',tags=[],body=body.name,draft=True,demo=False))
index.write_text(json.dumps(posts,indent=2)+'\n');print('Created draft:',body)
