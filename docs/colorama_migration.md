# Migrating from Colorama to TermTint

This guide provides practical side-by-side examples and migration patterns for transitioning from **Colorama** to **TermTint**.

---

## Why Switch to TermTint?

| Feature | Colorama | TermTint |
| :--- | :--- | :--- |
| **Runtime Dependencies** | External package | **Zero** (standard library only) |
| **Approach** | Module constants & string concatenation | Functional string formatting & helpers |
| **Stream Wrapping** | Modifies/wraps global `sys.stdout`/`sys.stderr` | Non-intrusive (pure string formatting) |
| **Stream Awareness** | Requires custom wrapping or strip configuration | Automatic per-stream TTY detection |
| **Color Support** | 8 basic colors + bright variants | Named, 24-bit True Color (RGB), and 256-color ANSI |
| **Multiple Styles** | Manual constant concatenation | Sequence or comma-delimited: `["bold", "underline"]` |
| **Theme System** | None | Built-in role-based `Theme` support |
| **Windows Support** | Legacy Win32 console emulation | Native Windows 10/11 Virtual Terminal processing |
| **NO_COLOR Standard** | No native support | Fully supported in automatic mode |

---

## Core Migration Patterns

### 1. Basic Colored Text

**Colorama:**
```python
from colorama import Fore, Style, init

init()
print(Fore.GREEN + "Operation succeeded!" + Style.RESET_ALL)
print(Fore.RED + "Error encountered" + Style.RESET_ALL)
```

**TermTint:**
```python
from termtint import colored, print_green, print_red

# Self-contained formatted strings (no trailing resets needed)
print(colored("Operation succeeded!", "green"))

# Or direct convenience print helpers
print_green("Operation succeeded!")
print_red("Error encountered")
```

### 2. Styling (Bold, Dim, Underline, etc.)

**Colorama:**
```python
from colorama import Fore, Style

print(Fore.YELLOW + Style.BRIGHT + "Warning!" + Style.RESET_ALL)
print(Style.DIM + "Debug line" + Style.RESET_ALL)
```

**TermTint:**
```python
from termtint import colored, styled

# Using colored()
print(colored("Warning!", "yellow", style="bold"))

# Using styled()
print(styled("Warning!", color="yellow", style="bold"))
print(styled("Debug line", style="dim"))
```

### 3. Combining Multiple Styles

**Colorama:**
```python
# Colorama requires manually concatenating constants
print(Fore.CYAN + Style.BRIGHT + "\033[4m" + "Important Link" + Style.RESET_ALL)
```

**TermTint:**
```python
from termtint import styled

# Pass a list, tuple, or comma-separated string
print(styled("Important Link", color="cyan", style=["bold", "underline"]))
print(styled("Alert", color="red", style=("bold", "reverse")))
print(styled("Notice", color="yellow", style="bold, italic"))
```

### 4. Initialization & Windows Setup

**Colorama:**
```python
import colorama

# Required on Windows to wrap streams
colorama.init(autoreset=True)
```

**TermTint:**
```python
# No initialization needed!
# Windows 10/11 Virtual Terminal processing is handled automatically on first use.
from termtint import print_green

print_green("Works immediately out of the box")
```

### 5. File Redirection & Non-TTY Streams

**Colorama:**
When redirecting output (`python script.py > output.txt`), Colorama requires configuring `strip` flags during `init()`, or ANSI escape codes may leak into text files.

**TermTint:**
TermTint automatically inspects destination streams. If output is redirected to a file or pipe, ANSI codes are omitted automatically:
```bash
python script.py > output.txt  # Clean plain text, zero ANSI escape sequences
```

Inside Python scripts:
```python
from termtint import print_green

with open("output.log", "w") as f:
    print_green("System healthy", file=f)  # Automatically plain text
```

### 6. Role-Based Theming

Colorama has no concept of semantic themes. TermTint provides first-class, lightweight themes:

**TermTint:**
```python
from termtint import Theme, get_theme, styled

# Use built-in semantic roles
print(styled("Build passed", theme="success"))
print(styled("Test failed", theme="error"))
print(styled("Review deprecations", theme="warning"))

# Or create a custom corporate/CLI theme
cli_theme = Theme({
    "success": {"color": "green", "style": "bold"},
    "brand": {"rgb": (0, 150, 255), "style": "bold"},
    "muted": {"style": "dim"},
})

cli_theme.print("Connected to cloud", "brand")
cli_theme.print("All synced", "success")
```

---

## API Equivalent Cheat Sheet

| Colorama | TermTint Equivalent |
| :--- | :--- |
| `init()` | *(Not needed; automated)* |
| `deinit()` / `reinit()` | `reset_color_state()` |
| `Fore.RED` | `colored(text, "red")` or `styled(text, "red")` |
| `Fore.GREEN` | `colored(text, "green")` or `styled(text, "green")` |
| `Fore.YELLOW` | `colored(text, "yellow")` or `styled(text, "yellow")` |
| `Fore.BLUE` | `colored(text, "blue")` or `styled(text, "blue")` |
| `Fore.MAGENTA` | `colored(text, "magenta")` or `styled(text, "magenta")` |
| `Fore.CYAN` | `colored(text, "cyan")` or `styled(text, "cyan")` |
| `Fore.WHITE` | `colored(text, "white")` or `styled(text, "white")` |
| `Fore.BLACK` | `colored(text, "black")` or `styled(text, "black")` |
| `Fore.RESET` | *(Automatic trailing reset in all functions)* |
| `Style.BRIGHT` | `style="bold"` or `style="bright"` |
| `Style.DIM` | `style="dim"` |
| `Style.NORMAL` | `style="normal"` |
| `Style.RESET_ALL` | *(Automatic trailing reset in all functions)* |
| *(None)* | `style="italic"` |
| *(None)* | `style="underline"` |
| *(None)* | `style="reverse"` |
| *(None)* | `style="strikethrough"` |
| *(None)* | `rgb=(r, g, b)` (24-bit True Color) |
| *(None)* | `color256=n` (256-color ANSI) |
| *(None)* | `Theme` and semantic role styling |
