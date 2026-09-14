"""Core text coloring and styling implementation for TermTint."""

import sys
from collections.abc import Sequence
from typing import Any, Optional, TextIO, Union

from termtint._detect import (
    ColorState,
    set_color_state,
    should_color,
)
from termtint._detect import (
    reset_color_state as _reset_state,
)

COLORS: dict[str, str] = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
}

STYLES: dict[str, str] = {
    "normal": "0",
    "bright": "1",
    "bold": "1",
    "dim": "2",
    "italic": "3",
    "underline": "4",
    "reverse": "7",
    "strikethrough": "9",
}

RESET_CODE: str = "\033[0m"


def _validate_rgb(rgb: Any) -> str:
    """Validate RGB tuple and return ANSI SGR color code string.

    Args:
        rgb: Sequence of 3 integer components (0-255).

    Returns:
        str: SGR parameter string '38;2;R;G;B'.

    Raises:
        TypeError: If rgb or any component is not an integer or is a boolean.
        ValueError: If rgb does not have 3 items or values are out of 0-255 range.
    """
    if isinstance(rgb, (bool, bytes, str)):
        raise TypeError(
            f"RGB must be a tuple or list of 3 integers, got {type(rgb).__name__}."
        )
    try:
        rgb_list = list(rgb)
    except TypeError:
        raise TypeError(
            f"RGB must be a sequence of 3 integers, got {type(rgb).__name__}."
        )

    if len(rgb_list) != 3:
        raise ValueError(
            f"RGB must contain exactly 3 components (r, g, b), got {len(rgb_list)}."
        )

    for i, c in enumerate(rgb_list):
        if isinstance(c, bool) or not isinstance(c, int):
            tname = type(c).__name__
            raise TypeError(
                f"RGB component at index {i} must be an integer, got {tname} ({c!r})."
            )
        if not (0 <= c <= 255):
            raise ValueError(
                f"RGB component at index {i} must be between 0 and 255, got {c}."
            )

    r, g, b = rgb_list
    return f"38;2;{r};{g};{b}"


def _validate_color256(color256: Any) -> str:
    """Validate 256-color index and return ANSI SGR color code string.

    Args:
        color256: Integer color code (0-255).

    Returns:
        str: SGR parameter string '38;5;N'.

    Raises:
        TypeError: If color256 is not an integer or is a boolean.
        ValueError: If color256 is out of 0-255 range.
    """
    if isinstance(color256, bool) or not isinstance(color256, int):
        tname = type(color256).__name__
        raise TypeError(
            f"color256 must be an integer, got {tname} ({color256!r})."
        )
    if not (0 <= color256 <= 255):
        raise ValueError(
            f"color256 must be between 0 and 255, got {color256}."
        )

    return f"38;5;{color256}"


def _normalize_styles(style: Any) -> list[str]:
    """Normalize and validate style input into a list of ANSI style codes.

    Args:
        style: Single style string, comma-separated string, or sequence of styles.

    Returns:
        list[str]: Unique ANSI style code strings.

    Raises:
        TypeError: If style or any element is not a string or is a boolean.
        ValueError: If any style name is unrecognized.
    """
    if style is None:
        return []

    if isinstance(style, bool):
        raise TypeError("Style must be a string or sequence of strings, got bool.")

    style_names: list[str] = []
    if isinstance(style, str):
        if "," in style:
            style_names = [s.strip() for s in style.split(",") if s.strip()]
        else:
            style_names = [style.strip()]
    elif isinstance(style, (list, tuple, set)):
        for item in style:
            if isinstance(item, bool) or not isinstance(item, str):
                tname = type(item).__name__
                raise TypeError(
                    f"Style element must be a string, got {tname} ({item!r})."
                )
            if "," in item:
                style_names.extend(
                    s.strip() for s in item.split(",") if s.strip()
                )
            else:
                style_names.append(item.strip())
    else:
        tname = type(style).__name__
        raise TypeError(
            f"Style must be a string or sequence of strings, got {tname}."
        )

    codes: list[str] = []
    valid_styles = ", ".join(sorted(STYLES.keys()))
    for name in style_names:
        name_lower = name.lower()
        if name_lower not in STYLES:
            raise ValueError(
                f"Invalid style '{name}'. Supported styles are: {valid_styles}"
            )
        code = STYLES[name_lower]
        if code not in codes:
            codes.append(code)

    if len(codes) > 1 and "0" in codes:
        codes.remove("0")

    return codes


