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
    "dim": "2",
    "underline": "4",
}

RESET_CODE: str = "\033[0m"


def colored(
    text: Any,
    color: str,
    style: Optional[str] = None,
    stream: Optional[TextIO] = None,
) -> str:
    """Format text with ANSI escape codes for specified color and optional style.

    Args:
        text: Any object to be converted to a string and styled.
        color: Name of the foreground color (black, red, green, yellow, etc.).
        style: Optional style (normal, bright, dim, underline).
        stream: Optional destination stream for color capability detection.

    Returns:
        str: ANSI formatted string when color is enabled, plain text otherwise.

    Raises:
        ValueError: If an unsupported color or style is specified.
    """
    color_lower = str(color).lower()
    if color_lower not in COLORS:
        valid_colors = ", ".join(sorted(COLORS.keys()))
        raise ValueError(
            f"Invalid color '{color}'. Supported colors are: {valid_colors}"
        )

    if style is not None:
        style_lower = str(style).lower()
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

    color_code = COLORS[color_lower]
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
    output = colored(text, color, style=style, stream=target)
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
