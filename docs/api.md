# TermTint API Reference

This document provides complete documentation for the public API surface of **TermTint**.

---

## Functions

### `colored(text, color, style=None, stream=None)`

Formats a given string or object with ANSI escape sequences for color and optional styling.

- **`text`** (`Any`): The content to be styled. Will be converted to string.
- **`color`** (`str`): Foreground color name.
  - Supported: `"black"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, `"white"`.
- **`style`** (`str`, optional): Text styling. Defaults to `None` (`"normal"`).
  - Supported: `"normal"`, `"bright"`, `"dim"`, `"underline"`.
- **`stream`** (`TextIO`, optional): Destination output stream for color capability detection. Defaults to `sys.stdout`.

**Returns:**
- `str`: Formatted ANSI string if color output is enabled for the stream; plain text string otherwise.

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

Explicitly disables colored output across all subsequent calls, outputting plain text without ANSI escape sequences.

**Example:**
```python
from termtint import disable_color, colored

disable_color()
print(colored("Plain text only", "green"))  # Output: Plain text only
```

---

### `is_color_enabled(stream=None)`

Returns the current active status of color formatting for a given output stream.

- **`stream`** (`TextIO`, optional): Output stream to inspect. Defaults to `sys.stdout`.

**Returns:**
- `bool`: `True` if colors will be applied to the stream, `False` otherwise.

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

TermTint provides helper functions that combine formatting and printing in a single call. They inspect the destination `file` stream automatically to avoid adding ANSI escape sequences to non-TTY streams.

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

# Writing to a log file automatically avoids ANSI codes
with open("app.log", "w") as f:
    print_green("Log entry without ANSI codes", file=f)
```
