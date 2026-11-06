"""Build the 6-month content calendar from data/month-*.json.

Outputs (next to this file):
  calendar.html  - branded, browsable calendar (open in any browser)
  calendar.pdf   - same content as a printable PDF (rendered with Playwright)
  schedule.csv   - one row per post, for importing into a scheduler
"""
import csv, html, json, glob, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = "../carousels/ecommerce-seo-8-reasons/fonts"
IMG = "../carousels/ecommerce-seo-8-reasons/img"


def esc(s):
    return html.escape(str(s or "")).replace("\n", "<br>")


def load():
    months = []
    for f in sorted(glob.glob(os.path.join(HERE, "data", "month-*.json"))):
        with open(f) as fh:
            months.append(json.load(fh))
    return months


FMT_CLASS = {"Image Post": "img", "Carousel": "car", "Reel": "reel"}


def post_card(p):
    v = p.get("visual", {}) or {}
    fmt = p.get("format", "")
    parts = []
    if fmt == "Carousel":
        rows = "".join(
            f'<tr><td class="n">{esc(s.get("n"))}</td><td><b class="bebas">{esc(s.get("heading"))}</b>'
            f'<span class="lbl">{esc(s.get("label"))}</span><p>{esc(s.get("content"))}</p></td></tr>'
            for s in v.get("slides", []))
        parts.append(f'<h5>Slides ({len(v.get("slides", []))})</h5><table class="slides">{rows}</table>')
    elif fmt == "Reel":
        rows = "".join(
            f'<tr><td class="t">{esc(b.get("time"))}</td><td>{esc(b.get("visual"))}</td>'
            f'<td><b>{esc(b.get("on_screen_text"))}</b></td><td>“{esc(b.get("voiceover"))}”</td></tr>'
            for b in v.get("script", []))
        parts.append(
            f'<div class="kv"><span>Cover text</span><b class="bebas">{esc(v.get("cover_text"))}</b>'
            f'<span>Length</span><b>{esc(v.get("duration"))}</b></div>'
            f'<h5>Script</h5><table class="script"><tr><th>Time</th><th>Shot / visual</th><th>On-screen text</th><th>Voiceover</th></tr>{rows}</table>'
            f'<h5>B-roll to film</h5><p>{esc(v.get("broll"))}</p><h5>Music</h5><p>{esc(v.get("music"))}</p>')
    else:
        parts.append(
            f'<div class="kv"><span>Top label</span><b>{esc(v.get("top_label"))}</b>'
            f'<span>Heading</span><b class="bebas">{esc(v.get("heading"))}</b></div>'
            f'<h5>Graphic</h5><p>{esc(v.get("body"))}</p>')
    return f'''
<article class="post {FMT_CLASS.get(fmt, "")}" id="{esc(p.get("id"))}">
 <header>
  <div class="date">{esc(p.get("date"))}</div>
  <div class="badges"><span class="fmt">{esc(fmt)}</span><span class="pill">{esc(p.get("pillar"))}</span><span class="pf">{esc(p.get("platforms"))}</span></div>
 </header>
 <h4>{esc(p.get("title"))}</h4>
 <div class="hook"><span>Hook</span>{esc(p.get("hook"))}</div>
 {''.join(parts)}
 <div class="caps">
  <div><h5>LinkedIn caption</h5><p>{esc(p.get("caption_linkedin"))}</p></div>
  <div><h5>Instagram caption</h5><p>{esc(p.get("caption_instagram"))}</p></div>
 </div>
 <div class="cta"><span>CTA</span>{esc(p.get("cta"))}</div>
 <h5>AI image prompt</h5><p class="prompt">{esc(p.get("ai_image_prompt"))}</p>
 <h5>Design notes</h5><p>{esc(p.get("design_notes"))}</p>
</article>'''


