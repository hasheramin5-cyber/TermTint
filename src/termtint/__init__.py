"""TermTint: A lightweight Python library for simple colored terminal output."""

from termtint.core import (
    colored,
    disable_color,
    enable_color,
    is_color_enabled,
    print_black,
    print_blue,
    print_cyan,
    print_green,
    print_magenta,
    print_red,
    print_white,
    print_yellow,
    reset_color_state,
)

__version__ = "0.1.0"

__all__ = [
    "colored",
    "enable_color",
    "disable_color",
    "is_color_enabled",
    "reset_color_state",
    "print_black",
    "print_red",
    "print_green",
    "print_yellow",
    "print_blue",
    "print_magenta",
    "print_cyan",
    "print_white",
    "__version__",
]
