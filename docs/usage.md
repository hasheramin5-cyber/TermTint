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

## Handling Environment and Redirected Output

TermTint automatically detects when your script output is redirected to a file or piped to another program:

```bash
# Colors are automatically disabled when output is redirected
python my_script.py > log.txt
```

Inside `log.txt`, the text will be clean and free from raw ANSI control sequences like `\033[31m`.

### NO_COLOR Compliance

If the `NO_COLOR` environment variable is set (any non-empty value), TermTint respects standard behavior and disables color output automatically:

```bash
NO_COLOR=1 python my_script.py
```

### Overriding Automatic Detection

If you explicitly want colors regardless of TTY state, or if you want to turn off colors programmatically:

```python
from termtint import enable_color, disable_color, colored

# Force color application
enable_color()
print(colored("Forced color text", "magenta"))

# Disable all color output
disable_color()
print(colored("Plain text output", "magenta"))
```
