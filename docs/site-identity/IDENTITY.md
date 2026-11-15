# Visual system / one author, distinct projects

## Direction

The family resemblance is editorial rather than corporate: strong typography, patient spacing, restrained colour, readable figures and enough personality to feel written by someone. The projects do not need the same logo or the same brightness.

**Blackjack is dark and tactical.** Use dense graphite surfaces, cool silver text, olive/green operational cues and a restrained orange accent. Its existing stencil wordmark supplies the industrial character. Render the wordmark directly on the surface, without a black rectangular badge. The starter uses theme-aware CSS compositing while retaining the original PNG. Keep that stencil out of paragraphs and long headings. Avoid neon dashboards, fake telemetry, crosshairs, warning stripes, military claims and glowing effects. A tactical visual direction does not establish a robot's deployment capability.

**dum-e is light and editorial.** Preserve the paper canvas, deep green text, orange middle dot and lime highlights. This kit supplies a compatible light theme, not a replacement export of the existing dum-e site.

## Three identities

| Role | Identity | Rule |
| --- | --- | --- |
| Author | Alessandro Pistella / original AP monogram | Author credit and personal links; do not invent a new AP asset |
| Project | dum-e / dum·e wordmark | Original mark for that project only |
| Project | Blackjack / approved BLACKJACK artwork | Original stencil, not the dum-e wordmark with a different name |

The trailing orange dot is **not** a mandatory family logo feature. Do not attach it to Blackjack. A small orange section marker is an editorial component, not a logo extension.

## Typography

| Role | Font | Desktop | Mobile | Treatment |
| --- | --- | --- | --- | --- |
| Editorial h1 | Georgia, Times New Roman, serif | fluid 48-78 px | 49 px | Regular, 1.05 line-height, restrained negative tracking |
| Section h2 | Same serif | fluid 30-44 px | 31-33 px | Regular, 1.15 line-height |
| Article/list title | Same serif | 31 px | 29 px | Sentence case, no all-caps paragraphs |
| Body | Inter if present, then system UI / Apple system / Segoe UI / sans-serif | 17 px | 16 px | 1.75-1.85 line-height, roughly 65-70 characters per line |
| Standfirst | Same sans | 21 px | 20 px | 1.55 line-height, around 42 characters per line |
| Metadata / code | UI monospace / SFMono / Consolas | 11 px labels, 13 px code | Same or readable equivalent | Tracking only on short labels; no long uppercase prose |
| Captions | Body sans | 12 px | 12 px | Explain content and provenance |
| Blackjack logo | Supplied artwork | Width 170 px in header | 140 px | Preserve ratio; do not retype |

The font stack is intentionally local. Inter is not downloaded or guaranteed. If exact cross-platform metrics become necessary, choose and license a self-hosted font explicitly, update both projects' rules, and recheck wrapping. Never claim that a raster logo is composed in Georgia, Inter or a guessed stencil font.

## Semantic colour contract

| Token | Tactical dark | Field light | Purpose |
| --- | --- | --- | --- |
| bg | #111714 | #fafbf5 | Page canvas |
| surface | #19211d | #edf2e3 | Callouts and support panels |
| surface-raised | #222d26 | #e3ebd9 | Nested or elevated surface |
| text | #e1e7df | #233d39 | Primary reading |
| muted | #a9b5ac | #5c6f68 | Metadata, captions, secondary text |
| line | #3a4b40 | #b5c4ae | Separators and borders, never critical text |
| accent | #ec956b | #a64121 | Restrained warm accent |
| signal | #b0c98a | #205a49 | Primary action and labelled state |
| link | #bad2b7 | #205a49 | Text links, also underlined in prose |
| highlight | #35432a | #e0f09b | Highlight backing, not small text |
| code-bg | #0c120f | #eaf0e2 | Code panel |
| focus | #efba78 | #8d3d23 | Keyboard focus ring |

Dark accents are adjusted for legibility, not copied from the light theme. The light body's orange is darker than dum-e's decorative #d75f36 because small coloured text needs sufficient contrast. Use the original brighter orange only for non-text decorative elements when appropriate. Colour roles are defined in `starter/assets/tokens.css`; JSON is the handoff mirror.

## Layout and spacing

- Maximum canvas: 1220 px. Desktop gutters: 48 px. Mobile gutters: 20 px.
- Body grid: 4 px base; common increments 8, 12, 16, 24, 32, 48, 64 and 96 px.
- Homepage: project statement next to real imagery, a status strip, project/bio section, then actual notes. No endless uniform feature-card grid.
- Article: max reading width 70ch; an optional 170 px sticky index alongside the prose. On mobile the index becomes an inline list.
- Prefer fine rules, alignment and whitespace to boxed containers. Use a panel only when it groups useful secondary information.
- Corner radius: typically 3-6 px for Blackjack. Keep industrial restraint; no bubble UI or pill-shaped everything.
- Tables/code scroll inside their containers; the entire page must never require horizontal scrolling.

## Images, figures and motion

Use the real project image or existing CAD render with an honest caption. Keep landscape 16:9 or 16:11 image slots stable with explicit dimensions. Do not brighten, restage or retouch evidence to imply a test that did not happen. The copied Blackjack assets are local reference copies of the author's existing media; see SOURCES.md for their terms.

Diagrams explain inputs, outputs, component boundaries and dependencies. Use units on axes and readable labels at mobile width. A before/after table includes both conditions. Do not use nominal frames per second, timing or counts as unqualified performance claims.

No decorative animations by default. Motion is appropriate for a recorded trajectory, a mechanism or a state transition. Provide a static reading path and respect `prefers-reduced-motion`.

## Ready-to-use components

`starter/dist/styleguide.html` is the visual reference: theme controls, semantic palette, headings, standfirst, metadata, code, evidence callout and primary/secondary buttons. The example study adds an index, table, architecture sequence and provenance callouts. Reuse these instead of starting another design language in each article.
