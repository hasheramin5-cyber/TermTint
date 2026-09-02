# TermTint Development Guide

This guide explains how to set up your local development environment, run tests, lint code, execute benchmarks, and build package distributions.

---

## Environment Setup

### 1. Clone Repository & Create Virtual Environment

```bash
# Clone the repository
git clone https://github.com/your-username/termtint.git
cd termtint

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### 2. Install Development Dependencies

Install TermTint in editable mode along with development dependencies:

```bash
pip install -e ".[dev]"
```

---

## Testing

Run the test suite with `pytest`:

```bash
pytest
```

To include coverage reporting:

```bash
pytest --cov=termtint
```

---

## Linting and Code Style

TermTint enforces clean Python formatting using **Ruff**:

```bash
# Check code for lint issues
ruff check .

# Automatically fix lint issues where applicable
ruff check . --fix
```

---

## Running Benchmarks

Execute the micro-benchmark script to verify performance:

```bash
python benchmarks/benchmark.py
```

---

## Building Distribution Packages

To generate the source distribution (`.tar.gz`) and wheel (`.whl`):

```bash
python -m build
```

Artifacts will be produced in the `dist/` directory.

To test installing the wheel locally into a fresh environment:

```bash
pip install dist/termtint-0.1.0-py3-none-any.whl
python -c "from termtint import colored; print(colored('Local build working!', 'green'))"
```
