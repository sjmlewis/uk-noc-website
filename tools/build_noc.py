#!/usr/bin/env python3
"""Build the UK National Offset Council (UK-NOC) website.

Writes four pages next to this file:
  index.html, uk-offset-policy.html, offset-green-book.html, papers.html
Edit this file, never the HTML, then run:  python3 build_noc.py
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent
if OUT.name == "tools":
    OUT = OUT.parent  # in the repository, the pages sit in the folder above tools/
DRAFT = False  # True shows the "Draft for review" strip
CONTACT = "stephen.lewis@nationaloffsetcouncil.uk"
REG_FORM = "https://forms.cloud.microsoft/e/Jwnrp5mxYh"  # Microsoft Forms: UK National Offset Council: register your interest
OGL = "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/"
GOV = {
    "policy": "https://www.gov.uk/government/publications/uk-offset-policy/uk-offset-policy",
    "greenbook": "https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026",
    "sdr": "https://www.gov.uk/government/publications/the-strategic-defence-review-2025-making-britain-safer-secure-at-home-strong-abroad",
    "dis": "https://www.gov.uk/government/publications/defence-industrial-strategy-2025-making-defence-an-engine-for-growth",
    "dip": "https://www.gov.uk/government/publications/the-defence-investment-plan",
    "footprint": "https://www.gov.uk/government/publications/uk-defence-footprint-2026-rearm-the-country-reindustrialise-our-communities",
    "lis": "https://www.gov.uk/government/publications/land-industrial-strategy",
    "nsbs": "https://www.gov.uk/government/publications/refresh-to-the-national-shipbuilding-strategy",
    "cas": "https://www.gov.uk/government/publications/combat-air-strategy-an-ambitious-vision-for-the-future",
    "dss": "https://www.gov.uk/government/publications/defence-space-strategy-operationalising-the-space-domain",
}

CSS = r"""/* VOICE formal but relaxed: an independent forum's own site, calm and exact, nothing to sell
   IDEA the table plan, meeting notice and reading pack for a round-table meeting in a London office
   PICTURE a round table seen from above, places set for government, UK companies and overseas suppliers
   COLOUR white paper and ink; a deep sea-teal field top and bottom; seat colours sky blue, coral and saffron
   TYPE Newsreader 600 for headings, Inter for text
   LAYOUT laptop: teal band with the table left, title and buttons right, ruled sections below. Phone: title, table, buttons */
