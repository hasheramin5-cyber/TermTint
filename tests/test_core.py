"""Tests for termtint.core module."""

import io

import pytest

import termtint
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
    with pytest.raises(ValueError, match="Invalid style 'italic'"):
        colored("text", "red", style="italic")


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


def test_convenience_print_custom_file():
    enable_color()
    buf = io.StringIO()
    print_red("buffer output", file=buf, end="")
    assert buf.getvalue() == "\033[31mbuffer output\033[0m"


def test_package_exports():
    assert termtint.colored is colored
    assert termtint.enable_color is enable_color
    assert termtint.disable_color is disable_color
    assert termtint.print_red is print_red
    assert termtint.__version__ == "0.1.0"