def month_section(i, m):
    overview = "".join(
        f'<tr><td>{esc(p.get("date"))}</td><td><span class="dot {FMT_CLASS.get(p.get("format"), "")}"></span>{esc(p.get("format"))}</td>'
        f'<td><a href="#{esc(p.get("id"))}">{esc(p.get("title"))}</a></td><td>{esc(p.get("pillar"))}</td></tr>'
        for w in m["weeks"] for p in w["posts"])
    weeks = "".join(
        f'<div class="week"><h3><span>Week {w["week"]}</span>{esc(w.get("focus"))}</h3>'
        + "".join(post_card(p) for p in w["posts"]) + "</div>"
        for w in m["weeks"])
    kpis = "".join(f"<li>{esc(k)}</li>" for k in m.get("kpis", []))
    return f'''
<section class="month" id="m{i}">
 <div class="mband"><div class="mnum">MONTH {i:02d}</div><h2>{esc(m["month"])}</h2><div class="mtheme">{esc(m.get("theme"))}</div></div>
 <div class="mgrid">
  <div class="card"><h5>Goal</h5><p>{esc(m.get("goal"))}</p></div>
  <div class="card"><h5>Lead magnet</h5><p>{esc(m.get("lead_magnet"))}</p></div>
  <div class="card"><h5>Monthly targets</h5><ul>{kpis}</ul></div>
 </div>
 <h3 class="sub">At a glance</h3>
 <table class="glance"><tr><th>Date</th><th>Format</th><th>Post</th><th>Pillar</th></tr>{overview}</table>
 {weeks}
 <div class="mgrid two">
  <div class="card"><h5>Instagram Stories plan</h5><p>{esc(m.get("stories"))}</p></div>
  <div class="card"><h5>Daily engagement routine</h5><p>{esc(m.get("engagement_routine"))}</p></div>
 </div>
</section>'''


def page(months):
    nav = "".join(f'<a href="#m{i}"><b>{i:02d}</b>{esc(m["month"])}<span>{esc(m.get("theme"))}</span></a>'
                  for i, m in enumerate(months, 1))
    total = sum(len(w["posts"]) for m in months for w in m["weeks"])
    sections = "".join(month_section(i, m) for i, m in enumerate(months, 1))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Content Calendar — Shehroz Shafique</title>
