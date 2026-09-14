"""Tests for termtint.core module."""

import io

import pytest

import termtint
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
)


@pytest.fixture(autouse=True)
def reset_state_after_test():
    """Ensure color state is always reset to AUTO after each test."""
    yield
    reset_color_state()


def test_colored_enabled():
    enable_color()
    assert is_color_enabled() is True

    # Test basic foreground colors
    assert colored("hello", "red") == "\033[31mhello\033[0m"
    assert colored("hello", "green") == "\033[32mhello\033[0m"
    assert colored("hello", "yellow") == "\033[33mhello\033[0m"
    assert colored("hello", "blue") == "\033[34mhello\033[0m"
    assert colored("hello", "magenta") == "\033[35mhello\033[0m"
    assert colored("hello", "cyan") == "\033[36mhello\033[0m"
    assert colored("hello", "white") == "\033[37mhello\033[0m"
    assert colored("hello", "black") == "\033[30mhello\033[0m"


def test_colored_with_styles():
    enable_color()
    assert colored("bold red", "red", style="bright") == "\033[1;31mbold red\033[0m"
    assert colored("dim red", "red", style="dim") == "\033[2;31mdim red\033[0m"
    expected_underline = "\033[4;31munderline red\033[0m"
    assert colored("underline red", "red", style="underline") == expected_underline
    assert colored("normal red", "red", style="normal") == "\033[31mnormal red\033[0m"


def test_colored_disabled():
    disable_color()
    assert is_color_enabled() is False

    assert colored("hello", "red") == "hello"
    assert colored("hello", "green", style="bright") == "hello"


def test_colored_invalid_color():
    with pytest.raises(ValueError, match="Invalid color 'purple'"):
        colored("text", "purple")


def test_colored_invalid_style():
    with pytest.raises(ValueError, match="Invalid style 'unknown'"):
        colored("text", "red", style="unknown")


def test_colored_non_string_input():
    enable_color()
    assert colored(12345, "green") == "\033[32m12345\033[0m"
    assert colored(True, "blue") == "\033[34mTrue\033[0m"


def test_convenience_print_functions(capsys):
    enable_color()

    print_red("red message")
    captured = capsys.readouterr()
    assert captured.out == "\033[31mred message\033[0m\n"

    print_green("green message", style="bright")
    captured = capsys.readouterr()
    assert captured.out == "\033[1;32mgreen message\033[0m\n"

    print_yellow("yellow message")
    captured = capsys.readouterr()
    assert captured.out == "\033[33myellow message\033[0m\n"

    print_blue("blue message")
    captured = capsys.readouterr()
    assert captured.out == "\033[34mblue message\033[0m\n"

    print_magenta("magenta message")
    captured = capsys.readouterr()
    assert captured.out == "\033[35mmagenta message\033[0m\n"

    print_cyan("cyan message")
    captured = capsys.readouterr()
    assert captured.out == "\033[36mcyan message\033[0m\n"

    print_white("white message")
    captured = capsys.readouterr()
    assert captured.out == "\033[37mwhite message\033[0m\n"

    print_black("black message")
    captured = capsys.readouterr()
    assert captured.out == "\033[30mblack message\033[0m\n"


def test_convenience_print_multiple_values(capsys):
    enable_color()
    print_green("Hello", "World", 2026, sep="-")
    captured = capsys.readouterr()
    assert captured.out == "\033[32mHello-World-2026\033[0m\n"


def test_convenience_print_custom_file_auto_mode():
    reset_color_state()
    buf = io.StringIO()
    # StringIO is a non-TTY stream, so AUTO mode should produce plain text
    print_red("buffer output", file=buf, end="")
    assert buf.getvalue() == "buffer output"


def test_colored_with_explicit_stream(monkeypatch):
    reset_color_state()
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")

    non_tty_buf = io.StringIO()
    assert colored("test", "red", stream=non_tty_buf) == "test"

    from unittest.mock import MagicMock, patch
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True
    with patch("termtint._detect.enable_vt_mode", return_value=True):
        assert colored("test", "red", stream=mock_tty) == "\033[31mtest\033[0m"


def test_explicit_overrides_with_custom_stream():
    non_tty_buf = io.StringIO()

    enable_color()
    assert colored("test", "green", stream=non_tty_buf) == "\033[32mtest\033[0m"

    disable_color()
    from unittest.mock import MagicMock
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True
    assert colored("test", "green", stream=mock_tty) == "test"


def test_colored_with_closed_stream():
    reset_color_state()
    closed_buf = io.StringIO()
    closed_buf.close()
    # isatty() on a closed stream raises ValueError; colored should handle gracefully
    assert colored("hello", "green", stream=closed_buf) == "hello"


def test_convenience_print_auto_mode_non_tty(capsys, monkeypatch):
    reset_color_state()
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.delenv("CLICOLOR_FORCE", raising=False)
    # capsys captures stdout as non-TTY, so in AUTO mode output is plain text
    print_red("uncolored red")
    captured = capsys.readouterr()
    assert captured.out == "uncolored red\n"


