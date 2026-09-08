"""Core text coloring and styling implementation for TermTint."""

import sys
from typing import Any, Optional, TextIO

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
    else:
        style_lower = "normal"

    text_str = str(text)

    if not should_color(stream=stream):
        return text_str

    if style_lower != "normal":
        style_code = STYLES[style_lower]
        prefix = f"\033[{style_code};{color_code}m"
    else:
        prefix = f"\033[{color_code}m"

    return f"{prefix}{text_str}{RESET_CODE}"


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
