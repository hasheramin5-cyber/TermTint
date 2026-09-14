# TermTint Architecture

This document describes the design, internal component breakdown, and detection workflow of **TermTint**.

---

## Architectural Principles

1. **Zero Runtime Dependencies**: Uses exclusively Python standard library modules (`os`, `sys`, `ctypes`, `enum`, `typing`, `collections.abc`).
2. **Non-Intrusive**: Avoids wrapping or monkey-patching global streams (`sys.stdout` or `sys.stderr`).
3. **Pure String Formatting**: Converts text inputs into standard Python strings enriched with ANSI SGR codes when color is enabled.
4. **Shared Rendering Engine**: Both `colored()` and `styled()` share a unified ANSI renderer (`_render_ansi(...)`) ensuring consistent escaping and reset handling.
5. **Predictable Stream-Aware Fallback**: Evaluates target destination stream TTY state, environment flags (`NO_COLOR`), and platform VT support before generating color codes.

---

## Module Layout

```text
src/termtint/
├── __init__.py      # Clean public API exports
├── core.py          # Primary colored(), styled(), & print_* implementations
├── theme.py         # Theme class, role validation, & global theme registry
├── _detect.py       # TTY, environment, and state capability detection
├── _windows.py      # Isolated Win32 Virtual Terminal enablement
└── py.typed         # PEP 561 type annotation marker
```

---

## Detection & Formatting Flow

```text
User Application Call
        │
        ├── styled("Header", style=["bold", "underline"], theme="success", stream=...)
        │       │
        │       ▼ (Resolves role from active Theme, combines multi-styles)
        │
        └── colored("text", "green", stream=...)
                │
                ▼
      should_color(stream)? ────────► Check State (ENABLED / DISABLED / AUTO)
                │                                    │
                ├── AUTO Mode:                        │
                │   ├── Check NO_COLOR env           │
                │   ├── Check FORCE_COLOR env        │
                │   ├── Check target_stream.isatty() │
                │   ├── Check TERM == "dumb"         │
                │   └── Check Win32 VT (_windows.py) │
                │                                    │
                ▼                                    ▼
       Color Disabled? ──────────────────────► Return plain str(text)
                │
                ▼ (No)
       _render_ansi(text, codes)
       "\033[code1;code2m" + text + "\033[0m"
                │
                ▼
       Return Styled String
```

---

## Module Responsibilities

### `core.py`
- Defines ANSI lookup tables for foreground colors and styles.
- Implements `_normalize_styles()` to parse and validate single or multiple style specifications.
- Implements `_render_ansi()` as the shared ANSI escape sequence builder.
- Exposes `styled()`, `colored()`, state toggles (`enable_color()`, `disable_color()`, `reset_color_state()`), and `print_*()` helper functions.
- Resolves theme roles via `theme.py` when `theme=` is passed to `styled()`.

### `theme.py`
- Implements the immutable `Theme` class representing semantic roles.
- Validates role definitions against supported colors, True Color RGB tuples, 256-color codes, and styles.
- Provides `Theme.styled(...)`, `Theme.print(...)`, and non-mutating `Theme.extend(...)`.
- Maintains global theme state (`DEFAULT_THEME`, `get_theme()`, `set_theme()`, `reset_theme()`).

### `_detect.py`
- Encapsulates environment inspection (`NO_COLOR` in automatic mode, `FORCE_COLOR`, `TERM`).
- Performs target stream TTY checks (`isatty()`) and state caching to minimize runtime overhead.

### `_windows.py`
- Uses `ctypes` to call `kernel32.SetConsoleMode` with `ENABLE_VIRTUAL_TERMINAL_PROCESSING` (0x0004) on Windows 10/11 platforms.
- Safe against missing DLLs, execution errors, or non-Windows platforms.