<style>
@font-face{{font-family:Bebas;src:url({FONTS}/BebasNeue-Regular.ttf)}}
@font-face{{font-family:Inter;font-weight:400;src:url({FONTS}/Inter-Regular.otf)}}
@font-face{{font-family:Inter;font-weight:600;src:url({FONTS}/Inter-SemiBold.otf)}}
@font-face{{font-family:Inter;font-weight:700;src:url({FONTS}/Inter-Bold.otf)}}
@font-face{{font-family:Inter;font-weight:800;src:url({FONTS}/Inter-ExtraBold.otf)}}
:root{{--red:#C40303;--red2:#E41B1B;--deep:#8E0202;--tint:#FDE9E9;--ink:#1F0B0B;--muted:#6E5C5C;--line:rgba(196,3,3,.14)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Inter,sans-serif;color:var(--ink);background:#FFF9F9;background-image:linear-gradient(rgba(196,3,3,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(196,3,3,.055) 1px,transparent 1px);background-size:54px 54px;font-size:15px;line-height:1.55}}
.wrap{{max-width:1120px;margin:0 auto;padding:48px 24px 80px}}
.bebas{{font-family:Bebas;font-weight:400;letter-spacing:.5px;font-size:1.25em}}
a{{color:inherit}}
/* hero */
.hero{{display:flex;gap:32px;align-items:flex-end;justify-content:space-between;border-bottom:2px solid var(--line);padding-bottom:32px}}
.toplabel{{font-weight:600;font-size:13px;letter-spacing:3.5px;color:var(--muted)}}
.hero h1{{font-family:Bebas;font-weight:400;font-size:clamp(52px,9vw,104px);line-height:.9;margin-top:14px}}
.hero h1 span{{color:var(--red)}}
.hero p{{margin-top:18px;font-size:19px;max-width:620px}}
.me{{display:flex;align-items:center;gap:14px;flex:none}}
.me img{{width:74px;height:74px;border-radius:50%;border:3px solid var(--red);padding:3px;background:#fff}}
.me b{{display:block;font-size:18px}} .me span{{color:var(--muted);font-size:14px}}
.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:28px}}
.stat{{background:#fff;border:1.5px solid rgba(31,11,11,.08);border-radius:18px;padding:18px 20px}}
.stat b{{font-family:Bebas;font-weight:400;font-size:46px;line-height:1;color:var(--red)}}
.stat span{{display:block;color:var(--muted);font-size:14px}}
/* generic */
h2.sec{{font-family:Bebas;font-weight:400;font-size:52px;line-height:1;margin:64px 0 18px}}
h2.sec span{{color:var(--red)}}
h3.sub{{font-family:Bebas;font-weight:400;font-size:32px;margin:34px 0 12px}}
h5{{font-size:12px;letter-spacing:2.5px;text-transform:uppercase;color:var(--red);margin:18px 0 6px}}
.card{{background:#fff;border:1.5px solid rgba(31,11,11,.08);border-radius:20px;padding:20px 22px;box-shadow:0 10px 26px rgba(31,11,11,.05)}}
.card h5{{margin-top:0}}
.card ul{{padding-left:18px}}
.grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.grid2{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:16px;overflow:hidden;border:1.5px solid rgba(31,11,11,.08)}}
th{{background:var(--ink);color:#fff;text-align:left;font-size:12px;letter-spacing:1.5px;text-transform:uppercase;padding:10px 12px}}
td{{padding:10px 12px;border-top:1px solid rgba(31,11,11,.07);vertical-align:top}}
.sw{{display:flex;gap:10px;flex-wrap:wrap}}
.sw div{{width:120px;border-radius:14px;overflow:hidden;border:1.5px solid rgba(31,11,11,.08);background:#fff;font-size:12px}}
.sw i{{display:block;height:58px}} .sw p{{padding:8px 10px}}
/* nav */
.nav{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.nav a{{display:block;text-decoration:none;background:#fff;border:1.5px solid rgba(31,11,11,.08);border-radius:18px;padding:16px 18px;font-weight:700}}
.nav a b{{display:block;font-family:Bebas;font-weight:400;font-size:34px;line-height:1;color:var(--red)}}
.nav a span{{display:block;font-weight:400;color:var(--muted);font-size:14px}}
/* month */
.month{{margin-top:80px}}
.mband{{background:linear-gradient(150deg,var(--red),var(--deep));color:#fff;border-radius:24px;padding:30px 32px;box-shadow:0 16px 34px rgba(196,3,3,.25)}}
.mnum{{font-weight:700;letter-spacing:4px;font-size:13px;color:#FFD0D0}}
.mband h2{{font-family:Bebas;font-weight:400;font-size:66px;line-height:1;margin-top:6px}}
.mtheme{{font-size:20px;font-weight:600;color:#FFE1E1}}
.mgrid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:18px}}
.mgrid.two{{grid-template-columns:1fr 1fr;margin-top:26px}}
.glance a{{text-decoration:none;font-weight:600}}
.dot{{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:8px;background:var(--ink)}}
.dot.car{{background:var(--red)}} .dot.reel{{background:var(--deep);outline:2px solid #FFC2C2}}
.week h3{{font-family:Bebas;font-weight:400;font-size:34px;margin:42px 0 12px;display:flex;gap:14px;align-items:baseline}}
.week h3 span{{background:var(--ink);color:#fff;border-radius:30px;padding:2px 14px 0;font-size:24px}}
.post{{background:#fff;border:1.5px solid rgba(31,11,11,.08);border-left:6px solid var(--ink);border-radius:20px;padding:22px 24px;margin-top:16px;box-shadow:0 10px 26px rgba(31,11,11,.05);break-inside:auto}}
.post.car{{border-left-color:var(--red)}} .post.reel{{border-left-color:var(--deep)}}
.post header{{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:center}}
.post .date{{font-weight:700;color:var(--muted);letter-spacing:1px}}
.badges span{{display:inline-block;font-size:12px;font-weight:700;border-radius:20px;padding:3px 10px;margin-left:6px}}
.fmt{{background:var(--ink);color:#fff}} .car .fmt{{background:var(--red)}} .reel .fmt{{background:var(--deep)}}
.pill{{background:var(--tint);color:var(--red)}} .pf{{background:#F3EDED;color:var(--muted)}}
.post h4{{font-size:22px;font-weight:800;margin-top:10px;line-height:1.25}}
.hook,.cta{{margin-top:12px;background:var(--tint);border-radius:12px;padding:10px 14px;font-weight:600}}
.cta{{background:#F7F2F2}}
.hook span,.cta span{{display:inline-block;margin-right:10px;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#fff;background:var(--red);border-radius:6px;padding:2px 8px}}
.cta span{{background:var(--ink)}}
.kv{{display:grid;grid-template-columns:110px 1fr;gap:4px 12px;margin-top:14px}}
.kv span{{color:var(--muted);font-size:13px;padding-top:3px}}
table.slides td.n{{width:36px;font-family:Bebas;font-size:24px;color:var(--red)}}
table.slides .lbl{{float:right;font-size:11px;letter-spacing:2px;color:var(--muted)}}
table.slides p{{margin-top:4px}}
table.script td.t{{white-space:nowrap;font-weight:700;color:var(--red)}}
table.script td{{font-size:14px}}
.caps{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.caps p{{background:#FCFAFA;border:1px solid rgba(31,11,11,.07);border-radius:12px;padding:12px 14px;font-size:14px}}
.prompt{{font-family:ui-monospace,Menlo,monospace;font-size:13px;background:#1F0B0B;color:#FBEAEA;border-radius:12px;padding:12px 14px}}
footer.end{{margin-top:80px;border-top:2px solid var(--line);padding-top:22px;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}}
footer.end .tag{{color:var(--muted);text-align:right}} footer.end .tag b{{color:var(--red)}}
@media (max-width:760px){{.hero{{flex-direction:column;align-items:flex-start}}.stats,.grid3,.grid2,.nav,.mgrid,.mgrid.two,.caps{{grid-template-columns:1fr}}.kv{{grid-template-columns:1fr}}table.script th:nth-child(2),table.script td:nth-child(2){{display:none}}}}
@media print{{body{{background:#fff}}.wrap{{padding:0 8px}}.month{{break-before:page}}.post{{box-shadow:none}}}}
</style></head><body><div class="wrap">

<section class="hero">
 <div>
  <div class="toplabel">LINKEDIN + INSTAGRAM · DEC 2026 – MAY 2027</div>
  <h1>6-MONTH SOCIAL MEDIA<br><span>CONTENT CALENDAR</span></h1>
  <p>A month-by-month plan to grow Shehroz Shafique’s personal brand and bring in SEO clients for Permanent SEO — every post designed in the same master template.</p>
 </div>
 <div class="me"><img src="{IMG}/avatar.png" alt=""><div><b>Shehroz Shafique</b><span>CEO, Permanent SEO</span></div></div>
</section>
<div class="stats">
 <div class="stat"><b>{len(months)}</b><span>months planned</span></div>
 <div class="stat"><b>{total}</b><span>posts, fully written</span></div>
 <div class="stat"><b>3×</b><span>per week on both platforms</span></div>
 <div class="stat"><b>4K</b><span>4:5 posts · 9:16 Reels</span></div>
</div>

<h2 class="sec">THE <span>STRATEGY</span></h2>
<div class="grid3">
 <div class="card"><h5>Who we attract</h5><p>E-commerce store owners (Shopify / WooCommerce), local service businesses and small-to-mid business owners or marketing managers who need SEO that lasts.</p></div>
 <div class="card"><h5>How it turns into clients</h5><p>Teach for free → build trust with process and proof → invite people to comment a keyword for a free resource → DM conversation → free SEO audit call.</p></div>
 <div class="card"><h5>Content pillars</h5><ul><li><b>Educate</b> ~50% — practical SEO lessons</li><li><b>Process</b> ~20% — behind the scenes, how we work</li><li><b>Personal brand</b> ~15% — story, opinions</li><li><b>Offer</b> ~15% — lead magnets, audit call</li></ul></div>
</div>

<h3 class="sub">Weekly rhythm</h3>
<table><tr><th>Day</th><th>Format</th><th>LinkedIn</th><th>Instagram</th><th>Best time to post*</th></tr>
<tr><td><b>Monday</b></td><td><span class="dot"></span>Image post (4:5)</td><td>Single image + long caption</td><td>Feed post</td><td>LinkedIn 8–10 am · Instagram 12–2 pm</td></tr>
<tr><td><b>Wednesday</b></td><td><span class="dot car"></span>Carousel (4:5, 7–10 slides)</td><td>PDF document post</td><td>Carousel post</td><td>LinkedIn 8–10 am · Instagram 6–8 pm</td></tr>
<tr><td><b>Friday</b></td><td><span class="dot reel"></span>Reel (9:16, 30–60 s)</td><td>Native video</td><td>Reel (share to Stories)</td><td>LinkedIn 9–11 am · Instagram 6–9 pm</td></tr>
</table>
<p style="margin-top:8px;color:var(--muted);font-size:13px">*Starting points in your audience’s local time zone. After 4 weeks, check LinkedIn analytics and Instagram Insights and move posts to the hours your followers are most active.</p>

<h2 class="sec">BRAND <span>SYSTEM</span></h2>
<div class="grid2">
 <div class="card"><h5>Colours</h5><div class="sw">
  <div><i style="background:#C40303"></i><p><b>#C40303</b><br>Brand red</p></div>
  <div><i style="background:#FFFFFF;border-bottom:1px solid #eee"></i><p><b>#FFFFFF</b><br>White</p></div>
  <div><i style="background:#FFF9F9;border-bottom:1px solid #eee"></i><p><b>#FFF9F9</b><br>Background</p></div>
  <div><i style="background:#FDE9E9"></i><p><b>#FDE9E9</b><br>Red tint</p></div>
  <div><i style="background:#1F0B0B"></i><p><b>#1F0B0B</b><br>Ink</p></div>
  <div><i style="background:#6E5C5C"></i><p><b>#6E5C5C</b><br>Muted</p></div>
 </div></div>
 <div class="card"><h5>Type &amp; layout</h5><ul>
  <li><b class="bebas">BEBAS NEUE</b> — one-line, full-width headings, same size on every slide (“<span style="color:var(--red)">01 —</span> HEADING”)</li>
  <li><b>Inter</b> — body text (lead 33px, bold key phrase) · <b>JetBrains Mono</b> — URLs and code</li>
  <li>Light #FFF9F9 background with faint red grid · white cards · red outline icons</li>
  <li>Top row: dark “03 / 10” counter + letter-spaced label</li>
  <li>Footer: photo + Shehroz Shafique / CEO, Permanent SEO · tagline on the right</li>
  <li>Grey = before / bad · Red = after / good · final CTA slide may be full red</li>
 </ul></div>
</div>
<div class="grid3" style="margin-top:16px">
 <div class="card"><h5>Image posts</h5><p>1080×1350 (exported 3840×4800). One slide from the master template: counter row, full-width heading, one diagram or checklist, footer.</p></div>
 <div class="card"><h5>Carousels</h5><p>Copy <code>carousels/ecommerce-seo-8-reasons/</code>: cover → teaching slides → solution → full-red CTA. Run <code>node render.js</code> for 4K PNGs; export the PNGs as one PDF for LinkedIn.</p></div>
 <div class="card"><h5>Reels</h5><p>1080×1920. Cover: grid background, Bebas full-width headline with one red word, Shehroz cut-out at the bottom. Captions: Inter Bold white on a red or ink rounded box.</p></div>
</div>

<h2 class="sec">MONTH <span>BY MONTH</span></h2>
<div class="nav">{nav}</div>

{sections}

<footer class="end">
 <div class="me"><img src="{IMG}/avatar.png" alt=""><div><b>Shehroz Shafique</b><span>CEO, Permanent SEO</span></div></div>
 <div class="tag">Helping businesses build their<br><b>brand &amp; permanent growth</b></div>
</footer>
</div></body></html>'''


def main():
    months = load()
    out = os.path.join(HERE, "calendar.html")
    with open(out, "w") as fh:
        fh.write(page(months))
    with open(os.path.join(HERE, "schedule.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "date", "month", "theme", "format", "platforms", "pillar", "title", "hook", "cta"])
        for m in months:
            for wk in m["weeks"]:
                for p in wk["posts"]:
                    w.writerow([p.get("id"), p.get("date"), m["month"], m.get("theme"), p.get("format"),
                                p.get("platforms"), p.get("pillar"), p.get("title"), p.get("hook"), p.get("cta")])
    subprocess.run(["node", "-e", f'''
const {{chromium}}=require("playwright");(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto("file://{out}");await p.evaluate(()=>document.fonts.ready);
await p.pdf({{path:"{os.path.join(HERE, "calendar.pdf")}",format:"A4",printBackground:true,margin:{{top:"14mm",bottom:"14mm",left:"10mm",right:"10mm"}}}});
await b.close()}})();'''], check=True)
    print("built", sum(len(w["posts"]) for m in months for w in m["weeks"]), "posts from", len(months), "months")


if __name__ == "__main__":
    main()
