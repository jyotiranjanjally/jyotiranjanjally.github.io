# Technical knowledge hub

The existing HTML/CSS/JavaScript portfolio remains intact. The hub uses a Python standard-library generator; there is no Node package-manager installation or lockfile requirement for deployment.

## Build and preview

```sh
python3 scripts/build.py --stage
python3 scripts/validate.py
node scripts/test-charts.cjs
node scripts/test-content.cjs
python3 -m http.server 8000 --directory _site
```

Open `/articles.html`. Generated pages are committed under `articles/`, so the repository also works as a static preview without running a server-side application. GitHub Actions regenerates and validates `_site` before uploading it to Pages. Push to `main` to trigger the existing deployment workflow.

## Content organization

- `content/articles.json`: canonical metadata, topic paths, series order, related slugs, content/example paths, and diagram type.
- `content/categories.json`: category → topic → child-topic hierarchy. Empty categories have filter states, not placeholder articles.
- `content/regression/*.html`: original article bodies, with semantic headings, LaTeX, and component markers.
- `content/templates/`: shared header and footer following the portfolio's existing design.
- `content/legacy-articles.html`: preserved original three engineering notes. Their anchors remain on the listing page so homepage links and existing bookmarks work.
- `examples/*.py`: standalone runnable source; the generator embeds the same bytes into the corresponding article.
- `assets/hub/hub.css`: styles scoped to hub pages.
- `assets/hub/hub.js`: search/filter URL state, math rendering, Python token highlighting, code copy, table-of-contents state, and reading progress.
- `assets/hub/charts.js`: accessible SVG experiments and pure numerical helpers.
- `assets/hub/vendor/katex/`: locally bundled KaTeX 0.16.22, fonts, and MIT license. No third-party network request is needed to read equations.
- `scripts/build.py`: reusable listing/detail rendering, reading-time calculation, sitemap generation, and deployment staging.

Do not hand-edit generated `articles.html`, `articles/*/index.html`, `assets/hub/catalog.json`, or `sitemap.xml`.

## Add an article

1. Add an HTML body under `content/` with unique `h2 id` attributes. Use `<div class="math">…LaTeX…</div>` for display equations; HTML-escape ampersands and less-than signs.
2. Add a metadata entry with `slug`, `title`, `summary`, `category`, `subcategory`, `topicPath`, `tags`, `difficulty`, ISO `date`, `related`, and `content` (repository-relative path). Use the actual publication date.
3. Optionally add `series` and `seriesOrder` for ordered navigation, `example` pointing to a standalone Python file, and `chart` for an existing interactive lab.
4. Use `<!-- PYTHON -->` where the downloadable script belongs and `<!-- CHART -->` where the selected diagram belongs. Available chart types: `line`, `polynomial`, `ridge`, `lasso`, `elastic`, `metrics`, `descent`, `residual`, and `compare`.
5. Add new categories/topics to `content/categories.json` if needed. Rebuild and run checks. Core page components do not need modification.

Search includes titles, summaries, tags, and topic paths. The original notes are searched by their text. All tutorial bodies and navigation are static HTML. JavaScript enhances filters, diagrams, math, highlighting, and progress. Without JavaScript, text and links remain available; equations retain their LaTeX source and labs provide a fallback message.

## Python examples

```sh
python3 -m venv /tmp/hub-examples
/tmp/hub-examples/bin/pip install -r examples/requirements.txt
/tmp/hub-examples/bin/python scripts/check-examples.py
/tmp/hub-examples/bin/python examples/end-to-end-regression-project.py
```

The pinned environment was tested with Python 3.14, NumPy 2.5.4, Pandas 3.1.0, Matplotlib 3.11.2, and scikit-learn 1.9.1. On an interactive backend, each script displays its plot. The check runner uses Agg and verifies numerical execution and assertions; a noninteractive `plt.show()` warning is expected. The diabetes dataset is bundled with scikit-learn; no dataset download is required.

The static production build does not install or execute the scientific Python environment. The examples are educational and the real-dataset project is not a clinical deployment claim.

## Validation and lint

`validate.py` checks internal files/anchors, unique IDs, canonical URLs, structured data, article metadata, code syntax, interview sections, and local math fonts. `test-content.cjs` renders every equation with KaTeX in strict error mode. `test-charts.cjs` checks analytical thresholds, endpoint equivalence, metric arithmetic, and polynomial recovery.

The root `eslint.config.mjs` supplies an ESLint 9 flat configuration for first-party hub JavaScript and Node validation scripts. It replaces the legacy Astro configuration for these checks without introducing a site runtime dependency:

```sh
npx --yes --package=eslint@9.39.1 eslint assets/hub/hub.js assets/hub/charts.js scripts/*.cjs
```

There is no TypeScript in this repository, so no type-check build applies. Future articles should be validated with the same content and code contracts. The featured regression series on the listing is intentionally editorial; category cards, filters, dates, reading times, and series navigation are metadata-driven.
