"""Reusable and composable Style object for TermTint."""

import sys
from collections.abc import Sequence
from typing import Any, Optional, TextIO, Union

from termtint._detect import supports_256color, supports_truecolor
from termtint.core import (
    BG_COLORS,
    COLORS,
    _normalize_styles,
    _render_ansi,
    _validate_bg_color256,
    _validate_bg_rgb,
    _validate_color256,
    _validate_rgb,
    color256_to_ansi,
    rgb_to_256,
    rgb_to_ansi,
)


class Style:
    """A reusable, immutable styling configuration for terminal output."""

    def __init__(
        self,
        color: Optional[str] = None,
        style: Optional[Union[str, Sequence[str]]] = None,
        rgb: Optional[tuple[int, int, int]] = None,
        color256: Optional[int] = None,
        theme: Optional[str] = None,
        fallback: bool = False,
        bg: Optional[str] = None,
        bg_rgb: Optional[tuple[int, int, int]] = None,
        bg_color256: Optional[int] = None,
    ) -> None:
        """Initialize a new Style instance.

        Args:
            color: Optional standard named foreground color.
            style: Optional style or sequence of styles.
            rgb: Optional 24-bit True Color tuple (r, g, b).
            color256: Optional 256-color ANSI code (0-255).
            theme: Optional semantic theme role name.
            fallback: Whether to downgrade True Color/256-color if unsupported.
            bg: Optional standard named background color.
            bg_rgb: Optional 24-bit True Color background tuple (r, g, b).
            bg_color256: Optional 256-color ANSI background code (0-255).

        Raises:
            ValueError: If conflicting options or invalid values are specified.
            TypeError: If arguments have invalid types.
        """
        if not isinstance(fallback, bool):
            raise TypeError(
                f"fallback must be a boolean, got {type(fallback).__name__}."
            )
        self._fallback = fallback

        if theme is not None:
            if isinstance(theme, bool) or not isinstance(theme, str):
                tname = type(theme).__name__
                raise TypeError(f"Theme role must be a string, got {tname}.")
            if any(
                x is not None
                for x in (color, rgb, color256, bg, bg_rgb, bg_color256)
            ):
                raise ValueError(
                    "Cannot specify 'theme' together with 'color', 'rgb', "
                    "'color256', 'bg', 'bg_rgb', or 'bg_color256'."
                )
            self._theme = theme
            self._color: Optional[str] = None
            self._rgb: Optional[tuple[int, int, int]] = None
            self._color256: Optional[int] = None
            self._bg: Optional[str] = None
            self._bg_rgb: Optional[tuple[int, int, int]] = None
            self._bg_color256: Optional[int] = None
        else:
            self._theme = None
            color_specs = sum(x is not None for x in (color, rgb, color256))
            if color_specs > 1:
                raise ValueError(
                    "Only one of 'color', 'rgb', or 'color256' may be specified."
                )

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
                self._color = color_lower
                self._rgb = None
                self._color256 = None
            elif rgb is not None:
                _validate_rgb(rgb)
                self._rgb = tuple(rgb)
                self._color = None
                self._color256 = None
            elif color256 is not None:
                _validate_color256(color256)
                self._color256 = color256
                self._color = None
                self._rgb = None
            else:
                self._color = None
                self._rgb = None
                self._color256 = None

            bg_specs = sum(x is not None for x in (bg, bg_rgb, bg_color256))
            if bg_specs > 1:
                raise ValueError(
                    "Only one of 'bg', 'bg_rgb', or 'bg_color256' may be specified."
                )

            if bg is not None:
                if isinstance(bg, bool) or not isinstance(bg, str):
                    tname = type(bg).__name__
                    raise TypeError(
                        f"Named background color must be a string, got {tname}."
                    )
                bg_lower = bg.lower()
                if bg_lower not in BG_COLORS:
                    valid_bgs = ", ".join(sorted(BG_COLORS.keys()))
                    raise ValueError(
                        f"Invalid background color '{bg}'. "
                        f"Supported background colors are: {valid_bgs}"
                    )
                self._bg = bg_lower
                self._bg_rgb = None
                self._bg_color256 = None
            elif bg_rgb is not None:
                _validate_bg_rgb(bg_rgb)
                self._bg_rgb = tuple(bg_rgb)
                self._bg = None
                self._bg_color256 = None
            elif bg_color256 is not None:
                _validate_bg_color256(bg_color256)
                self._bg_color256 = bg_color256
                self._bg = None
                self._bg_rgb = None
            else:
                self._bg = None
                self._bg_rgb = None
                self._bg_color256 = None

        if style is not None:
            _normalize_styles(style)
            if isinstance(style, str):
                if "," in style:
                    self._styles: tuple[str, ...] = tuple(
                        s.strip() for s in style.split(",") if s.strip()
                    )
                else:
                    self._styles = (style.strip(),)
            elif isinstance(style, (list, tuple, set)):
                items = []
                for item in style:
                    if "," in item:
                        items.extend(
                            s.strip() for s in item.split(",") if s.strip()
                        )
                    else:
                        items.append(item.strip())
                self._styles = tuple(items)
        else:
            self._styles = ()

    @property
    def color(self) -> Optional[str]:
        """Return the named color if configured."""
        return self._color

    @property
    def rgb(self) -> Optional[tuple[int, int, int]]:
        """Return the RGB tuple if configured."""
        return self._rgb

    @property
    def color256(self) -> Optional[int]:
        """Return the 256-color index if configured."""
        return self._color256

    @property
    def bg(self) -> Optional[str]:
        """Return the named background color if configured."""
        return self._bg

    @property
    def bg_rgb(self) -> Optional[tuple[int, int, int]]:
        """Return the background RGB tuple if configured."""
        return self._bg_rgb

    @property
    def bg_color256(self) -> Optional[int]:
        """Return the 256-color background index if configured."""
        return self._bg_color256

    @property
    def style(self) -> tuple[str, ...]:
        """Return the tuple of configured text styles."""
        return self._styles

    @property
    def theme(self) -> Optional[str]:
        """Return the theme role if configured."""
        return self._theme

    @property
    def fallback(self) -> bool:
        """Return whether smart color fallback is enabled."""
        return self._fallback

    def _clone(
        self,
        color: Any = ...,
        style: Any = ...,
        rgb: Any = ...,
        color256: Any = ...,
        theme: Any = ...,
        fallback: Any = ...,
        bg: Any = ...,
        bg_rgb: Any = ...,
        bg_color256: Any = ...,
    ) -> "Style":
        """Internal helper to create a modified clone."""
        new_color = self._color if color is ... else color
        new_style = self._styles if style is ... else style
        new_rgb = self._rgb if rgb is ... else rgb
        new_color256 = self._color256 if color256 is ... else color256
        new_theme = self._theme if theme is ... else theme
        new_fallback = self._fallback if fallback is ... else fallback
        new_bg = self._bg if bg is ... else bg
        new_bg_rgb = self._bg_rgb if bg_rgb is ... else bg_rgb
        new_bg_color256 = self._bg_color256 if bg_color256 is ... else bg_color256
        return Style(
            color=new_color,
            style=new_style,
            rgb=new_rgb,
            color256=new_color256,
            theme=new_theme,
            fallback=new_fallback,
            bg=new_bg,
            bg_rgb=new_bg_rgb,
            bg_color256=new_bg_color256,
        )

    def bold(self) -> "Style":
        """Return a new Style with 'bold' added."""
        styles = list(self._styles)
        if "bold" not in styles:
            styles.append("bold")
        return self._clone(style=styles)

    def italic(self) -> "Style":
        """Return a new Style with 'italic' added."""
        styles = list(self._styles)
        if "italic" not in styles:
            styles.append("italic")
        return self._clone(style=styles)

    def underline(self) -> "Style":
        """Return a new Style with 'underline' added."""
        styles = list(self._styles)
        if "underline" not in styles:
            styles.append("underline")
        return self._clone(style=styles)

    def reverse(self) -> "Style":
        """Return a new Style with 'reverse' added."""
        styles = list(self._styles)
        if "reverse" not in styles:
            styles.append("reverse")
        return self._clone(style=styles)

    def strikethrough(self) -> "Style":
        """Return a new Style with 'strikethrough' added."""
        styles = list(self._styles)
        if "strikethrough" not in styles:
            styles.append("strikethrough")
        return self._clone(style=styles)

    def dim(self) -> "Style":
        """Return a new Style with 'dim' added."""
        styles = list(self._styles)
        if "dim" not in styles:
            styles.append("dim")
        return self._clone(style=styles)

    def with_color(self, color: Optional[str]) -> "Style":
        """Return a new Style with the specified named color."""
        return self._clone(color=color, rgb=None, color256=None, theme=None)

    def with_rgb(self, rgb: Optional[tuple[int, int, int]]) -> "Style":
        """Return a new Style with the specified RGB tuple."""
        return self._clone(color=None, rgb=rgb, color256=None, theme=None)

    def with_color256(self, color256: Optional[int]) -> "Style":
        """Return a new Style with the specified 256-color index."""
        return self._clone(color=None, rgb=None, color256=color256, theme=None)

    def with_bg(self, bg: Optional[str]) -> "Style":
        """Return a new Style with the specified named background color."""
        return self._clone(bg=bg, bg_rgb=None, bg_color256=None, theme=None)

    def with_bg_rgb(self, bg_rgb: Optional[tuple[int, int, int]]) -> "Style":
        """Return a new Style with the specified background RGB tuple."""
        return self._clone(bg=None, bg_rgb=bg_rgb, bg_color256=None, theme=None)

    def with_bg_color256(self, bg_color256: Optional[int]) -> "Style":
        """Return a new Style with the specified 256-color background index."""
        return self._clone(bg=None, bg_rgb=None, bg_color256=bg_color256, theme=None)

    def with_style(
        self, style: Optional[Union[str, Sequence[str]]]
    ) -> "Style":
        """Return a new Style with the specified styles."""
        return self._clone(style=style)

    def with_theme(self, theme: Optional[str]) -> "Style":
        """Return a new Style with the specified theme role."""
        return self._clone(
            color=None,
            rgb=None,
            color256=None,
            bg=None,
            bg_rgb=None,
            bg_color256=None,
            theme=theme,
        )

    def with_fallback(self, fallback: bool) -> "Style":
        """Return a new Style with the specified fallback behavior."""
        return self._clone(fallback=fallback)

    def to_dict(self) -> dict[str, Any]:
        """Convert style attributes to a role definition dictionary."""
        d: dict[str, Any] = {}
        if self._color is not None:
            d["color"] = self._color
        elif self._rgb is not None:
            d["rgb"] = self._rgb
        elif self._color256 is not None:
            d["color256"] = self._color256

        if self._bg is not None:
            d["bg"] = self._bg
        elif self._bg_rgb is not None:
            d["bg_rgb"] = self._bg_rgb
        elif self._bg_color256 is not None:
            d["bg_color256"] = self._bg_color256

        if self._styles:
            d["style"] = list(self._styles)
        return d

    @classmethod
    def from_role(
        cls, role: str, theme: Optional[Any] = None
    ) -> "Style":
        """Create a Style instance from a registered theme role.

        Args:
            role: Name of the semantic role.
            theme: Optional Theme instance (defaults to active global theme).

        Returns:
            Style: Reusable Style matching the theme role.
        """
        if theme is None:
            from termtint.theme import get_theme

            theme = get_theme()
        return theme.get_style(role)

    def apply(self, text: Any, stream: Optional[TextIO] = None) -> str:
        """Apply this style to text, returning an ANSI string or plain text.

        Args:
            text: Any content to convert to string and style.
            stream: Optional destination stream for color capability detection.

        Returns:
            str: Styled ANSI string if color is enabled, plain text otherwise.
        """
        if self._theme is not None:
            from termtint.theme import get_theme

            active_theme = get_theme()
            role_def = active_theme.get_role(self._theme)

            color_code: Optional[str] = None
            if "color" in role_def:
                color_code = COLORS[role_def["color"]]
            elif "rgb" in role_def:
                role_rgb = role_def["rgb"]
                if self._fallback and not supports_truecolor(stream):
                    if supports_256color(stream):
                        color_code = _validate_color256(rgb_to_256(role_rgb))
                    else:
                        color_code = COLORS[rgb_to_ansi(role_rgb)]
                else:
                    color_code = _validate_rgb(role_rgb)
            elif "color256" in role_def:
                role_256 = role_def["color256"]
                if self._fallback and not supports_256color(stream):
                    color_code = COLORS[color256_to_ansi(role_256)]
                else:
                    color_code = _validate_color256(role_256)

            bg_code: Optional[str] = None
            if "bg" in role_def:
                bg_code = BG_COLORS[role_def["bg"]]
            elif "bg_rgb" in role_def:
                role_bg_rgb = role_def["bg_rgb"]
                if self._fallback and not supports_truecolor(stream):
                    if supports_256color(stream):
                        bg_code = _validate_bg_color256(rgb_to_256(role_bg_rgb))
                    else:
                        bg_code = BG_COLORS[rgb_to_ansi(role_bg_rgb)]
                else:
                    bg_code = _validate_bg_rgb(role_bg_rgb)
            elif "bg_color256" in role_def:
                role_bg_256 = role_def["bg_color256"]
                if self._fallback and not supports_256color(stream):
                    bg_code = BG_COLORS[color256_to_ansi(role_bg_256)]
                else:
                    bg_code = _validate_bg_color256(role_bg_256)

            all_styles: list[Any] = []
            if "style" in role_def:
                rs = role_def["style"]
                if isinstance(rs, (list, tuple, set)):
                    all_styles.extend(rs)
                else:
                    all_styles.append(rs)
            all_styles.extend(self._styles)
            style_codes = _normalize_styles(all_styles) if all_styles else []
            return _render_ansi(
                text,
                color_code=color_code,
                style_codes=style_codes,
                bg_code=bg_code,
                stream=stream,
            )

        color_code = None
        if self._color is not None:
            color_code = COLORS[self._color]
        elif self._rgb is not None:
            if self._fallback and not supports_truecolor(stream):
                if supports_256color(stream):
                    color_code = _validate_color256(rgb_to_256(self._rgb))
                else:
                    color_code = COLORS[rgb_to_ansi(self._rgb)]
            else:
                color_code = _validate_rgb(self._rgb)
        elif self._color256 is not None:
            if self._fallback and not supports_256color(stream):
                color_code = COLORS[color256_to_ansi(self._color256)]
            else:
                color_code = _validate_color256(self._color256)

        bg_code = None
        if self._bg is not None:
            bg_code = BG_COLORS[self._bg]
        elif self._bg_rgb is not None:
            if self._fallback and not supports_truecolor(stream):
                if supports_256color(stream):
                    bg_code = _validate_bg_color256(rgb_to_256(self._bg_rgb))
                else:
                    bg_code = BG_COLORS[rgb_to_ansi(self._bg_rgb)]
            else:
                bg_code = _validate_bg_rgb(self._bg_rgb)
        elif self._bg_color256 is not None:
            if self._fallback and not supports_256color(stream):
                bg_code = BG_COLORS[color256_to_ansi(self._bg_color256)]
            else:
                bg_code = _validate_bg_color256(self._bg_color256)

        style_codes = _normalize_styles(self._styles) if self._styles else []
        return _render_ansi(
            text,
            color_code=color_code,
            style_codes=style_codes,
            bg_code=bg_code,
            stream=stream,
        )

    def print(
        self,
        *values: Any,
        sep: str = " ",
        end: str = "\n",
        file: Optional[TextIO] = None,
        flush: bool = False,
    ) -> None:
        """Print styled values directly to a stream.

        Args:
            *values: Objects to format and print.
            sep: Separator between values (default: single space).
            end: Trailing string (default: newline).
            file: Destination stream (default: sys.stdout).
            flush: Whether to forcibly flush the stream.
        """
        target_file = file if file is not None else sys.stdout
        if not values:
            target_file.write(end)
        else:
            formatted = [self.apply(v, stream=target_file) for v in values]
            target_file.write(sep.join(formatted) + end)
        if flush:
            target_file.flush()

    def __call__(self, text: Any, stream: Optional[TextIO] = None) -> str:
        """Allow calling the Style instance directly like a function."""
        return self.apply(text, stream=stream)

    def __add__(self, other: Any) -> "Style":
        """Combine two styles together into a new Style instance."""
        if not isinstance(other, Style):
            return NotImplemented

        styles_combined = list(self._styles)
        for s in other._styles:
            if s not in styles_combined:
                styles_combined.append(s)

        if other._theme is not None:
            color = None
            rgb = None
            color256 = None
            bg = None
            bg_rgb = None
            bg_color256 = None
            theme = other._theme
        elif (
            other._color is not None
            or other._rgb is not None
            or other._color256 is not None
            or other._bg is not None
            or other._bg_rgb is not None
            or other._bg_color256 is not None
        ):
            theme = None
            if other._color is not None:
                color = other._color
                rgb = None
                color256 = None
            elif other._rgb is not None:
                color = None
                rgb = other._rgb
                color256 = None
            elif other._color256 is not None:
                color = None
                rgb = None
                color256 = other._color256
            else:
                color = self._color
                rgb = self._rgb
                color256 = self._color256

            if other._bg is not None:
                bg = other._bg
                bg_rgb = None
                bg_color256 = None
            elif other._bg_rgb is not None:
                bg = None
                bg_rgb = other._bg_rgb
                bg_color256 = None
            elif other._bg_color256 is not None:
                bg = None
                bg_rgb = None
                bg_color256 = other._bg_color256
            else:
                bg = self._bg
                bg_rgb = self._bg_rgb
                bg_color256 = self._bg_color256
        else:
            theme = self._theme
            color = self._color
            rgb = self._rgb
            color256 = self._color256
            bg = self._bg
            bg_rgb = self._bg_rgb
            bg_color256 = self._bg_color256

        fallback = self._fallback or other._fallback

        return Style(
            color=color,
            style=styles_combined,
            rgb=rgb,
            color256=color256,
            theme=theme,
            fallback=fallback,
            bg=bg,
            bg_rgb=bg_rgb,
            bg_color256=bg_color256,
        )

    def __repr__(self) -> str:
        parts = []
        if self._color:
            parts.append(f"color={self._color!r}")
        if self._rgb:
            parts.append(f"rgb={self._rgb!r}")
        if self._color256 is not None:
            parts.append(f"color256={self._color256!r}")
        if self._bg:
            parts.append(f"bg={self._bg!r}")
        if self._bg_rgb:
            parts.append(f"bg_rgb={self._bg_rgb!r}")
        if self._bg_color256 is not None:
            parts.append(f"bg_color256={self._bg_color256!r}")
        if self._styles:
            parts.append(f"style={list(self._styles)!r}")
        if self._theme:
            parts.append(f"theme={self._theme!r}")
        if self._fallback:
            parts.append("fallback=True")
        return f"Style({', '.join(parts)})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Style):
            return False
        return (
            self._color == other._color
            and self._rgb == other._rgb
            and self._color256 == other._color256
            and self._bg == other._bg
            and self._bg_rgb == other._bg_rgb
            and self._bg_color256 == other._bg_color256
            and self._theme == other._theme
            and self._styles == other._styles
            and self._fallback == other._fallback
        )

    def __hash__(self) -> int:
        return hash(
            (
                self._color,
                self._rgb,
                self._color256,
                self._bg,
                self._bg_rgb,
                self._bg_color256,
                self._theme,
                self._styles,
                self._fallback,
            )
        )
