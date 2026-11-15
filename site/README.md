# Blackjack engineering notebook

Adopted from AP editorial kit 1.0 (15 November 2026). The source of the project identity is `../docs/site-identity/`. Site-specific instructions are in `AGENTS.md`. Public text is English; project theme is fixed to tactical dark.

## Local review

From this directory:

```sh
python3 build.py
python3 check.py
python3 smoke_test.py
python3 -m http.server 8771 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:8771/. Review mode adds a local banner and component reference. The launch dossier was approved for publication by Alessandro on 15 November 2026. Review mode is local only; production excludes its banner and component-reference page.

## Production

```sh
python3 build.py --production
python3 check.py
```

The root workflow `.github/workflows/pages.yml` builds pull requests without deploying them. Pushes to `main` touching the site or workflow deploy through GitHub Pages. GitHub Pages was configured to use GitHub Actions on 15 November 2026. Alessandro authorised this release on 15 November 2026. Before a push, inspect the complete range, author identity, workflow and media inventory. Never push the private workspace.

Public destination: https://alepistella.github.io/blackjack/.

## Editing

Edit `content/posts/*.html` and `content/posts.json`, then rebuild. `dist/` is ignored generated output. Images and video use relative paths, including project subpaths. `new_post.py` creates a draft. Non-draft dates do not schedule publication.

The homepage and navigation link to the launch dossier by stable slugs. Keep these pages available if adding, removing or drafting other posts. The smoke test covers an additional excluded draft and nested deployment rather than assuming the launch pages can all be removed.

The current web video is an H.264 MP4 exported from Alessandro’s `BlackJack_HiQ_V6_L.mov`, using FFmpeg with libx264 CRF 18, AAC audio at 192 kbit/s and fast-start metadata. The mobile rendition is 1080 × 1350, cropped from `BlackJack_HiQ_V6_P.mov` and selected on initial viewports up to 700 px. Both source masters remain unchanged. Native controls, no autoplay and `preload=none` avoid loading the full video on ordinary page visits.

Website implementation follows the repository’s source-code terms. Article text and diagrams follow its documentation terms; project renderings and video retain all rights reserved. See `../LICENSING.md` and `../REUSE.toml`.