def test_colored_new_styles():
    enable_color()
    assert colored("bold", "red", style="bold") == "\033[1;31mbold\033[0m"
    assert colored("bright", "red", style="bright") == "\033[1;31mbright\033[0m"
    assert colored("italic", "green", style="italic") == "\033[3;32mitalic\033[0m"
    assert colored("dim", "yellow", style="dim") == "\033[2;33mdim\033[0m"
    assert (
        colored("underline", "blue", style="underline")
        == "\033[4;34munderline\033[0m"
    )
    assert colored("reverse", "magenta", style="reverse") == "\033[7;35mreverse\033[0m"
    assert (
        colored("strikethrough", "cyan", style="strikethrough")
        == "\033[9;36mstrikethrough\033[0m"
    )
    assert colored("normal", "white", style="normal") == "\033[37mnormal\033[0m"


def test_colored_rgb_output():
    enable_color()
    assert colored("rgb", rgb=(255, 0, 0)) == "\033[38;2;255;0;0mrgb\033[0m"
    assert colored("black", rgb=(0, 0, 0)) == "\033[38;2;0;0;0mblack\033[0m"
    assert (
        colored("white", rgb=(255, 255, 255))
        == "\033[38;2;255;255;255mwhite\033[0m"
    )
    assert (
        colored("teal", rgb=(0, 128, 128))
        == "\033[38;2;0;128;128mteal\033[0m"
    )


def test_colored_256_output():
    enable_color()
    assert colored("first", color256=0) == "\033[38;5;0mfirst\033[0m"
    assert colored("last", color256=255) == "\033[38;5;255mlast\033[0m"
    assert colored("orange", color256=208) == "\033[38;5;208morange\033[0m"
    assert colored("bright red", color256=196) == "\033[38;5;196mbright red\033[0m"


@pytest.mark.parametrize(
    "style,code",
    [
        ("normal", ""),
        ("bright", "1;"),
        ("bold", "1;"),
        ("dim", "2;"),
        ("italic", "3;"),
        ("underline", "4;"),
        ("reverse", "7;"),
        ("strikethrough", "9;"),
    ],
)
def test_colored_rgb_all_styles(style, code):
    enable_color()
    expected = f"\033[{code}38;2;10;20;30mtext\033[0m"
    assert colored("text", rgb=(10, 20, 30), style=style) == expected


@pytest.mark.parametrize(
    "style,code",
    [
        ("normal", ""),
        ("bright", "1;"),
        ("bold", "1;"),
        ("dim", "2;"),
        ("italic", "3;"),
        ("underline", "4;"),
        ("reverse", "7;"),
        ("strikethrough", "9;"),
    ],
)
def test_colored_256_all_styles(style, code):
    enable_color()
    expected = f"\033[{code}38;5;123mtext\033[0m"
    assert colored("text", color256=123, style=style) == expected


def test_invalid_rgb():
    # Not a sequence or boolean
    with pytest.raises(TypeError, match="RGB must be a"):
        colored("text", rgb=123)
    with pytest.raises(TypeError, match="RGB must be a"):
        colored("text", rgb="red")
    with pytest.raises(TypeError, match="RGB must be a"):
        colored("text", rgb=True)

    # Wrong length
    with pytest.raises(ValueError, match="exactly 3 components"):
        colored("text", rgb=(255, 0))
    with pytest.raises(ValueError, match="exactly 3 components"):
        colored("text", rgb=(255, 0, 0, 0))
    with pytest.raises(ValueError, match="exactly 3 components"):
        colored("text", rgb=())

    # Component types and boolean rejection
    with pytest.raises(TypeError, match="must be an integer"):
        colored("text", rgb=("255", 0, 0))
    with pytest.raises(TypeError, match="must be an integer"):
        colored("text", rgb=(255.5, 0, 0))
    with pytest.raises(TypeError, match="must be an integer"):
        colored("text", rgb=(True, 0, 0))
    with pytest.raises(TypeError, match="must be an integer"):
        colored("text", rgb=(255, False, 0))

    # Component ranges
    with pytest.raises(ValueError, match="between 0 and 255"):
        colored("text", rgb=(-1, 0, 0))
    with pytest.raises(ValueError, match="between 0 and 255"):
        colored("text", rgb=(256, 0, 0))
    with pytest.raises(ValueError, match="between 0 and 255"):
        colored("text", rgb=(0, 300, 0))
    with pytest.raises(ValueError, match="between 0 and 255"):
        colored("text", rgb=(0, 0, -5))


def test_invalid_color256():
    # Non-integer and boolean rejection
    with pytest.raises(TypeError, match="color256 must be an integer"):
        colored("text", color256="196")
    with pytest.raises(TypeError, match="color256 must be an integer"):
        colored("text", color256=12.5)
    with pytest.raises(TypeError, match="color256 must be an integer"):
        colored("text", color256=True)
    with pytest.raises(TypeError, match="color256 must be an integer"):
        colored("text", color256=False)

    # Out of range
    with pytest.raises(ValueError, match="between 0 and 255"):
        colored("text", color256=-1)
    with pytest.raises(ValueError, match="between 0 and 255"):
        colored("text", color256=256)
    with pytest.raises(ValueError, match="between 0 and 255"):
        colored("text", color256=1000)


