"""Tests for termtint.theme module."""

import io
from unittest.mock import MagicMock

import pytest

from termtint import (
    DEFAULT_THEME,
    Theme,
    disable_color,
    enable_color,
    get_theme,
    reset_color_state,
    reset_theme,
    set_theme,
)


@pytest.fixture(autouse=True)
def reset_state():
    """Ensure color and theme state is reset after each test."""
    enable_color()
    yield
    reset_color_state()
    reset_theme()


def test_theme_init_valid():
    theme = Theme({
        "success": {"color": "green", "style": "bold"},
        "warning": {"color": "yellow"},
        "brand": {"rgb": (255, 128, 0), "style": "italic"},
        "badge": {"color256": 196, "style": ["bold", "reverse"]},
        "plain": {},
    })

    assert len(theme) == 5
    assert "success" in theme
    assert "brand" in theme
    assert "nonexistent" not in theme
    assert repr(theme).startswith("Theme({")

    role = theme["success"]
    assert role == {"color": "green", "style": "bold"}
    # Modifying returned role dict does not affect internal theme
    role["color"] = "red"
    assert theme["success"]["color"] == "green"


def test_theme_init_with_kwargs():
    theme = Theme(
        {"success": {"color": "green"}},
        error={"color": "red", "style": "bold"},
    )
    assert len(theme) == 2
    assert theme["success"]["color"] == "green"
    assert theme["error"]["color"] == "red"


def test_theme_equality():
    t1 = Theme({"success": {"color": "green"}})
    t2 = Theme({"success": {"color": "green"}})
    t3 = Theme({"success": {"color": "blue"}})

    assert t1 == t2
    assert t1 != t3
    assert t1 != "not_a_theme"


def test_theme_init_invalid_roles():
    with pytest.raises(TypeError, match="Theme roles must be provided as a dictionary"):
        Theme(roles="not_a_dict")

    with pytest.raises(TypeError, match="Theme roles must be provided as a dictionary"):
        Theme(roles=123)

    with pytest.raises(TypeError, match="Theme roles must be provided as a dictionary"):
        Theme(roles=True)

    with pytest.raises(TypeError, match="Theme role name must be a string"):
        Theme({123: {"color": "green"}})

    with pytest.raises(TypeError, match="Theme role name must be a string"):
        Theme({True: {"color": "green"}})

    with pytest.raises(ValueError, match="Theme role name cannot be empty"):
        Theme({"": {"color": "green"}})

    with pytest.raises(TypeError, match="definition must be a dict"):
        Theme({"success": "not_a_dict"})

    with pytest.raises(TypeError, match="definition must be a dict"):
        Theme({"success": True})


def test_theme_init_invalid_role_definitions():
    with pytest.raises(ValueError, match="Invalid key 'unknown'"):
        Theme({"success": {"color": "green", "unknown": "value"}})

    # Conflicting color options
    with pytest.raises(ValueError, match="cannot specify more than one of"):
        Theme({"s": {"color": "green", "rgb": (1, 2, 3)}})

    with pytest.raises(ValueError, match="cannot specify more than one of"):
        Theme({"s": {"color": "green", "color256": 100}})

    with pytest.raises(ValueError, match="cannot specify more than one of"):
        Theme({"s": {"rgb": (1, 2, 3), "color256": 100}})

    # Invalid color values
    with pytest.raises(TypeError, match="color must be a string"):
        Theme({"s": {"color": 123}})

    with pytest.raises(TypeError, match="color must be a string"):
        Theme({"s": {"color": True}})

    with pytest.raises(ValueError, match="Invalid color 'neon'"):
        Theme({"s": {"color": "neon"}})

    # Invalid RGB values
    with pytest.raises(ValueError, match="between 0 and 255"):
        Theme({"s": {"rgb": (300, 0, 0)}})

    with pytest.raises(TypeError, match="must be an integer"):
        Theme({"s": {"rgb": (True, 0, 0)}})

    # Invalid 256 values
    with pytest.raises(ValueError, match="between 0 and 255"):
        Theme({"s": {"color256": 300}})

    with pytest.raises(TypeError, match="color256 must be an integer"):
        Theme({"s": {"color256": True}})

    # Invalid styles
    with pytest.raises(ValueError, match="Invalid style 'fancy'"):
        Theme({"s": {"style": "fancy"}})

    with pytest.raises(TypeError, match="Style must be a string"):
        Theme({"s": {"style": True}})


def test_theme_unknown_role():
    theme = Theme({"success": {"color": "green"}})
    with pytest.raises(KeyError, match="Unknown theme role 'missing'"):
        theme.get_role("missing")

    with pytest.raises(KeyError, match="Unknown theme role 'missing'"):
        _ = theme["missing"]

    with pytest.raises(KeyError, match="Unknown theme role 'missing'"):
        theme.styled("text", "missing")


