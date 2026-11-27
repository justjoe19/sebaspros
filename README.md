# Sebas Pros Lawn Care

One-page website for a Michiana lawn care and leaf cleanup business. Call or text **574-360-5040** for a free estimate.

Website by [Michiana.dev](https://michiana.dev). I built this website free of charge for a young entrepreneur who is starting a lawn care business.

## How it works

- Hand-written HTML, CSS and a little JavaScript. No framework and no dependencies.
- Hosted on Netlify. Every push to `main` deploys the `public/` folder.
- The estimate form uses Netlify Forms with spam filtering, a honeypot field and reCAPTCHA. The notification email is set in the Netlify dashboard, so it is not stored in this repo.
- AVIF and WebP images in several sizes, structured data, `sitemap.xml`, `robots.txt` and `llms.txt`.

## Editing

The site is in English (`/`) and Spanish (`/es/`). Text, services, prices, towns and FAQs live in `scripts/build.py`, with the Spanish wording in `scripts/es.py`. After changing them:

```sh
python3 scripts/build.py
```

Then commit and push. Preview locally with `python3 -m http.server 4321 -d public`.

Photos and logo belong to Sebas Pros Lawn Care.
