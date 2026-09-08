# TermTint API Reference

This document provides complete documentation for the public API surface of **TermTint**.

---

## Functions

### `colored(text, color=None, style=None, rgb=None, color256=None, stream=None)`

Formats a given string or object with ANSI escape sequences for color and optional styling.

- **`text`** (`Any`): The content to be styled. Converted to string.
- **`color`** (`str`, optional): Standard foreground color name.
  - Supported: `"black"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, `"white"`.
- **`style`** (`str`, optional): Text styling. Defaults to `None` (`"normal"`).
  - Supported: `"normal"`, `"bold"`, `"bright"`, `"dim"`, `"italic"`, `"underline"`, `"reverse"`, `"strikethrough"`.
- **`rgb`** (`tuple[int, int, int]`, optional): Sequence of 3 integers `(r, g, b)` between 0 and 255 for 24-bit True Color.
- **`color256`** (`int`, optional): Extended 256-color ANSI code between 0 and 255.
- **`stream`** (`TextIO`, optional): Destination output stream for color capability detection. Defaults to `sys.stdout`.

> [!NOTE]
> `color`, `rgb`, and `color256` are mutually exclusive. Exactly one color source must be provided.

**Returns:**
- `str`: Formatted ANSI string if color output is enabled for the stream; plain text string otherwise.

**Raises:**
- `ValueError`: If an unsupported color or style is provided, or if color specifications conflict.
- `TypeError`: If invalid types (such as booleans or non-integers) are provided for colors or styles.

**Examples:**
```python
from termtint import colored

# Named color
print(colored("Task completed!", "green"))
print(colored("High priority alert", "red", style="bold"))

# 24-bit True Color (RGB)
print(colored("Coral header", rgb=(255, 127, 80)))
print(colored("Styled sky blue", rgb=(135, 206, 235), style="italic"))

# 256-color ANSI
print(colored("Vibrant orange", color256=208))
print(colored("Hot pink", color256=198, style="underline"))
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

### Named Color Print Functions
- `print_black(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_red(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_green(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_yellow(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_blue(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_magenta(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_cyan(*values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_white(*values, style=None, sep=" ", end="\n", file=None, flush=False)`

### RGB & 256-Color Print Functions
- `print_rgb(rgb, *values, style=None, sep=" ", end="\n", file=None, flush=False)`
- `print_256(color256, *values, style=None, sep=" ", end="\n", file=None, flush=False)`

**Example:**
```python
from termtint import print_green, print_red, print_rgb, print_256

print_green("Operation successful!")
print_red("Fatal Error:", "File not found", sep=" ", style="bold")
print_rgb((255, 140, 0), "Battery level critical")
print_256(208, "Sensor calibration warning")

# Writing to a log file automatically avoids ANSI codes
with open("app.log", "w") as f:
    print_green("Log entry without ANSI codes", file=f)
```
