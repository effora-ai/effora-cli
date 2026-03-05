# Release Guide

This document explains how to release a new version of `effora-ai` to PyPI.

---

## How releases work

Releases are fully automated via GitHub Actions. When you push a version tag, the pipeline:

1. Checks out the repo
2. Builds the package with `hatch`
3. Publishes to PyPI via Trusted Publisher (no API token needed)

---

## Release checklist

### 1. Make sure all changes are committed and pushed

```bash
git status
git push origin main
```

### 2. Bump the version in `pyproject.toml`

```toml
[project]
version = "0.2.0"  # update this
```

Effora follows [Semantic Versioning](https://semver.org):

| Change type | Example | Version bump |
|---|---|---|
| Bug fix | Fix broken command | `0.1.2` → `0.1.3` |
| New feature | Add new ML command | `0.1.3` → `0.2.0` |
| Breaking change | Rename CLI commands | `0.2.0` → `1.0.0` |

### 3. Commit the version bump

```bash
git add pyproject.toml
git commit -m "release v0.2.0"
git push origin main
```

### 4. Tag the release

```bash
git tag v0.2.0
git push origin v0.2.0
```

### 5. Verify on PyPI

Go to [pypi.org/project/effora-ai](https://pypi.org/project/effora-ai) and confirm the new version appears.

Then test the install:

```bash
pip install --upgrade effora-ai
effora --help
```

---

## Trusted Publisher setup

This repo uses PyPI Trusted Publishing (OIDC) — no API tokens required.

It is configured at:
- **PyPI:** Account → Publishing → effora-ai → GitHub trusted publisher
- **GitHub:** `.github/workflows/publish.yml`

If the trusted publisher needs to be reconfigured:
1. Go to [pypi.org](https://pypi.org) → Account → Publishing
2. Add a new trusted publisher with:
   - Repository: `effora-ai/effora-cli`
   - Workflow: `publish.yml`
   - Environment: (Any)

---

## Troubleshooting

**Action fails with OIDC error**
- Check that the trusted publisher is configured on PyPI
- Check that the workflow file has the correct repo and workflow name

**Version already exists on PyPI**
- PyPI does not allow re-uploading the same version
- Bump the version in `pyproject.toml`, commit, and re-tag

**Tag points to wrong commit**
```bash
git tag -d v0.2.0
git push origin --delete v0.2.0
git tag v0.2.0
git push origin v0.2.0
```