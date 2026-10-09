"""Tests for termtint.style.Style class."""

import io
from unittest.mock import MagicMock, patch

import pytest

from termtint import (
    Style,
    Theme,
    enable_color,
    reset_color_state,
    reset_theme,
    set_theme,
)


@pytest.fixture(autouse=True)
def clean_environment():
    """Reset color state and themes before each test."""
    enable_color()
    reset_theme()
    yield
    reset_color_state()
    reset_theme()


def test_style_init_and_properties():
    # Basic named color + single style
    s1 = Style(color="green", style="bold")
    assert s1.color == "green"
    assert s1.style == ("bold",)
    assert s1.rgb is None
    assert s1.color256 is None
    assert s1.theme is None
    assert s1.fallback is False

    # RGB
    s2 = Style(rgb=(10, 20, 30), style=["italic", "underline"])
    assert s2.color is None
    assert s2.rgb == (10, 20, 30)
    assert s2.style == ("italic", "underline")

    # 256 color
    s3 = Style(color256=196, style="bold, reverse")
    assert s3.color256 == 196
    assert s3.style == ("bold", "reverse")

    # Empty
    s4 = Style()
    assert s4.color is None
    assert s4.style == ()

    # Theme
    s5 = Style(theme="success", fallback=True)
    assert s5.theme == "success"
    assert s5.fallback is True


def test_style_apply_and_call():
    s = Style(color="red", style="bold")
    formatted = s.apply("Alert")
    assert "\033[1;31mAlert\033[0m" == formatted

    # Calling instance directly
    assert s("Alert") == formatted

    # Stream without color
    reset_color_state()
    mock_nontty = MagicMock()
    mock_nontty.isatty.return_value = False
    assert s.apply("Alert", stream=mock_nontty) == "Alert"
    enable_color()


def test_style_composable_methods():
    base = Style(color="blue")
    assert base.style == ()

    s_bold = base.bold()
    assert s_bold.style == ("bold",)
    assert base.style == ()  # immutability check

    s_italic = s_bold.italic()
    assert s_italic.style == ("bold", "italic")

    s_under = s_italic.underline()
    assert s_under.style == ("bold", "italic", "underline")

    s_rev = s_under.reverse()
    assert s_rev.style == ("bold", "italic", "underline", "reverse")

    s_strike = s_rev.strikethrough()
    assert s_strike.style == (
        "bold", "italic", "underline", "reverse", "strikethrough"
    )

    s_dim = s_strike.dim()
    assert s_dim.style == (
        "bold", "italic", "underline", "reverse", "strikethrough", "dim"
    )

    # Calling method when style already exists does not duplicate
    s_bold_again = s_bold.bold()
    assert s_bold_again.style == ("bold",)


def test_style_modifier_helpers():
    s = Style(color="red", style="bold")

    # with_color
    s2 = s.with_color("green")
    assert s2.color == "green"
    assert s2.style == ("bold",)

    # with_rgb
    s3 = s.with_rgb((1, 2, 3))
    assert s3.rgb == (1, 2, 3)
    assert s3.color is None

    # with_color256
    s4 = s.with_color256(42)
    assert s4.color256 == 42
    assert s4.color is None

    # with_theme
    s_theme = s.with_theme("success")
    assert s_theme.theme == "success"
    assert s_theme.color is None

    # with_style
    s5 = s.with_style(["italic", "dim"])
    assert s5.style == ("italic", "dim")

    # with_fallback
    s6 = s.with_fallback(True)
    assert s6.fallback is True

    # to_dict
    assert s.to_dict() == {"color": "red", "style": ["bold"]}
    assert Style(rgb=(1, 2, 3)).to_dict() == {"rgb": (1, 2, 3)}
    assert Style(color256=10).to_dict() == {"color256": 10}
    assert Style().to_dict() == {}


