"""Theme support and semantic styling for TermTint."""

import sys
from typing import Any, Optional, TextIO

from termtint.core import (
    COLORS,
    _normalize_styles,
    _render_ansi,
    _validate_color256,
    _validate_rgb,
)

ALLOWED_ROLE_KEYS = {"color", "style", "rgb", "color256"}


def _validate_role_definition(role: str, definition: Any) -> dict[str, Any]:
    """Validate a theme role definition dictionary.

    Args:
        role: Name of the semantic role.
        definition: Dict containing styling specifications.

    Returns:
        dict[str, Any]: Validated role definition copy.

    Raises:
        TypeError: If role or definition types are invalid.
        ValueError: If definition contains invalid or conflicting keys.
    """
    if isinstance(role, bool) or not isinstance(role, str):
        tname = type(role).__name__
        raise TypeError(f"Theme role name must be a string, got {tname}.")
    if not role.strip():
        raise ValueError("Theme role name cannot be empty.")

    if hasattr(definition, "to_dict") and callable(definition.to_dict):
        definition = definition.to_dict()

    if isinstance(definition, bool) or not isinstance(definition, dict):
        tname = type(definition).__name__
        raise TypeError(
            f"Theme role '{role}' definition must be a dict, got {tname}."
        )

    # Check for unrecognized keys
    for k in definition:
        if k not in ALLOWED_ROLE_KEYS:
            allowed = ", ".join(sorted(ALLOWED_ROLE_KEYS))
            raise ValueError(
                f"Invalid key '{k}' in theme role '{role}'. "
                f"Allowed keys are: {allowed}."
            )

    # Check color mutual exclusivity
    color_keys = [
        k for k in ("color", "rgb", "color256")
        if k in definition and definition[k] is not None
    ]
    if len(color_keys) > 1:
        raise ValueError(
            f"Theme role '{role}' cannot specify more than one of "
            "'color', 'rgb', or 'color256'."
        )

    validated: dict[str, Any] = {}

    if "color" in definition and definition["color"] is not None:
        color_val = definition["color"]
        if isinstance(color_val, bool) or not isinstance(color_val, str):
            tname = type(color_val).__name__
            raise TypeError(
                f"Role '{role}' color must be a string, got {tname}."
            )
        color_lower = color_val.lower()
        if color_lower not in COLORS:
            valid_colors = ", ".join(sorted(COLORS.keys()))
            raise ValueError(
                f"Invalid color '{color_val}' in role '{role}'. "
                f"Supported colors are: {valid_colors}"
            )
        validated["color"] = color_lower

    if "rgb" in definition and definition["rgb"] is not None:
        _validate_rgb(definition["rgb"])
        validated["rgb"] = tuple(definition["rgb"])

    if "color256" in definition and definition["color256"] is not None:
        _validate_color256(definition["color256"])
        validated["color256"] = definition["color256"]

    if "style" in definition and definition["style"] is not None:
        style_val = definition["style"]
        _normalize_styles(style_val)
        if isinstance(style_val, (list, tuple, set)):
            validated["style"] = list(style_val)
        else:
            validated["style"] = style_val

    return validated