def _render_ansi(
    text: Any,
    color_code: Optional[str] = None,
    style_codes: Optional[list[str]] = None,
    stream: Optional[TextIO] = None,
) -> str:
    """Render text with ANSI escape codes for color and styles.

    Args:
        text: Content to render.
        color_code: Optional ANSI color code string (e.g. '31', '38;2;R;G;B').
        style_codes: Optional list of ANSI style code strings.
        stream: Optional destination stream for color capability detection.

    Returns:
        str: ANSI formatted string when color is enabled, plain text otherwise.
    """
    text_str = str(text)

    active_styles = (
        [c for c in (style_codes or []) if c != "0"]
        if color_code
        else (style_codes or [])
    )

    if not color_code and not active_styles:
        return text_str

    if not should_color(stream=stream):
        return text_str

    codes: list[str] = []
    if active_styles:
        codes.extend(active_styles)
    if color_code:
        codes.append(color_code)

    prefix = f"\033[{';'.join(codes)}m"
    return f"{prefix}{text_str}{RESET_CODE}"


def colored(
    text: Any,
    color: Optional[str] = None,
    style: Optional[str] = None,
    rgb: Optional[tuple[int, int, int]] = None,
    color256: Optional[int] = None,
    stream: Optional[TextIO] = None,
) -> str:
    """Format text with ANSI escape codes for specified color and optional style.

    Supports named colors, 24-bit True Color (RGB), and 256-color ANSI.

    Args:
        text: Any object to be converted to a string and styled.
        color: Name of the foreground color (black, red, green, yellow, etc.).
        style: Optional style (normal, bold, bright, dim, italic, underline, etc.).
        rgb: Optional tuple/list of 3 integers (r, g, b) between 0 and 255.
        color256: Optional integer color code between 0 and 255.
        stream: Optional destination stream for color capability detection.

    Returns:
        str: ANSI formatted string when color is enabled, plain text otherwise.

    Raises:
        ValueError: If invalid color/style or conflicting color options are specified.
        TypeError: If invalid types are supplied for color, rgb, or color256.
    """
    color_specs = sum(x is not None for x in (color, rgb, color256))
    if color_specs == 0:
        raise ValueError(
            "A color must be specified using 'color', 'rgb', or 'color256'."
        )
    if color_specs > 1:
        raise ValueError(
            "Only one of 'color', 'rgb', or 'color256' may be specified."
        )

    if color is not None:
        if isinstance(color, bool) or not isinstance(color, str):
            raise TypeError(
                f"Named color must be a string, got {type(color).__name__}."
            )
        color_lower = color.lower()
        if color_lower not in COLORS:
            valid_colors = ", ".join(sorted(COLORS.keys()))
            raise ValueError(
                f"Invalid color '{color}'. Supported colors are: {valid_colors}"
            )
        color_code = COLORS[color_lower]
    elif rgb is not None:
        color_code = _validate_rgb(rgb)
    else:
        color_code = _validate_color256(color256)

    if style is not None:
        if isinstance(style, bool) or not isinstance(style, str):
            raise TypeError(
                f"Style must be a string, got {type(style).__name__}."
            )
        style_lower = style.lower()
        if style_lower not in STYLES:
            valid_styles = ", ".join(sorted(STYLES.keys()))
            raise ValueError(
                f"Invalid style '{style}'. Supported styles are: {valid_styles}"
            )
        style_codes = [STYLES[style_lower]]
    else:
        style_codes = ["0"]

    return _render_ansi(
        text, color_code=color_code, style_codes=style_codes, stream=stream
    )


