# BLACKJACK wordmark / artwork, not body type

The approved local project asset is copied unchanged from:

`/Users/alessandropistella/Documents/Curriculum/ROS/Tank/blackjack/blackjack/docs/images/blackjack-lettering-spray.png`

The copy used by the starter is `starter/assets/images/blackjack-lettering.png`. It is a cold grey, spray-finished, uppercase stencil on black, with chamfered forms and diagonal cuts. The original author selected the second flat variant and asked for a spray treatment; the published variant is the opaque black-background artwork.

## Font status

The creating chat **Revisore testi** records an image-generation workflow with bespoke stencil lettering. Its prompts request custom letter forms; they do not identify an installed or licensed font. The visible artwork is not evidence that a particular commercial font was used. The creating chat confirmed on 15 November 2026 that no named font, font file, vector paths or exact typographic parameters exist. The approved master is the opaque RGB PNG, 2172 x 724 px, at `Tank/media/texts/blackjack-lettering-spray-black.png`; the repository copy is identical.

Treat BLACKJACK as a **custom raster wordmark with no identified font file**. Do not guess a similar font or claim one as exact. Typography for body copy, metadata and editorial headings remains separately defined in IDENTITY.md.

## Application

- Keep the approved PNG unchanged as the source master. On the website, show the lettering directly on the page using the theme-aware compositing rule in `.brand-image`, with no visible black rectangle.
- Preserve aspect ratio, letter spacing, diagonal cuts, counters and finish. Do not mirror, stretch, italicise or add an orange middle dot.
- Web compositing: `mix-blend-mode: screen` removes the black field on the fixed dark masthead/footer surface. The light reference uses `filter: invert(1)` and `mix-blend-mode: multiply`, giving dark lettering without a white rectangle. These are display treatments, not new alpha masters or calibrated pigment colours. Do not place this composited mark over photographs or arbitrary backgrounds; review contrast on the exact surface.
- The logo is not a font for headings or UI. Use it once in the masthead and, if appropriate, in the footer. Never set body text in an approximate military stencil.
- Do not add a panel, border, shadow, glow or background rectangle around the wordmark. The approved geometry stays unchanged. For applications requiring a true transparent file, obtain a reviewed clean-alpha master; do not label this CSS display technique as a transparent PNG.
- For print or fabrication requiring vector outlines, commission or produce a reviewed tracing as a separate deliverable. This kit does not claim to contain an exact vector source.

The small `b` favicon in the starter is only a provisional interface icon. It is not a replacement Blackjack logo and should be reviewed before deployment. The user-approved full wordmark remains the authoritative mark.
