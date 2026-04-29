# CLAUDE.md

Personal site for Khandaker Md. Al-Amin. Static HTML + CSS + a tiny Express server for local preview. Deployed to GitHub Pages on a custom domain (`CNAME`).

## Commands

- `npm install` - install dependencies
- `npm start` - run local preview at `http://localhost:3000`

## Layout

- `index.html` - home page (about, experience, research interests, education, talks)
- `projects/index.html` - projects listing
- `publications/index.html` - publications listing
- `blog/index.html` - blog index
- `blog/*.html` - individual blog posts (Markdown-like HTML with MathJax and Prism)
- `styles.css` - global design tokens and components
- `blog/blog-styles.css` - blog-specific overrides
- `script.js` - theme toggle, mobile nav, citation modal, smooth scroll
- `photography/index.html` - photography gallery
- `404.html` - not-found page
- `uploads/resume.pdf` - current CV (replace this file to publish a new CV)
- `.github/workflows/deploy.yml` - static GitHub Pages deploy (no Jekyll, no Hugo, no build step)
- `.nojekyll` - disables Jekyll processing on Pages

The repo was cleaned of an earlier Hugo/Wowchemy export (Apr 2026). If you see references to `post/`, `publication/`, `project/`, `tag/`, `category/`, `publication-type/`, `slides/`, `event/`, `talk/`, `css/wowchemy*`, `js/wowchemy*`, `webfonts/`, `media/icon_*`, `authors/`, or `en/` in new commits, those paths no longer exist — use the primary pages above instead.

## Design tokens

Defined in `:root` in `styles.css`.

- Palette: soothing warm-paper light (`#FAF7F2` bg, `#1F2933` text) and soft near-black dark (`#0F1720` bg, `#E6EDF3` text), low-contrast by design to reduce eye strain.
- Accents: teal `#2A8C8C` (primary) and warm amber `#C9883A` (accent). Dark-mode variants are brighter.
- Fonts:
  - Headings: Source Serif 4 (book-quality serif)
  - Body: Inter (17px base, 1.65 line-height, max 65-72ch measure)
  - Code: JetBrains Mono
- Spacing: 4/8/12/20/28/40/48 scale via `--spacing-*` tokens
- Radius: `--radius-sm/md/lg/full`

Never use purple or indigo hues. Keep contrast WCAG AA in both modes.

## Editing content (no CMS, direct in GitHub)

1. Open the repo on `github.com/eNipu/eNipu.github.io`
2. Navigate to the file you want to edit (`index.html`, `projects/index.html`, etc.)
3. Click the pencil icon, edit, commit directly to `master` (or open a PR)
4. GitHub Pages rebuilds automatically

To add a new blog post:
1. Copy an existing file in `blog/` (e.g. `blog/understanding-homomorphic-encryption.html`)
2. Rename to `blog/your-slug.html`
3. Update `<title>`, headline, date, tags, and body
4. Add a card entry in `blog/index.html`

To update the CV: replace `uploads/resume.pdf`.

### Adding a new photograph

The photography gallery is backed by the Supabase `photos` table and a public Storage bucket. The gallery on `/photography/` fetches from Supabase at page load, so nothing in this repo needs to change.

Two-minute workflow from the Supabase dashboard:

1. Open the project at `supabase.com` and go to **Storage** &rarr; bucket `photos` (create it as a public bucket if it does not exist yet).
2. Upload the full image into `full/your-slug.jpg` and a ~720px thumbnail into `thumb/your-slug.jpg`.
3. Copy the public URLs for both.
4. Go to **Table Editor** &rarr; `photos` &rarr; **Insert row** and fill in: `title`, `location`, `country`, `category` (lowercased slug like `japan`, `france`, `bangladesh`, `germany`), `taken_on`, `caption` (optional), `image_url`, `thumb_url`, `camera` (optional), `sort_order` (lower numbers come first).
5. Leave `hidden = false` to publish. Set `hidden = true` to stage a draft.

The filter buttons on `/photography/` are generated from distinct `category` values, so new categories appear automatically.

### Reading inbound hire requests

Form submissions from `/hire/` land in the `contact_requests` table. RLS only allows INSERT for the public; read them in the Supabase **Table Editor** &rarr; `contact_requests`.

## Conventions

- Preserve the `<link rel="stylesheet" href="styles.css">` import on all primary pages so tokens stay unified.
- Keep math in `$...$` / `$$...$$` (MathJax handles rendering).
- Keep code fences as `<pre><code class="language-XYZ">...</code></pre>` (Prism handles highlighting).
- Use the `.btn .btn-primary` / `.btn-secondary` pattern for calls to action.
- Use `var(--color-*)` tokens, never hardcoded colors.

## Dynamic data

Minimal Supabase usage for two features only:

- `photos` table + `photos` Storage bucket &mdash; powers `/photography/`.
- `contact_requests` table &mdash; captures submissions from the `/hire/` form.

Both tables have RLS enabled. Public SELECT is allowed only on non-hidden photos; public INSERT is allowed only on `contact_requests`. Writes on `photos` must come from the Supabase dashboard (service role).