def styled(
    text: Any,
    color: Optional[str] = None,
    style: Optional[Union[str, Sequence[str]]] = None,
    rgb: Optional[tuple[int, int, int]] = None,
    color256: Optional[int] = None,
    theme: Optional[str] = None,
    stream: Optional[TextIO] = None,
) -> str:
    """Format text with ANSI escape codes for colors, styles, and themes.

    Supports pure styles, named colors, RGB, 256-color, multiple styles, and themes.

    Args:
        text: Any object to be converted to a string and styled.
        color: Optional name of the foreground color (black, red, green, etc.).
        style: Optional style or sequence of styles (bold, italic, underline, etc.).
        rgb: Optional sequence of 3 integers (r, g, b) between 0 and 255.
        color256: Optional integer color code between 0 and 255.
        theme: Optional theme role name (e.g. 'success', 'error', 'warning', 'info').
        stream: Optional destination stream for color capability detection.

    Returns:
        str: Formatted ANSI string when color is enabled, plain text otherwise.

    Raises:
        ValueError: If conflicting options or invalid color/style values are specified.
        TypeError: If invalid types are supplied.
        KeyError: If an unknown theme role is specified.
    """
    if theme is not None:
        if isinstance(theme, bool) or not isinstance(theme, str):
            tname = type(theme).__name__
            raise TypeError(f"Theme role must be a string, got {tname}.")
        if any(x is not None for x in (color, rgb, color256)):
            raise ValueError(
                "Cannot specify 'theme' together with 'color', 'rgb', or 'color256'."
            )
        from termtint.theme import get_theme

        active_theme = get_theme()
        role_def = active_theme.get_role(theme)

        color_code: Optional[str] = None
        if "color" in role_def:
            color_code = COLORS[role_def["color"]]
        elif "rgb" in role_def:
            color_code = _validate_rgb(role_def["rgb"])
        elif "color256" in role_def:
            color_code = _validate_color256(role_def["color256"])

        all_styles: list[Any] = []
        if "style" in role_def:
            role_style = role_def["style"]
            if isinstance(role_style, (list, tuple, set)):
                all_styles.extend(role_style)
            else:
                all_styles.append(role_style)
        if style is not None:
            if isinstance(style, (list, tuple, set)):
                all_styles.extend(style)
            else:
                all_styles.append(style)

        style_codes = _normalize_styles(all_styles) if all_styles else []
        return _render_ansi(
            text, color_code=color_code, style_codes=style_codes, stream=stream
        )

    color_specs = sum(x is not None for x in (color, rgb, color256))
    if color_specs > 1:
        raise ValueError(
            "Only one of 'color', 'rgb', or 'color256' may be specified."
        )

    color_code = None
    if color is not None:
        if isinstance(color, bool) or not isinstance(color, str):
            tname = type(color).__name__
            raise TypeError(f"Named color must be a string, got {tname}.")
        color_lower = color.lower()
        if color_lower not in COLORS:
            valid_colors = ", ".join(sorted(COLORS.keys()))
            raise ValueError(
                f"Invalid color '{color}'. Supported colors are: {valid_colors}"
            )
        color_code = COLORS[color_lower]
    elif rgb is not None:
        color_code = _validate_rgb(rgb)
    elif color256 is not None:
        color_code = _validate_color256(color256)

    style_codes = _normalize_styles(style)
    return _render_ansi(
        text, color_code=color_code, style_codes=style_codes, stream=stream
    )


def enable_color() -> None:
    """Explicitly enable colored output."""
    set_color_state(ColorState.ENABLED)


def disable_color() -> None:
    """Explicitly disable colored output."""
    set_color_state(ColorState.DISABLED)


def is_color_enabled(stream: Optional[TextIO] = None) -> bool:
    """Check whether colored output is currently enabled.

    Args:
        stream: Optional file stream to inspect for color support.

    Returns:
        bool: True if color output is enabled, False otherwise.
    """
    return should_color(stream=stream)


