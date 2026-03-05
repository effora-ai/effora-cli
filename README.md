# effora-ai

**ML and GenAI for Finance — CLI**

Effora is an open-source CLI and API platform that brings machine learning and generative AI to finance and accounting teams. Built for developers who work with financial data.

---

## Install

```bash
pip install effora-ai
```

## Quickstart

```bash
effora --help
effora ml --help
effora genai --help
```

## Commands

### ML for Finance
```bash
effora ml risk AAPL        # Predict 30-day portfolio VaR for a ticker
effora ml anomaly          # Detect anomalies in journal entries
```

### GenAI for Finance
```bash
effora genai close         # Run agentic financial close automation
effora genai query "What was Q3 revenue?"   # Query financial documents via RAG
```

---

## Roadmap

- [ ] `effora ml risk` — Temporal Fusion Transformer for portfolio VaR
- [ ] `effora ml anomaly` — IsolationForest anomaly detection on journal entries
- [ ] `effora genai close` — LangGraph agentic close automation
- [ ] `effora genai query` — RAG over financial documents
- [ ] FastAPI backend
- [ ] API key authentication

---

## Contributing

We welcome contributions. See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

### Local setup

```bash
git clone https://github.com/effora-ai/effora-cli.git
cd effora-cli
python -m venv venv
source venv/bin/activate
pip install -e .
effora --help
```

### Project structure

```
effora/
├── __init__.py
├── cli.py              # Root CLI app
└── commands/
    ├── ml.py           # ML for Finance commands
    └── genai.py        # GenAI for Finance commands
```

### Branch naming
- `feat/your-feature`
- `fix/your-fix`

### Submitting a PR
1. Fork the repo
2. Create a branch
3. Open a pull request against `main`

---

## License

MIT — see [LICENSE](LICENSE)

---

Built by [Effora AI](https://effora.ai)