# Knowledge hub validation — 27 October 2026

## Completed

- Built 12 standalone regression tutorials and retained the original three engineering notes and their anchor URLs.
- Generated 14 HTML pages, canonical URLs, Article JSON-LD, sitemap, and a staged GitHub Pages artifact.
- Checked all local links, fragments, unique IDs, heading counts, metadata, related slugs, Python syntax, and KaTeX font references.
- Rendered all 55 display-math expressions with the bundled KaTeX parser in throw-on-error mode.
- Passed numerical chart checks for soft thresholding, ridge/elastic-net endpoints, negative R², constant-target handling, and quadratic recovery.
- Executed all 12 downloadable Python scripts with Python 3.14, NumPy 2.5.4, Pandas 3.1.0, Matplotlib 3.11.2, and scikit-learn 1.9.1. NumPy implementations matched library predictions within the scripts' specified tolerances; lasso KKT and gradient-convergence checks passed.
- ESLint passed for first-party hub JavaScript and Node validation scripts. The retained legacy `.eslintignore` emits an ESLint 9 migration warning; the flat config supplies its own exclusions.
- Browser checks passed for search, filter reset, empty categories, Regression filtering, code copying, slider interaction, light/dark themes, legacy article anchors, and mobile menu open/Escape behaviour.
- Every tutorial rendered at a 390-pixel viewport with no document-level horizontal overflow, no KaTeX error nodes, and populated diagram and syntax-highlight components. No browser console errors were observed. The listing was visually reviewed at 1440 pixels and mobile article/diagram views at 390 pixels.
- `git diff --check` passed. The homepage, shared portfolio JS/CSS, resume, and existing `.idea/` files were not modified.

## Measured example output

The end-to-end script used 353 training rows and 89 test rows. Training-only model selection chose Lasso with library `alpha=0.1`. The square root of mean cross-validation MSE was 55.4041. On the reserved test rows:

| Model | MAE | RMSE | R² |
| --- | ---: | ---: | ---: |
| Training-mean baseline | 64.0065 | 73.2225 | -0.0120 |
| Selected pipeline | 42.8052 | 53.7087 | 0.4555 |

These are observed results from this fixed split and environment, not a general benchmark or a clinical-use claim. The page itself computes output through the downloadable script rather than presenting invented scores.

## Boundaries

- GitHub Actions and public deployment have not been run from this session. The updated workflow builds and validates before upload when pushed to `main`.
- There is no TypeScript code or type-check toolchain.
- Scientific examples ran with a noninteractive Agg backend. Numerical execution and assertions passed; their Matplotlib windows were not visually reviewed. Browser SVG diagrams were reviewed separately.
- Categories beyond the initial regression series and preserved notes have navigable empty states, with no placeholder articles.
- JavaScript enhances math rendering, diagrams, filtering, highlighting, and progress. Without it, article text, links, code, and source LaTeX remain available.

See `KNOWLEDGE-HUB.md` for commands and content authoring instructions.