def test_color_specification_conflicts():
    # Missing all
    with pytest.raises(ValueError, match="A color must be specified"):
        colored("text")

    # Conflicting specifications
    with pytest.raises(ValueError, match="Only one of 'color', 'rgb', or 'color256'"):
        colored("text", "red", rgb=(255, 0, 0))
    with pytest.raises(ValueError, match="Only one of 'color', 'rgb', or 'color256'"):
        colored("text", "red", color256=196)
    with pytest.raises(ValueError, match="Only one of 'color', 'rgb', or 'color256'"):
        colored("text", rgb=(255, 0, 0), color256=196)
    with pytest.raises(ValueError, match="Only one of 'color', 'rgb', or 'color256'"):
        colored("text", "red", rgb=(255, 0, 0), color256=196)

    # Invalid named color type and booleans
    with pytest.raises(TypeError, match="Named color must be a string"):
        colored("text", color=123)
    with pytest.raises(TypeError, match="Named color must be a string"):
        colored("text", color=True)

    # Invalid style type and booleans
    with pytest.raises(TypeError, match="Style must be a string"):
        colored("text", "red", style=123)
    with pytest.raises(TypeError, match="Style must be a string"):
        colored("text", "red", style=True)


def test_print_rgb(capsys):
    enable_color()
    print_rgb((255, 80, 80), "custom red")
    captured = capsys.readouterr()
    assert captured.out == "\033[38;2;255;80;80mcustom red\033[0m\n"

    print_rgb((0, 255, 0), "styled", "green", sep="-", style="bold")
    captured = capsys.readouterr()
    assert captured.out == "\033[1;38;2;0;255;0mstyled-green\033[0m\n"


def test_print_256(capsys):
    enable_color()
    print_256(196, "bright red")
    captured = capsys.readouterr()
    assert captured.out == "\033[38;5;196mbright red\033[0m\n"

    print_256(208, "styled", "orange", sep=" ", style="italic")
    captured = capsys.readouterr()
    assert captured.out == "\033[3;38;5;208mstyled orange\033[0m\n"


def test_rgb_and_256_stream_awareness(monkeypatch):
    reset_color_state()
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")

    non_tty_buf = io.StringIO()
    # non-TTY stream returns plain text in auto mode
    assert (
        colored("rgb text", rgb=(255, 0, 0), stream=non_tty_buf) == "rgb text"
    )
    assert colored("256 text", color256=196, stream=non_tty_buf) == "256 text"

    # print_rgb and print_256 to non-TTY stream
    buf = io.StringIO()
    print_rgb((255, 0, 0), "hello rgb", file=buf, end="")
    assert buf.getvalue() == "hello rgb"

    buf2 = io.StringIO()
    print_256(196, "hello 256", file=buf2, end="")
    assert buf2.getvalue() == "hello 256"


def test_rgb_and_256_no_color_and_force_color(monkeypatch):
    # NO_COLOR disables RGB and 256-color
    monkeypatch.setenv("NO_COLOR", "1")
    reset_color_state()
    assert colored("text", rgb=(255, 0, 0)) == "text"
    assert colored("text", color256=196) == "text"

    # FORCE_COLOR forces RGB and 256-color even on non-TTY
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("FORCE_COLOR", "1")
    reset_color_state()
    non_tty_buf = io.StringIO()
    assert (
        colored("text", rgb=(255, 0, 0), stream=non_tty_buf)
        == "\033[38;2;255;0;0mtext\033[0m"
    )
    assert (
        colored("text", color256=196, stream=non_tty_buf)
        == "\033[38;5;196mtext\033[0m"
    )


def test_rgb_and_256_enable_disable_state():
    reset_color_state()
    non_tty_buf = io.StringIO()

    # enable_color forces output on non-TTY
    enable_color()
    assert (
        colored("text", rgb=(1, 2, 3), stream=non_tty_buf)
        == "\033[38;2;1;2;3mtext\033[0m"
    )
    assert (
        colored("text", color256=42, stream=non_tty_buf)
        == "\033[38;5;42mtext\033[0m"
    )

    # disable_color forces plain text
    disable_color()
    from unittest.mock import MagicMock

    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True
    assert colored("text", rgb=(1, 2, 3), stream=mock_tty) == "text"
    assert colored("text", color256=42, stream=mock_tty) == "text"


def test_package_exports():
    assert termtint.colored is colored
    assert termtint.styled is termtint.core.styled
    assert termtint.enable_color is enable_color
    assert termtint.disable_color is disable_color
    assert termtint.print_red is print_red
    assert termtint.print_rgb is print_rgb
    assert termtint.print_256 is print_256
    assert termtint.Theme is termtint.theme.Theme
    assert termtint.DEFAULT_THEME is termtint.theme.DEFAULT_THEME
    assert termtint.get_theme is termtint.theme.get_theme
    assert termtint.set_theme is termtint.theme.set_theme
    assert termtint.reset_theme is termtint.theme.reset_theme
    assert termtint.__version__ == "0.3.0"



