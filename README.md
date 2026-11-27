# Sebas Pros Lawn Care

One-page website in English and Spanish for a lawn care and leaf cleanup business in South Bend, Indiana, serving the Michiana area.

**Live site:** [sebaspros.com](https://sebaspros.com) · [En español](https://sebaspros.com/es/)

Call or text **574-360-5040** for a free estimate. Follow [Sebas Pros on Facebook](https://www.facebook.com/profile.php?id=61596584897221).

Website by [Michiana.dev](https://michiana.dev). I built this website free of charge for a young entrepreneur who is starting a lawn care business.

## Features

- Services, starting prices, before-and-after photos, service area, FAQ and an estimate form
- English (`/`) and Spanish (`/es/`) pages with an EN | ES switcher that keeps the visitor in the same section
- On phones, a section menu plus call, text and estimate buttons pinned to the bottom of the screen
- Phone numbers formatted as `574-555-0123` while typing, and a confirmation panel with a "Send another request" link
- Spam protection from Netlify's filtering, a honeypot field and reCAPTCHA
- Custom "page not found" and thank-you pages in both languages
- Logo share image for Facebook and text message previews, one per language

### Search and AI visibility

- Page titles, descriptions, canonical links and `hreflang` tags
- `LocalBusiness`, `WebSite` and `FAQPage` structured data, including services and starting prices
- Town-by-town service area across Northern Indiana and Southwest Michigan
- `sitemap.xml`, a `robots.txt` that welcomes search and AI crawlers, and `llms.txt` (English)
- Search Console ownership is verified with a `TXT` record in the domain settings; leave that record in place

## Tech

- Hand-written HTML, CSS and a little JavaScript, with no framework or npm packages
- A small Python script generates the pages; the output is committed, so Netlify runs no build step
- Responsive AVIF and WebP images, and a self-hosted Plus Jakarta Sans font (license in `public/fonts/`)
- Styles are inlined into the home pages, and reCAPTCHA loads only when a visitor nears the form

## Project layout

| Path | What it is | Edit by hand? |
| --- | --- | --- |
| `scripts/build.py` | Page layout and English content | Yes |
| `scripts/es.py` | Spanish wording, keyed by the English text | Yes |
| `public/styles.css`, `public/main.js` | Styling (rebuild after editing) and behavior | Yes |
| `public/index.html`, `public/es/` | Generated pages | No |
| `public/404.html`, `public/thanks.html` | Generated pages | No |
| `public/llms.txt`, `public/robots.txt`, `public/sitemap.xml` | Generated files | No |
| `public/img/`, `public/share*.jpg`, icons | Optimized images | Replace as needed |
| `netlify.toml` | Publish folder, redirects, security headers, caching, Spanish 404 | Yes |

The original, full-size photos and logo, and any PDFs saved in this folder, are kept out of the repository (see `.gitignore`).

## Editing

1. Change the content in `scripts/build.py`. Services, prices, towns and FAQs are lists near the top.
2. Add or update the matching Spanish text in `scripts/es.py`. The build stops with a `KeyError` if a translation is missing.
3. Rebuild (Python 3, no extra packages):

```sh
python3 scripts/build.py
```

4. Preview at <http://localhost:4321>:

```sh
python3 -m http.server 4321 -d public
```

5. Commit and push to `main`.

The local preview cannot receive form submissions, and the reCAPTCHA box only appears on Netlify.

### How the reCAPTCHA delay works

Netlify writes Google's script and widget into the `data-netlify-recaptcha` placeholder when it deploys. The placeholder sits inside a `<template>`, so nothing loads until `public/main.js` copies it into the form as the visitor gets close. After changing the form, check the live site: the "I'm not a robot" box should appear, and a test request should arrive.

## Checking quality

Run [Lighthouse](https://developer.chrome.com/docs/lighthouse) against the live site, for phones and for desktops:

```sh
npx lighthouse https://sebaspros.com --view
```

```sh
npx lighthouse https://sebaspros.com --preset=desktop --view
```

### Details that live in more than one place

- **Prices:** the `PRICES` list, plus "Mowing from $40" in the page description (`DESC` in `build.py` and its Spanish match in `es.py`).
- **Phone number:** `PHONE` and `TEL` in `build.py`, the error messages in `public/main.js`, and the artwork in both share images.
- **Top photo:** wide screens use `hero-*` images; phones use the portrait crops, `hero-m-*`. Replace both sets together.
- **Tagline and town:** the share images have their text drawn into them, so new wording needs new images. Give a replacement a new file name so Facebook and phones fetch it again.

## Hosting

- **Netlify:** every push to `main` publishes the `public/` folder.
- **Domain:** `sebaspros.com` is registered at Namecheap, which also hosts its DNS. An `ALIAS` record on `@` points to `apex-loadbalancer.netlify.com` and a `CNAME` on `www` points to `sebaspros.netlify.app`. Netlify manages the HTTPS certificate and redirects `www` to the main domain. `netlify.toml` also redirects `sebaspros.netlify.app` there.
- **Estimate form:** submissions appear under Forms in the Netlify dashboard. The notification email address is set there, so it is not stored in this repository. Each submission records the page language, and Spanish requests say so in the subject line.

Photos and logo belong to Sebas Pros Lawn Care.
