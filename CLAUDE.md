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
- `uploads/resume.pdf` - current CV (update this file to publish a new CV)
- `authors/admin/avatar.jpg` - profile photo

Generated folders (`post/`, `publication/`, `tag/`, `category/`, `publication-type/`, `slides/`, `event/`, `en/`, `home/`, `css/wowchemy.*.css`, `js/wowchemy*.js`, `webfonts/`) are leftovers from an earlier Hugo/Wowchemy export. They are served as-is but are not the source of truth. New content should be authored in the four primary pages above.

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

## Conventions

- Preserve the `<link rel="stylesheet" href="styles.css">` import on all primary pages so tokens stay unified.
- Keep math in `$...$` / `$$...$$` (MathJax handles rendering).
- Keep code fences as `<pre><code class="language-XYZ">...</code></pre>` (Prism handles highlighting).
- Use the `.btn .btn-primary` / `.btn-secondary` pattern for calls to action.
- Use `var(--color-*)` tokens, never hardcoded colors.

## Not used

No database, no auth service, no build step. Supabase is available in the environment for future dynamic additions (contact form, analytics) but is not required.
