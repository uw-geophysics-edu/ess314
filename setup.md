# Setting Up Your Computing Environment

This page walks you through everything you need to run the lab notebooks on your own computer.
If you prefer not to install anything, you can run every notebook in **Google Colab** using the badge at the top of each lab — no setup required.

---

## Option A: Google Colab (no installation)

Every lab notebook has a **"Open in Colab"** badge at the top. Click it, sign in with any Google account, and the notebook will open with all dependencies pre-installed. This is the easiest option and works on any device.

:::{note}
Colab sessions are temporary. Save your work to your Google Drive or download the notebook before closing the tab.
:::

---

## Option B: Run locally on your computer

Running locally gives you persistent files, faster execution, and the ability to work offline. Follow the three steps below.

---

### Step 1 — Get Git and clone the repository

Git is version-control software that lets you download ("clone") the course repository and pull updates when new materials are posted.

#### Install Git

| Platform | What to do |
|----------|-----------|
| **macOS** | Open **Terminal** and run `git --version`. If Git is not found, macOS will prompt you to install the Xcode Command Line Tools — click **Install**. |
| **Windows** | Download and run the installer from [git-scm.com/download/win](https://git-scm.com/download/win). Accept all defaults. |
| **Linux** | Run `sudo apt install git` (Ubuntu/Debian) or `sudo dnf install git` (Fedora). |

#### Optional: GitHub Desktop (recommended for beginners)

If you prefer a graphical interface over the command line, install [**GitHub Desktop**](https://desktop.github.com). It wraps the most common Git operations in a point-and-click interface.

- Download and install GitHub Desktop.
- Sign in with your GitHub account (create a free account at [github.com](https://github.com) if you do not have one).
- Use **File → Clone repository → URL** and paste the repository URL (see below).

#### Clone the repository

**Command line:**
```bash
git clone https://github.com/uw-geophysics-edu/ess314.git
cd ess314
```

**GitHub Desktop:**
1. Open GitHub Desktop.
2. Go to **File → Clone Repository → URL**.
3. Paste `https://github.com/uw-geophysics-edu/ess314.git`
4. Choose a local folder and click **Clone**.

You now have a local copy of all lecture notes, notebooks, and lab files.

#### Pulling updates during the quarter

New materials are posted regularly. Before each lab, update your local copy:

```bash
# Command line
cd ess314
git pull
```

In GitHub Desktop, click **Fetch origin** then **Pull**.

:::{tip}
Never edit files that are part of the course materials directly; you will get merge conflicts when you pull updates. Instead, make a copy of any notebook you want to modify (e.g., rename `Lab1-FirstnameLastname.ipynb` with your actual name before filling it in).
:::

---

### Step 2 — Install the Python environment

The labs use a specific set of Python packages (NumPy, SciPy, Matplotlib, ObsPy, etc.). Installing them into an isolated environment prevents conflicts with any other Python software on your computer.

We support two environment managers: **Pixi** (preferred — faster, handles everything automatically) and **conda/miniconda** (familiar to many scientists).

#### Option B-1: Pixi (preferred)

[Pixi](https://prefix.dev/docs/pixi/overview) is a fast, cross-platform package manager that reads the `pixi.toml` file already in the repository.

1. **Install Pixi** — open a terminal and run:

   ```bash
   curl -fsSL https://pixi.sh/install.sh | sh
   ```

   On Windows, open PowerShell and run:
   ```powershell
   iwr -useb https://pixi.sh/install.ps1 | iex
   ```

   Close and reopen your terminal after installation so the `pixi` command is on your PATH.

2. **Install all dependencies** — from inside the `ess314` folder:

   ```bash
   pixi install
   ```

   This reads `pixi.toml` and installs all required packages into a local `.pixi/` folder inside the repository. It does **not** affect your system Python.

3. **Launch JupyterLab:**

   ```bash
   pixi run lab
   ```

   Your browser will open JupyterLab. Navigate to `notebooks/` and open any lab file.

#### Option B-2: conda / miniconda

If you already use conda, you can create the course environment from the included `environment.yml` file.

1. **Install Miniconda** (if not already installed) — download from [docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html) and run the installer.

2. **Create the environment** — from inside the `ess314` folder:

   ```bash
   conda env create -f environment.yml
   ```

   This creates an environment named `ess314`.

3. **Activate the environment** — you must do this every time you open a new terminal:

   ```bash
   conda activate ess314
   ```

4. **Launch JupyterLab:**

   ```bash
   jupyter lab
   ```

---

### Step 3 — Verify your installation

Once JupyterLab is open, navigate to `notebooks/` and open `Lab1-Intro-Python.ipynb`. Run the first few cells. If you see output from `import numpy` and `import matplotlib` without errors, your environment is working correctly.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `git: command not found` | Git not installed | Follow Step 1 above |
| `pixi: command not found` after install | Terminal not restarted | Close and reopen terminal |
| `ModuleNotFoundError: No module named 'numpy'` | Wrong environment active | Run `pixi run lab` or `conda activate ess314` |
| JupyterLab opens but kernel fails to start | Kernel not linked to environment | In conda: run `python -m ipykernel install --user --name ess314` |
| `git pull` gives "merge conflict" | You edited a tracked file | Copy your changes to a separate file, run `git checkout -- <filename>`, then pull |

If you are stuck, post a screenshot of the error on the course Slack or bring your laptop to office hours.
