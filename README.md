# ESS 314: Introduction to Geophysics

[![Deploy Jupyter Book](https://github.com/uw-geophysics-edu/ess314/actions/workflows/deploy-book.yml/badge.svg)](https://github.com/uw-geophysics-edu/ess314/actions/workflows/deploy-book.yml)

Computational labs and lecture notes for ESS 314 Introduction to Geophysics at the University of Washington by Marine Denolle.

📖 **Course site**: [https://uw-geophysics-edu.github.io/ess314/](https://uw-geophysics-edu.github.io/ess314/)

## Quick Start

```bash
# Option 1: Pixi (preferred)
pixi install
pixi run install-marp   # one-time: installs @marp-team/marp-cli globally
pixi run lab

# Option 2: Conda
conda env create -f environment.yml
conda activate ess314
npm install -g @marp-team/marp-cli   # one-time
jupyter lab
```

Each notebook includes a **Colab badge** — click it to run in Google Colab with no local setup.

> **Pre-commit hooks** (enforced on commit): set them up once with
> `pixi run -e dev -- pre-commit install`

## Repository Structure

```
lectures/           MyST Markdown lecture notes (JupyterBook source)
notebooks/          Jupyter lab notebooks (with Colab badges)
slides/
  ess314.css        Shared Marp theme (WCAG AA colorblind-safe)
  *_slides.md       Marp source decks
  *_slides.html     Compiled HTML — committed and served via GitHub Pages
assets/
  figures/          Python-generated PNGs (colorblind-safe palette)
    ai_gen/         AI-generated illustrations (prompts logged in scripts/)
  scripts/          Figure generation scripts (fig_NAME.py)
_static/            Logo, custom CSS for JupyterBook
_config.yml         Jupyter Book configuration
_toc.yml            Table of contents
pixi.toml           Pixi tasks & dependencies
references.bib      Shared BibTeX bibliography
.pre-commit-config.yaml   Pre-commit hooks (auto-compiles slide decks on commit)
```

Slides are served at `https://uw-geophysics-edu.github.io/ess314/slides/` — the same
GitHub Pages deployment as the book. Each lecture page links directly to its slide HTML.

## Building the Book

```bash
pixi run slides-html     # Compile all Marp decks → HTML (into slides/)
pixi run build-book      # Build JupyterBook locally
pixi run build-all       # slides-html + build-book in one step
pixi run serve-book      # Serve book at http://localhost:8000

# PDF output for slides:
pixi run slides-pdf

# Live slide preview with hot-reload:
marp --preview --theme slides/ess314.css slides/lecture_01_slides.md
```

The book is automatically deployed to GitHub Pages on every push to `main`. CI compiles
all slide decks to HTML and places them in `website/slides/` before uploading the artifact,
so compiled slides are always in sync with the deployed book.

## Contributing

1. Add a Colab badge as the first cell in every notebook.
2. Update `_toc.yml` when adding new content.
3. For new slide decks, place them in `slides/` as `lecture_NN_slides.md` and add a
   `:::{seealso}` link block near the top of the matching `lectures/NN_*.md` file:
   ```markdown
   :::{seealso}
   📊 **Lecture slides** — [open in new tab](https://uw-geophysics-edu.github.io/ess314/slides/lecture_NN_slides.html)
   :::
   ```
4. The pre-commit hook compiles slide decks automatically on commit — just `git add` the `.md`
   and the generated `.html` will be staged and committed alongside it.
5. Run `pixi run build-all` to verify slides and book before pushing.

## License

MIT — see [LICENSE](LICENSE).
