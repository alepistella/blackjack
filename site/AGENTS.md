# Shared editorial identity / agent contract

This document governs work inside this kit. If adopting the kit in a repository, retain it as site-level instructions and reconcile it with that repository's existing instructions; do not overwrite a repository's root AGENTS.md blindly. Human instructions take precedence.

## Read first

Read `../docs/site-identity/IDENTITY.md`, `../docs/site-identity/EDITORIAL.md`, `../docs/site-identity/BLACKJACK_WORDMARK.md`, and `../docs/site-identity/PUBLISHING.md`. Then inspect the current project source and status. The kit is a scaffold, not authority for technical claims.

## Identity boundaries

- Blackjack: `tactical-dark`, original BLACKJACK stencil artwork, graphite/green surfaces, cool lettering and restrained warm accent. No dum-e middle dot appended to its logo.
- dum-e: `field-light`, original dum·e artwork and the existing light editorial site. Do not deploy this Blackjack configuration over dum-e.
- Alessandro Pistella: author identity. AP is a separate personal monogram; do not generate or approximate it. No new series name, lab name or umbrella brand without a user request.
- Shared signature: editorial headline hierarchy, body stack, spacing, evidence components, navigation patterns and writing standards. A later shared domain must not require changing project marks.

## Implementation rules

1. Modify sources, not `dist/`. Use `site.json` for project configuration, `assets/tokens.css` for semantic colours, `assets/style.css` for reusable components, and `templates/` for layouts. Update `tokens/design-tokens.json` if changing the contract.
2. Use existing components before inventing a variant. Never scatter literal colours in article HTML. Do not add a framework, build service, font download or package dependency merely to publish a static article.
3. Keep pages readable without JS. Search and theme controls are enhancements; the archive and article bodies must already exist in HTML. The public project theme is fixed by configuration, not by OS preference or a browser-stored toggle.
4. Keep local URLs relative to each generated page. Configure the exact final `site.url` for canonical, RSS and sitemap. Test project subpaths, not only a domain root.
5. Authored HTML fragments are trusted code in the repository, not sanitised user content. Never ingest remote comments, arbitrary Markdown-to-HTML output or untrusted HTML without an explicit sanitisation design.
6. Use one h1, meaningful h2 IDs, descriptive links, image alternatives, dimensions and captions. Tables need units, captions and header cells. Use visible focus, keyboard operability and non-colour distinctions. Keep body contrast at least WCAG AA where tested.
7. Respect existing media rights. Do not invent a font name for a raster wordmark. Do not upscale or redraw the Blackjack mark as if it were an approved vector. Preserve its aspect ratio, counters, cuts and finish.

## Content rules

Public prose is English unless requested otherwise. Working instructions can be Italian. Write as an experienced engineer explaining a concrete choice to a peer. No em dashes, self-congratulation, sensational comparisons, unsupported superlatives, recruitment pitches or claims of novelty without evidence.

Distinguish design intent, analysis, simulation and physical measurement. Name versions, test boundaries and data sources where they affect interpretation. A render is not a built prototype. A planned measurement is not a result. Attribute work accurately: who set the goal, generated code or weights, selected changes, ran tests and interpreted evidence. Do not append a generic assistant footer; do not hide method provenance when it matters.

No fake dates, metrics, testimonials, test counts, badges, GitHub statistics, benchmark wins or unsupported hardware capabilities. Keep demo=true for examples, draft=true for unfinished notes. Production rejects visible demos and basic placeholders; this gate does not replace human fact review.

## Required verification and handoff

- `python3 build.py` and `python3 check.py` in starter (or the adopted site folder).
- `python3 smoke_test.py` after changing generator/configuration contracts.
- Before publication: `python3 build.py --production` and `python3 check.py` with actual content.
- Inspect the homepage, archive, long article and component reference on desktop and at 390 px; check an intermediate width too. Ensure no page-wide horizontal overflow. Tables and code may scroll within their containers.
- Exercise search, category filtering, empty results, article anchors and the local theme reference. Inspect images and console errors. Honour reduced motion and readable print output.
- Confirm the correct source branch, site path and Pages settings. Do not publish simply because a workflow file exists. User authorisation is still required for the actual destination.
- Report changed files, checks performed, any untested limits, and where to open the preview. Preserve unrelated work and do not run broad cleanup commands in another repository.
