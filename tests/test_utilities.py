import pytest

from termtint import (
    Style,
    colored,
    enable_color,
    reset_color_state,
    strip_ansi,
    styled,
    visible_len,
)


@pytest.fixture(autouse=True)
def setup_color():
    """Ensure color output is enabled for predictable test assertions."""
    enable_color()
    yield
    reset_color_state()


def test_strip_ansi_plain_text():
    """Verify strip_ansi leaves plain text untouched."""
    assert strip_ansi("hello world") == "hello world"
    assert strip_ansi("") == ""
    assert strip_ansi("12345") == "12345"


def test_strip_ansi_colored():
    """Verify strip_ansi removes standard ANSI color escapes."""
    red_text = colored("error", "red")
    assert red_text != "error"
    assert strip_ansi(red_text) == "error"

    green_bold = colored("success", "green", style="bold")
    assert strip_ansi(green_bold) == "success"


def test_strip_ansi_rgb_and_256():
    """Verify strip_ansi removes RGB and 256-color codes."""
    rgb_text = colored("truecolor", rgb=(255, 128, 64))
    assert strip_ansi(rgb_text) == "truecolor"

    c256_text = colored("palette", color256=198)
    assert strip_ansi(c256_text) == "palette"


def test_strip_ansi_styled_and_themes():
    """Verify strip_ansi strips output from styled and Style."""
    st = styled("Header", color="cyan", style=["bold", "underline"])
    assert strip_ansi(st) == "Header"

    style_obj = Style(color="yellow", style="dim", bg="blue")
    rendered = style_obj.apply("Notice")
    assert strip_ansi(rendered) == "Notice"


def test_strip_ansi_interspersed():
    """Verify stripping when multiple ANSI codes are interspersed with text."""
    mixed = (
        colored("Part1", "red")
        + " and "
        + colored("Part2", "blue")
        + " with "
        + styled("Part3", style="bold")
    )
    assert strip_ansi(mixed) == "Part1 and Part2 with Part3"


def test_strip_ansi_non_strings():
    """Verify strip_ansi handles non-string inputs properly."""
    assert strip_ansi(12345) == "12345"
    assert strip_ansi(True) == "True"
    assert strip_ansi(None) == "None"


def test_strip_ansi_osc_sequences():
    """Verify OSC escape sequences like hyperlinks are stripped."""
    hyperlink = "\x1b]8;;https://example.com\x1b\\Click Here\x1b]8;;\x1b\\"
    assert strip_ansi(hyperlink) == "Click Here"


def test_visible_len():
    """Verify visible_len computes character length ignoring ANSI codes."""
    assert visible_len("hello") == 5
    assert visible_len("") == 0
    assert visible_len(123) == 3

    colored_text = colored("Hello World", "red")
    assert visible_len(colored_text) == 11

    styled_text = styled("Test", color="green", style=["bold", "underline"], bg="red")
    assert visible_len(styled_text) == 4


def test_visible_len_padding_alignment():
    """Verify visible_len enables correct terminal column padding and alignment."""
    item1 = colored("OK", "green")
    item2 = colored("FAILED", "red")

    width = 10
    pad1 = " " * (width - visible_len(item1))
    pad2 = " " * (width - visible_len(item2))

    col1 = f"Status: [{item1}{pad1}]"
    col2 = f"Status: [{item2}{pad2}]"

    # Stripped lengths must be identical
    assert visible_len(col1) == visible_len(col2)
    assert strip_ansi(col1) == "Status: [OK        ]"
    assert strip_ansi(col2) == "Status: [FAILED    ]"
