#!/usr/bin/env python3
"""Generates public/index.html and the SEO text files from one source of truth.

Edit the data below, then run:  python3 scripts/build.py
The output is committed, so Netlify needs no build step.
"""
import json, html, datetime, pathlib

SITE = "https://sebaspros.netlify.app"   # change here if a .com is added
NAME = "Sebas Pros Lawn Care"
PHONE = "574-360-5040"
TEL = "+15743605040"
FACEBOOK = "https://www.facebook.com/profile.php?id=61596584897221"
TITLE = "Lawn Care & Leaf Cleanup in Michiana | Sebas Pros"
DESC = ("Sebas Pros Lawn Care offers leaf cleanup, leaf hauling, mowing, edging, trimming and yard "
        "cleanups in South Bend, Mishawaka, Elkhart and Michiana. Free estimates: 574-360-5040.")

SERVICES = [
    ("leaf", "Leaf Services", "Fall is busy. Hand off the raking and get your yard back.", [
        ("Leaf cleanups", "Leaves cleared from lawns, beds and walkways."),
        ("Leaf blowing and piling to the curb", "Blown into neat piles at the curb for pickup."),
        ("Leaf removal and hauling", "Collected and hauled away for you."),
        ("Full-service fall cleanups", "The whole yard readied for winter."),
    ]),
    ("lawn", "Lawn Care Services", "Keep the place looking sharp through the growing season.", [
        ("Lawn mowing", "A clean, even cut."),
        ("Weed trimming / weed wacking", "Tidy fence lines, posts, trees and foundations."),
        ("Lawn edging", "Crisp borders along drives and sidewalks."),
        ("Bush trimming", "Shrubs shaped and cut back."),
        ("General yard cleanups", "Sticks, debris and overgrowth cleared out."),
    ]),
]

AREAS = {
    "Indiana": ["South Bend", "Mishawaka", "Granger", "Osceola", "Notre Dame", "Roseland", "Elkhart",
                "Dunlap", "Goshen", "Bristol", "Middlebury", "Wakarusa", "Nappanee", "Bremen",
                "Lakeville", "North Liberty", "Walkerton", "New Carlisle", "Plymouth", "La Porte",
                "Michigan City"],
    "Michigan": ["Niles", "Buchanan", "Edwardsburg", "Cassopolis", "Dowagiac", "Berrien Springs",
                 "Three Oaks", "New Buffalo", "St. Joseph", "Benton Harbor"],
}

FAQS = [
    ("Are estimates free?",
     f"Yes. Estimates are always free. Call or text {PHONE}, or send the form on this page."),
    ("What services does Sebas Pros offer?",
     "Leaf cleanups, leaf blowing and piling to the curb, leaf removal and hauling, full-service fall "
     "cleanups, lawn mowing, weed trimming, lawn edging, bush trimming and general yard cleanups."),
    ("Do you haul leaves away, or only pile them at the curb?",
     "Both. Choose curbside piles for municipal pickup, or have the leaves removed and hauled away."),
    ("What areas do you serve?",
     "The Michiana area, including South Bend, Mishawaka, Granger, Osceola, Elkhart, Goshen and nearby "
     "towns in Northern Indiana, plus Niles, Buchanan, Edwardsburg and other Southwest Michigan "
     "communities. If you don't see your town, just ask."),
    ("How do I get a quote?",
     f"Tell us your town and what your yard needs using the form, or call or text {PHONE}."),
]

e = html.escape
ALL_TOWNS = [f"{t}, {'IN' if s == 'Indiana' else 'MI'}" for s, ts in AREAS.items() for t in ts]
ALL_SERVICES = [n for _, _, _, items in SERVICES for n, _ in items]

def picture(name, alt, widths, sizes, w, h, cls="", eager=False):
    ss = lambda x: ", ".join(f"/img/{name}-{i}.{x} {i}w" for i in widths)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>'
            f'<source type="image/avif" srcset="{ss("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{ss("webp")}" sizes="{sizes}">'
            f'<img src="/img/{name}-{widths[-1]}.webp" alt="{e(alt)}" width="{w}" height="{h}" {load}></picture>')

