# Jyoti Ranjan Jally — Machine Learning Portfolio

Source code for my personal portfolio and technical blog, available at [jyotiranjanjally.github.io](https://jyotiranjanjally.github.io/).

The site presents my work as a Machine Learning Developer and Quality Engineering Lead, alongside articles on machine learning, AI, data science, test automation, and software engineering.

## Highlights

- Professional portfolio covering experience, skills, certifications, and education
- Project showcase for machine-learning and engineering work
- Technical articles with mathematics, Python examples, and tags
- Responsive design with light and dark themes
- Search, RSS feed, sitemap, and generated Open Graph images

## Technology Stack

- [Astro](https://astro.build/)
- TypeScript and React
- Tailwind CSS
- Markdown content collections
- Fuse.js search

## Project Structure

```text
src/
├── content/blog/          # Technical articles
│   └── ml/                # Machine-learning articles
├── pages/                 # Site routes
│   ├── about.md
│   ├── portfolio.md
│   └── projects.md
├── components/            # Shared UI components
├── layouts/               # Page and post layouts
└── config.ts              # Site metadata and social links
public/                    # Static assets
```

## Run Locally

Requirements: Node.js 18 or later and npm.

```bash
npm install
npm run dev
```

The local site is served at `http://localhost:4321`.

## Useful Commands

| Command                | Description                                       |
| ---------------------- | ------------------------------------------------- |
| `npm run dev`          | Start the local development server                |
| `npm run build`        | Generate an optimized production build in `dist/` |
| `npm run preview`      | Preview the production build locally              |
| `npm run lint`         | Run ESLint                                        |
| `npm run format:check` | Check formatting with Prettier                    |
| `npm run format`       | Format supported source files                     |

## Add a Blog Article

Create a Markdown file under `src/content/blog/`. Machine-learning articles belong under `src/content/blog/ml/`.

```md
---
title: "Article title"
description: "A concise article summary."
pubDatetime: 2026-08-29T10:00:00Z
tags:
  - machine-learning
  - python
draft: false
---
```

Set `draft: true` to keep an article out of the public site.

## Deployment

The site is configured for GitHub Pages. A production build is generated with:

```bash
npm run build
```

## Contact

- [GitHub](https://github.com/jyotiranjanjally)
- [LinkedIn](https://www.linkedin.com/in/jyotiranjanjally)
- [Email](mailto:jyotiranjanjally@gmail.com)
