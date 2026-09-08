# TermTint Usage Guide

This guide provides real-world examples and recipes for incorporating **TermTint** into CLI tools, scripts, and Python applications.

---

## Basic Formatting

### Standard Named Colors
To format text, pass string content and a supported color to `colored()`:

```python
from termtint import colored

# Basic colors
print(colored("Success!", "green"))
print(colored("Warning!", "yellow"))
print(colored("Error!", "red"))
print(colored("Info:", "cyan"))
```

### True Color (RGB)
For 24-bit True Color, supply an `(r, g, b)` tuple with values from 0 to 255 to `rgb=`:

```python
from termtint import colored

print(colored("Custom coral", rgb=(255, 127, 80)))
print(colored("Deep sea blue", rgb=(0, 105, 148)))
```

### 256-Color ANSI
For 8-bit ANSI extended colors, pass an integer from 0 to 255 to `color256=`:

```python
from termtint import colored

print(colored("Bright orange", color256=208))
print(colored("Vibrant purple", color256=141))
```

---

## Adding Styles

Styles enhance visual hierarchy in CLI outputs:

```python
from termtint import colored

# Bold / Bright
print(colored("CRITICAL ERROR", "red", style="bold"))

# Dim / De-emphasized
print(colored("Debug log line 42...", "white", style="dim"))

# Italic
print(colored("Note: see documentation below", "cyan", style="italic"))

# Underline
print(colored("https://example.com/docs", "blue", style="underline"))

# Reverse / Inverted
print(colored(" STATUS: ACTIVE ", "yellow", style="reverse"))

# Strikethrough
print(colored("Deprecated v0.1 syntax", "white", style="strikethrough"))
```

Styles combine seamlessly with RGB and 256-color options:

```python
print(colored("Bold truecolor", rgb=(255, 69, 0), style="bold"))
print(colored("Underlined 256", color256=45, style="underline"))
```

---

## Convenience Functions

Convenience functions allow direct printing without explicitly calling `print(colored(...))`:

```python
from termtint import print_green, print_yellow, print_red

print_green("Deployment complete!")
print_yellow("Memory usage above 85%")
print_red("Database connection lost!", style="bright")
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

You can also pass a destination `file` parameter directly to convenience functions:

```python
from termtint import print_green

with open("output.txt", "w") as f:
    print_green("Hello file", file=f)  # Automatically outputs plain text without ANSI codes
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
from termtint import enable_color, disable_color, colored

# Explicitly force colors ON (overrides automatic detection and NO_COLOR)
enable_color()
print(colored("Forced color text", "magenta"))

# Explicitly force colors OFF
disable_color()
print(colored("Plain text output", "magenta"))
```
