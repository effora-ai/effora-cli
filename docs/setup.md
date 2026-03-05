# Development Setup

This guide walks through setting up the Effora CLI for local development from scratch.

---

## Prerequisites

- Python 3.10+
- Git
- A GitHub account with access to `effora-ai` org

---

## 1. Clone the repo

```bash
git clone https://github.com/effora-ai/effora-cli.git
cd effora-cli
```

## 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

## 3. Install in editable mode

```bash
pip install -e .
```

## 4. Verify the CLI works

```bash
effora --help
effora ml --help
effora genai --help
```

---

## Project structure

```
effora-cli/
├── effora/
│   ├── __init__.py          # Package version
│   ├── cli.py               # Root CLI — registers command groups
│   └── commands/
│       ├── ml.py            # ML for Finance commands
│       └── genai.py         # GenAI for Finance commands
├── docs/
│   ├── setup.md             # This file
│   └── release.md           # How to release to PyPI
├── .github/
│   └── workflows/
│       └── publish.yml      # Auto-publish to PyPI on tag
├── pyproject.toml           # Package config and dependencies
├── README.md
└── CONTRIBUTING.md
```

---

## Making changes

### Adding a new ML command

Open `effora/commands/ml.py` and add a new function:

```python
@app.command()
def your_command(ticker: str = typer.Argument(..., help="Ticker symbol")):
    """One-line description."""
    typer.echo(f"[effora ml] your_command — {ticker}")
```

### Adding a new command group

1. Create `effora/commands/your_group.py`
2. Register it in `effora/cli.py`:

```python
from effora.commands import your_group
app.add_typer(your_group.app, name="your_group", help="Description.")
```

---

## Common issues

**`effora` command not found after install**
```bash
# Check if there is a conflicting alias
which effora
type effora

# Remove any alias
unalias effora
```

**Editable install not reflecting changes**
```bash
pip install -e .
```

---

## GitHub Actions

The repo has one workflow: `.github/workflows/publish.yml`

It triggers on version tags (`v*`) and publishes to PyPI automatically.

See [release.md](release.md) for the full release process.