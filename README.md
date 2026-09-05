# TermTint

> A lightweight, zero-dependency Python library for simple colored and styled terminal output.

[![CI](https://github.com/hasheramin5-cyber/TermTint/actions/workflows/ci.yml/badge.svg)](https://github.com/hasheramin5-cyber/TermTint/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/termtint.svg)](https://pypi.org/project/termtint/)
[![Python Versions](https://img.shields.io/pypi/pyversions/termtint.svg)](https://pypi.org/project/termtint/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Why TermTint?

Normally, Python prints unstyled plain text in your terminal:

```python
print("Success!")
```

If you want colored output, writing raw ANSI escape sequences manually can quickly make your code hard to read:

```python
print("\033[32mSuccess!\033[0m")
```

**TermTint** solves this by providing a clean, simple, zero-dependency interface for colored terminal text without the overhead of heavy CLI frameworks:

```python
from termtint import colored

print(colored("Success!", "green"))
```

---

## Features

- **Zero Runtime Dependencies**: Uses only the Python standard library.
- **8 Foreground Colors & 4 Text Styles**: Simple, predictable ANSI styling.
- **Modern Windows Support**: Native Virtual Terminal support on Windows 10/11.
- **NO_COLOR Compliant**: TermTint respects `NO_COLOR` in automatic mode.
- **Redirect & Stream Aware**: TermTint automatically avoids adding ANSI escape sequences when output is redirected to a file or pipe.
- **Convenience Helpers**: Direct `print_green()`, `print_red()`, and other function helpers.
- **Ultra-Lightweight**: Minimal runtime overhead and simple code structure.

---

## Installation

Install TermTint via PyPI using `pip`:

```bash
pip install termtint
```

---

## Quick Start

```python
from termtint import colored, print_green, print_red, print_yellow

# Simple string coloring
print(colored("Operation succeeded", "green"))
print(colored("Disk space low", "yellow", style="bright"))
print(colored("Database error", "red", style="underline"))

# Convenience print functions
print_green("System online")
print_yellow("Deprecated feature warning")
print_red("Fatal crash occurred!")
```

---

## Supported Colors

TermTint supports 8 standard terminal foreground colors:

| Color | Value | Code Example |
| :--- | :--- | :--- |
| `black` | Black | `colored("text", "black")` |
| `red` | Red | `colored("text", "red")` |
| `green` | Green | `colored("text", "green")` |
| `yellow` | Yellow | `colored("text", "yellow")` |
| `blue` | Blue | `colored("text", "blue")` |
| `magenta` | Magenta | `colored("text", "magenta")` |
| `cyan` | Cyan | `colored("text", "cyan")` |
| `white` | White | `colored("text", "white")` |

Invalid color names raise a `ValueError` with a helpful error message.

---

## Supported Styles

TermTint supports 4 essential text styles:

| Style | Description | Code Example |
| :--- | :--- | :--- |
| `normal` | Default normal weight | `colored("text", "green", style="normal")` |
| `bright` | Bold / bright weight | `colored("text", "green", style="bright")` |
| `dim` | Faded / lower intensity | `colored("text", "white", style="dim")` |
| `underline` | Underlined text | `colored("text", "blue", style="underline")` |

---

## Convenience Print Functions

In addition to `colored()`, TermTint provides direct print functions for fast CLI output:

```python
from termtint import (
    print_black,
    print_red,
    print_green,
    print_yellow,
    print_blue,
    print_magenta,
    print_cyan,
    print_white,
)

print_green("Success message")
print_red("Error message", style="bright")
print_yellow("Warning message", style="underline")
```

All convenience functions support standard Python `print()` keyword arguments: `sep`, `end`, `file`, and `flush`.

---

## Enabling & Disabling Colors

By default, TermTint uses automatic terminal detection. You can explicitly force or disable colors programmatically:

```python
from termtint import enable_color, disable_color, reset_color_state, colored

# Force colors ON (e.g. CLI --color=always flag)
enable_color()
print(colored("Always colored", "cyan"))

# Force colors OFF (e.g. CLI --no-color flag)
disable_color()
print(colored("Plain text only", "cyan"))  # Output: "Plain text only"

# Reset back to automatic detection
reset_color_state()
```

---

## Automatic Terminal & Stream Detection

TermTint automatically detects terminal capabilities using a multi-step check:

1. **Explicit Toggle**: Respects programmatic `enable_color()` or `disable_color()`.
2. **`NO_COLOR` Variable**: TermTint respects `NO_COLOR` in automatic mode ([no-color.org](https://no-color.org)).
3. **`FORCE_COLOR` Variable**: If `FORCE_COLOR=1`, colors are forced on in automatic mode.
4. **Destination Stream & TTY Check**: If output is redirected (e.g. `python script.py > output.txt`) or a file-like stream is supplied (`file=f`), ANSI escape sequences are avoided automatically.
5. **Dumb Terminal Check**: If `TERM=dumb`, colors are disabled.

---

## Windows Support

On Windows 10 and 11, TermTint automatically enables Virtual Terminal (VT) processing using standard-library `ctypes` bindings to the Win32 Console API. If VT mode cannot be enabled, TermTint safely falls back to plain text without crashing.

---

## Colorama Comparison

TermTint is a focused, lightweight alternative for developers who primarily need simple colored terminal output, whereas Colorama provides broader historical ANSI translation.

| Feature / Goal | TermTint | Colorama |
| :--- | :--- | :--- |
| **Runtime Dependencies** | **Zero (Standard Library)** | External package |
| **Primary Goal** | Lightweight colored output | Legacy ANSI translation |
| **API Style** | Clean functional API | Module constants & stream wrappers |
| **`stdout` Patching** | Avoided (pure string format) | Global stream wrapping option |
| **Modern Windows 10/11** | Native VT API | Supported |
| **`NO_COLOR` Standard** | Supported in auto mode | Not native |

---

## Limitations

TermTint is intentionally small and focused. It is **not** a full terminal UI framework:
- No progress bars or spinners
- No table or layout formatters
- No cursor movement or screen clearing
- No markdown or syntax highlighting

If you require full TUI widgets or complex terminal graphics, consider tools like `Rich` or `Textual`.

---

## Development

Set up TermTint locally:

```bash
git clone https://github.com/hasheramin5-cyber/TermTint.git
cd TermTint
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

Run tests and linters:

```bash
# Run test suite
pytest

# Run linter
ruff check .

# Run micro-benchmarks
python benchmarks/benchmark.py
```

---

## Documentation

Full documentation is available in the [`docs/`](docs/) directory:
- [API Reference](docs/api.md)
- [Usage Guide](docs/usage.md)
- [Architecture Overview](docs/architecture.md)
- [Development Guide](docs/development.md)
- [Publishing Guide](docs/publishing.md)

---

## License

TermTint is licensed under the [MIT License](LICENSE).
