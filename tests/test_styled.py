"""Tests for termtint.core.styled() function."""

import io
from unittest.mock import MagicMock

import pytest

from termtint import (
    disable_color,
    enable_color,
    reset_color_state,
    reset_theme,
    set_theme,
    styled,
)
from termtint.theme import Theme


@pytest.fixture(autouse=True)
def reset_state():
    """Ensure color and theme state is reset after each test."""
    enable_color()
    yield
    reset_color_state()
    reset_theme()


def test_styled_no_styling():
    assert styled("plain text") == "plain text"
    assert styled(12345) == "12345"
    assert styled(True) == "True"


@pytest.mark.parametrize(
    "style_name,ansi_code",
    [
        ("bold", "1"),
        ("bright", "1"),
        ("dim", "2"),
        ("italic", "3"),
        ("underline", "4"),
        ("reverse", "7"),
        ("strikethrough", "9"),
        ("normal", "0"),
    ],
)
def test_styled_single_style_only(style_name, ansi_code):
    expected = f"\033[{ansi_code}mtext\033[0m"
    assert styled("text", style=style_name) == expected


def test_styled_multiple_styles():
    assert (
        styled("Badge", color256=198, style=["bold", "reverse"])
        == "\033[1;7;38;5;198mBadge\033[0m"
    )
    assert (
        styled("Alert", color="red", style=("bold", "underline"))
        == "\033[1;4;31mAlert\033[0m"
    )
    assert (
        styled("Comma separated", color="green", style="bold, underline")
        == "\033[1;4;32mComma separated\033[0m"
    )
    assert (
        styled("Deduplicated", style=["bold", "bold"])
        == "\033[1mDeduplicated\033[0m"
    )
    assert (
        styled("Normal dropped with others", style=["normal", "italic"])
        == "\033[3mNormal dropped with others\033[0m"
    )


def test_styled_colors_and_styles():
    assert (
        styled("Warning!", color="yellow", style="bold")
        == "\033[1;33mWarning!\033[0m"
    )
    assert (
        styled("Accent", rgb=(255, 128, 0), style="italic")
        == "\033[3;38;2;255;128;0mAccent\033[0m"
    )
    assert (
        styled("Normal color", color="blue", style="normal")
        == "\033[34mNormal color\033[0m"
    )
    assert (
        styled("Only named color", color="cyan")
        == "\033[36mOnly named color\033[0m"
    )
    assert (
        styled("Only rgb", rgb=(10, 20, 30))
        == "\033[38;2;10;20;30mOnly rgb\033[0m"
    )
    assert (
        styled("Only 256", color256=208)
        == "\033[38;5;208mOnly 256\033[0m"
    )


def test_styled_theme_roles():
    assert (
        styled("Success message", theme="success")
        == "\033[1;32mSuccess message\033[0m"
    )
    assert (
        styled("Error message", theme="error")
        == "\033[1;31mError message\033[0m"
    )
    assert (
        styled("Warning message", theme="warning")
        == "\033[33mWarning message\033[0m"
    )
    assert (
        styled("Info message", theme="info")
        == "\033[3;36mInfo message\033[0m"
    )
    assert (
        styled("Muted message", theme="muted")
        == "\033[2mMuted message\033[0m"
    )


def test_styled_theme_with_additional_style():
    # Adding underline to default success (green + bold) -> green + bold + underline
    assert (
        styled("Success alert", theme="success", style="underline")
        == "\033[1;4;32mSuccess alert\033[0m"
    )


def test_styled_custom_theme_roles():
    custom = Theme({
        "brand": {"rgb": (255, 140, 0), "style": "bold"},
        "subtle": {"color256": 240, "style": "dim"},
    })
    set_theme(custom)

    assert (
        styled("Brand text", theme="brand")
        == "\033[1;38;2;255;140;0mBrand text\033[0m"
    )
    assert (
        styled("Subtle text", theme="subtle")
        == "\033[2;38;5;240mSubtle text\033[0m"
    )


