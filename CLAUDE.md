# Shehroz Shafique / Permanent SEO — Social Post Brand Guide

Every social media post in this repo follows this guide. The approved reference
template is `carousels/ecommerce-seo-8-reasons/` (10-slide carousel): reuse its
`common.css`, `fit.js`, `render.js`, `fonts/` and `img/` for new posts.

## Who
- Name: **Shehroz Shafique** — CEO, Permanent SEO
- Tagline: "Helping businesses build their **brand & permanent growth**"
- Photo: `img/avatar.png` (round, footer) and `img/cutout.png` (background removed, for cover/about slides)
- Logo mark: `img/logo-white.png` (white mark; place on a red tile when needed)

## Colours
- Brand red: **#C40303** (main accent, with white)
- Lighter red (gradients): #E41B1B · Deep red: #8E0202
- Red tint (soft backgrounds, chips, icon squares): #FDE9E9
- Ink / dark text and dark panels: #1F0B0B · Muted text: #6E5C5C
- "Bad / before" states use grey (#EEE7E7 bg, #6E5C5C text); "good / after" states use red

## Background
- Light theme: #FFF9F9 with a faint red grid (54px squares, lines rgba(196,3,3,.055))
- Closing CTA slide may be full red (gradient #C40303 → #6E0101) with the same grid in white at 6%

## Fonts
- Headings: **Bebas Neue** (condensed, uppercase)
- Body: **Inter** (400 / 500 / 600 / 700 / 800)
- Code / URLs: **JetBrains Mono Bold**

## Sizes (designed at 1080 × 1350, exported 4K 3840 × 4800)
- Heading: one line, **full width** of the 920px content area, same size on every slide
  (auto-fit by `fit.js`, capped at 110px; short headings get letter-spacing to reach the edge).
  Pattern: red number + dash, then dark text — e.g. "**01 —** THIN COLLECTION PAGES"
- Lead text under heading: Inter 33px, key phrase bold
- Top row: dark pill counter "03 / 10" (Bebas 34px, "/ 10" in light red) left; letter-spaced label right (Inter 600, 20px, muted)
- Page margins: 80px left/right, top row at 64px

## Layout / components
- White cards, 20–24px radius, soft shadow, thin border
- Icons: outline style, red stroke, in red-tint rounded squares
- Footer on every slide (except the cover): thin red divider line, then
  - left: round photo with red ring + **Shehroz Shafique** (bold) / "CEO, Permanent SEO"
  - right: tagline "Helping businesses build their **brand & permanent growth**"
  - **No "PERMANENT SEO" logo + wordmark text in the footer**
- Cover: counter + label top row, full-width heading, red bar, subtitle, name card, "SWIPE TO LEARN →", photo cutout in a red arch

## Output
- Render with `node render.js` (Playwright, deviceScaleFactor 3840/1080) → PNGs in `out/`
- Always 4K, 4:5 (3840 × 4800)
- Keep text clean and simple; fix factual errors from reference posts and mention them
