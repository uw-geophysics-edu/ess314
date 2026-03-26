# ESS 314: Introduction to Geophysics

[![Deploy Jupyter Book](https://github.com/uw-geophysics-edu/ess314/actions/workflows/deploy-book.yml/badge.svg)](https://github.com/uw-geophysics-edu/ess314/actions/workflows/deploy-book.yml)

Computational labs and lecture notes for ESS 314 Introduction to Geophysics at the University of Washington by Marine Denolle.

📖 **Course site**: [https://uw-geophysics-edu.github.io/ess314/](https://uw-geophysics-edu.github.io/ess314/)

## Quick Start

```bash
# Option 1: Pixi (preferred)
pixi install
pixi run lab

# Option 2: Conda
conda env create -f environment.yml
conda activate ess314
jupyter lab
```

Each notebook includes a **Colab badge** — click it to run in Google Colab with no local setup.

## Repository Structure

```
lectures/           MyST Markdown lecture notes
notebooks/          Jupyter lab notebooks (with Colab badges)
_static/            Logo, custom CSS
_config.yml         Jupyter Book configuration
_toc.yml            Table of contents
pixi.toml           Pixi tasks & dependencies
references.bib      Shared BibTeX bibliography
```

## Building the Book

```bash
pixi run build-book     # Build locally
pixi run serve-book     # Serve at http://localhost:8000
```

The book is automatically deployed to GitHub Pages on every push to `main`.

## Contributing

1. Add a Colab badge as the first cell in every notebook
2. Update `_toc.yml` when adding new content
3. Run `pixi run build-book` to verify before committing

## License

MIT — see [LICENSE](LICENSE).
