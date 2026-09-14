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

**TermTint** solves this by providing a clean, simple, zero-dependency interface for colored and styled terminal text without the overhead of heavy CLI frameworks:

```python
from termtint import colored, styled

print(colored("Success!", "green"))
print(styled("Alert!", color="red", style=["bold", "underline"]))
print(styled("Deployed", theme="success"))
```

---

## Features

- **Zero Runtime Dependencies**: Uses only the Python standard library.
- **Fluent Styling (`styled`)**: Flexible formatting with single or multiple styles (`["bold", "underline"]`).
- **Semantic Themes (`Theme`)**: Role-based theming (`"success"`, `"error"`, `"warning"`, `"info"`, `"muted"`, `"brand"`) and custom application themes.
- **Named, RGB & 256 Colors**: 8 standard colors, 24-bit True Color (`rgb=(r, g, b)`), and 256-color ANSI (`color256=n`).
- **8 Text Styles**: `normal`, `bold`, `bright`, `dim`, `italic`, `underline`, `reverse`, and `strikethrough`.
- **Modern Windows Support**: Native Virtual Terminal support on Windows 10/11.
- **NO_COLOR Compliant**: TermTint respects `NO_COLOR` in automatic mode.
- **Redirect & Stream Aware**: TermTint automatically avoids adding ANSI escape sequences when output is redirected to a file or pipe.
- **Convenience Helpers**: Direct `print_green()`, `print_rgb()`, `print_256()`, and other function helpers.
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
from termtint import colored, styled, Theme, print_green, print_red, print_rgb, print_256

# 1. Fluent styling with styled()
print(styled("Header", style="bold"))
print(styled("Warning!", color="yellow", style="bold"))
print(styled("Accent", rgb=(255, 128, 0), style="italic"))
print(styled("Badge", color256=198, style=["bold", "reverse"]))
print(styled("Alert", color="red", style=("bold", "underline")))
print(styled("Success", theme="success"))

# 2. Classic colored() API
print(colored("Operation succeeded", "green"))
print(colored("Custom coral text", rgb=(255, 127, 80)))
print(colored("Vibrant orange", color256=208))

# 3. Role-based Theme API
custom_theme = Theme({
    "success": {"color": "green", "style": "bold"},
    "brand": {"rgb": (0, 122, 255), "style": "bold"},
    "notice": {"color256": 214, "style": "italic"},
})
custom_theme.print("System online", "brand")
custom_theme.print("Backup complete", "success")

# 4. Convenience print functions
print_green("System online")
print_red("Fatal crash occurred!", style="bold")
print_rgb((255, 165, 0), "Warning: battery at 15%")
print_256(196, "Critical temperature threshold exceeded")
```

---

## Fluent Styling with `styled()`

The `styled()` function provides a unified entry point for all formatting:

```python
from termtint import styled

# Single or multiple styles
styled("Single style", style="bold")
styled("Multiple styles list", color="cyan", style=["bold", "underline"])
styled("Multiple styles tuple", color="red", style=("bold", "reverse"))
styled("Comma-separated string", color="green", style="bold, italic")

# Fallback with no styling returns plain text
styled("Plain text")  # -> "Plain text"
```

---

## Theme System

TermTint includes role-based theming so you can style messages by purpose rather than hardcoded colors.

### Built-in Roles

Use `styled(..., theme="role")` to tap into the active theme:

```python
from termtint import styled

print(styled("Task completed successfully", theme="success"))  # green + bold
print(styled("Database error", theme="error"))                # red + bold
print(styled("Low disk space", theme="warning"))              # yellow
print(styled("Syncing data...", theme="info"))                 # cyan + italic
print(styled("2026-09-14 12:00:00", theme="muted"))           # dim
print(styled("Acme CLI", theme="brand"))                      # RGB blue + bold
```

### Custom Themes and Extension

```python
from termtint import Theme, set_theme, reset_theme

app_theme = Theme({
    "success": {"color": "green", "style": "bold"},
    "danger": {"color": "red", "style": ["bold", "underline"]},
    "brand": {"rgb": (120, 80, 255), "style": "bold"},
})