def test_style_addition():
    s1 = Style(color="green", style="bold")
    s2 = Style(color="red", style="underline")

    # s1 + s2: s2 overrides color, styles are combined
    combined = s1 + s2
    assert combined.color == "red"
    assert combined.style == ("bold", "underline")

    # s2 + s1: s1 overrides color
    combined2 = s2 + s1
    assert combined2.color == "green"
    assert combined2.style == ("underline", "bold")

    # cross-type addition: named + RGB
    s_rgb = Style(rgb=(10, 20, 30))
    comb_rgb = s1 + s_rgb
    assert comb_rgb.color is None
    assert comb_rgb.rgb == (10, 20, 30)
    assert comb_rgb.style == ("bold",)

    # cross-type addition: named + 256
    s_256 = Style(color256=198)
    comb_256 = s1 + s_256
    assert comb_256.color is None
    assert comb_256.color256 == 198

    # cross-type addition: theme + named
    s_th = Style(theme="success")
    comb_th = s_th + s1
    assert comb_th.theme is None
    assert comb_th.color == "green"

    # cross-type addition: named + theme
    comb_th2 = s1 + s_th
    assert comb_th2.color is None
    assert comb_th2.theme == "success"

    # addition when other has only style (no color or theme)
    comb_pure = s1 + Style(style="italic")
    assert comb_pure.color == "green"
    assert comb_pure.style == ("bold", "italic")

    # invalid addition
    with pytest.raises(TypeError):
        _ = s1 + "not_a_style"


def test_style_repr_and_equality():
    s1 = Style(color="red", style="bold", fallback=True)
    s2 = Style(color="red", style="bold", fallback=True)
    s3 = Style(color="blue", style="bold")

    assert s1 == s2
    assert s1 != s3
    assert s1 != "not_a_style"

    # Hashable
    style_set = {s1, s2, s3}
    assert len(style_set) == 2

    # Repr
    repr_str = repr(s1)
    assert "color='red'" in repr_str
    assert "style=['bold']" in repr_str
    assert "fallback=True" in repr_str

    repr_rgb = repr(Style(rgb=(1, 2, 3)))
    assert "rgb=(1, 2, 3)" in repr_rgb

    repr_256 = repr(Style(color256=196))
    assert "color256=196" in repr_256

    repr_theme = repr(Style(theme="success"))
    assert "theme='success'" in repr_theme


def test_style_validation_errors():
    # Invalid fallback type
    with pytest.raises(TypeError):
        Style(color="red", fallback="true")

    # Invalid theme type
    with pytest.raises(TypeError):
        Style(theme=123)

    # Theme with color/rgb/color256
    with pytest.raises(ValueError):
        Style(theme="success", color="red")
    with pytest.raises(ValueError):
        Style(theme="success", rgb=(1, 2, 3))
    with pytest.raises(ValueError):
        Style(theme="success", color256=10)

    # Conflicting colors
    with pytest.raises(ValueError):
        Style(color="red", rgb=(1, 2, 3))
    with pytest.raises(ValueError):
        Style(color="red", color256=10)
    with pytest.raises(ValueError):
        Style(rgb=(1, 2, 3), color256=10)

    # Invalid color types and values
    with pytest.raises(TypeError):
        Style(color=True)
    with pytest.raises(TypeError):
        Style(color=123)
    with pytest.raises(ValueError):
        Style(color="neon_pink")

    # Invalid RGB
    with pytest.raises(TypeError):
        Style(rgb=True)
    with pytest.raises(ValueError):
        Style(rgb=(1, 2))

    # Invalid color256
    with pytest.raises(TypeError):
        Style(color256=True)
    with pytest.raises(ValueError):
        Style(color256=300)

    # Invalid style
    with pytest.raises(TypeError):
        Style(style=True)
    with pytest.raises(ValueError):
        Style(style="sparkly")


def test_style_print():
    mock_file = io.StringIO()
    mock_file.isatty = lambda: True

    s = Style(color="yellow", style="bold")
    s.print("Message", file=mock_file)

    output = mock_file.getvalue()
    assert "\033[1;33mMessage\033[0m\n" == output

    # Empty print writes newline
    empty_file = io.StringIO()
    s.print(file=empty_file)
    assert empty_file.getvalue() == "\n"

    # Flush parameter
    flush_mock = MagicMock()
    flush_mock.isatty.return_value = True
    s.print("Test", file=flush_mock, flush=True)
    flush_mock.flush.assert_called_once()


