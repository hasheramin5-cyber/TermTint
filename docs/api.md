# TermTint API Reference

This document provides complete documentation for the public API surface of **TermTint**.

---

## Core Formatting Functions

### `styled(text, color=None, style=None, rgb=None, color256=None, theme=None, stream=None, fallback=False)`

Formats text with optional colors, single or multiple styles, semantic theme roles, or smart color fallback.

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
- **`fallback`** (`bool`, optional): When `True`, automatically downgrades True Color (RGB) to 256-color or 16-color ANSI, or 256-color to 16-color ANSI, if the destination stream does not support the higher color tier. Defaults to `False`.

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

## Reusable Style Class

Introduced in **v0.4.0**, `Style` represents an immutable styling object that encapsulates colors, styles, theme roles, and fallback settings.

### `Style(color=None, style=None, rgb=None, color256=None, theme=None, fallback=False)`

Creates an immutable `Style` definition.

- **`color`** (`str`, optional): Standard foreground color name (`"black"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, `"white"`).
- **`style`** (`str | Sequence[str]`, optional): One or more text styles.
- **`rgb`** (`tuple[int, int, int]`, optional): 24-bit True Color `(r, g, b)` tuple.
- **`color256`** (`int`, optional): 256-color ANSI integer code (0-255).
- **`theme`** (`str`, optional): Semantic role in the active theme.
- **`fallback`** (`bool`, optional): If `True`, enables graceful degradation when the destination terminal lacks high-color support.

> [!NOTE]
> `color`, `rgb`, and `color256` are mutually exclusive. Furthermore, `theme` cannot be combined with explicit colors.

**Methods:**

#### `Style.apply(text, stream=None)`
Applies this style to `text`.
- **`text`** (`Any`): Content to style.
- **`stream`** (`TextIO`, optional): Destination output stream for capability detection.

#### `Style.__call__(text, stream=None)`
Shorthand for `Style.apply(text, stream=stream)` allowing direct invocation: `my_style("text")`.

#### `Style.print(*values, sep=" ", end="\n", file=None, flush=False)`
Prints styled values directly to `file` (defaults to `sys.stdout`), ensuring stream-aware capability checks are honored.

#### Composable Chaining Methods
All chaining methods return a **new** `Style` instance without mutating the original:
- **`Style.bold()`**: Returns a new `Style` with bold styling added.
- **`Style.italic()`**: Returns a new `Style` with italic styling added.
- **`Style.underline()`**: Returns a new `Style` with underline styling added.
- **`Style.reverse()`**: Returns a new `Style` with reverse styling added.
- **`Style.strikethrough()`**: Returns a new `Style` with strikethrough styling added.
- **`Style.dim()`**: Returns a new `Style` with dim styling added.
- **`Style.with_color(color)`**: Returns a new `Style` with the specified color name (clears `rgb` and `color256`).
- **`Style.with_rgb(rgb)`**: Returns a new `Style` with the specified RGB tuple (clears `color` and `color256`).
- **`Style.with_color256(code)`**: Returns a new `Style` with the specified 256-color index (clears `color` and `rgb`).
- **`Style.with_style(style)`**: Returns a new `Style` with the specified style or sequence of styles.
- **`Style.with_theme(role)`**: Returns a new `Style` referencing the specified theme role (clears explicit colors).
- **`Style.with_fallback(fallback)`**: Returns a new `Style` with the fallback flag set.

#### Operators
- **`style1 + style2`**: Combines two `Style` instances. Merges unique styles, and overrides color/theme from `style2` if defined.

#### Serialization & Factories
- **`Style.to_dict()`**: Returns a dictionary mapping of this style's attributes (suitable for passing into `Theme(...)`).
- **`Style.from_role(role)`**: Class method that creates a `Style` bound to a semantic `Theme` role name.

**Example:**
```python
from termtint import Style

header = Style("cyan", style="bold").underline()
alert = Style("red", style="bold")
subtle = Style(style="dim")

# Shorthand call or .apply()
print(header("Section 1"))
print(alert.apply("Danger!"))

# Direct print
header.print("Dashboard", "Active", sep=" - ")

# Style composition via operator
badge = Style("yellow") + Style(style="reverse")
```

---

## Theme System

TermTint provides a lightweight, semantic theme system through the `Theme` class and module-level functions.

### `Theme(roles=None, **role_kwargs)`

Represents an immutable set of semantic styling roles.

**Role Definition Schema:**
A role definition can be a `dict` or a `Style` instance specifying:
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

#### `Theme.get_style(role)`
Returns a `Style` instance representing the specified `role` in this theme.

#### `Theme.extend(roles=None, **role_kwargs)`
Returns a **new** `Theme` instance merging this theme's roles with the supplied roles without mutating the original.

**Example:**
```python
from termtint import Theme, Style

custom_theme = Theme({
    "success": Style("green", style="bold"),
    "warning": {"color": "yellow"},
    "error": Style("red", style=["bold", "underline"]),
    "brand": {"rgb": (0, 150, 255), "style": "bold"},
})

print(custom_theme.styled("All systems go", "success"))
custom_theme.print("Caution: high temperature", "warning")

# Retrieve as a reusable Style
brand_style = custom_theme.get_style("brand")
brand_style.print("Welcome to Acme CLI")

# Extend with additional roles
extended_theme = custom_theme.extend(
    accent=Style(color256=214, style="italic")
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

## Terminal Capability & Fallback Functions

Introduced in **v0.4.0**, these functions provide direct query access to terminal color capabilities and color model conversion utilities.

### `supports_color(stream=None)`
Determines if basic color (standard 8/16-color ANSI) is supported for the given stream.
- **`stream`** (`TextIO`, optional): Destination stream to check. Defaults to `sys.stdout`.
- **Returns:** `bool` — `True` if colors are supported; `False` otherwise.

### `supports_256color(stream=None)`
Determines if 256-color ANSI palette is supported for the given stream.
- Checks TTY status, `FORCE_COLOR >= 2`, `COLORTERM`, `TERM` matching `256color`, modern terminal emulators, and Windows VT console.
- **`stream`** (`TextIO`, optional): Destination stream to check. Defaults to `sys.stdout`.
- **Returns:** `bool` — `True` if 256-color is supported; `False` otherwise.

### `supports_truecolor(stream=None)`
Determines if 24-bit True Color (RGB) is supported for the given stream.
- Checks TTY status, `FORCE_COLOR >= 3`, `COLORTERM` (`truecolor`, `24bit`), known True Color terminals, and Windows 10 build >= 14931.
- **`stream`** (`TextIO`, optional): Destination stream to check. Defaults to `sys.stdout`.
- **Returns:** `bool` — `True` if 24-bit True Color is supported; `False` otherwise.

### `rgb_to_ansi(rgb)`
Converts an RGB tuple `(r, g, b)` to the closest standard named ANSI color name based on Euclidean distance in RGB color space.
- **`rgb`** (`tuple[int, int, int]`): 3-tuple of integers between 0 and 255.
- **Returns:** `str` — Named color string (`"black"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, `"white"`).

### `rgb_to_256(rgb)`
Converts an RGB tuple `(r, g, b)` to the nearest ANSI 256-color index (0-255).
- **`rgb`** (`tuple[int, int, int]`): 3-tuple of integers between 0 and 255.
- **Returns:** `int` — ANSI 256-color code index.

### `color256_to_ansi(code)`
Converts an ANSI 256-color index (0-255) to the nearest standard named ANSI color name.
- **`code`** (`int`): 256-color code integer between 0 and 255.
- **Returns:** `str` — Named color string.

**Example:**
```python
from termtint import (
    supports_color,
    supports_256color,
    supports_truecolor,
    rgb_to_ansi,
    rgb_to_256,
    color256_to_ansi,
)

if supports_truecolor():
    print("Full 24-bit True Color is supported!")

print(rgb_to_ansi((255, 0, 0)))    # -> "red"
print(rgb_to_256((255, 0, 0)))     # -> 196
print(color256_to_ansi(196))       # -> "red"
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
