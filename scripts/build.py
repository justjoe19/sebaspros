#!/usr/bin/env python3
"""Generates the English and Spanish pages and the SEO text files from one source of truth.

Edit the English text below and its Spanish match in es.py, then run:  python3 scripts/build.py
The output is committed, so Netlify needs no build step.
"""
import json, html, datetime, pathlib
from es import ES

SITE = "https://sebaspros.com"
NAME = "Sebas Pros Lawn Care"
PHONE = "574-360-5040"
TEL = "+15743605040"
FACEBOOK = "https://www.facebook.com/profile.php?id=61596584897221"
TITLE = "Leaf Cleanup & Lawn Care in South Bend, IN | Sebas Pros"
DESC = ("Professional, affordable leaf cleanups and lawn care in South Bend, Indiana, and surrounding "
        "Michiana towns. Mowing from $40. Free estimates: {phone}.")

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

# Starting prices: (card title, matching service, note, [(yard size, minimum, shown text)])
PRICES = [
    ("Lawn Mowing", "Lawn mowing", "Priced by yard size.", [
        ("Small yards", 40, "$40+"), ("Medium yards", 50, "$50+"), ("Large yards", 65, "$65+")]),
    ("Leaf Blowing", "Leaf blowing and piling to the curb", "Leaves blown to the curb.", [
        ("Small yards", 60, "$60+"), ("Medium yards", 100, "$100+"), ("Large yards", 150, "$150+"),
        ("Very large yards", 200, "$200\u2013$500+")]),
    ("Leaf Removal", "Leaf removal and hauling", "One starting price for any yard.", [
        ("All yard sizes", 80, "$80+")]),
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
     "Yes. Estimates are always free. Call or text {phone}, or send the form on this page."),
    ("What services does Sebas Pros offer?",
     "Leaf cleanups, leaf blowing and piling to the curb, leaf removal and hauling, full-service fall "
     "cleanups, lawn mowing, weed trimming, lawn edging, bush trimming and general yard cleanups."),
    ("How much do lawn mowing and leaf cleanup cost?",
     "Starting prices. {prices} Estimates are free."),
    ("Do you haul leaves away, or only pile them at the curb?",
     "Both. Choose curbside piles for municipal pickup, or have the leaves removed and hauled away."),
    ("What areas do you serve?",
     "South Bend, Indiana, and surrounding areas across Michiana, including Mishawaka, Granger, Osceola, "
     "Elkhart, Goshen and nearby towns in Northern Indiana, plus Niles, Buchanan, Edwardsburg and other "
     "Southwest Michigan communities. If you don't see your town, just ask."),
    ("How do I get a quote?",
     "Tell us your town and what your yard needs using the form, or call or text {phone}."),
]

e = html.escape
# styles.css is copied into the home pages; the small thank-you and 404 pages link to it.
CSS = (pathlib.Path(__file__).resolve().parent.parent / "public" / "styles.css").read_text()
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
LOGO_ALT_WIDTHS = [240, 360, 640, 960]


def hero_set(ext):
    return ", ".join(f"/img/hero-{w}.{ext} {w}w" for w in (640, 1024, 1600, 2048))


def logo_set(ext):
    return ", ".join(f"/img/logo-{w}.{ext} {w}w" for w in LOGO_ALT_WIDTHS)

ICON = {
 "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 3h-2a4 4 0 0 0-4 4v3H6v4h3v7h4v-7h3l1-4h-4V7.5A.5.5 0 0 1 13.5 7H16V3Z"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12a8 8 0 0 1-8 8H4l2-3a8 8 0 1 1 15-5Z"/></svg>',
 "leaf": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19C4 9 10 4 20 4c0 10-5 16-15 15Zm0 0 8-8"/></svg>',
 "lawn": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21h18M6 21c0-5-1-8-3-10 4 1 6 4 6 10M12 21c-1-8 0-13 2-17 1 5 1 11 0 17M17 21c0-5 1-8 4-10-1 3-1 6-1 10"/></svg>',
}

