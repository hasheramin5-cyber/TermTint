# TermTint API Reference

This document provides complete documentation for the public API surface of **TermTint**.

---

## Functions

### `colored(text, color, style=None)`

Formats a given string or object with ANSI escape sequences for color and optional styling.

- **`text`** (`Any`): The content to be styled. Will be converted to string.
- **`color`** (`str`): Foreground color name.
  - Supported: `"black"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, `"white"`.
- **`style`** (`str`, optional): Text styling. Defaults to `None` (`"normal"`).
  - Supported: `"normal"`, `"bright"`, `"dim"`, `"underline"`.

**Returns:**
- `str`: Formatted ANSI string if color output is enabled; plain text string if color output is disabled.

**Raises:**
- `ValueError`: If an unsupported `color` or `style` is provided.

**Example:**
```python
from termtint import colored

print(colored("Task completed!", "green"))
print(colored("High priority alert", "red", style="bright"))
```

---

### `enable_color()`

Explicitly enables colored output across all subsequent calls, overriding automatic terminal capability detection and environment variables.

**Example:**
```python
from termtint import enable_color, colored

enable_color()
print(colored("Always colored", "cyan"))
```

---

### `disable_color()`

Explicitly disables colored output across all subsequent calls, stripping all ANSI codes and returning plain text.

**Example:**
```python
from termtint import disable_color, colored

disable_color()
print(colored("Plain text only", "green"))  # Output: Plain text only
```

---

### `is_color_enabled()`

Returns the current active status of color formatting.

**Returns:**
- `bool`: `True` if colors will be applied, `False` otherwise.

**Example:**
```python
from termtint import is_color_enabled

if is_color_enabled():
    print("Terminal supports colors!")
```

---

### `reset_color_state()`

Resets color configuration back to automatic terminal capability and environment detection (`AUTO` mode).

**Example:**
```python
from termtint import reset_color_state

reset_color_state()
```

---

## Convenience Print Functions

TermTint provides helper functions that combine formatting and printing in a single call. They accept all standard `print()` arguments (`sep`, `end`, `file`, `flush`) as well as an optional `style` keyword argument.

- `print_black(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_red(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_green(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_yellow(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_blue(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_magenta(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_cyan(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_white(*values, style=None, sep=" ", end="\n", file=None, flush=False)`

**Example:**
```python
from termtint import print_green, print_red, print_yellow

print_green("Operation successful!")
print_yellow("Disk space low", style="bright")
print_red("Fatal Error:", "File not found", sep=" ")
```