:root{color-scheme:light dark;--bg:light-dark(#ffffff,#0e1315);--ink:light-dark(#151a1d,#e6ecee);--muted:light-dark(#4b575d,#a7b4b9);--rule:light-dark(#d5dde0,#2a3439);--panel:light-dark(#f2f5f6,#141b1e);--field:light-dark(#0b4a55,#0a3840);--line:light-dark(#7d8b91,#5d6c72);--err:light-dark(#b3261e,#ff8a80);--focus:light-dark(#0b4a55,#7fd0dc);--link:light-dark(#0b4a55,#8fd6e1);--gov:#8ab4ff;--uk:#ff8f6b;--ovs:#ffcf5c}
:root[data-theme=light]{color-scheme:light}
:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}
html{scroll-padding-top:12px;scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;overflow-x:clip}
h1,h2,h3{font-family:Newsreader,Georgia,"Times New Roman",serif;font-weight:600;line-height:1.1;letter-spacing:-.01em;margin:0}
h1{font-size:clamp(36px,5vw,54px);line-height:1.05;letter-spacing:-.02em;text-wrap:balance;margin-bottom:16px}
h2{font-size:clamp(26px,3vw,34px);text-wrap:balance;margin-bottom:14px}
h3{font-size:21px;margin-bottom:8px}
p{margin:0 0 1em}
a{color:inherit;text-underline-offset:3px}
main a:not(.btn){color:var(--link)}
dt{font-weight:600}
dd{margin:0}
.wrap{max-width:1180px;margin:0 auto}
.band{padding-block:clamp(36px,5vw,72px);padding-inline:max(5vw,16px)}
.draft{background:light-dark(#fff1c2,#3b300c);color:light-dark(#3d2f00,#ffe7a3);font-size:14px;padding:8px max(5vw,16px)}
.top,.hero,.pagehead,footer{background:var(--field);color:#f1f7f8}
.top{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:4px 28px;padding:12px max(5vw,16px)}
.mark{display:inline-flex;align-items:center;gap:10px;font:600 22px/1 Newsreader,Georgia,serif;text-decoration:none;padding:8px 0}
.mark svg{width:30px;height:30px;flex:none}
nav{display:flex;flex-wrap:wrap;gap:0 22px;font-size:15px}
nav a{display:inline-block;padding:11px 0;text-decoration:none}
nav a:hover,nav a[aria-current=page]{text-decoration:underline}
.hero{padding-top:clamp(12px,3vw,32px)}
.hero .wrap{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);grid-template-areas:"fig txt" "fig act";column-gap:clamp(24px,5vw,72px);align-items:center}
.txt{grid-area:txt;align-self:end}
.act{grid-area:act;align-self:start}
.fig{grid-area:fig}
.lede,.pagehead p{font-size:18px;color:#d6e7ea;max-width:44em}
.when{font-weight:600;margin:4px 0 22px}
.pagehead h1{max-width:18em}
.pagehead .btns{margin-top:22px}
.crumbs{font-size:15px;margin:0 0 12px}
.pagehead .crumbs a{color:#fff}
.btns{display:flex;flex-wrap:wrap;gap:12px}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 22px;border-radius:6px;border:2px solid transparent;font:600 16px/1.2 Inter,system-ui,sans-serif;text-decoration:none;cursor:pointer}
.btn.p{background:var(--ovs);color:#1d1600}
.btn.s{border-color:rgba(255,255,255,.7);color:#fff}
.btn.d{background:var(--field);color:#fff}
.btn:hover{filter:brightness(1.07)}
.top a:focus-visible,.hero a:focus-visible,.pagehead a:focus-visible,.chip:focus-visible,footer a:focus-visible{outline:3px solid #fff;outline-offset:3px}
.plan{max-width:440px;margin:0 auto}
.plan svg{display:block;width:100%;height:auto}
.seat{transition:opacity .25s}
svg[data-hl] .seat{opacity:.2}
svg[data-hl=gov] .gov,svg[data-hl=uk] .uk,svg[data-hl=ovs] .ovs{opacity:1}
.legend{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-top:10px}
.chip{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 14px;border-radius:22px;border:1px solid rgba(255,255,255,.35);background:transparent;color:#fff;font:15px/1.2 Inter,system-ui,sans-serif;cursor:pointer}
.chip[aria-pressed=true]{background:rgba(255,255,255,.14);border-color:#fff}
.dot{display:inline-block;width:13px;height:13px;border-radius:50%;background:var(--c);box-shadow:0 0 0 1.5px rgba(0,0,0,.28);flex:none}
.split{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:clamp(20px,4vw,64px)}
.split p{max-width:40em}
.sec+.sec{border-top:1px solid var(--rule)}
.intro{color:var(--muted);margin-bottom:22px}
.three{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px clamp(20px,3vw,44px);border-top:2px solid var(--ink);padding-top:20px}
.three h3{display:flex;align-items:flex-start;gap:10px}
.three h3 .dot{margin-top:6px}
.three p{margin:0;color:var(--muted)}
.two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px clamp(20px,3vw,44px);border-top:2px solid var(--ink);padding-top:20px}
.two p{margin:0}
.ruled{margin:0;border-top:2px solid var(--ink)}
.ruled div{display:grid;grid-template-columns:minmax(0,230px) minmax(0,1fr);gap:4px 24px;padding:16px 0;border-bottom:1px solid var(--rule)}
.ruled dt{font:600 20px/1.25 Newsreader,Georgia,serif}
.ruled.short div{grid-template-columns:minmax(0,150px) minmax(0,1fr)}
.ruled.small{font-size:15px}
.ruled.small dt{font:600 15px/1.5 Inter,system-ui,sans-serif}
.gb{display:block;font-weight:600;font-size:14px;color:var(--muted)}
.notice{border:1px solid var(--rule);border-radius:10px;overflow:hidden;background:var(--bg)}
.facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin:0;background:var(--panel)}
.facts div{padding:18px 20px;border-left:1px solid var(--rule)}
.facts div:first-child{border-left:0}
.facts dt{font-size:14px;color:var(--muted);margin-bottom:4px}
.rows{margin:0}
.rows div{display:grid;grid-template-columns:minmax(0,210px) minmax(0,1fr);gap:4px 24px;padding:16px 20px;border-top:1px solid var(--rule)}
.list{margin:0;padding-left:1.2em;max-width:44em}
.list li{margin:0 0 10px}
.callout{background:var(--panel);border:1px solid var(--rule);border-radius:10px;padding:18px 20px;font-size:15px;margin-top:28px;max-width:52em}
.callout p:last-child{margin:0}
.group+.group{margin-top:clamp(32px,4vw,52px)}
.papers{border-top:2px solid var(--ink)}
.paper{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 28px;padding:16px 0;border-bottom:1px solid var(--rule)}
.paper h3{font-size:20px;margin:0 0 4px}
.paper p{margin:0;color:var(--muted)}
.paper .by{font-size:14px;color:var(--muted);white-space:nowrap;padding-top:4px}
.paper .also{margin-top:6px;font-size:15px;color:var(--ink)}
.reg,.band.tint{background:var(--panel)}
.reg .split{align-items:start}
form,.regcard{background:var(--bg);border:1px solid var(--rule);border-radius:10px;padding:clamp(18px,3vw,32px);display:grid;gap:18px}
.regcard p,.regcard ul{margin:0}
.regcard ul{padding-left:22px;display:grid;gap:4px}
label{display:block;font-weight:600;font-size:15px;margin-bottom:6px}
.opt{font-weight:400;color:var(--muted)}
input[type=text],input[type=email],select{width:100%;min-height:48px;padding:10px 12px;font:16px/1.3 Inter,system-ui,sans-serif;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:6px}
input:focus-visible,select:focus-visible,form .btn:focus-visible,main a:focus-visible{outline:3px solid var(--focus);outline-offset:2px}
[aria-invalid=true]{border-color:var(--err)}
.err{color:var(--err);font-size:14px;margin-top:4px}
.err:empty{display:none}
.check{display:flex;gap:12px;align-items:flex-start;font-weight:400;margin:0}
.check input{width:22px;height:22px;margin:2px 0 0;flex:none;accent-color:#0b4a55}
.note{font-size:14px;color:var(--muted);margin:0}
form .btn,.regcard .btn{background:var(--field);color:#fff;justify-self:start}
.status{border:1px solid var(--rule);border-radius:8px;padding:12px 14px;background:var(--panel);font-size:15px;margin:0}
.status[hidden]{display:none}
.small{font-size:15px}
footer .wrap{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:16px 48px}
footer p{margin:0 0 6px;color:#d6e7ea}
footer .name{font:600 22px/1.2 Newsreader,Georgia,serif;color:#fff;margin-bottom:8px}
footer a{color:#fff;overflow-wrap:anywhere}
@media(max-width:900px){.three{grid-template-columns:minmax(0,1fr)}.facts{grid-template-columns:repeat(2,minmax(0,1fr))}.facts div:nth-child(3){border-left:0}.facts div:nth-child(n+3){border-top:1px solid var(--rule)}}
@media(max-width:640px){.split,.two,footer .wrap{grid-template-columns:minmax(0,1fr)}}
@media(max-width:600px){.hero .wrap{grid-template-columns:minmax(0,1fr);grid-template-areas:"txt" "fig" "act";row-gap:18px}.plan{max-width:340px}.lede,.pagehead p{font-size:17px}.facts{grid-template-columns:minmax(0,1fr)}.facts div{border-left:0}.facts div+div{border-top:1px solid var(--rule)}.rows div,.ruled div,.ruled.short div,.paper{grid-template-columns:minmax(0,1fr)}.paper .by{white-space:normal;padding-top:0}}
@media(prefers-reduced-motion:reduce){.seat{transition:none}html{scroll-behavior:auto}}"""

HEAD = """<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@</title>
<meta name="description" content="@@DESC@@">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Newsreader:opsz,wght@6..72,600&display=swap">
<style>
@@CSS@@
</style>
</head>
<body id="top">
"""

MARK = ('<svg viewBox="0 0 30 30" aria-hidden="true"><circle cx="15" cy="15" r="8" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<circle cx="15" cy="2.8" r="2.6" fill="var(--gov)"/><circle cx="25.6" cy="21.1" r="2.6" fill="var(--uk)"/>'
        '<circle cx="4.4" cy="21.1" r="2.6" fill="var(--ovs)"/></svg>')

NAV = [("About", "#about"), ("Who it is for", "#who"), ("How it works", "#how"),
       ("Policy papers", "papers.html"), ("Register", "#register")]


def header(current):
    home = current == "index.html"
    links = []
    for label, href in NAV:
        target = href if (home or not href.startswith("#")) else "index.html" + href
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{target}"{cur}>{label}</a>')
    mark_href = "#top" if home else "index.html"
    draft = ('<div class="draft" role="note">Draft for review. The sign-up form is not connected yet.</div>\n'
             if DRAFT else "")
    return (draft + '<header class="top">\n'
            f'<a class="mark" href="{mark_href}" aria-label="UK-NOC home">{MARK}UK-NOC</a>\n'
            f'<nav aria-label="Sections">{"".join(links)}</nav>\n</header>\n')


FOOTER = f"""<footer class="band">
<div class="wrap">
<div><p class="name">UK National Offset Council</p><p>An informal, independent forum. It is not a government body and does not speak for the Ministry of Defence.</p></div>
<div><p>Organised by Capital Offset Services Limited, registered in England and Wales, company number 08803140.</p><p>Contact: <a href="mailto:{CONTACT}">{CONTACT}</a></p></div>
</div>
</footer>
"""

OGL_LINE = f'<p class="small">Contains public sector information licensed under the <a href="{OGL}">Open Government Licence v3.0</a>.</p>'


def page(name, title, desc, body, script=""):
    html = HEAD.replace("@@TITLE@@", title).replace("@@DESC@@", desc).replace("@@CSS@@", CSS)
    html += header(name) + "<main>\n" + body.strip() + "\n</main>\n" + FOOTER
    if script:
        html += "<script>\n" + script.strip() + "\n</script>\n"
    html += "</body>\n</html>\n"
    (OUT / name).write_text(html, encoding="utf-8")
    print(f"wrote {name}: {len(html.splitlines())} lines")


def seat_group(cls, angles):
    uses = "".join(f'<use href="#seat" transform="rotate({a})"/>' for a in angles)
    return f'<g class="seat {cls}" style="color:var(--{cls})">{uses}</g>'


TABLE_SVG = (
    '<svg id="tbl" viewBox="38 38 324 324" role="img" aria-labelledby="tbl-t">\n'
    '<title id="tbl-t">A round table with places set for government, UK companies and overseas suppliers</title>\n'
    '<defs>\n<radialGradient id="top-g" cx="38%" cy="32%" r="80%"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#d6e4e7"/></radialGradient>\n'
    '<g id="seat"><rect x="-19" y="-151" width="38" height="12" rx="5" fill="currentColor" opacity=".6"/>'
    '<rect x="-17" y="-141" width="34" height="27" rx="8" fill="currentColor" stroke="#ffffff" stroke-opacity=".35" stroke-width="1.5"/>'
    '<rect x="-12" y="-104" width="24" height="10" rx="2" fill="#ffffff" stroke="currentColor" stroke-width="2.5"/></g>\n</defs>\n'
    '<g transform="translate(200 200)">\n'
    '<ellipse cx="9" cy="13" rx="108" ry="106" fill="#000000" opacity=".22"/>\n'
    '<circle r="106" fill="url(#top-g)" stroke="#ffffff" stroke-opacity=".85" stroke-width="2"/>\n'
    '<circle r="72" fill="none" stroke="#0b4a55" stroke-opacity=".14" stroke-width="1.5"/>\n'
    + seat_group("gov", [-60, -30, 0, 30]) + "\n"
    + seat_group("uk", [60, 90, 120, 150]) + "\n"
    + seat_group("ovs", [180, 210, 240, 270]) + "\n"
    '<text y="9" text-anchor="middle" font-family="Newsreader,Georgia,serif" font-weight="600" font-size="27" fill="#0b4a55">UK-NOC</text>\n'
    '</g>\n</svg>'
)

# ---------------------------------------------------------------- home page
HOME = f"""
<section class="hero band" aria-labelledby="t">
<div class="wrap">
<div class="txt">
<h1 id="t">UK National Offset Council</h1>
<p class="lede">An informal gathering in central London for people with an interest in UK Offset and the UK Offset Policy: officials from the Ministry of Defence and other government departments, UK companies and overseas suppliers. Each meeting is half a day, free to attend, and brings industry and government together on how Offset works in practice.</p>
<p class="when">Meetings are held quarterly whenever possible.</p>
</div>
<div class="fig">
<div class="plan">
{TABLE_SVG}
</div>
<div class="legend" role="group" aria-label="Highlight a group at the table">
<button type="button" class="chip" data-g="gov" aria-pressed="false"><span class="dot" style="--c:var(--gov)"></span>MOD and government</button>
<button type="button" class="chip" data-g="uk" aria-pressed="false"><span class="dot" style="--c:var(--uk)"></span>UK companies</button>
<button type="button" class="chip" data-g="ovs" aria-pressed="false"><span class="dot" style="--c:var(--ovs)"></span>Overseas suppliers</button>
</div>
</div>
<div class="act btns"><a class="btn p" href="#register">Register your interest</a><a class="btn s" href="#register">Offer a venue</a></div>
</div>
</section>

<section class="band sec" id="about" aria-labelledby="h-about">
<div class="wrap split">
<h2 id="h-about">Why UK-NOC, and why now</h2>
<div>
<p>The Ministry of Defence published the <a href="uk-offset-policy.html">UK Offset Policy</a> in October 2026, applying Offset to large defence purchases from abroad. Overseas suppliers, their UK partners and government all gain from a shared, practical understanding of how commitments are set, met and credited.</p>
<p>Many overseas companies already manage Offset obligations in other countries, and many UK companies already supply them. UK-NOC gives both a regular place to compare experience, raise practical problems early and understand the thinking behind the rules.</p>
<p>It is deliberately informal: half a day of open discussion and networking, not a conference or a sales event.</p>
</div>
</div>
</section>

<section class="band sec" id="who" aria-labelledby="h-who">
<div class="wrap">
<h2 id="h-who">Who it is for</h2>
<p class="intro">Anyone with a working interest in UK Offset is welcome.</p>
<div class="three">
<div><h3><span class="dot" style="--c:var(--gov)"></span>The Ministry of Defence and government</h3><p>Officials responsible for UK Offset policy and defence procurement, invited to set out policy and hear industry's experience.</p></div>
<div><h3><span class="dot" style="--c:var(--uk)"></span>UK companies</h3><p>UK companies of every size, from primes to SMEs, that partner with overseas suppliers or want to.</p></div>
<div><h3><span class="dot" style="--c:var(--ovs)"></span>Overseas suppliers</h3><p>Overseas defence companies with UK Offset commitments, or expecting them on future UK contracts, and their UK subsidiaries.</p></div>
</div>
</div>
</section>

<section class="band sec" aria-labelledby="h-what">
<div class="wrap split">
<div><h2 id="h-what">What the Council discusses</h2><p class="intro">Three themes run through every meeting.</p></div>
<dl class="ruled">
<div><dt>Macroeconomic rules</dt><dd>How commitments are set and valued, what counts towards them, how they are reported, and the economic goals behind them.</dd></div>
<div><dt>National security requirements</dt><dd>Sovereign capability, security of supply, ownership, protection of intellectual property and export control.</dd></div>
<div><dt>Supply contract obligations</dt><dd>How commitments are written into contracts, flow down to UK suppliers, and are delivered and evidenced over the life of a programme.</dd></div>
</dl>
</div>
</section>

<section class="band sec" id="how" aria-labelledby="h-how">
<div class="wrap">
<h2 id="h-how">How it works</h2>
<div class="notice">
<dl class="facts">
<div><dt>When</dt><dd>Quarterly whenever possible, for half a day.</dd></div>
<div><dt>Where</dt><dd>Central London, at the offices of an organisation that lends a meeting room.</dd></div>
<div><dt>Cost</dt><dd>Free. Attendees cover their own travel and expenses.</dd></div>
<div><dt>Format</dt><dd>Informal: open discussion, then time to meet people.</dd></div>
</dl>
<dl class="rows">
<div><dt>Ground rules</dt><dd>Policy and general practice only. Live competitions, individual bids and prices are not discussed.</dd></div>
<div><dt>Chatham House Rule</dt><dd>All meetings are held under the Chatham House Rule. You may use what you hear, but you may not reveal who said it or which organisation they represent. This allows everyone to speak freely.</dd></div>
<div><dt>Organiser</dt><dd>Capital Offset Services Limited organises each meeting. UK-NOC is independent: it is not a government body and does not speak for the Ministry of Defence.</dd></div>
</dl>
</div>
</div>
</section>

<section class="band sec" id="papers" aria-labelledby="h-papers">
<div class="wrap">
<h2 id="h-papers">Policy papers</h2>
<p class="intro">Background reading for meetings, with links to the official documents on GOV.UK.</p>
<div class="three">
<div><h3><a href="uk-offset-policy.html">The UK Offset Policy in brief</a></h3><p>The main points of the policy the Ministry of Defence published on 30 October 2026.</p></div>
<div><h3><a href="offset-green-book.html">Offset and the Green Book</a></h3><p>How HM Treasury's appraisal principles are expected to shape the value of Offset projects.</p></div>
<div><h3><a href="papers.html">All policy papers</a></h3><p>The Strategic Defence Review, the Defence Industrial Strategy, the Defence Investment Plan, and the land, sea, air and space strategies.</p></div>
</div>
</div>
</section>

<section class="band reg" id="register" aria-labelledby="h-reg">
<div class="wrap split">
<div>
<h2 id="h-reg">Register your interest</h2>
<p>Please provide your details. Following due diligence, we will let you know when you have been added to the mailing list.</p>
<p><strong>Offering a venue?</strong> If your organisation could lend a meeting room in central London for half a day, say so on the form.</p>
</div>
<div class="regcard">
<p>The form takes about two minutes. It asks for:</p>
<ul><li>your name and job title</li><li>your organisation and work email</li><li>which group describes you best</li><li>whether your organisation could lend a meeting room</li></ul>
<p class="note">We use your details only to check your registration and to send UK-NOC invitations and updates. We never share them, and every email has an unsubscribe link. <a href="#privacy">How we use your details</a>.</p>
<a class="btn" href="{REG_FORM}" target="_blank" rel="noopener">Register your interest</a>
<p class="note">The form opens in a new tab, on Microsoft Forms.</p>
</div>
</div>
</section>

<section class="band sec" id="privacy" aria-labelledby="h-priv">
<div class="wrap split">
<h2 id="h-priv">How we use your details</h2>
<dl class="ruled small">
<div><dt>Who is responsible</dt><dd>Capital Offset Services Limited, which organises UK-NOC. Registered in England and Wales, company number 08803140.</dd></div>
<div><dt>What we keep</dt><dd>Your name, job title, organisation, work email, the group you belong to, and whether you can offer a venue.</dd></div>
<div><dt>Why</dt><dd>To check your registration before adding you to the mailing list, then to send invitations and updates about UK-NOC meetings and to plan each meeting. We rely on your consent.</dd></div>
<div><dt>Who else sees them</dt><dd>No one. Our email and mailing-list providers store them for us, under contract.</dd></div>
<div><dt>How long</dt><dd>Until you unsubscribe or ask us to delete them.</dd></div>
<div><dt>Your rights</dt><dd>Unsubscribe with the link in any email, or email us to see, correct or delete your details. You can also complain to the Information Commissioner's Office at ico.org.uk.</dd></div>
</dl>
</div>
</section>
"""

HOME_JS = r"""
{
const svg=document.getElementById('tbl');
const chips=[...document.querySelectorAll('.chip')];
let held=null;
const show=g=>{
if(g)svg.setAttribute('data-hl',g);else svg.removeAttribute('data-hl');
for(const c of chips)c.setAttribute('aria-pressed',String(c.dataset.g===held));
};
for(const c of chips){
c.addEventListener('mouseenter',()=>{if(!held)show(c.dataset.g)});
c.addEventListener('mouseleave',()=>{if(!held)show(null)});
c.addEventListener('click',()=>{held=held===c.dataset.g?null:c.dataset.g;show(held||null)});
}
}
"""

# ------------------------------------------------------- policy in brief page
POINTS = [
    ("When", "Published on 30 October 2026. The Ministry of Defence will publish more detail before it applies Offset to defence and security procurements in 2027."),
    ("Who", "Overseas suppliers of defence or national security materiel, systems, services, support, upgrades and life-cycle activity. It may also apply where a supplier is registered in the UK but a significant part of the contract value comes from abroad."),
    ("Threshold", "Contracts worth £50 million or more. Related acquisitions may be added together over up to five years."),
    ("Obligation", "Normally 100% of the contract value, in a separate Offset Agreement. The main contract is not signed until the Offset Agreement is in place. Projects are then agreed with the Offset Authority."),
    ("Timescale", "Normally up to ten years, with milestones of 30% by the end of Year 3, 50% by Year 5 and 100% by Year 10. The Offset Authority may vary these."),
    ("What counts", "Direct Offset, tied to what is being bought, and indirect Offset, which supports the wider UK defence and security sector: contracts with UK businesses, technology and know-how transfer, research and development with UK universities and industry, investment in UK facilities, maintenance and sustainment capability, training and apprenticeships, and help for UK partners to export."),
    ("Approval", "A project is eligible for credit only if the Offset Authority approves it in writing before it starts. Offset activity must be additional to ordinary business."),
    ("Value", 'The Offset Authority values projects with a transparent framework consistent with HM Treasury\'s Green Book principles. <a href="offset-green-book.html">How the Green Book shapes value</a>.'),
    ("Multipliers", "Extra credit for priority activities, such as strengthening regional clusters and supply chains, developing frontier technologies, apprenticeships and critical skills, opportunities for SMEs and mid-tier firms, and sovereign capability. Details are to be published."),
    ("Credits", "Normally awarded in arrears, after delivery and verification. Suppliers report by 31 March each year. Banked credit normally expires after five years."),
    ("Remedies", "Compensation for a missed milestone is normally at least 10% of the value not delivered at that milestone. Penalties are a last resort, for suppliers that do not engage with the policy."),
    ("Transparency", "The Offset Authority will keep a public list of suppliers with Offset Agreements and the value each still has to deliver."),
]

POLICY = f"""
<section class="pagehead band" aria-labelledby="t">
<div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / <a href="papers.html">Policy papers</a></p>
<h1 id="t">The UK Offset Policy in brief</h1>
<p>On 30 October 2026 the Ministry of Defence published the UK Offset Policy. An overseas supplier that wins a large UK defence contract commits to deliver UK value equal to the contract, through projects agreed with a new Offset Authority. These are the main points.</p>
<div class="btns"><a class="btn p" href="{GOV['policy']}">Read the policy on GOV.UK</a><a class="btn s" href="offset-green-book.html">Offset and the Green Book</a></div>
</div>
</section>

<section class="band sec" aria-labelledby="h-main">
<div class="wrap split">
<div><h2 id="h-main">The main points</h2><p class="intro">A summary, not legal advice. The policy on GOV.UK is the authority. Further guidance, including details of the multipliers, is due to be published.</p></div>
<dl class="ruled short">
{"".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in POINTS)}
</dl>
</div>
</section>

<section class="band sec" aria-labelledby="h-means">
<div class="wrap split">
<h2 id="h-means">What it means</h2>
<div class="two">
<div><h3>For overseas suppliers</h3><p>Plan early. You will need UK partners that can make your parts now, and partners that could with your support, with evidence of where and how they work in the UK.</p></div>
<div><h3>For UK companies</h3><p>The policy opens supply chains to UK primes, mid-tier companies, SMEs, universities and research organisations. Overseas suppliers will be looking for capable UK partners.</p></div>
</div>
</div>
</section>

<section class="band tint" aria-labelledby="h-talk">
<div class="wrap split">
<h2 id="h-talk">Talk it through</h2>
<div><p>Discuss the policy with others working on it at UK-NOC meetings.</p><div class="btns"><a class="btn d" href="index.html#register">Register your interest</a></div>{OGL_LINE.replace('<p class="small">', '<p class="small" style="margin-top:22px">')}</div>
</div>
</section>
"""

# ------------------------------------------------------------ Green Book page
TERMS = [
    ("Additionality", "additionality", "Credit only for value that would not exist without the Offset obligation."),
    ("Incrementality", "deadweight", "Business that would have happened anyway, such as existing contracts and routine re-orders, earns nothing."),
    ("Baseline", "business as usual", "The starting position that new business is measured against."),
    ("Causality", "outcomes that happen as a result of the intervention", "The supplier must show that its obligation caused the work."),
    ("UK content", "leakage", "Only value made in the UK counts; imported content is deducted."),
    ("No re-badging", "displacement and substitution", "Moving work between UK firms, or relabelling existing work, adds nothing."),
    ("Sustainability", "durability and discounting", "Capability that lasts for years counts for more than one-off work."),
    ("Credit on delivery", "optimism bias", "Credit is for what is delivered and checked, not what is promised."),
    ("Activity, not payments", "transfers", "A payment on its own is not value; credit follows the UK activity it pays for."),
    ("Capability building", "supply-side benefits", "Credit follows lasting gains in skills, technology and productivity, not turnover."),
    ("Regional and SME multipliers", "place-based and distributional analysis", "Benefits in less productive regions and in smaller firms carry extra weight."),
    ("Strategic fit", "the strategic case", "Projects should serve the published priority areas."),
    ("Verification", "monitoring and evaluation", "Evidence of delivery is checked before credit is granted."),
]

GREEN = f"""
<section class="pagehead band" aria-labelledby="t">
<div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / <a href="papers.html">Policy papers</a></p>
<h1 id="t">Offset and the Green Book</h1>
<p>The UK Offset Policy says the Offset Authority will value Offset with a framework consistent with the principles of HM Treasury's Green Book. Its detailed guidance is still to come. Until then, this page explains what the Green Book is and puts its principles into the terms Offset managers already use.</p>
<div class="btns"><a class="btn p" href="{GOV['greenbook']}">Read the Green Book on GOV.UK</a><a class="btn s" href="uk-offset-policy.html">The UK Offset Policy in brief</a></div>
</div>
</section>

<section class="band sec" aria-labelledby="h-gb">
<div class="wrap split">
<h2 id="h-gb">What the Green Book is</h2>
<div>
<p>The Green Book is HM Treasury's guidance on appraisal: how government assesses the costs, benefits and risks of different ways of meeting its objectives. It is mandatory for central government departments and their arm's-length bodies. HM Treasury published the 2026 edition in February 2026.</p>
<p>It asks one question of every proposal: how much better off is the UK as a whole, compared with what would have happened anyway?</p>
</div>
</div>
</section>

<section class="band sec" aria-labelledby="h-why">
<div class="wrap split">
<h2 id="h-why">Why it matters for Offset</h2>
<div>
<p>Section 3.11.1 of the policy says the Offset Authority will use a transparent value framework consistent with the Green Book's principles. The policy defines UK value added as value genuinely generated in the UK that can be evidenced.</p>
<p>So the face value of a contract, an investment or a licence is the starting point, not the credit. Multipliers then add extra credit for priority places, activities and sectors. Their values are still to be published.</p>
</div>
</div>
</section>

<section class="band sec" aria-labelledby="h-terms">
<div class="wrap split">
<div><h2 id="h-terms">The Green Book in Offset terms</h2><p class="intro">Each line pairs a familiar Offset term with the Green Book idea behind it.</p></div>
<dl class="ruled">
{"".join(f'<div><dt>{t}</dt><dd><span class="gb">Green Book: {g}</span>{d}</dd></div>' for t, g, d in TERMS)}
</dl>
</div>
</section>

<section class="band sec" aria-labelledby="h-practice">
<div class="wrap split">
<h2 id="h-practice">What this means in practice</h2>
<div>
<ul class="list">
<li>Real UK makers with high UK content count for more than distributors and importers.</li>
<li>New capability, such as technology transfer, research and skills, counts for more than more of the same.</li>
<li>New work for established UK companies on what they already make still counts as UK value, even where it attracts no multiplier.</li>
<li>Plan the evidence from day one: the starting position, the UK content, new jobs and who fills them, approvals and exports.</li>
</ul>
<div class="callout"><p><strong>A plain-English reading, not the Offset Authority's guidance.</strong> The Offset Authority will publish its own valuation guidance. The <a href="{GOV['policy']}">policy</a> and the <a href="{GOV['greenbook']}">Green Book</a> on GOV.UK are the authority.</p>{OGL_LINE}</div>
</div>
</div>
</section>
"""

# --------------------------------------------------------------- papers page
PAPERS = [
    ("UK Offset", [
        ("The UK Offset Policy", "policy", "Ministry of Defence, 30 October 2026",
         "The policy itself: when Offset applies, the obligation, the Offset Authority and how credit is given.",
         ("The UK Offset Policy in brief", "uk-offset-policy.html")),
        ("The Green Book (2026)", "greenbook", "HM Treasury, February 2026",
         "Government guidance on appraisal. The Offset Authority's value framework will be consistent with its principles.",
         ("Offset and the Green Book", "offset-green-book.html")),
    ]),
    ("Defence and industry", [
        ("The Strategic Defence Review 2025: Making Britain Safer", "sdr", "Ministry of Defence, 2 June 2025",
         "The government's root-and-branch review of UK Defence.", None),
        ("Defence Industrial Strategy 2025: Making Defence an Engine for Growth", "dis", "Ministry of Defence, 8 September 2025",
         "The defence sector plan of the UK's Modern Industrial Strategy.", None),
        ("The Defence Investment Plan", "dip", "Ministry of Defence, 30 June 2026",
         "The major investment choices for UK Defence, backed by £298 billion over four years.", None),
        ("UK Defence Footprint 2026", "footprint", "Ministry of Defence, 27 October 2026",
         "The Ministry of Defence's report on its spending with UK industry and the jobs it supports.", None),
    ]),
    ("Land, sea, air and space", [
        ("Land Industrial Strategy", "lis", "Ministry of Defence, May 2022",
         "How the Army, the wider Ministry of Defence and industry will work together on land capability.", None),
        ("Refresh to the National Shipbuilding Strategy", "nsbs", "Ministry of Defence, March 2022",
         "Naval and civil shipbuilding, with a 30-year pipeline of more than 150 government vessels.", None),
        ("Combat Air Strategy: An ambitious vision for the future", "cas", "Ministry of Defence, July 2018",
         "The UK's strategic approach to its combat air sector.", None),
        ("Defence Space Strategy: Operationalising the Space Domain", "dss", "Ministry of Defence, February 2022",
         "How Defence will protect and defend UK and allied interests in space.", None),
    ]),
]


def paper_rows(items):
    rows = []
    for title, key, by, text, also in items:
        extra = f'<p class="also">Our summary: <a href="{also[1]}">{also[0]}</a></p>' if also else ""
        rows.append(f'<div class="paper"><div><h3><a href="{GOV[key]}">{title}</a></h3><p>{text}</p>{extra}</div>'
                    f'<p class="by">{by}</p></div>')
    return "".join(rows)


PAPERS_BODY = """
<section class="pagehead band" aria-labelledby="t">
<div class="wrap">
<p class="crumbs"><a href="index.html">Home</a></p>
<h1 id="t">Policy papers</h1>
<p>Official documents for anyone working with UK Offset. Each title links to the document on GOV.UK, which holds the current version.</p>
</div>
</section>
<section class="band" aria-label="Papers">
<div class="wrap">
""" + "".join(
    f'<div class="group"><h2>{name}</h2><div class="papers">{paper_rows(items)}</div></div>'
    for name, items in PAPERS
) + """
<div class="callout"><p>The land, sea, air and space strategies were published before the 2025 Strategic Defence Review and the Defence Industrial Strategy, which now set the overall direction.</p></div>
</div>
</section>
"""

if __name__ == "__main__":
    page("index.html", "UK National Offset Council",
         "An informal forum in central London for government, UK companies and overseas suppliers working with the UK Offset Policy.",
         HOME, HOME_JS)
    (OUT / "CNAME").write_text("nationaloffsetcouncil.uk\n", encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://nationaloffsetcouncil.uk/sitemap.xml\n", encoding="utf-8")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>https://nationaloffsetcouncil.uk/{u}</loc></url>\n" for u in ("", "uk-offset-policy.html", "offset-green-book.html", "papers.html"))
        + "</urlset>\n", encoding="utf-8")
    page("uk-offset-policy.html", "The UK Offset Policy in brief | UK-NOC",
         "The main points of the UK Offset Policy published by the Ministry of Defence on 30 October 2026.", POLICY)
    page("offset-green-book.html", "Offset and the Green Book | UK-NOC",
         "How HM Treasury's Green Book principles are expected to shape the value of UK Offset projects.", GREEN)
    page("papers.html", "Policy papers | UK-NOC",
         "Official documents on UK Offset, defence and industry, and the land, sea, air and space strategies.", PAPERS_BODY)
