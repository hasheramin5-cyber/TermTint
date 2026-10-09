"""Terminal color capability detection and state management."""

import os
import sys
from enum import Enum, auto
from typing import Optional, TextIO

from termtint._windows import enable_vt_mode


class ColorState(Enum):
    """Enumeration for explicit color configuration state."""

    AUTO = auto()
    ENABLED = auto()
    DISABLED = auto()


_current_state: ColorState = ColorState.AUTO
_cached_auto_result: Optional[bool] = None


def set_color_state(state: ColorState) -> None:
    """Set explicit color state.

    Args:
        state: The ColorState to set (AUTO, ENABLED, or DISABLED).
    """
    global _current_state, _cached_auto_result
    _current_state = state
    _cached_auto_result = None


def get_color_state() -> ColorState:
    """Get current color state.

    Returns:
        ColorState: Current color configuration.
    """
    return _current_state


def reset_color_state() -> None:
    """Reset color state to AUTO mode."""
    set_color_state(ColorState.AUTO)


def should_color(stream: Optional[TextIO] = None) -> bool:
    """Determine whether color output should be enabled.

    Args:
        stream: Optional file stream to check. Defaults to sys.stdout.

    Returns:
        bool: True if colors should be output, False otherwise.
    """
    if _current_state == ColorState.ENABLED:
        return True
    if _current_state == ColorState.DISABLED:
        return False

    global _cached_auto_result
    target_stream = stream if stream is not None else sys.stdout

    if target_stream is sys.stdout:
        if _cached_auto_result is not None:
            return _cached_auto_result
        res = _detect_color_support(sys.stdout)
        _cached_auto_result = res
        return res

    return _detect_color_support(target_stream)


def _detect_color_support(stream: TextIO) -> bool:
    """Perform actual environment and terminal detection.

    Args:
        stream: TextIO stream to inspect for TTY support.

    Returns:
        bool: True if terminal supports color output, False otherwise.
    """
    # 1. Respect NO_COLOR standard (https://no-color.org)
    if os.environ.get("NO_COLOR", "") != "":
        return False

    # 2. Check explicit force environment flags
    if os.environ.get("FORCE_COLOR") in ("1", "2", "3", "true", "TRUE"):
        return True
    if os.environ.get("CLICOLOR_FORCE") in ("1", "true", "TRUE"):
        return True

    # 3. Check stream TTY capability
    try:
        if not hasattr(stream, "isatty") or not stream.isatty():
            return False
    except Exception:
        return False

    # 4. Check TERM environment variable
    term = os.environ.get("TERM", "").lower()
    if term == "dumb":
        return False

    # 5. Windows specific console checks
    if sys.platform == "win32":
        if any(env in os.environ for env in ("WT_SESSION", "ANSICON", "ConEmuANSI")):
            return True
        colorterm = os.environ.get("COLORTERM", "").lower()
        if colorterm in ("truecolor", "24bit"):
            return True
        return enable_vt_mode()

    return True


def supports_color(stream: Optional[TextIO] = None) -> bool:
    """Determine whether the terminal or stream supports color output.

    Args:
        stream: Optional file stream to check. Defaults to sys.stdout.

    Returns:
        bool: True if colors are supported and enabled, False otherwise.
    """
    return should_color(stream=stream)


def supports_256color(stream: Optional[TextIO] = None) -> bool:
    """Determine whether the terminal or stream supports 256-color ANSI output.

    Args:
        stream: Optional file stream to check. Defaults to sys.stdout.

    Returns:
        bool: True if 256-color output is supported, False otherwise.
    """
    if not supports_color(stream=stream):
        return False

    if os.environ.get("FORCE_COLOR") in ("2", "3"):
        return True

    colorterm = os.environ.get("COLORTERM", "").lower()
    if colorterm in ("truecolor", "24bit"):
        return True

    term = os.environ.get("TERM", "").lower()
    if "256color" in term or term.endswith("-256"):
        return True
    if term in (
        "xterm-kitty",
        "alacritty",
        "foot",
        "wezterm",
        "ghostty",
        "screen-256color",
        "tmux-256color",
    ):
        return True

    if sys.platform == "win32":
        if any(env in os.environ for env in ("WT_SESSION", "ANSICON", "ConEmuANSI")):
            return True
        return enable_vt_mode()

    return False


def supports_truecolor(stream: Optional[TextIO] = None) -> bool:
    """Determine whether the terminal or stream supports 24-bit True Color (RGB).

    Args:
        stream: Optional file stream to check. Defaults to sys.stdout.

    Returns:
        bool: True if 24-bit True Color is supported, False otherwise.
    """
    if not supports_color(stream=stream):
        return False

    if os.environ.get("FORCE_COLOR") == "3":
        return True

    colorterm = os.environ.get("COLORTERM", "").lower()
    if colorterm in ("truecolor", "24bit"):
        return True

    term = os.environ.get("TERM", "").lower()
    if term in (
        "xterm-kitty",
        "alacritty",
        "foot",
        "wezterm",
        "ghostty",
        "iterm2",
    ):
        return True
    if term.startswith("xterm-direct"):
        return True

    if sys.platform == "win32":
        if "WT_SESSION" in os.environ:
            return True
        try:
            win_ver = sys.getwindowsversion()
            if getattr(win_ver, "build", 0) >= 14393:
                return enable_vt_mode()
        except Exception:
            return False

    return False
