# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.5.0] - 2026-11-03

### Added
- **Background Color Support**: Full background color rendering across all public APIs:
  - Standard named background colors (`bg="blue"`, supporting 8 ANSI colors: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`).
  - 24-bit True Color backgrounds (`bg_rgb=(r, g, b)`).
  - 256-color ANSI backgrounds (`bg_color256=n`).
  - Integration with `colored()`, `styled()`, `Style`, `Theme`, and all convenience `print_*()` functions.
- **Background Color Fallback**: Automatic graceful background color degradation when `fallback=True`:
  - 24-bit True Color backgrounds degrade to ANSI 256-color or standard ANSI 16-color on limited terminals.
  - 256-color backgrounds degrade to nearest ANSI 16-color standard background.
  - Consistent color distance matching with foreground color fallback.
- **Fluent Style Chaining for Backgrounds**: Added `.with_bg()`, `.with_bg_rgb()`, and `.with_bg_color256()` to the `Style` class.
- **Theme Background Support**: Allowed `bg`, `bg_rgb`, and `bg_color256` in `Theme` role definitions, `Theme.styled()`, and `Theme.get_style()`.
- **ANSI Utility Functions**:
  - `strip_ansi(text)`: Strips all ANSI SGR escape codes and OSC hyperlinks, returning clean unformatted text.
  - `visible_len(text)`: Measures displayed terminal character width by discounting ANSI escape bytes, enabling table column and border alignment.
- Comprehensive test suites in `tests/test_background.py` and `tests/test_utilities.py`.

### Changed
- Updated `Style.__add__()` to properly merge and override theme and background definitions.
- Updated `README.md`, `docs/api.md`, `docs/usage.md`, and `docs/architecture.md` with complete documentation and recipes.

---

## [0.4.0] - 2026-10-25

### Added
- **Reusable `Style` Class**: Immutable styling definitions with fluent chaining methods (`.bold()`, `.italic()`, `.underline()`, `.reverse()`, `.strikethrough()`, `.dim()`, `.with_*()`), direct call execution `style("text")`, and operator composition (`+`).
- **Terminal Capability Detection**: Stream-aware capability query functions:
  - `supports_color(stream=None)`
  - `supports_256color(stream=None)`
  - `supports_truecolor(stream=None)`
- **Intelligent Color Fallback**: Automatic degradation of True Color and 256-color to supported terminal palettes via `fallback=True`.
- **Color Conversion Utilities**: `rgb_to_ansi()`, `rgb_to_256()`, and `color256_to_ansi()`.
- **Theme Integration**: `Theme` roles now accept `Style` instances, and `Theme.get_style()` returns reusable `Style` objects.

---

## [0.3.0] - 2026-09-14

### Added
- **Fluent Styling (`styled`)**: Formats text with single or multiple styles as strings, lists, or tuples.
- **Semantic Theme System**:
  - `Theme` class for role-based terminal styling.
  - Pre-configured `DEFAULT_THEME` with `"success"`, `"error"`, `"warning"`, `"info"`, `"muted"`, and `"brand"`.
  - Global theme state functions: `get_theme()`, `set_theme()`, and `reset_theme()`.

---

## [0.2.0] - 2026-08-01

### Added
- 24-bit True Color (`rgb=(r, g, b)`) support in `colored()`.
- 256-color ANSI (`color256=n`) support in `colored()`.
- Convenience print helpers: `print_rgb()` and `print_256()`.

---

## [0.1.0] - 2026-07-01

### Added
- Initial release of TermTint.
- 8 standard terminal foreground colors (`black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`).
- 8 text styles (`normal`, `bold`, `bright`, `dim`, `italic`, `underline`, `reverse`, `strikethrough`).
- Core formatting functions: `colored()`.
- Direct convenience functions: `print_black()`, `print_red()`, `print_green()`, `print_yellow()`, `print_blue()`, `print_magenta()`, `print_cyan()`, `print_white()`.
- Stream-aware output avoiding ANSI codes when redirected.
- `NO_COLOR` standard and `FORCE_COLOR` support.
- Windows 10/11 native Virtual Terminal processing via standard library `ctypes`.
- Explicit state control: `enable_color()`, `disable_color()`, `is_color_enabled()`, and `reset_color_state()`.
