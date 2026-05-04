FinSight
========

Developer setup
---------------

Quick steps to set up a development environment and run tests locally:

1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the project in editable mode and runtime deps

```bash
pip install -e .
pip install -r requirements.txt
```

3. Run tests (the project uses local imports; run with `PYTHONPATH=.`)

```bash
PYTHONPATH=. python3 -m pytest -q
```

Notes
-----
- The workspace already contains `.vscode/settings.json` which adds the project root to `python.analysis.extraPaths` for the VS Code Python/Pylance server.
- CI is provided in `.github/workflows/ci.yml` and will run `ruff`, `mypy`, and `pytest` on PRs/pushes.