def test_styled_invalid_combinations():
    with pytest.raises(ValueError, match="Only one of 'color', 'rgb', or 'color256'"):
        styled("text", color="red", rgb=(255, 0, 0))

    with pytest.raises(ValueError, match="Only one of 'color', 'rgb', or 'color256'"):
        styled("text", color="red", color256=196)

    with pytest.raises(ValueError, match="Only one of 'color', 'rgb', or 'color256'"):
        styled("text", rgb=(255, 0, 0), color256=196)

    with pytest.raises(ValueError, match="Cannot specify 'theme' together with"):
        styled("text", color="red", theme="success")

    with pytest.raises(ValueError, match="Cannot specify 'theme' together with"):
        styled("text", rgb=(255, 0, 0), theme="success")

    with pytest.raises(ValueError, match="Cannot specify 'theme' together with"):
        styled("text", color256=196, theme="success")


def test_styled_invalid_types_and_values():
    with pytest.raises(TypeError, match="Named color must be a string"):
        styled("text", color=123)
    with pytest.raises(TypeError, match="Named color must be a string"):
        styled("text", color=True)
    with pytest.raises(ValueError, match="Invalid color 'neon'"):
        styled("text", color="neon")

    with pytest.raises(TypeError, match="Style must be a string"):
        styled("text", style=123)
    with pytest.raises(TypeError, match="Style must be a string"):
        styled("text", style=True)
    with pytest.raises(TypeError, match="Style element must be a string"):
        styled("text", style=["bold", 123])
    with pytest.raises(TypeError, match="Style element must be a string"):
        styled("text", style=["bold", True])
    with pytest.raises(ValueError, match="Invalid style 'fancy'"):
        styled("text", style="fancy")
    with pytest.raises(ValueError, match="Invalid style 'fancy'"):
        styled("text", style=["bold", "fancy"])

    with pytest.raises(TypeError, match="Theme role must be a string"):
        styled("text", theme=123)
    with pytest.raises(TypeError, match="Theme role must be a string"):
        styled("text", theme=True)
    with pytest.raises(KeyError, match="Unknown theme role 'unknown'"):
        styled("text", theme="unknown")


def test_styled_stream_awareness(monkeypatch):
    reset_color_state()
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")

    non_tty_buf = io.StringIO()
    # non-TTY stream strips ANSI escape codes in auto mode
    assert styled("Header", style="bold", stream=non_tty_buf) == "Header"
    assert (
        styled("Warning!", color="yellow", style="bold", stream=non_tty_buf)
        == "Warning!"
    )
    assert styled("Success", theme="success", stream=non_tty_buf) == "Success"


def test_styled_no_color_and_force_color(monkeypatch):
    # NO_COLOR disables styling
    monkeypatch.setenv("NO_COLOR", "1")
    reset_color_state()
    assert styled("Header", style="bold") == "Header"
    assert styled("Success", theme="success") == "Success"

    # FORCE_COLOR forces styling even on non-TTY
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("FORCE_COLOR", "1")
    reset_color_state()
    non_tty_buf = io.StringIO()
    assert (
        styled("Header", style="bold", stream=non_tty_buf)
        == "\033[1mHeader\033[0m"
    )
    assert (
        styled("Success", theme="success", stream=non_tty_buf)
        == "\033[1;32mSuccess\033[0m"
    )


def test_styled_enable_disable():
    reset_color_state()
    non_tty_buf = io.StringIO()

    enable_color()
    assert (
        styled("Header", style="bold", stream=non_tty_buf)
        == "\033[1mHeader\033[0m"
    )

    disable_color()
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True
    assert styled("Header", style="bold", stream=mock_tty) == "Header"
    assert styled("Success", theme="success", stream=mock_tty) == "Success"


def test_styled_list_of_comma_styles_and_theme_list_styles():
    # Comma inside a list element: style=["bold, italic"]
    assert styled("text", style=["bold, italic"]) == "\033[1;3mtext\033[0m"

    # Theme role with a list of styles and user passing list of styles
    t = Theme({"badge": {"color": "magenta", "style": ["bold", "reverse"]}})
    set_theme(t)
    assert (
        styled("text", theme="badge", style=["underline", "dim"])
        == "\033[1;7;4;2;35mtext\033[0m"
    )