P = [480, 800, 1200]
ICON = {
 "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 3h-2a4 4 0 0 0-4 4v3H6v4h3v7h4v-7h3l1-4h-4V7.5A.5.5 0 0 1 13.5 7H16V3Z"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12a8 8 0 0 1-8 8H4l2-3a8 8 0 1 1 15-5Z"/></svg>',
 "leaf": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19C4 9 10 4 20 4c0 10-5 16-15 15Zm0 0 8-8"/></svg>',
 "lawn": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21h18M6 21c0-5-1-8-3-10 4 1 6 4 6 10M12 21c-1-8 0-13 2-17 1 5 1 11 0 17M17 21c0-5 1-8 4-10-1 3-1 6-1 10"/></svg>',
}

graph = [
 {"@type": "LocalBusiness", "@id": f"{SITE}/#business", "name": NAME, "alternateName": "Sebas Pros",
  "url": f"{SITE}/", "telephone": TEL, "sameAs": [FACEBOOK], "description": DESC,
  "image": f"{SITE}/og-image.jpg", "logo": f"{SITE}/img/logo-640.png",
  "areaServed": [{"@type": "City", "name": t} for t in ALL_TOWNS] + [{"@type": "Place", "name": "Michiana"}],
  "knowsAbout": ALL_SERVICES,
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Lawn care and leaf services", "itemListElement": [
      {"@type": "OfferCatalog", "name": title, "itemListElement": [
          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d}} for n, d in items]}
      for _, title, _, items in SERVICES]},
  "contactPoint": {"@type": "ContactPoint", "telephone": TEL, "contactType": "Free estimates"}},
 {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": NAME, "publisher": {"@id": f"{SITE}/#business"}},
 {"@type": "FAQPage", "@id": f"{SITE}/#faq", "mainEntity": [
     {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]},
]
ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, separators=(",", ":")).replace("<", "\\u003c")

service_cards = "".join(f'''
      <article class="card reveal" id="{key}-services">
        <div class="card-head"><span class="icon">{ICON[key]}</span><div><h3>{e(title)}</h3><p>{e(sub)}</p></div></div>
        <ul>{"".join(f"<li><h4>{e(n)}</h4><p>{e(d)}</p></li>" for n, d in items)}</ul>
        <a class="link" href="#contact">Get a free estimate &rarr;</a>
      </article>''' for key, title, sub, items in SERVICES)

area_blocks = "".join(f'''
      <div class="area reveal"><h3>{"Northern Indiana" if s == "Indiana" else "Southwest Michigan"}</h3>
        <ul class="towns">{"".join(f"<li>{e(t)}</li>" for t in ts)}</ul></div>''' for s, ts in AREAS.items())

faqs = "".join(f'<details class="reveal" name="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQS)
checks = "".join(f'<label class="chip"><input type="checkbox" name="services[]" value="{e(n)}"><span>{e(n)}</span></label>' for n in ALL_SERVICES + ["Other"])
town_opts = "".join(f'<option value="{e(t)}">' for t in ALL_TOWNS)
year = datetime.date.today().year
AD = "https://michiana.dev/?utm_source=sebaspros&amp;utm_medium=referral&amp;utm_campaign="

page = f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESC)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{SITE}/">
<meta name="theme-color" content="#050805">
<meta name="geo.region" content="US-IN">
<meta name="geo.placename" content="Michiana">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(TITLE)}">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Sebas Pros Lawn Care logo over a freshly mowed Michiana yard">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/fonts/jakarta.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
<script src="/main.js" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav">
  <a class="brand" href="#top" aria-label="{NAME} home"><img src="/img/logo-360.webp" alt="" width="360" height="189"></a>
  <nav aria-label="Main"><a href="#services">Services</a><a href="#work">Our Work</a><a href="#areas">Areas</a><a href="#faq">FAQ</a></nav>
  <a class="btn btn-sm" href="tel:{TEL}">{ICON["phone"]}<span>{PHONE}</span></a>
</header>

