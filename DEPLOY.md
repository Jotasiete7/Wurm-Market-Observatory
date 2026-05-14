# Wurm Market Observatory — Deploy Instructions

## What this project is

A static data publication site built with Observable Framework.
It reads pre-computed JSON datasets and renders historical economic analysis
of Wurm Online trade channel logs.

No backend. No database. No live queries. 100% static after build.

---

## Project structure

```
wurm-observatory/
├── observablehq.config.js     ← site config, nav, title
├── package.json               ← dependencies (only @observablehq/framework)
├── .gitignore
└── src/
    ├── index.md               ← home (Observatory)
    ├── corpus.md              ← Corpus Explorer page
    ├── methodology.md         ← Methodology page
    ├── style/
    │   └── observatory.css    ← all site styles
    ├── data/
    │   ├── corpus-meta.json   ← active corpus metadata + timeline
    │   └── seller-activity.json ← seller lens dataset (mock)
    ├── components/
    │   ├── corpus-health.js   ← CorpusHealthCard component
    │   ├── coverage-timeline.js ← CoverageTimeline component
    │   └── lens-card.js       ← LensCard component
    └── lenses/
        └── seller.md          ← Seller Activity Lens page
```

---

## To run locally

```bash
npm install
npm run dev
# opens at http://localhost:3000
```

---

## To build for production

```bash
npm run build
# output goes to dist/
```

---

## Cloudflare Pages settings

| Setting | Value |
|---|---|
| Build command | `npm run build` |
| Build output directory | `dist` |
| Node version | 18 or 20 (set in environment variables: `NODE_VERSION = 20`) |
| Root directory | `/` (project root) |

---

## GitHub → Cloudflare Pages connection

1. Push this repo to GitHub (any visibility)
2. In Cloudflare Dashboard → Workers & Pages → Create
3. Connect GitHub account → select `wurm-observatory` repo
4. Apply build settings from table above
5. Deploy

Every subsequent `git push` to `main` triggers automatic redeploy.

---

## Adding a new Lens (future)

1. Create `src/data/your-lens.json` with the dataset
2. Create `src/lenses/your-lens.md` following the seller.md template
3. Add the lens card to `src/index.md`
4. Add the page to `observablehq.config.js` pages array

---

## Adding a new Corpus (future)

Update `src/data/corpus-meta.json`:
- Change `active` to the new corpus
- Append to `all_corpora` array

Then regenerate any lens datasets from the new corpus and update the JSON files in `src/data/`.

---

## Notes on mock data

All data in `src/data/` is currently mocked.
When a real corpus pipeline exists (Python), it will write directly to these JSON files.
The site structure does not need to change — only the data files.

---

## Tabler Icons

The site uses Tabler Icons (outline only) loaded via CDN in the Observable Framework config.
To add a new icon: use `<i class="ti ti-ICONNAME">` syntax.
Full icon list: https://tabler.io/icons
