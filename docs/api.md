# TermTint API Reference

This document provides complete documentation for the public API surface of **TermTint**.

---

## Core Formatting Functions

### `styled(text, color=None, style=None, rgb=None, color256=None, theme=None, stream=None)`

Formats text with optional colors, single or multiple styles, or semantic theme roles.

- **`text`** (`Any`): The content to be styled. Converted to string. If no styling or theme is specified, returns `str(text)`.
- **`color`** (`str`, optional): Standard foreground color name (`"black"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, `"white"`).
- **`style`** (`str | Sequence[str]`, optional): One or more text styles.
  - Can be a single style string: `"bold"`
  - A comma-separated string: `"bold, underline"`
  - A sequence of strings: `["bold", "reverse"]` or `("italic", "underline")`
  - Supported style tokens: `"normal"`, `"bold"`, `"bright"`, `"dim"`, `"italic"`, `"underline"`, `"reverse"`, `"strikethrough"`.
- **`rgb`** (`tuple[int, int, int]`, optional): Sequence of 3 integers `(r, g, b)` between 0 and 255 for 24-bit True Color.
- **`color256`** (`int`, optional): Extended 256-color ANSI code between 0 and 255.
- **`theme`** (`str`, optional): Name of a role in the active theme (e.g., `"success"`, `"error"`, `"warning"`, `"info"`, `"muted"`, `"brand"`).
- **`stream`** (`TextIO`, optional): Destination output stream for color capability detection. Defaults to `sys.stdout`.

> [!NOTE]
> `theme` cannot be combined with explicit `color`, `rgb`, or `color256`.
> Furthermore, `color`, `rgb`, and `color256` are mutually exclusive.

**Returns:**
- `str`: Formatted ANSI string if color output is enabled for the stream; plain text string otherwise.

**Raises:**
- `ValueError`: If an invalid color, style, or conflicting arguments are provided.
- `TypeError`: If arguments have invalid types.
- `KeyError`: If the specified `theme` role is not registered in the active theme.

**Examples:**
```python
from termtint import styled

# Single style
print(styled("Header", style="bold"))

# Color and style
print(styled("Warning!", color="yellow", style="bold"))

# True Color and style
print(styled("Accent", rgb=(255, 128, 0), style="italic"))

# Multiple styles
print(styled("Badge", color256=198, style=["bold", "reverse"]))
print(styled("Alert", color="red", style=("bold", "underline")))

# Semantic theme role
print(styled("Success", theme="success"))

# Plain text fallback (returns str(text))
print(styled("Plain content"))
```

---

### `colored(text, color=None, style=None, rgb=None, color256=None, stream=None)`

Formats a given string or object with ANSI escape sequences for a color and optional single style.

- **`text`** (`Any`): The content to be styled. Converted to string.
- **`color`** (`str`, optional): Standard foreground color name (`"black"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, `"white"`).
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

## Theme System

TermTint provides a lightweight, semantic theme system through the `Theme` class and module-level functions.

### `Theme(roles=None, **role_kwargs)`

Represents an immutable set of semantic styling roles.

**Role Definition Schema:**
A role definition is a `dict` specifying any combination of:
- `color` (`str`, optional): Named color.
- `rgb` (`tuple[int, int, int]`, optional): 24-bit True Color tuple.
- `color256` (`int`, optional): 256-color ANSI integer (0-255).
- `style` (`str | Sequence[str]`, optional): Single style or sequence of styles.

> [!NOTE]
> `color`, `rgb`, and `color256` are mutually exclusive within each role definition.

**Methods:**

#### `Theme.styled(text, role, stream=None)`
Formats `text` according to the specified `role` in this theme.
- **`text`** (`Any`): The content to style.
- **`role`** (`str`): The name of the registered role.
- **`stream`** (`TextIO`, optional): Output stream for capability detection.

**Raises:**
- `KeyError`: If `role` is not defined in the theme.

#### `Theme.print(*values, role=None, sep=" ", end="\n", file=None, flush=False)`
Prints formatted text according to the specified `role`.
- `role` can be passed as a keyword argument (`role="success"`) or as the last positional argument (`theme.print("text", "success")`).
- Passes `stream=file` to ensure destination stream capability checks are honored.

#### `Theme.extend(roles=None, **role_kwargs)`
Returns a **new** `Theme` instance merging this theme's roles with the supplied roles without mutating the original.

**Example:**
```python
from termtint import Theme

custom_theme = Theme({
    "success": {"color": "green", "style": "bold"},
    "warning": {"color": "yellow"},
    "error": {"color": "red", "style": ["bold", "underline"]},
    "brand": {"rgb": (0, 150, 255), "style": "bold"},
})

print(custom_theme.styled("All systems go", "success"))
custom_theme.print("Caution: high temperature", "warning")

# Extend with additional roles
extended_theme = custom_theme.extend(
    accent={"color256": 214, "style": "italic"}
)
```

---

### Global Theme State Functions

#### `DEFAULT_THEME`
The built-in default theme containing standard semantic roles:
- `"success"`: green + bold
- `"error"`: red + bold
- `"warning"`: yellow
- `"info"`: cyan + italic
- `"muted"`: dim
- `"brand"`: rgb=(0, 122, 255) + bold

#### `get_theme()`
Returns the current active global `Theme`.

#### `set_theme(theme)`
Sets the active global `Theme`. Raises `TypeError` if `theme` is not an instance of `Theme`.

#### `reset_theme()`
Resets the active global theme back to `DEFAULT_THEME`.

---

## State Control Functions

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