def test_theme_styled():
    theme = Theme({
        "success": {"color": "green", "style": "bold"},
        "brand": {"rgb": (255, 128, 0), "style": "italic"},
        "badge": {"color256": 208, "style": "reverse"},
        "plain": {},
    })

    assert (
        theme.styled("Done", "success")
        == "\033[1;32mDone\033[0m"
    )
    assert (
        theme.styled("Brand", "brand")
        == "\033[3;38;2;255;128;0mBrand\033[0m"
    )
    assert (
        theme.styled("Badge", "badge")
        == "\033[7;38;5;208mBadge\033[0m"
    )
    assert theme.styled("No style", "plain") == "No style"


def test_theme_print(capsys):
    theme = Theme({
        "success": {"color": "green", "style": "bold"},
        "error": {"color": "red", "style": "bold"},
    })

    # Positional role: theme.print(text, role)
    theme.print("System online", "success")
    captured = capsys.readouterr()
    assert captured.out == "\033[1;32mSystem online\033[0m\n"

    # Multiple positional values with role at the end: theme.print(v1, v2, role)
    theme.print("Build", "passed", "success", sep=" - ")
    captured = capsys.readouterr()
    assert captured.out == "\033[1;32mBuild - passed\033[0m\n"

    # Keyword role: theme.print(text, role="success")
    theme.print("Deployment complete", role="success")
    captured = capsys.readouterr()
    assert captured.out == "\033[1;32mDeployment complete\033[0m\n"

    # Custom stream target
    buf = io.StringIO()
    theme.print("Buffer test", "success", file=buf)
    # Stream is StringIO (non-TTY), so in AUTO mode output is plain text
    reset_color_state()
    buf2 = io.StringIO()
    theme.print("Plain buffer", "success", file=buf2)
    assert buf2.getvalue() == "Plain buffer\n"


def test_theme_print_invalid():
    theme = Theme({"success": {"color": "green"}})

    with pytest.raises(TypeError, match="Missing required argument 'role'"):
        theme.print("OnlyOneArgWithoutRole")

    with pytest.raises(TypeError, match="No text values provided"):
        theme.print(role="success")

    with pytest.raises(TypeError, match="Role must be a string"):
        theme.print("text", 123)

    with pytest.raises(KeyError, match="Unknown theme role 'unknown'"):
        theme.print("text", "unknown")


def test_theme_extend():
    base = Theme({
        "success": {"color": "green", "style": "bold"},
        "warning": {"color": "yellow"},
    })

    extended = base.extend(
        {"warning": {"color": "yellow", "style": "underline"}},
        accent={"rgb": (255, 0, 128)},
    )

    # Verify base was not mutated
    assert base["warning"] == {"color": "yellow"}
    assert "accent" not in base
    assert len(base) == 2

    # Verify extended has overrides and new roles
    assert extended["success"] == {"color": "green", "style": "bold"}
    assert extended["warning"] == {"color": "yellow", "style": "underline"}
    assert extended["accent"]["rgb"] == (255, 0, 128)
    assert len(extended) == 3

    with pytest.raises(TypeError, match="Theme roles must be provided as a dictionary"):
        base.extend("not_a_dict")


def test_global_theme_management():
    # Initial state is DEFAULT_THEME
    assert get_theme() is DEFAULT_THEME
    assert "success" in DEFAULT_THEME
    assert "error" in DEFAULT_THEME
    assert "warning" in DEFAULT_THEME
    assert "info" in DEFAULT_THEME
    assert "muted" in DEFAULT_THEME

    custom = Theme({"brand": {"color": "blue", "style": "bold"}})
    set_theme(custom)
    assert get_theme() is custom

    with pytest.raises(TypeError, match="theme must be a Theme instance"):
        set_theme("not_a_theme")

    reset_theme()
    assert get_theme() is DEFAULT_THEME


def test_theme_stream_awareness(monkeypatch):
    reset_color_state()
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")

    theme = Theme({"success": {"color": "green", "style": "bold"}})
    non_tty_buf = io.StringIO()

    # In AUTO mode on non-TTY stream, styled returns plain text
    assert theme.styled("Done", "success", stream=non_tty_buf) == "Done"


def test_theme_no_color_and_force_color(monkeypatch):
    theme = Theme({"success": {"color": "green", "style": "bold"}})

    # NO_COLOR disables theme styling
    monkeypatch.setenv("NO_COLOR", "1")
    reset_color_state()
    assert theme.styled("Done", "success") == "Done"

    # FORCE_COLOR forces theme styling on non-TTY
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("FORCE_COLOR", "1")
    reset_color_state()
    non_tty_buf = io.StringIO()
    assert (
        theme.styled("Done", "success", stream=non_tty_buf)
        == "\033[1;32mDone\033[0m"
    )


def test_theme_enable_disable():
    theme = Theme({"success": {"color": "green", "style": "bold"}})
    reset_color_state()
    non_tty_buf = io.StringIO()

    enable_color()
    assert (
        theme.styled("Done", "success", stream=non_tty_buf)
        == "\033[1;32mDone\033[0m"
    )

    disable_color()
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True
    assert theme.styled("Done", "success", stream=mock_tty) == "Done"