def test_style_theme_integration():
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True

    # Style from role
    s_success = Style.from_role("success")
    assert s_success.color == "green"
    assert "bold" in s_success.style
    assert "\033[1;32mDone\033[0m" == s_success("Done", stream=mock_tty)

    # Theme accepting Style instances
    custom_theme = Theme(
        ok=Style(color="green", style="bold"),
        fail=Style(color="red", style="underline"),
    )
    assert custom_theme.get_role("ok") == {"color": "green", "style": ["bold"]}

    # Theme.get_style
    style_fail = custom_theme.get_style("fail")
    assert style_fail.color == "red"
    assert style_fail.style == ("underline",)

    # Theme.get_style with unknown role
    with pytest.raises(KeyError):
        custom_theme.get_style("unknown")

    # Style(theme="...")
    st_role = Style(theme="error")
    assert "\033[1;31mFailed\033[0m" == st_role("Failed", stream=mock_tty)

    # Style(theme="...") with custom theme instance
    custom_theme_obj = Theme(notice=Style(color="magenta", style="italic"))
    st_from_custom = Style.from_role("notice", theme=custom_theme_obj)
    assert st_from_custom.color == "magenta"
    assert st_from_custom.style == ("italic",)


def test_style_fallback():
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True

    s_rgb = Style(rgb=(255, 0, 0), fallback=True)

    # When truecolor is not supported but 256color is:
    with patch("termtint.style.supports_truecolor", return_value=False):
        with patch("termtint.style.supports_256color", return_value=True):
            res = s_rgb.apply("Red", stream=mock_tty)
            assert "\033[38;5;196m" in res

    # When neither truecolor nor 256color is supported:
    with patch("termtint.style.supports_truecolor", return_value=False):
        with patch("termtint.style.supports_256color", return_value=False):
            res = s_rgb.apply("Red", stream=mock_tty)
            assert "\033[31m" in res

    # Style with 256color and fallback
    s_256 = Style(color256=196, fallback=True)
    with patch("termtint.style.supports_256color", return_value=False):
        res = s_256.apply("Red", stream=mock_tty)
        assert "\033[31m" in res

    # Style with theme having RGB and fallback
    theme_rgb = Theme(brand={"rgb": (0, 122, 255), "style": "bold"})
    set_theme(theme_rgb)
    s_theme = Style(theme="brand", fallback=True)
    with patch("termtint.style.supports_truecolor", return_value=False):
        with patch("termtint.style.supports_256color", return_value=True):
            res = s_theme.apply("Brand", stream=mock_tty)
            assert "38;5;" in res

    with patch("termtint.style.supports_truecolor", return_value=False):
        with patch("termtint.style.supports_256color", return_value=False):
            res = s_theme.apply("Brand", stream=mock_tty)
            assert ";36m" in res or "\033[36m" in res

    # Style with theme having color256 and fallback
    theme_256 = Theme(notice={"color256": 196})
    set_theme(theme_256)
    s_theme_256 = Style(theme="notice", fallback=True)
    with patch("termtint.style.supports_256color", return_value=False):
        res = s_theme_256.apply("Notice", stream=mock_tty)
        assert "\033[31m" in res


def test_style_direct_rgb_and_256_no_fallback():
    # Comma inside sequence item
    s_comma_seq = Style(style=["bold, italic", "underline"])
    assert s_comma_seq.style == ("bold", "italic", "underline")

    # RGB without fallback
    s_rgb_direct = Style(rgb=(10, 20, 30), fallback=False)
    assert "\033[38;2;10;20;30m" in s_rgb_direct.apply("RGB")

    # 256color without fallback
    s_256_direct = Style(color256=100, fallback=False)
    assert "\033[38;5;100m" in s_256_direct.apply("256")

    # Theme role with RGB without fallback
    t_rgb = Theme(glow={"rgb": (50, 100, 150)})
    set_theme(t_rgb)
    s_t_rgb = Style(theme="glow", fallback=False)
    assert "\033[38;2;50;100;150m" in s_t_rgb.apply("Glow")

    # Theme role with color256 without fallback
    t_256 = Theme(badge={"color256": 120})
    set_theme(t_256)
    s_t_256 = Style(theme="badge", fallback=False)
    assert "\033[38;5;120m" in s_t_256.apply("Badge")

    # Theme role with list of styles
    t_multi = Theme(shout={"style": ["bold", "underline"]})
    set_theme(t_multi)
    s_t_multi = Style(theme="shout")
    assert "\033[1;4m" in s_t_multi.apply("Shout")