<main id="main">
<section class="hero" id="top">
  {picture("hero", "Freshly mowed yard with mature trees in a Michiana neighborhood on a sunny fall day", [640, 1024, 1600, 2048], "100vw", 2048, 1536, "hero-bg", True)}
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow"><span class="dot"></span>Now booking fall leaf cleanups</p>
      <h1>Lawn care &amp; leaf cleanup in <em>Michiana</em></h1>
      <p class="lead">Mowing, edging, trimming and full fall cleanups from a local business that shows up ready to work. Serving South Bend, Mishawaka, Elkhart and the towns around them.</p>
      <div class="actions">
        <a class="btn" href="#contact">Get a free estimate</a>
        <a class="btn btn-ghost" href="tel:{TEL}">{ICON["phone"]}Call {PHONE}</a>
      </div>
      <ul class="ticks"><li>Free estimates</li><li>Locally owned</li><li>Leaf hauling available</li></ul>
    </div>
    <img class="hero-logo" src="/img/logo-960.webp" srcset="/img/logo-640.webp 640w, /img/logo-960.webp 960w" sizes="(min-width: 960px) 480px, 80vw" alt="{NAME} logo" width="960" height="504">
  </div>
</section>

<section class="section" id="services">
  <div class="wrap">
    <p class="kicker">Services</p>
    <h2>Everything your yard needs</h2>
    <div class="cards">{service_cards}
    </div>
  </div>
</section>

<section class="section alt" id="work">
  <div class="wrap">
    <p class="kicker">Our Work</p>
    <h2>From buried in leaves to clean green</h2>
    <div class="compare">
      <figure class="reveal">{picture("leaves", "Lawn covered in yellow fall leaves before cleanup", P, "(min-width: 760px) 560px, 100vw", 1200, 900)}<figcaption>Before</figcaption></figure>
      <figure class="reveal">{picture("clean", "The same lot with the leaves cleared and the grass cut", P, "(min-width: 760px) 560px, 100vw", 1200, 900)}<figcaption class="after">After</figcaption></figure>
    </div>
    <div class="gallery">
      <figure class="reveal tall">{picture("tree", "Trimmed lawn beneath a large shade tree", [480, 800], "(min-width: 760px) 380px, 50vw", 800, 1067)}</figure>
      <figure class="reveal">{picture("front", "Wide mowed lot facing a neighborhood street", P, "(min-width: 760px) 380px, 50vw", 1200, 900)}</figure>
      <figure class="reveal">{picture("yard", "Mowed side yard with a red maple in the distance", P, "(min-width: 760px) 380px, 50vw", 1200, 900)}</figure>
      <figure class="reveal wide">{picture("covered", "Large yard blanketed in leaves and ready for a fall cleanup", P, "(min-width: 760px) 760px, 100vw", 1200, 900)}</figure>
    </div>
  </div>
</section>

<section class="section" id="about">
  <div class="wrap about">
    <div class="reveal">
      <p class="kicker">About</p>
      <h2>Local, hardworking and easy to reach</h2>
      <p>Sebas Pros Lawn Care is a Michiana business started by Sebastian. When you hire Sebas Pros, you are supporting a local entrepreneur who is building the company one yard at a time.</p>
    </div>
    <ol class="steps">
      <li class="reveal"><h3>Reach out</h3><p>Call, text or send the form with your town and what you need.</p></li>
      <li class="reveal"><h3>Free estimate</h3><p>Get a clear price for your yard, with no obligation.</p></li>
      <li class="reveal"><h3>Enjoy your yard</h3><p>Pick a time and let Sebas Pros handle the work.</p></li>
    </ol>
  </div>
</section>

<section class="section alt" id="areas">
  <div class="wrap">
    <p class="kicker">Service Area</p>
    <h2>Serving the Michiana area</h2>
    <p class="intro">{NAME} provides leaf cleanup and lawn care for homes across Northern Indiana and Southwest Michigan. Don't see your town? Ask anyway.</p>
    <div class="areas">{area_blocks}
    </div>
  </div>
</section>

<section class="section" id="faq">
  <div class="wrap narrow">
    <p class="kicker">FAQ</p>
    <h2>Common questions</h2>
    {faqs}
  </div>
</section>