# Print directly with the theme
app_theme.print("Application ready", "brand")

# Extend without mutating the original
extended = app_theme.extend(
    accent={"color256": 208, "style": "italic"}
)

# Or set globally
set_theme(app_theme)
print(styled("App startup", theme="brand"))
reset_theme()  # Restore default theme
```

---

## Supported Colors

### 1. Named Terminal Colors

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

### 2. RGB / True Color (24-bit)

Pass an `(r, g, b)` tuple with values from 0 to 255 to `rgb=`:

```python
print(colored("Custom purple", rgb=(138, 43, 226)))
print(styled("Sunset orange", rgb=(255, 69, 0), style="bold"))
```

### 3. 256-Color ANSI

Pass an integer color index (0 to 255) to `color256=`:

```python
print(colored("Bright red", color256=196))
print(styled("Electric blue", color256=33, style="underline"))
```

> [!NOTE]
> `color`, `rgb`, and `color256` are mutually exclusive. Specify at most one color source per call.

---

## Supported Styles

TermTint supports 8 standard text styles:

| Style | Description | Code Example |
| :--- | :--- | :--- |
| `normal` | Default normal weight | `styled("text", style="normal")` |
| `bold` | Bold weight (ANSI 1) | `styled("text", style="bold")` |
| `bright` | Bright / bold weight (ANSI 1) | `styled("text", style="bright")` |
| `dim` | Faded / lower intensity (ANSI 2) | `styled("text", style="dim")` |
| `italic` | Italic text (ANSI 3) | `styled("text", style="italic")` |
| `underline` | Underlined text (ANSI 4) | `styled("text", style="underline")` |
| `reverse` | Inverted foreground/background (ANSI 7) | `styled("text", style="reverse")` |
| `strikethrough` | Strikethrough text (ANSI 9) | `styled("text", style="strikethrough")` |

`bold` and `bright` map to the same ANSI escape code (1). All styles combine seamlessly with named colors, RGB, 256-color output, and themes.

---

## Convenience Print Functions

In addition to `colored()` and `styled()`, TermTint provides direct print functions:

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
    print_rgb,
    print_256,
)

print_green("Success message")
print_red("Error message", style="bold")
print_yellow("Warning message", style="underline")
print_rgb((100, 200, 255), "Custom RGB notice")
print_256(214, "256-color amber alert")
```

All convenience functions support standard Python `print()` keyword arguments: `sep`, `end`, `file`, and `flush`.

---

## Enabling & Disabling Colors

By default, TermTint uses automatic terminal detection. You can explicitly force or disable colors programmatically:

```python
from termtint import enable_color, disable_color, reset_color_state, styled

# Force colors ON (e.g. CLI --color=always flag)
enable_color()
print(styled("Always colored", color="cyan"))

# Force colors OFF (e.g. CLI --no-color flag)
disable_color()
print(styled("Plain text only", color="cyan"))  # Output: "Plain text only"

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

TermTint is a focused, lightweight alternative for developers who primarily need simple colored terminal output:

| Feature / Goal | TermTint | Colorama |
| :--- | :--- | :--- |
| **Runtime Dependencies** | **Zero (Standard Library)** | External package |
| **Primary Goal** | Lightweight colored & styled output | Legacy ANSI translation |
| **API Style** | Clean functional API (`colored`, `styled`, `Theme`) | Module constants & stream wrappers |
| **`stdout` Patching** | Avoided (pure string format) | Global stream wrapping option |
| **Theme System** | Built-in role-based themes | Not supported |
| **Multiple Styles** | Supported natively | Manual constant concatenation |
| **Modern Windows 10/11** | Native VT API | Supported |
| **`NO_COLOR` Standard** | Supported in auto mode | Not native |

See [Migrating from Colorama to TermTint](docs/colorama_migration.md) for a side-by-side migration guide.

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
- [Migrating from Colorama](docs/colorama_migration.md)
- [Development Guide](docs/development.md)
- [Publishing Guide](docs/publishing.md)

---

## License

TermTint is licensed under the [MIT License](LICENSE).