def render(lang):
    """Returns the home page in one language."""
    def t(text):
        out_text = ES[text] if lang == "es" else text
        return out_text.replace("{phone}", PHONE).replace("{name}", NAME)

    def lang_link(code, href, label, name):
        current = ' class="active" aria-current="true"' if code == lang else ""
        return f'<a href="{href}" hreflang="{code}" lang="{code}" aria-label="{label}, {name}"{current}>{label}</a>'

    prefix = "/es/" if lang == "es" else "/"
    url = SITE + prefix
    share = "share-es.jpg" if lang == "es" else "share.jpg"
    title_text, desc_text = t(TITLE), t(DESC)
    subject = ("New estimate request (Spanish) from the Sebas Pros website" if lang == "es"
               else "New estimate request from the Sebas Pros website")
    prices = " ".join(f"{t(c)}: " + ", ".join(f"{t(size).lower()} {shown}" for size, _, shown in rows) + "."
                      for c, _, _, rows in PRICES)
    faq_list = [(t(q), t(a).replace("{prices}", prices)) for q, a in FAQS]

    def offer(name, desc, key):
        data = {"@type": "Offer", "itemOffered": {"@type": "Service", "name": name, "description": desc}}
        for _, service, _, rows in PRICES:
            if service == key:
                data["priceSpecification"] = {"@type": "PriceSpecification", "priceCurrency": "USD",
                                              "minPrice": min(low for _, low, _ in rows)}
        return data

    graph = [
     {"@type": "LocalBusiness", "@id": f"{SITE}/#business", "name": NAME, "alternateName": "Sebas Pros",
      "url": f"{SITE}/", "telephone": TEL, "sameAs": [FACEBOOK], "description": desc_text,
      "image": f"{SITE}/{share}", "logo": f"{SITE}/img/logo-640.png",
      "areaServed": [{"@type": "City", "name": t} for t in ALL_TOWNS] + [{"@type": "Place", "name": "Michiana"}],
      "knowsAbout": ALL_SERVICES,
      "hasOfferCatalog": {"@type": "OfferCatalog", "name": t("Lawn care and leaf services"), "itemListElement": [
          {"@type": "OfferCatalog", "name": t(title), "itemListElement": [
              offer(t(n), t(d), n) for n, d in items]}
          for _, title, _, items in SERVICES]},
      "contactPoint": {"@type": "ContactPoint", "telephone": TEL, "contactType": t("Free estimates")}},
     {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": NAME, "publisher": {"@id": f"{SITE}/#business"}},
     {"@type": "FAQPage", "@id": f"{url}#faq", "inLanguage": lang, "mainEntity": [
         {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_list]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, separators=(",", ":")).replace("<", "\\u003c")

    service_cards = "".join(f'''
          <article class="card reveal" id="{key}-services">
            <div class="card-head"><span class="icon">{ICON[key]}</span><div><h3>{e(t(title))}</h3><p>{e(t(sub))}</p></div></div>
            <ul>{"".join(f"<li><h4>{e(t(n))}</h4><p>{e(t(d))}</p></li>" for n, d in items)}</ul>
            <a class="link" href="#contact">{t("Get a free estimate")} &rarr;</a>
          </article>''' for key, title, sub, items in SERVICES)

    price_cards = "".join(f'''
          <article class="price reveal">
            <h3>{e(t(title))}</h3><p>{e(t(note))}</p>
            <dl>{"".join(f"<div><dt>{e(t(size))}</dt><dd>{e(shown)}</dd></div>" for size, _, shown in rows)}</dl>
          </article>''' for title, _, note, rows in PRICES)

    area_blocks = "".join(f'''
          <div class="area reveal"><h3>{t("Northern Indiana" if s == "Indiana" else "Southwest Michigan")}</h3>
            <ul class="towns">{"".join(f"<li>{e(t)}</li>" for t in ts)}</ul></div>''' for s, ts in AREAS.items())

    faqs = "".join(f'<details class="reveal" name="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq_list)
    checks = "".join(f'<label class="chip"><input type="checkbox" name="services[]" value="{e(n)}"><span>{e(t(n))}</span></label>' for n in ALL_SERVICES + ["Other"])
    town_opts = "".join(f'<option value="{e(t)}">' for t in ALL_TOWNS)
    year = datetime.date.today().year
    AD = "https://michiana.dev/?utm_source=sebaspros&amp;utm_medium=referral&amp;utm_campaign="

    menu_links = f'''<a href="#services">{t('Services')}</a><a href="#pricing">{t('Pricing')}</a><a href="#work">{t('Our Work')}</a><a href="#areas">{t('Areas')}</a><a href="#faq">{t('FAQ')}</a>'''
    page = f'''<!doctype html>
<html lang="{"es" if lang == "es" else "en-US"}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title_text)}</title>
<meta name="description" content="{e(desc_text)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE}/">
<link rel="alternate" hreflang="es" href="{SITE}/es/">
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta name="theme-color" content="#050805">
<meta name="geo.region" content="US-IN">
<meta name="geo.placename" content="South Bend, Indiana">
<meta property="og:type" content="website">
<meta property="og:locale" content="{"es_US" if lang == "es" else "en_US"}">
<meta property="og:locale:alternate" content="{"en_US" if lang == "es" else "es_US"}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(title_text)}">
<meta property="og:description" content="{e(desc_text)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{share}">
<meta property="og:image:secure_url" content="{SITE}/{share}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{t("Sebas Pros Lawn Care logo with phone number {phone}")}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title_text)}">
<meta name="twitter:description" content="{e(desc_text)}">
<meta name="twitter:image" content="{SITE}/{share}">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/fonts/jakarta.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
<script src="/main.js" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">{t('Skip to content')}</a>
<header class="nav">
  <a class="brand" href="#top" aria-label="{t("{name} home")}"><picture><source type="image/avif" srcset="/img/logo-240.avif"><img src="/img/logo-240.webp" alt="" width="240" height="126"></picture></a>
  <nav aria-label="{t("Main")}">{menu_links}</nav>
  <details class="menu"><summary aria-label="{t("Menu")}"><span></span></summary><nav aria-label="{t("Menu")}">{menu_links}</nav></details>
  <div class="lang" role="group" aria-label="{t("Language selector")}">{lang_link("en", "/", "EN", "English")}<span aria-hidden="true">|</span>{lang_link("es", "/es/", "ES", "Español")}</div>
  <a class="btn btn-sm" href="tel:{TEL}" aria-label="{t("Call {phone}")}">{ICON["phone"]}<span>{PHONE}</span></a>
</header>

<main id="main">
<section class="hero" id="top">
  <picture class="hero-bg">
    <source media="(max-width: 759px)" type="image/avif" srcset="/img/hero-m-640.avif 640w, /img/hero-m-900.avif 900w" sizes="100vw">
    <source media="(max-width: 759px)" type="image/webp" srcset="/img/hero-m-640.webp 640w, /img/hero-m-900.webp 900w" sizes="100vw">
    <source type="image/avif" srcset="{hero_set("avif")}" sizes="100vw">
    <source type="image/webp" srcset="{hero_set("webp")}" sizes="100vw">
    <img src="/img/hero-1600.webp" alt="{t("Freshly mowed yard with mature trees in a Michiana neighborhood on a sunny fall day")}" width="2048" height="1536" fetchpriority="high">
  </picture>
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow"><span class="dot"></span>{t('Now booking in South Bend and Michiana')}</p>
      <h1>{t('Leaf cleanup &amp; lawn care in <em>South Bend</em>')}</h1>
      <p class="lead">{t('Professional, affordable leaf cleanups, plus mowing, weed trimming, edging and bush trimming. Serving South Bend, Mishawaka, Elkhart and surrounding Michiana towns.')}</p>
      <div class="actions">
        <a class="btn" href="#contact">{t('Get a free estimate')}</a>
        <a class="btn btn-ghost" href="tel:{TEL}">{ICON["phone"]}{t("Call {phone}")}</a>
      </div>
      <ul class="ticks"><li>{t('Free estimates')}</li><li>{t('Locally owned')}</li><li>{t('Leaf hauling available')}</li></ul>
    </div>
    <picture class="hero-logo"><source type="image/avif" srcset="{logo_set("avif")}" sizes="(min-width: 960px) 480px, 290px"><img src="/img/logo-640.webp" srcset="{logo_set("webp")}" sizes="(min-width: 960px) 480px, 290px" alt="{t("{name} logo")}" width="960" height="504" fetchpriority="high"></picture>
  </div>
</section>

<section class="section" id="services">
  <div class="wrap">
    <p class="kicker">{t('Services')}</p>
    <h2>{t('Everything your yard needs')}</h2>
    <div class="cards">{service_cards}
    </div>
  </div>
</section>

<section class="section alt" id="pricing">
  <div class="wrap">
    <p class="kicker">{t('Pricing')}</p>
    <h2>{t('Starting prices')}</h2>
    <p class="intro">{t('Your final price depends on the size and condition of your yard. Estimates are always free.')}</p>
    <div class="prices">{price_cards}
    </div>
    <p class="price-cta"><a class="btn" href="#contact">{t('Get your free estimate')}</a></p>
  </div>
</section>

<section class="section" id="work">
  <div class="wrap">
    <p class="kicker">{t('Our Work')}</p>
    <h2>{t('From buried in leaves to clean green')}</h2>
    <div class="compare">
      <figure class="reveal">{picture("leaves", t("Lawn covered in yellow fall leaves before cleanup"), P, "(min-width: 760px) 560px, 100vw", 1200, 900)}<figcaption>{t('Before')}</figcaption></figure>
      <figure class="reveal">{picture("clean", t("The same lot with the leaves cleared and the grass cut"), P, "(min-width: 760px) 560px, 100vw", 1200, 900)}<figcaption class="after">{t('After')}</figcaption></figure>
    </div>
    <div class="gallery">
      <figure class="reveal tall">{picture("tree", t("Trimmed lawn beneath a large shade tree"), [480, 800], "(min-width: 760px) 380px, 50vw", 800, 1067)}</figure>
      <figure class="reveal">{picture("front", t("Wide mowed lot facing a neighborhood street"), P, "(min-width: 760px) 380px, 50vw", 1200, 900)}</figure>
      <figure class="reveal">{picture("yard", t("Mowed side yard with a red maple in the distance"), P, "(min-width: 760px) 380px, 50vw", 1200, 900)}</figure>
      <figure class="reveal wide">{picture("covered", t("Large yard blanketed in leaves and ready for a fall cleanup"), P, "(min-width: 760px) 760px, 100vw", 1200, 900)}</figure>
    </div>
  </div>
</section>

<section class="section alt" id="about">
  <div class="wrap about">
    <div class="reveal">
      <p class="kicker">{t('About')}</p>
      <h2>{t('Local, hardworking and easy to reach')}</h2>
      <p>{t('Sebas Pros Lawn Care specializes in professional and affordable leaf cleanups in South Bend, Indiana, and surrounding areas. We help keep your yard looking clean and beautiful by blowing leaves into piles and moving them to the curb. We also offer lawn mowing, weed trimming, edging and bush trimming.')}</p>
      <p>{t('Our goal is to provide reliable service, quality work, and leave every yard looking its best. Sebastian started the business, so when you hire Sebas Pros you are supporting a local entrepreneur.')}</p>
    </div>
    <ol class="steps">
      <li class="reveal"><h3>{t('Reach out')}</h3><p>{t('Call, text or send the form with your town and what you need.')}</p></li>
      <li class="reveal"><h3>{t('Free estimate')}</h3><p>{t('Get a clear price for your yard, with no obligation.')}</p></li>
      <li class="reveal"><h3>{t('Enjoy your yard')}</h3><p>{t('Pick a time and let Sebas Pros handle the work.')}</p></li>
    </ol>
  </div>
</section>

<section class="section" id="areas">
  <div class="wrap">
    <p class="kicker">{t('Service Area')}</p>
    <h2>{t('Serving the Michiana area')}</h2>
    <p class="intro">{t("Based in the South Bend area, {name} provides leaf cleanup and lawn care for homes across Northern Indiana and Southwest Michigan. Don't see your town? Ask anyway.")}</p>
    <div class="areas">{area_blocks}
    </div>
  </div>
</section>

<section class="section alt" id="faq">
  <div class="wrap narrow">
    <p class="kicker">{t('FAQ')}</p>
    <h2>{t('Common questions')}</h2>
    {faqs}
  </div>
</section>

<section class="section" id="contact">
  <div class="wrap contact">
    <div>
      <p class="kicker">{t('Free Estimates')}</p>
      <h2>{t("Let's clean up your yard")}</h2>
      <p class="intro">{t('Send a few details and Sebastian will get back to you. Prefer to talk? Call or text.')}</p>
      <a class="big-phone" href="tel:{TEL}">{PHONE}</a>
      <div class="actions">
        <a class="btn btn-ghost" href="tel:{TEL}">{ICON["phone"]}{t("Call")}</a>
        <a class="btn btn-ghost" href="sms:{TEL}">{ICON["chat"]}{t("Text")}</a>
        <a class="btn btn-ghost" href="{e(FACEBOOK)}" target="_blank" rel="noopener">{ICON["fb"]}Facebook</a>
      </div>
    </div>
    <div class="form-area">
    <form class="form" name="estimate" method="POST" action="{prefix}thanks" data-netlify="true" netlify-honeypot="bot-field" data-netlify-recaptcha="true">
      <input type="hidden" name="form-name" value="estimate">
      <input type="hidden" name="subject" value="{subject}">
      <input type="hidden" name="language" value="{"Spanish" if lang == "es" else "English"}">
      <p class="hp"><label>{t("Leave this empty")} <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <div class="row">
        <label>{t("Name")}<input name="name" autocomplete="name" required maxlength="100"></label>
        <label>{t("Phone")}<input name="phone" type="tel" inputmode="tel" autocomplete="tel" required maxlength="20" placeholder="574-555-0123" pattern="[0-9]{{3}}-[0-9]{{3}}-[0-9]{{4}}" title="{t("Enter a 10-digit phone number, like 574-555-0123")}"></label>
      </div>
      <div class="row">
        <label><span>{t("Email")} <small>{t("(optional)")}</small></span><input name="email" type="email" autocomplete="email" maxlength="150"></label>
        <label>{t("Town")}<input name="town" list="towns" required maxlength="80"><datalist id="towns">{town_opts}</datalist></label>
      </div>
      <fieldset><legend>{t('What do you need?')}</legend><div class="chips">{checks}</div></fieldset>
      <label><span>{t("Anything else?")} <small>{t("(optional)")}</small></span><textarea name="message" rows="4" maxlength="2000"></textarea></label>
      <div class="captcha"><template><div data-netlify-recaptcha="true"></div></template></div>
      <button class="btn" type="submit">{t('Request my free estimate')}</button>
      <p class="status" role="status" aria-live="polite"></p>
    </form>
    <div class="form sent" tabindex="-1" role="status" hidden>
      <span class="sent-mark" aria-hidden="true">&#10003;</span>
      <h3>{t('Request sent!')}</h3>
      <p>{t("Thanks for reaching out. Sebastian will get back to you soon. Need an answer sooner? Call or text")} <a href="tel:{TEL}">{PHONE}</a>.</p>
      <button class="reset" type="button">{t('Send another request')}</button>
    </div>
    </div>
  </div>
</section>

<aside class="promo" aria-label="{t("Advertisement for Michiana.dev")}">
  <div class="wrap">
    <a class="promo-card reveal" href="{AD}promo" target="_blank" rel="noopener">
      <span class="promo-mark" aria-hidden="true">&lt;/&gt;</span>
      <span class="promo-text"><small>{t('Built by our web designer')}</small><strong>{t('Own a local business? Get a website like this one.')}</strong><span>{t('Custom, fast websites for Michiana businesses, hand-built in Mishawaka.')}</span></span>
      <span class="promo-cta">{t("Visit Michiana.dev")} &rarr;</span>
    </a>
  </div>
</aside>
</main>

<footer>
  <div class="wrap foot">
    <picture><source type="image/avif" srcset="/img/logo-360.avif"><img src="/img/logo-360.webp" alt="{NAME}" width="360" height="189" loading="lazy"></picture>
    <p>{t("Leaf cleanup and lawn care across the Michiana area.")}<br>{t("Free estimates:")} <a href="tel:{TEL}">{PHONE}</a><br><a class="social" href="{e(FACEBOOK)}" target="_blank" rel="noopener">{ICON["fb"]}{t("Follow us on Facebook")}</a></p>
  </div>
  <div class="wrap foot-base">
    <span>&copy; <span id="year">{year}</span> {NAME}. {t("All rights reserved.")}</span>
    <span>{t("Website by")} <a class="credit" href="{AD}footer" target="_blank" rel="noopener">Michiana.dev</a></span>
  </div>
</footer>

<div class="dock" aria-label="{t("Quick contact")}">
  <a href="tel:{TEL}">{ICON["phone"]}{t("Call")}</a>
  <a href="sms:{TEL}">{ICON["chat"]}{t("Text")}</a>
  <a class="primary" href="#contact">{t("Free estimate")}</a>
</div>
</body>
</html>
'''
    return page

out = pathlib.Path(__file__).resolve().parent.parent / "public"
(out / "es").mkdir(exist_ok=True)
(out / "index.html").write_text(render("en"))
(out / "es" / "index.html").write_text(render("es"))


def simple(path, lang, title, heading, message, buttons):
    """Thank-you and not-found pages."""
    def t(text):
        out_text = ES[text] if lang == "es" else text
        return out_text.replace("{phone}", PHONE)
    home = "/es/" if lang == "es" else "/"
    links = {
        "home": f'<a class="btn" href="{home}">{t("Back to the home page")}</a>',
        "again": f'<a class="link" href="{home}#contact">{t("Send another request")}</a>',
        "call": f'<a class="btn btn-ghost" href="tel:{TEL}">{t("Call {phone}")}</a>',
    }
    (out / path).write_text(f'''<!doctype html>
<html lang="{"es" if lang == "es" else "en-US"}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>{t(title)} | {NAME}</title><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css"></head>
<body><main class="thanks"><img src="/img/logo-640.webp" alt="{NAME}" width="640" height="336"><h1>{t(heading)}</h1><p>{t(message)}</p>{"".join(links[b] for b in buttons)}</main></body></html>
''')


for lang, folder in (("en", ""), ("es", "es/")):
    simple(f"{folder}thanks.html", lang, "Thank you", "Thank you!",
           "Your request was sent. Sebastian will be in touch soon.", ["home", "again"])
    simple(f"{folder}404.html", lang, "Page not found", "Page not found",
           "That page does not exist. Call or text {phone} for a free estimate.", ["home", "call"])

bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
        "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "CCBot", "Bingbot"]
(out / "robots.txt").write_text("User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\n" for b in bots)
                                + f"Allow: /\n\nSitemap: {SITE}/sitemap.xml\n")
alternates = "".join(f'<xhtml:link rel="alternate" hreflang="{code}" href="{SITE}{path}"/>'
                     for code, path in (("en", "/"), ("es", "/es/"), ("x-default", "/")))
(out / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "".join(f"  <url><loc>{SITE}{path}</loc><lastmod>{datetime.date.today()}</lastmod>{alternates}</url>\n"
              for path in ("/", "/es/"))
    + "</urlset>\n")
llms = [f"# {NAME}", "", f"> {DESC.replace('{phone}', PHONE)}", "", f"- Phone (call or text): {PHONE}", "- Estimates: free",
        f"- Website: {SITE}/", f"- Spanish version: {SITE}/es/", f"- Facebook: {FACEBOOK}", ""]
for _, title, _, items in SERVICES:
    llms += [f"## {title}", ""] + [f"- {n}: {d}" for n, d in items] + [""]
llms += ["## Links", "", f"- [Website]({SITE}/): services, prices and the free estimate form",
         f"- [Sitio en español]({SITE}/es/): the same information in Spanish",
         f"- [Facebook page]({FACEBOOK}): news and updates", ""]
llms += ["## Starting prices", ""]
for title, _, note, rows in PRICES:
    llms.append(f"- {title}: " + ", ".join(f"{size.lower()} {shown}" for size, _, shown in rows))
llms += ["", "## Service area", ""] + [f"- {s}: {', '.join(ts)}" for s, ts in AREAS.items()] + ["", "## FAQ", ""]
for q, a in FAQS:
    prices = " ".join(f"{c}: " + ", ".join(f"{size.lower()} {shown}" for size, _, shown in rows) + "."
                      for c, _, _, rows in PRICES)
    llms += [f"### {q}", "", a.replace("{phone}", PHONE).replace("{prices}", prices), ""]
(out / "llms.txt").write_text("\n".join(llms))
print("built")