<section class="section alt" id="contact">
  <div class="wrap contact">
    <div>
      <p class="kicker">Free Estimates</p>
      <h2>Let's clean up your yard</h2>
      <p class="intro">Send a few details and Sebastian will get back to you. Prefer to talk? Call or text.</p>
      <a class="big-phone" href="tel:{TEL}">{PHONE}</a>
      <div class="actions">
        <a class="btn btn-ghost" href="tel:{TEL}">{ICON["phone"]}Call</a>
        <a class="btn btn-ghost" href="sms:{TEL}">{ICON["chat"]}Text</a>
        <a class="btn btn-ghost" href="{e(FACEBOOK)}" target="_blank" rel="noopener">{ICON["fb"]}Facebook</a>
      </div>
    </div>
    <form class="form" name="estimate" method="POST" action="/thanks" data-netlify="true" netlify-honeypot="bot-field" data-netlify-recaptcha="true">
      <input type="hidden" name="form-name" value="estimate">
      <input type="hidden" name="subject" value="New estimate request from the Sebas Pros website">
      <p class="hp"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <div class="row">
        <label>Name<input name="name" autocomplete="name" required maxlength="100"></label>
        <label>Phone<input name="phone" type="tel" autocomplete="tel" required maxlength="30"></label>
      </div>
      <div class="row">
        <label><span>Email <small>(optional)</small></span><input name="email" type="email" autocomplete="email" maxlength="150"></label>
        <label>Town<input name="town" list="towns" required maxlength="80"><datalist id="towns">{town_opts}</datalist></label>
      </div>
      <fieldset><legend>What do you need?</legend><div class="chips">{checks}</div></fieldset>
      <label><span>Anything else? <small>(optional)</small></span><textarea name="message" rows="4" maxlength="2000"></textarea></label>
      <div class="captcha" data-netlify-recaptcha="true"></div>
      <button class="btn" type="submit">Request my free estimate</button>
      <p class="status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>

<aside class="promo" aria-label="Advertisement for Michiana.dev">
  <div class="wrap">
    <a class="promo-card reveal" href="{AD}promo" target="_blank" rel="noopener">
      <span class="promo-mark" aria-hidden="true">&lt;/&gt;</span>
      <span class="promo-text"><small>Built by our web designer</small><strong>Own a local business? Get a website like this one.</strong><span>Custom, fast websites for Michiana businesses, hand-built in Mishawaka.</span></span>
      <span class="promo-cta">Visit Michiana.dev &rarr;</span>
    </a>
  </div>
</aside>
</main>

<footer>
  <div class="wrap foot">
    <img src="/img/logo-360.webp" alt="{NAME}" width="360" height="189" loading="lazy">
    <p>Leaf cleanup and lawn care across the Michiana area.<br>Free estimates: <a href="tel:{TEL}">{PHONE}</a><br><a class="social" href="{e(FACEBOOK)}" target="_blank" rel="noopener">{ICON["fb"]}Follow us on Facebook</a></p>
  </div>
  <div class="wrap foot-base">
    <span>&copy; <span id="year">{year}</span> {NAME}. All rights reserved.</span>
    <span>Website by <a class="credit" href="{AD}footer" target="_blank" rel="noopener">Michiana.dev</a></span>
  </div>
</footer>

<div class="dock" aria-label="Quick contact">
  <a href="tel:{TEL}">{ICON["phone"]}Call</a>
  <a href="sms:{TEL}">{ICON["chat"]}Text</a>
  <a class="primary" href="#contact">Free estimate</a>
</div>
</body>
</html>
'''

out = pathlib.Path(__file__).resolve().parent.parent / "public"
(out / "index.html").write_text(page)

bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
        "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "CCBot", "Bingbot"]
(out / "robots.txt").write_text("User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\n" for b in bots)
                                + f"Allow: /\n\nSitemap: {SITE}/sitemap.xml\n")
(out / "sitemap.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{SITE}/</loc><lastmod>{datetime.date.today()}</lastmod></url>
</urlset>
''')
llms = [f"# {NAME}", "", f"> {DESC}", "", f"- Phone (call or text): {PHONE}", "- Estimates: free",
        f"- Website: {SITE}/", f"- Facebook: {FACEBOOK}", ""]
for _, title, _, items in SERVICES:
    llms += [f"## {title}", ""] + [f"- {n}: {d}" for n, d in items] + [""]
llms += ["## Service area", ""] + [f"- {s}: {', '.join(ts)}" for s, ts in AREAS.items()] + ["", "## FAQ", ""]
for q, a in FAQS:
    llms += [f"### {q}", "", a, ""]
(out / "llms.txt").write_text("\n".join(llms))
print("built")