def reset_color_state() -> None:
    """Reset color detection to automatic terminal capability detection."""
    _reset_state()


def _print_color(
    color: str,
    *values: Any,
    style: Optional[str] = None,
    sep: str = " ",
    end: str = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Internal helper to print colored values."""
    target = file if file is not None else sys.stdout
    text = sep.join(str(v) for v in values)
    output = colored(text, color=color, style=style, stream=target)
    print(output, end=end, file=target, flush=flush)


def print_rgb(
    rgb: tuple[int, int, int],
    *values: Any,
    style: Optional[str] = None,
    sep: str = " ",
    end: str = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print text formatted with 24-bit True Color (RGB).

    Args:
        rgb: Sequence of 3 integers (r, g, b) between 0 and 255.
        *values: Values to be printed.
        style: Optional text style (normal, bold, bright, dim, italic, etc.).
        sep: String inserted between values, default a space.
        end: String appended after the last value, default a newline.
        file: A file-like object (stream); defaults to sys.stdout.
        flush: Whether to forcibly flush the stream.
    """
    target = file if file is not None else sys.stdout
    text = sep.join(str(v) for v in values)
    output = colored(text, rgb=rgb, style=style, stream=target)
    print(output, end=end, file=target, flush=flush)


def print_256(
    color256: int,
    *values: Any,
    style: Optional[str] = None,
    sep: str = " ",
    end: str = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print text formatted with 256-color ANSI code.

    Args:
        color256: Integer color code between 0 and 255.
        *values: Values to be printed.
        style: Optional text style (normal, bold, bright, dim, italic, etc.).
        sep: String inserted between values, default a space.
        end: String appended after the last value, default a newline.
        file: A file-like object (stream); defaults to sys.stdout.
        flush: Whether to forcibly flush the stream.
    """
    target = file if file is not None else sys.stdout
    text = sep.join(str(v) for v in values)
    output = colored(text, color256=color256, style=style, stream=target)
    print(output, end=end, file=target, flush=flush)


def print_black(
    *values: Any,
    style: Optional[str] = None,
    sep: str = " ",
    end: str = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print text formatted in black."""
    _print_color(
        "black", *values, style=style, sep=sep, end=end, file=file, flush=flush
    )


def print_red(
    *values: Any,
    style: Optional[str] = None,
    sep: str = " ",
    end: str = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print text formatted in red."""
    _print_color(
        "red", *values, style=style, sep=sep, end=end, file=file, flush=flush
    )


def print_green(
    *values: Any,
    style: Optional[str] = None,
    sep: str = " ",
    end: str = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print text formatted in green."""
    _print_color(
        "green", *values, style=style, sep=sep, end=end, file=file, flush=flush
    )


def print_yellow(
    *values: Any,
    style: Optional[str] = None,
    sep: str = " ",
    end: str = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print text formatted in yellow."""
    _print_color(
        "yellow", *values, style=style, sep=sep, end=end, file=file, flush=flush
    )


def print_blue(
    *values: Any,
    style: Optional[str] = None,
    sep: str = " ",
    end: str = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print text formatted in blue."""
    _print_color(
        "blue", *values, style=style, sep=sep, end=end, file=file, flush=flush
    )


def print_magenta(
    *values: Any,
    style: Optional[str] = None,
    sep: str = " ",
    end: str = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print text formatted in magenta."""
    _print_color(
        "magenta", *values, style=style, sep=sep, end=end, file=file, flush=flush
    )


def print_cyan(
    *values: Any,
    style: Optional[str] = None,
    sep: str = " ",
    end: str = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print text formatted in cyan."""
    _print_color(
        "cyan", *values, style=style, sep=sep, end=end, file=file, flush=flush
    )


def print_white(
    *values: Any,
    style: Optional[str] = None,
    sep: str = " ",
    end: str = "\n",
    file: Optional[TextIO] = None,
    flush: bool = False,
) -> None:
    """Print text formatted in white."""
    _print_color(
        "white", *values, style=style, sep=sep, end=end, file=file, flush=flush
    )
