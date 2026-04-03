# Technology

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

[Pixi](https://pixi.prefix.dev/latest/) is a fast, cross-platform package manager that reads the `pixi.toml` file already in the repository. Full installation docs: [pixi.prefix.dev/latest/installation](https://pixi.prefix.dev/latest/installation/).

1. **Install Pixi.**

   **macOS / Linux** — open a terminal and run:
   ```bash
   curl -fsSL https://pixi.sh/install.sh | sh
   ```
   If your system does not have `curl`, use `wget` instead:
   ```bash
   wget -qO- https://pixi.sh/install.sh | sh
   ```
   On **macOS** you can also use Homebrew:
   ```bash
   brew install pixi
   ```

   **Windows** — open PowerShell and run:
   ```powershell
   winget install prefix-dev.pixi
   ```
   Or download the `.msi` installer from the [Pixi GitHub releases page](https://github.com/prefix-dev/pixi/releases/latest).

   **After installation, close and reopen your terminal** so that the `pixi` command is on your PATH.

2. **Install all dependencies** — from inside the `ess314` folder:

   ```bash
   pixi install
   ```

   This reads `pixi.toml` and installs all required packages into a local `.pixi/` folder inside the repository. It does **not** affect your system Python.

3. **Register the Jupyter kernel** (one-time, required so JupyterLab can find the environment):

   ```bash
   pixi run install-kernel
   ```

   This registers a kernel named **ESS 314 (Python 3)** that will appear in JupyterLab's kernel selector.

4. **Launch JupyterLab:**

   ```bash
   pixi run lab
   ```

   Your browser will open JupyterLab. Navigate to `notebooks/`, open a lab file, and select the **ESS 314 (Python 3)** kernel when prompted.

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

### Step 4 — Restarting the kernel

A **kernel** is the Python process that runs your notebook cells. You will need to restart it in several situations:

| When | What to do |
|------|------------|
| A cell seems stuck and never finishes | **Kernel → Interrupt Kernel**, then re-run if needed |
| Variables are in an unexpected state after deleting/reordering cells | **Kernel → Restart Kernel…** |
| You install a new package and need it to be importable | **Kernel → Restart Kernel…** |
| Before submitting: verify the notebook runs top-to-bottom cleanly | **Kernel → Restart Kernel and Run All Cells…** |

:::{important}
Always do a **Restart Kernel and Run All Cells** before submitting a lab. This catches bugs where later cells depend on variables set in cells that were later deleted or reordered.
:::

To restart in JupyterLab: click the **Kernel** menu at the top, or right-click in the notebook and choose from the kernel options. You can also click the ⟳ (restart) button in the toolbar.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `git: command not found` | Git not installed | Follow Step 1 above |
| `pixi: command not found` after install | Terminal not restarted | Close and reopen terminal |
| `ModuleNotFoundError: No module named 'numpy'` | Wrong environment active | Run `pixi run lab` (Pixi) or `conda activate ess314` then `jupyter lab` (conda) |
| Kernel selector shows no ESS 314 kernel | `install-kernel` not run | Run `pixi run install-kernel` once, then restart JupyterLab |
| JupyterLab opens but kernel fails to start | Kernel not linked to environment | Run `pixi run install-kernel` (Pixi) or `python -m ipykernel install --user --name ess314` (conda) |
| Cell output looks wrong after editing earlier cells | Stale kernel state | **Kernel → Restart Kernel and Run All Cells** |
| `git pull` gives "merge conflict" | You edited a tracked file | Copy your changes to a separate file, run `git checkout -- <filename>`, then pull |

If you are stuck, post a screenshot of the error on the course Slack or bring your laptop to office hours.
