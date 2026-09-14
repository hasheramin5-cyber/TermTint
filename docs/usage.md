# TermTint Usage Guide

This guide provides real-world examples and recipes for incorporating **TermTint** into CLI tools, scripts, and Python applications.

---

## Fluent Styling with `styled()`

The `styled()` function provides a flexible, unified interface for styling terminal text:

```python
from termtint import styled

# 1. Style without color
print(styled("Header", style="bold"))

# 2. Color and single style
print(styled("Warning!", color="yellow", style="bold"))

# 3. 24-bit True Color with style
print(styled("Accent", rgb=(255, 128, 0), style="italic"))

# 4. 256-color with multiple styles
print(styled("Badge", color256=198, style=["bold", "reverse"]))

# 5. Multiple styles using a tuple or comma-separated string
print(styled("Alert", color="red", style=("bold", "underline")))
print(styled("Notice", color="cyan", style="bold, italic"))

# 6. Plain text fallback (returns plain string if no style or color is given)
print(styled("Clean unstyled text"))
```

---

## Semantic Theme System

TermTint includes role-based theming, separating presentation logic from business code.

### 1. Built-in Roles via `styled()`

TermTint comes pre-configured with standard semantic roles:

```python
from termtint import styled

print(styled("Deployment succeeded", theme="success"))   # Green + Bold
print(styled("Critical disk error", theme="error"))     # Red + Bold
print(styled("Connection sluggish", theme="warning"))   # Yellow
print(styled("Checking status...", theme="info"))       # Cyan + Italic
print(styled("Timestamp: 12:00:00", theme="muted"))     # Dim
print(styled("Acme CLI v1.0", theme="brand"))           # RGB Blue + Bold
```

### 2. Custom Themes

Define domain-specific roles for your application using `Theme`:

```python
from termtint import Theme

# Define roles using color, rgb, color256, and style
app_theme = Theme({
    "success": {"color": "green", "style": "bold"},
    "danger": {"color": "red", "style": ["bold", "underline"]},
    "highlight": {"color256": 214, "style": "bold"},
    "brand": {"rgb": (120, 80, 255), "style": "bold"},
    "trace": {"style": "dim"},
})

# Format text with Theme.styled()
formatted = app_theme.styled("Operation OK", "success")
print(formatted)

# Print directly with Theme.print()
app_theme.print("System startup", "brand")
app_theme.print("Disk full", "danger")
```

### 3. Extending Themes

Create variations of existing themes without mutating the original:

```python
# Create an extended theme with additional roles
extended_theme = app_theme.extend(
    accent={"color": "magenta", "style": "italic"},
    danger={"color": "red", "style": ["bold", "reverse"]}  # Overrides danger
)

extended_theme.print("Special announcement", "accent")
```

### 4. Global Theme State

Set a theme application-wide so that `styled(..., theme="role")` automatically uses it:

```python
from termtint import set_theme, get_theme, reset_theme, styled

# Activate custom theme globally
set_theme(app_theme)

# styled() will now resolve roles from app_theme
print(styled("Startup notice", theme="brand"))

# Reset back to DEFAULT_THEME
reset_theme()
```

---

## Classic Formatting with `colored()`

`colored()` remains fully supported and 100% backward compatible:

```python
from termtint import colored

# Basic colors
print(colored("Success!", "green"))
print(colored("Warning!", "yellow"))
print(colored("Error!", "red"))
print(colored("Info:", "cyan"))

# 24-bit True Color (RGB)
print(colored("Custom coral", rgb=(255, 127, 80)))
print(colored("Deep sea blue", rgb=(0, 105, 148)))

# 256-color ANSI
print(colored("Bright orange", color256=208))
print(colored("Vibrant purple", color256=141))
```

---

## Supported Styles Reference

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

Styles can be combined in `styled()` using a list, tuple, or comma-separated string:
```python
styled("Combined", color="green", style=["bold", "underline"])
```

---

## Convenience Functions

Convenience functions allow direct printing without explicitly calling `print(colored(...))`:

```python
from termtint import print_green, print_yellow, print_red, print_rgb, print_256

print_green("Deployment complete!")
print_yellow("Memory usage above 85%")
print_red("Database connection lost!", style="bright")
print_rgb((255, 140, 0), "Battery level critical")
print_256(208, "Sensor calibration warning")
```

Multiple arguments and standard `print` options are fully supported:

```python
from termtint import print_cyan

print_cyan("Processing", "batch", 5, sep=" - ", end="...\n")
```

---

## Stream-Aware Output and Files

TermTint automatically avoids adding ANSI escape sequences when output is redirected to a file or piped to another program:

```bash
# ANSI escape sequences are avoided automatically when output is redirected
python my_script.py > log.txt
```

Inside `log.txt`, the text will be clean and free from raw ANSI control sequences like `\033[31m`.

You can also pass a destination `file` parameter directly:

```python
from termtint import print_green, styled

with open("output.txt", "w") as f:
    print_green("Hello file", file=f)  # Outputs clean plain text without ANSI
    f.write(styled("Logged event", color="blue", stream=f) + "\n")
```

---

## Environment Configuration

### NO_COLOR Compliance

TermTint respects `NO_COLOR` in automatic mode ([no-color.org](https://no-color.org)). When the `NO_COLOR` environment variable is set to any non-empty value, automatic color formatting is disabled:

```bash
NO_COLOR=1 python my_script.py
```

### Overriding Automatic Detection

If you explicitly want colors regardless of TTY state, or if you want to turn off colors programmatically, explicit function calls override automatic detection:

```python
from termtint import enable_color, disable_color, styled

# Explicitly force colors ON (overrides automatic detection and NO_COLOR)
enable_color()
print(styled("Forced color text", color="magenta"))

# Explicitly force colors OFF
disable_color()
print(styled("Plain text output", color="magenta"))
```
