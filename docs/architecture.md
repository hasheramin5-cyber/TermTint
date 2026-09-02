# TermTint Architecture

This document describes the design, internal component breakdown, and detection workflow of **TermTint**.

---

## Architectural Principles

1. **Zero Runtime Dependencies**: Uses exclusively Python standard library modules (`os`, `sys`, `ctypes`, `enum`, `typing`).
2. **Non-Intrusive**: Avoids wrapping or patching global streams (`sys.stdout` or `sys.stderr`).
3. **Pure String Formatting**: Converts text inputs into standard Python strings enriched with ANSI SGR codes.
4. **Predictable Fallback**: Evaluates TTY state, environment flags (`NO_COLOR`), and platform VT support to determine if color codes should be generated.

---

## Module Layout

```text
src/termtint/
├── __init__.py      # Clean public API exports
├── core.py          # Primary colored() & print_* implementations
├── _detect.py       # TTY, environment, and state capability detection
├── _windows.py      # Isolated Win32 Virtual Terminal enablement
└── py.typed         # PEP 561 type annotation marker
```

---

## Detection & Formatting Flow

```text
User Application Call
        │
        ▼
colored("text", "green")
        │
        ▼
Is Color Enabled? ──(should_color())──► Check State (ENABLED / DISABLED / AUTO)
        │                                        │
        ├── AUTO Mode:                            │
        │   ├── Check NO_COLOR env               │
        │   ├── Check FORCE_COLOR env            │
        │   ├── Check stream.isatty()            │
        │   ├── Check TERM == "dumb"             │
        │   └── Check Win32 VT Mode (_windows.py)│
        │                                        │
        ▼                                        ▼
 Color Disabled? ────────────────────────► Return plain text
        │
        ▼ (Yes)
Format ANSI SGR Sequence:
"\033[32m" + text + "\033[0m"
        │
        ▼
Return Styled String
```

---

## Module Responsibilities

### `core.py`
Defines ANSI lookup tables for foreground colors and styles. Exposes `colored()`, state toggles (`enable_color()`, `disable_color()`), and `print_*()` helper functions.

### `_detect.py`
Encapsulates environment inspection (`NO_COLOR`, `FORCE_COLOR`, `TERM`), TTY checks (`isatty()`), and state caching to minimize runtime overhead.

### `_windows.py`
Uses `ctypes` to call `kernel32.SetConsoleMode` with `ENABLE_VIRTUAL_TERMINAL_PROCESSING` (0x0004) on Windows 10/11 platforms. Safe against missing DLLs or execution errors.
