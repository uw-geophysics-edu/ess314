# ── ESS 314 Geophysics — JupyterLab Student Container ──────────────────────
#
# Base: quay.io/jupyter/scipy-notebook:python-3.11
#   Ships: Python 3.11, JupyterLab, ipykernel, numpy, matplotlib, scipy, pandas
#   No extra pip installs required — all lab dependencies are already present.
#
# Build:
#   docker build -t ess314 .
#
# Run (quick):
#   docker run -p 8888:8888 ess314
#   Open the token-bearing URL printed to stdout.
#
# Run (persistent student work):
#   docker compose up          # see docker-compose.yml
#
# Published image:
#   ghcr.io/uw-geophysics-edu/ess314:latest
# ────────────────────────────────────────────────────────────────────────────

FROM quay.io/jupyter/scipy-notebook:python-3.11

LABEL org.opencontainers.image.title="ESS 314 Geophysics — Student Labs"
LABEL org.opencontainers.image.description="JupyterLab environment for ESS 314 at UW. Contains all 8 lab notebooks and course figures."
LABEL org.opencontainers.image.authors="Marine Denolle <marinedenolle@uw.edu>"
LABEL org.opencontainers.image.source="https://github.com/uw-geophysics-edu/ess314"
LABEL org.opencontainers.image.licenses="MIT"

# ── Copy course content ──────────────────────────────────────────────────────
# jovyan is the default non-root user in Jupyter Docker Stacks
COPY --chown=jovyan:users notebooks/  /home/jovyan/work/notebooks/
COPY --chown=jovyan:users assets/figures/ /home/jovyan/work/assets/figures/

# ── Working directory ────────────────────────────────────────────────────────
WORKDIR /home/jovyan/work

# ── Expose JupyterLab port ────────────────────────────────────────────────────
EXPOSE 8888
