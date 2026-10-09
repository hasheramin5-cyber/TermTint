"""TermTint: A lightweight Python library for simple colored terminal output."""

from termtint._detect import (
    supports_256color,
    supports_color,
    supports_truecolor,
)
from termtint.core import (
    color256_to_ansi,
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
    rgb_to_256,
    rgb_to_ansi,
    styled,
)
from termtint.style import Style
from termtint.theme import (
    DEFAULT_THEME,
    Theme,
    get_theme,
    reset_theme,
    set_theme,
)

__version__ = "0.4.0"

__all__ = [
    "colored",
    "styled",
    "Style",
    "enable_color",
    "disable_color",
    "is_color_enabled",
    "reset_color_state",
    "supports_color",
    "supports_256color",
    "supports_truecolor",
    "rgb_to_ansi",
    "rgb_to_256",
    "color256_to_ansi",
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
