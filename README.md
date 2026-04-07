# Theodore Portfolio

Personal portfolio and technical blog for a QA / Quality Engineering profile, built with Astro and Tailwind CSS.

Live site: https://theodores.dev

## Tech Stack

- Astro 5
- Tailwind CSS
- React (for selected UI components)
- Radix UI primitives

## What This Repo Contains

- Portfolio landing page with experience, projects, and contact sections
- Blog pages with EN/ID language switching support
- Project case studies and QA documentation samples
- Static assets for gallery, OG images, and downloadable docs

## Local Development

```bash
npm install
npm run dev
```

Open http://localhost:4321

## Build and Preview

```bash
npm run build
npm run preview
```

Build output is generated in `dist/`.

## Project Structure

```text
.
├── public/                 # Static assets
├── src/
│   ├── components/         # UI and reusable Astro/React components
│   ├── content/            # Case studies and project content
│   ├── data/               # Site config and article metadata
│   ├── layouts/            # Main layout and blog layout
│   ├── pages/              # Routes (home, blog, project detail pages)
│   └── styles/             # Global styles
├── package.json
└── astro.config.mjs
```

## Blog Authoring Notes

- Article metadata is stored in `src/data/articles.ts`
- Article pages live in `src/pages/blog/*.astro`
- Raw draft notes can be stored in `src/pages/blog/raw/`
- Blog language strings are defined per page via `window.__blogI18n`

## Common Update Paths

- Update homepage copy and sections: `src/pages/index.astro`
- Add or update blog metadata: `src/data/articles.ts`
- Edit blog listing UI/text: `src/pages/blog/index.astro`
- Adjust blog layout behavior (theme/lang): `src/layouts/BlogLayout.astro`
