# PyPI Trusted Publishing & Release Guide

This document explains how to set up **PyPI Trusted Publishing** (OIDC) and automate package releases via GitHub Actions without storing long-lived PyPI API tokens.

---

## What is PyPI Trusted Publishing?

Trusted Publishing uses OpenID Connect (OIDC) tokens issued by GitHub Actions to securely authenticate releases to PyPI. You do **not** need to create or store a manual PyPI API secret token.

---

## Step 1: Configure PyPI Trusted Publisher

1. Log into your account on [PyPI](https://pypi.org/).
2. Go to **Account Settings** -> **Publishers** (or navigate to [PyPI Publishing Setup](https://pypi.org/manage/account/publishing/)).
3. Under **Add a new publisher**, select **GitHub Actions**.
4. Fill in the exact repository fields:
   - **PyPI Project Name**: `termtint`
   - **Owner**: `hasheramin5-cyber`
   - **Repository name**: `TermTint`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
5. Click **Add Publisher**.

> [!NOTE]
> If `termtint` has not yet been registered on PyPI, PyPI supports **Pending Publishers**. Setting up the publisher under your account before the first release allows the first release from GitHub Actions to automatically create and register the project on PyPI!

---

## Step 2: Configure GitHub Repository Environment

1. Go to your GitHub repository: `https://github.com/hasheramin5-cyber/TermTint`
2. Click **Settings** -> **Environments**.
3. Click **New environment**.
4. Name the environment exactly: `pypi`
5. Save the environment (no secrets need to be added to this environment).

---

## Step 3: Publish a New Release

To publish a new version of TermTint to PyPI:

1. **Update Version**: Update `version = "0.1.0"` in `pyproject.toml` and `__version__ = "0.1.0"` in `src/termtint/__init__.py`.
2. **Commit & Push**:
   ```bash
   git add pyproject.toml src/termtint/__init__.py
   git commit -m "chore: bump version to 0.1.0"
   git push origin main
   ```
3. **Create GitHub Release**:
   - Go to your GitHub repository -> **Releases** -> **Draft a new release**.
   - Choose or create a tag (e.g. `v0.1.0`).
   - Title the release (e.g. `v0.1.0`).
   - Click **Publish release**.

4. **Automated Publishing**:
   - Creating the release triggers `.github/workflows/publish.yml`.
   - GitHub Actions builds the wheel and source distribution, authenticates via PyPI Trusted Publishing, and uploads the release to PyPI automatically.

5. **Verify Installation**:
   ```bash
   pip install termtint
   ```
