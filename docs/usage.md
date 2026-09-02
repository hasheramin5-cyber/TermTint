# TermTint Usage Guide

This guide provides real-world examples and recipes for incorporating **TermTint** into CLI tools, scripts, and Python applications.

---

## Basic Formatting

To format text, pass string content and a supported color to `colored()`:

```python
from termtint import colored

# Basic colors
print(colored("Success!", "green"))
print(colored("Warning!", "yellow"))
print(colored("Error!", "red"))
print(colored("Info:", "cyan"))
```

---

## Adding Styles

Styles enhance visual hierarchy in CLI outputs:

```python
from termtint import colored

# Bright / Bold
print(colored("CRITICAL ERROR", "red", style="bright"))

# Dim / De-emphasized
print(colored("Debug log line 42...", "white", style="dim"))

# Underline
print(colored("https://example.com/docs", "blue", style="underline"))
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
