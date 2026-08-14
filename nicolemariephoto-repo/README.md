# Nicole Marie Photo — website

Static site. No build step, no dependencies. Cloudflare Pages serves the
`site/` folder as-is.

```
site/                  <- deployed. Nothing else is.
  index.html           Home
  portfolio.html       Gallery + category filter
  about.html           Bio
  services.html        Sessions & pricing
  contact.html         Inquiry form
  css/style.css        All styling. Tokens at the top of the file.
  js/main.js           Scroll reveal, filter, form submit
  images/              Optimized photos, 2 sizes x 2 formats each
tools/                 Build scripts. Not published.
photos-original/       Full-res exports. Gitignored — keep locally.
```

---

## 1. Get it live (about 15 minutes)

1. `git init`, commit, push to a GitHub repo.
2. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** →
   **Connect to Git**.
3. Build settings: **framework preset = None**, **build command = empty**.
4. **Output directory: `site`** — this is the important one. Leave it
   blank and Cloudflare publishes the whole repo, scripts included.
5. Deploy. You get a `*.pages.dev` URL immediately.

Every push to `main` redeploys. Pull requests get their own preview URLs.

## 2. Turn the form on

The form posts nowhere useful until you do this.

1. Go to web3forms.com, enter the address that should receive inquiries,
   and they email you an access key.
2. Open `site/js/main.js` and paste it into `ACCESS_KEY` at the top.
3. Push. Test by submitting the form yourself.

There is no account and no server to run. Web3Forms just relays the
submission to that inbox.

## 3. Custom domain

Cloudflare Pages → your project → **Custom domains**. If the domain is
registered at Cloudflare it's two clicks; elsewhere you'll point
nameservers or add a CNAME.

---

## Adding photos

Drop files in `images/`, then replace the placeholder div with a real
image tag:

```html
<!-- before -->
<div class="ph ph--portrait"><b>images/nb-01.jpg</b>4:5</div>

<!-- after -->
<img src="images/nb-01.jpg" alt="Newborn asleep on a bed in morning light" loading="lazy">
```

Before uploading, resize each photo to about **1800px on the long edge**
and export as JPEG at quality 80. Straight-out-of-Lightroom files are
5–10MB each and will make the site unusable on a phone.

`alt` text should describe the picture for someone who can't see it.
It's also what Google reads.

---

## Swapping in your own backend later

`site/js/main.js` has three constants at the top. That's the whole migration:

```js
const FORM_ENDPOINT = "https://nicolemariephoto.com/api/inquiries";
const USE_WEB3FORMS = false;   // stops sending access_key
```

Your endpoint receives `POST` with `Content-Type: application/json` and
this body:

```json
{
  "name": "string, 1-100",
  "email": "string, 1-150, email format",
  "phone": "string, 0-30, optional",
  "session_type": "Engagement | Maternity | Newborn | Family | Graduation or senior portraits | Birthday or event | Something else",
  "session_format": "Mini session (from $75) | Full session (from $150) | empty",
  "preferred_date": "YYYY-MM-DD, optional, may be empty string",
  "message": "string, 1-2000"
}
```

Return **2xx** for success. Anything else shows the error message and
re-enables the submit button.

Notes for the server side:

- `botcheck` (honeypot) is stripped client-side, so don't rely on it —
  a bot posting directly to your endpoint will skip the JS entirely.
  Re-add the check server-side.
- Same for the 3-second minimum submit time. Client-side only.
- CORS: if the API is on the same origin as the pages, nothing to do.
  Different origin means you configure `CORSMiddleware`.

---

## Content

All content is in. No placeholders remain on any page.

One deliberate decision worth recording: session length, image counts
and turnaround times are **intentionally not stated**. They vary too
much to publish, so the site says so plainly and promises the specifics
in writing at booking. If that changes, the copy to edit is the
"Every session is different" panel on services.html.

To add or reorder portfolio photos, edit the PHOTOS list at the top of
`tools/build_gallery.py` and rerun it. Don't hand-edit the gallery
markup.

## Worth doing at some point

- A business email (`nicole@yourdomain.com`) instead of the personal
  iCloud address. Cloudflare Email Routing forwards to her existing
  inbox for free.
- A Google Business Profile. For local family photography this usually
  drives more inquiries than the website does.
- `favicon.ico` and an Open Graph image so links look right when shared
  on Facebook.

## Regenerating images and gallery

Two scripts in `tools/`:

```
python tools/optimize_images.py photos-original site/images --manifest tools/manifest.csv
python tools/build_gallery.py
```

`optimize_images.py` strips EXIF, resizes, and writes JPEG + WebP at two
widths. `build_gallery.py` rebuilds the portfolio markup from the PHOTOS
list at the top of that file — edit the list, rerun, don't hand-edit the
HTML.