class Theme:
    """Represents a collection of semantic styling roles."""

    def __init__(
        self,
        roles: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a new Theme with validated semantic roles.

        Args:
            roles: Optional dictionary mapping role names to style dicts.
            **kwargs: Additional roles specified as keyword arguments.

        Raises:
            TypeError: If roles is not a dictionary or contains invalid types.
            ValueError: If role definitions contain invalid properties.
        """
        self._roles: dict[str, dict[str, Any]] = {}

        all_definitions: dict[str, Any] = {}
        if roles is not None:
            if isinstance(roles, bool) or not isinstance(roles, dict):
                tname = type(roles).__name__
                raise TypeError(
                    f"Theme roles must be provided as a dictionary, got {tname}."
                )
            all_definitions.update(roles)
        all_definitions.update(kwargs)

        for role_name, role_def in all_definitions.items():
            self._roles[role_name] = _validate_role_definition(
                role_name, role_def
            )

    def get_role(self, role: str) -> dict[str, Any]:
        """Retrieve the definition for a given role.

        Args:
            role: Name of the semantic role.

        Returns:
            dict[str, Any]: Copy of the role definition dictionary.

        Raises:
            KeyError: If role is not defined in this theme.
        """
        if role not in self._roles:
            available = ", ".join(sorted(self._roles.keys()))
            raise KeyError(
                f"Unknown theme role '{role}'. Available roles: {available}"
            )
        return dict(self._roles[role])

    def get_style(self, role: str) -> Any:
        """Retrieve a reusable Style instance for a registered role.

        Args:
            role: Name of the semantic role.

        Returns:
            Style: Reusable Style matching the theme role.

        Raises:
            KeyError: If role is not defined in this theme.
        """
        from termtint.style import Style

        role_def = self.get_role(role)
        return Style(
            color=role_def.get("color"),
            style=role_def.get("style"),
            rgb=role_def.get("rgb"),
            color256=role_def.get("color256"),
        )

    def styled(
        self,
        text: Any,
        role: str,
        stream: Optional[TextIO] = None,
    ) -> str:
        """Format text according to a semantic role in this theme.

        Args:
            text: Content to style.
            role: Semantic role name.
            stream: Optional destination stream for color capability detection.

        Returns:
            str: Styled ANSI string or plain text if color is disabled.

        Raises:
            KeyError: If role is not defined in this theme.
        """
        role_def = self.get_role(role)

        color_code: Optional[str] = None
        if "color" in role_def:
            color_code = COLORS[role_def["color"]]
        elif "rgb" in role_def:
            color_code = _validate_rgb(role_def["rgb"])
        elif "color256" in role_def:
            color_code = _validate_color256(role_def["color256"])

        style_codes = (
            _normalize_styles(role_def["style"])
            if "style" in role_def
            else []
        )
        return _render_ansi(
            text, color_code=color_code, style_codes=style_codes, stream=stream
        )

    def print(
        self,
        *values: Any,
        role: Optional[str] = None,
        file: Optional[TextIO] = None,
        sep: str = " ",
        end: str = "\n",
        flush: bool = False,
    ) -> None:
        """Print text styled with a semantic role.

        Supports both positional and keyword role:
            theme.print("Hello", "success")
            theme.print("Hello", "World", role="success")

        Args:
            *values: Content values to print.
            role: Semantic role name.
            file: Destination stream; defaults to sys.stdout.
            sep: String inserted between values, default a space.
            end: String appended after the last value, default a newline.
            flush: Whether to forcibly flush the stream.

        Raises:
            TypeError: If role is omitted or no content is provided.
            KeyError: If role is not defined in this theme.
        """
        if role is None:
            if len(values) < 2:
                raise TypeError(
                    "Missing required argument 'role'. Provide role as keyword "
                    "or last positional argument."
                )
            text_values = values[:-1]
            resolved_role = values[-1]
            if isinstance(resolved_role, bool) or not isinstance(
                resolved_role, str
            ):
                raise TypeError(
                    f"Role must be a string, got {type(resolved_role).__name__}."
                )
        else:
            if not values:
                raise TypeError("No text values provided to print.")
            text_values = values
            resolved_role = role

        target = file if file is not None else sys.stdout
        text = sep.join(str(v) for v in text_values)
        output = self.styled(text, role=resolved_role, stream=target)
        print(output, end=end, file=target, flush=flush)

    def extend(
        self,
        roles: Optional[dict[str, dict[str, Any]]] = None,
        **kwargs: dict[str, Any],
    ) -> "Theme":
        """Create a new Theme combining this theme's roles with additional roles.

        Does not mutate the existing Theme instance.

        Args:
            roles: Optional dictionary of additional or overridden roles.
            **kwargs: Additional or overridden roles as keyword arguments.

        Returns:
            Theme: A new Theme instance.
        """
        merged_roles = {k: dict(v) for k, v in self._roles.items()}
        if roles is not None:
            if isinstance(roles, bool) or not isinstance(roles, dict):
                tname = type(roles).__name__
                raise TypeError(
                    f"Theme roles must be provided as a dictionary, got {tname}."
                )
            merged_roles.update(roles)
        merged_roles.update(kwargs)
        return Theme(merged_roles)

    def __getitem__(self, role: str) -> dict[str, Any]:
        return self.get_role(role)

    def __contains__(self, role: str) -> bool:
        return role in self._roles

    def __len__(self) -> int:
        return len(self._roles)

    def __repr__(self) -> str:
        return f"Theme({self._roles!r})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Theme):
            return self._roles == other._roles
        return False


DEFAULT_THEME = Theme({
    "success": {"color": "green", "style": "bold"},
    "error": {"color": "red", "style": "bold"},
    "warning": {"color": "yellow"},
    "info": {"color": "cyan", "style": "italic"},
    "muted": {"style": "dim"},
})

_active_theme: Theme = DEFAULT_THEME


def get_theme() -> Theme:
    """Get the currently active global Theme.

    Returns:
        Theme: The current global theme instance.
    """
    return _active_theme


def set_theme(theme: Theme) -> None:
    """Set the active global Theme for theme-based styling.

    Args:
        theme: A Theme instance to set as active.

    Raises:
        TypeError: If theme is not a Theme instance.
    """
    if not isinstance(theme, Theme):
        tname = type(theme).__name__
        raise TypeError(f"theme must be a Theme instance, got {tname}.")
    global _active_theme
    _active_theme = theme


def reset_theme() -> None:
    """Reset the active global Theme to DEFAULT_THEME."""
    global _active_theme
    _active_theme = DEFAULT_THEME
