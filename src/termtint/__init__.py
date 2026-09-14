"""TermTint: A lightweight Python library for simple colored terminal output."""

from termtint.core import (
    colored,
    disable_color,
    enable_color,
    is_color_enabled,
    print_256,
    print_black,
    print_blue,
    print_cyan,
    print_green,
    print_magenta,
    print_red,
    print_rgb,
    print_white,
    print_yellow,
    reset_color_state,
    styled,
)
from termtint.theme import (
    DEFAULT_THEME,
    Theme,
    get_theme,
    reset_theme,
    set_theme,
)

__version__ = "0.3.0"

__all__ = [
    "colored",
    "styled",
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
    "print_rgb",
    "print_256",
    "Theme",
    "DEFAULT_THEME",
    "get_theme",
    "set_theme",
    "reset_theme",
    "__version__",
]
