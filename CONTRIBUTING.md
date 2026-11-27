# Contributing to TermTint

Thanks for your interest in TermTint! Bug reports, ideas and pull requests are welcome.

TermTint is intentionally small: **zero runtime dependencies**, standard library only.
Changes that add a runtime dependency will not be accepted.

## Development setup

```bash
git clone https://github.com/hasheramin5-cyber/TermTint.git
cd TermTint
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Before you open a pull request

```bash
pytest                          # run the test suite
ruff check .                    # lint
python benchmarks/benchmark.py  # optional: micro-benchmarks
```

- Supported Python versions: 3.9 and newer.
- Add or update tests for every behaviour change.
- Keep public API changes documented in `README.md`, `docs/api.md` and `CHANGELOG.md`.
- Keep pull requests focused: one topic per pull request.

## Reporting bugs

Please open an issue and include your TermTint version, Python version, operating
system, the terminal you use, and a minimal code sample. For security problems, follow
[SECURITY.md](SECURITY.md) instead of opening a public issue.

## License

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
