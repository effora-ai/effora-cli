# Contributing to Effora AI

Thanks for your interest in contributing. Effora is an open-source CLI and API platform for ML and GenAI in finance. Contributions of all kinds are welcome — bug fixes, new commands, documentation, and tests.

---

## Getting started

### 1. Fork and clone

```bash
git clone https://github.com/effora-ai/effora-cli.git
cd effora-cli
```

### 2. Set up your environment

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

### 3. Verify setup

```bash
effora --help
```

---

## Project structure

```
effora/
├── __init__.py
├── cli.py              # Root CLI — registers ml and genai command groups
└── commands/
    ├── ml.py           # ML for Finance — risk, anomaly detection
    └── genai.py        # GenAI for Finance — close automation, RAG query
```

---

## How to contribute

### Pick an issue
Check the [Issues](https://github.com/effora-ai/effora-cli/issues) tab for open tasks. Issues labeled `good first issue` are the best starting point.

### Branch naming
```
feat/your-feature-name
fix/your-bug-fix
docs/your-doc-update
```

### Making changes
- Keep each PR focused on one thing
- Add a clear description of what you changed and why
- If adding a new command, follow the existing pattern in `ml.py` or `genai.py`

### Submitting a PR
1. Push your branch to your fork
2. Open a pull request against `main`
3. Fill in the PR description — what does it do, how was it tested

---

## Adding a new command

Commands live in `effora/commands/`. To add a new ML command:

```python
# effora/commands/ml.py

@app.command()
def your_command(ticker: str = typer.Argument(..., help="Ticker symbol")):
    """One-line description of what this does."""
    typer.echo(f"[effora ml] your_command — {ticker}")
```

Then register it in `cli.py` if adding a new command group.

---

## Code style
- Python 3.10+
- Keep functions small and focused
- Use type hints

---

## Questions

Open an issue or start a discussion in the [GitHub Discussions](https://github.com/effora-ai/effora-cli/discussions) tab.