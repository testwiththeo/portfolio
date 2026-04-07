# Personal Portfolio

Personal portfolio and technical blog for a Software Quality Assurance, built with Astro and Tailwind CSS.

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
