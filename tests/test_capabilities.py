"""Tests for terminal capability detection and color conversion helpers."""

from unittest.mock import MagicMock, patch

import pytest

from termtint import (
    color256_to_ansi,
    disable_color,
    enable_color,
    reset_color_state,
    rgb_to_256,
    rgb_to_ansi,
    styled,
    supports_256color,
    supports_color,
    supports_truecolor,
)


@pytest.fixture(autouse=True)
def clean_environment():
    """Ensure clean color state before each test."""
    reset_color_state()
    yield
    reset_color_state()


def test_supports_color_explicit_state():
    enable_color()
    assert supports_color() is True

    disable_color()
    assert supports_color() is False


def test_supports_color_tty_and_no_color():
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True

    mock_nontty = MagicMock()
    mock_nontty.isatty.return_value = False

    with patch.dict("os.environ", {}, clear=True):
        with patch("sys.platform", "linux"):
            assert supports_color(mock_tty) is True
            assert supports_color(mock_nontty) is False

    with patch.dict("os.environ", {"NO_COLOR": "1"}, clear=True):
        assert supports_color(mock_tty) is False


def test_supports_256color():
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True

    # Disabled color means no 256color
    disable_color()
    assert supports_256color(mock_tty) is False
    reset_color_state()

    # FORCE_COLOR=2 or 3
    with patch.dict("os.environ", {"FORCE_COLOR": "2"}, clear=True):
        assert supports_256color(mock_tty) is True
    with patch.dict("os.environ", {"FORCE_COLOR": "3"}, clear=True):
        assert supports_256color(mock_tty) is True

    # COLORTERM=truecolor or 24bit
    with patch.dict("os.environ", {"COLORTERM": "truecolor"}, clear=True):
        assert supports_256color(mock_tty) is True
    with patch.dict("os.environ", {"COLORTERM": "24bit"}, clear=True):
        assert supports_256color(mock_tty) is True

    # TERM containing 256color
    with patch("sys.platform", "linux"):
        with patch.dict("os.environ", {"TERM": "xterm-256color"}, clear=True):
            assert supports_256color(mock_tty) is True
        with patch.dict("os.environ", {"TERM": "screen-256"}, clear=True):
            assert supports_256color(mock_tty) is True

        # Modern known 256-color terminals
        for term in ("xterm-kitty", "alacritty", "foot", "wezterm", "ghostty"):
            with patch.dict("os.environ", {"TERM": term}, clear=True):
                assert supports_256color(mock_tty) is True

        # Basic non-256 terminal on non-windows
        with patch.dict("os.environ", {"TERM": "vt100"}, clear=True):
            assert supports_256color(mock_tty) is False

    # Windows terminal environment checks
    for env in ("WT_SESSION", "ANSICON", "ConEmuANSI"):
        with patch.dict("os.environ", {env: "1"}, clear=True):
            with patch("sys.platform", "win32"):
                assert supports_256color(mock_tty) is True

    # Windows VT mode enable check
    with patch.dict("os.environ", {}, clear=True):
        with patch("sys.platform", "win32"):
            with patch("termtint._detect.enable_vt_mode", return_value=True):
                assert supports_256color(mock_tty) is True
            with patch("termtint._detect.enable_vt_mode", return_value=False):
                assert supports_256color(mock_tty) is False


def test_supports_truecolor():
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True

    # Disabled color means no truecolor
    disable_color()
    assert supports_truecolor(mock_tty) is False
    reset_color_state()

    # FORCE_COLOR=3
    with patch.dict("os.environ", {"FORCE_COLOR": "3"}, clear=True):
        assert supports_truecolor(mock_tty) is True

    # COLORTERM=truecolor or 24bit
    with patch.dict("os.environ", {"COLORTERM": "truecolor"}, clear=True):
        assert supports_truecolor(mock_tty) is True
    with patch.dict("os.environ", {"COLORTERM": "24bit"}, clear=True):
        assert supports_truecolor(mock_tty) is True

    # Known truecolor terminals
    with patch("sys.platform", "linux"):
        truecolor_terms = (
            "xterm-kitty",
            "alacritty",
            "foot",
            "wezterm",
            "ghostty",
            "iterm2",
            "xterm-direct",
        )
        for term in truecolor_terms:
            with patch.dict("os.environ", {"TERM": term}, clear=True):
                assert supports_truecolor(mock_tty) is True

        # Basic terminal on linux
        with patch.dict("os.environ", {"TERM": "xterm-256color"}, clear=True):
            assert supports_truecolor(mock_tty) is False

    # Windows WT_SESSION
    with patch.dict("os.environ", {"WT_SESSION": "1"}, clear=True):
        with patch("sys.platform", "win32"):
            assert supports_truecolor(mock_tty) is True

    # Windows 10 build >= 14393
    mock_winver = MagicMock()
    mock_winver.build = 19045
    with patch.dict("os.environ", {}, clear=True):
        with patch("sys.platform", "win32"):
            with patch("sys.getwindowsversion", return_value=mock_winver):
                with patch("termtint._detect.enable_vt_mode", return_value=True):
                    assert supports_truecolor(mock_tty) is True
                with patch("termtint._detect.enable_vt_mode", return_value=False):
                    assert supports_truecolor(mock_tty) is False

    # Windows older build < 14393
    mock_old_winver = MagicMock()
    mock_old_winver.build = 10240
    with patch.dict("os.environ", {}, clear=True):
        with patch("sys.platform", "win32"):
            with patch("sys.getwindowsversion", return_value=mock_old_winver):
                assert supports_truecolor(mock_tty) is False

    # Windows getwindowsversion exception
    enable_color()
    with patch.dict("os.environ", {}, clear=True):
        with patch("sys.platform", "win32"):
            with patch("sys.getwindowsversion", side_effect=RuntimeError):
                assert supports_truecolor(mock_tty) is False
    reset_color_state()


def test_rgb_to_ansi():
    assert rgb_to_ansi((255, 0, 0)) == "red"
    assert rgb_to_ansi((0, 255, 0)) == "green"
    assert rgb_to_ansi((0, 0, 255)) == "blue"
    assert rgb_to_ansi((255, 255, 0)) == "yellow"
    assert rgb_to_ansi((255, 0, 255)) == "magenta"
    assert rgb_to_ansi((0, 255, 255)) == "cyan"
    assert rgb_to_ansi((0, 0, 0)) == "black"
    assert rgb_to_ansi((255, 255, 255)) == "white"

    # Validation errors
    with pytest.raises(TypeError):
        rgb_to_ansi(True)
    with pytest.raises(TypeError):
        rgb_to_ansi((255, "0", 0))
    with pytest.raises(ValueError):
        rgb_to_ansi((255, 0))
    with pytest.raises(ValueError):
        rgb_to_ansi((300, 0, 0))


def test_rgb_to_256():
    # Primary colors in color cube
    assert rgb_to_256((255, 0, 0)) == 196
    assert rgb_to_256((0, 255, 0)) == 46
    assert rgb_to_256((0, 0, 255)) == 21

    # Grayscale
    assert rgb_to_256((0, 0, 0)) == 16
    assert rgb_to_256((255, 255, 255)) == 231
    assert 232 <= rgb_to_256((128, 128, 128)) <= 255

    # Validation errors
    with pytest.raises(TypeError):
        rgb_to_256("rgb")
    with pytest.raises(TypeError):
        rgb_to_256((10, False, 30))
    with pytest.raises(ValueError):
        rgb_to_256((-1, 0, 0))


def test_color256_to_ansi():
    # 0-7 standard
    assert color256_to_ansi(0) == "black"
    assert color256_to_ansi(1) == "red"
    assert color256_to_ansi(2) == "green"
    assert color256_to_ansi(3) == "yellow"
    assert color256_to_ansi(4) == "blue"
    assert color256_to_ansi(5) == "magenta"
    assert color256_to_ansi(6) == "cyan"
    assert color256_to_ansi(7) == "white"

    # 8-15 bright
    assert color256_to_ansi(8) == "black"
    assert color256_to_ansi(9) == "red"
    assert color256_to_ansi(10) == "green"
    assert color256_to_ansi(11) == "yellow"
    assert color256_to_ansi(12) == "blue"
    assert color256_to_ansi(13) == "magenta"
    assert color256_to_ansi(14) == "cyan"
    assert color256_to_ansi(15) == "white"

    # 16-231 cube
    assert color256_to_ansi(196) == "red"
    assert color256_to_ansi(46) == "green"
    assert color256_to_ansi(21) == "blue"

    # 232-255 grayscale
    assert color256_to_ansi(232) == "black"
    assert color256_to_ansi(255) == "white"

    # Validation errors
    with pytest.raises(TypeError):
        color256_to_ansi(False)
    with pytest.raises(TypeError):
        color256_to_ansi("100")
    with pytest.raises(ValueError):
        color256_to_ansi(-1)
    with pytest.raises(ValueError):
        color256_to_ansi(256)


def test_styled_smart_fallback():
    enable_color()
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True

    # 1. TrueColor supported: no downgrade
    with patch("termtint.core.supports_truecolor", return_value=True):
        res = styled("Text", rgb=(255, 0, 0), fallback=True, stream=mock_tty)
        assert "\033[38;2;255;0;0m" in res

    # 2. TrueColor unsupported, 256-color supported: downgrade to 256
    with patch("termtint.core.supports_truecolor", return_value=False):
        with patch("termtint.core.supports_256color", return_value=True):
            res = styled("Text", rgb=(255, 0, 0), fallback=True, stream=mock_tty)
            assert "\033[38;5;196m" in res

    # 3. Neither supported: downgrade to 16-color ANSI "red" -> 31
    with patch("termtint.core.supports_truecolor", return_value=False):
        with patch("termtint.core.supports_256color", return_value=False):
            res = styled("Text", rgb=(255, 0, 0), fallback=True, stream=mock_tty)
            assert "\033[31m" in res

    # 4. color256 with 256 unsupported: downgrade to 16-color ANSI
    with patch("termtint.core.supports_256color", return_value=False):
        res = styled("Text", color256=196, fallback=True, stream=mock_tty)
        assert "\033[31m" in res

    # 5. Theme with RGB and fallback
    from termtint import Theme, reset_theme, set_theme
    custom_brand = Theme(brand={"rgb": (0, 122, 255), "style": "bold"})
    set_theme(custom_brand)
    try:
        with patch("termtint.core.supports_truecolor", return_value=False):
            with patch("termtint.core.supports_256color", return_value=True):
                res = styled("Brand", theme="brand", fallback=True, stream=mock_tty)
                assert "38;5;" in res

        with patch("termtint.core.supports_truecolor", return_value=False):
            with patch("termtint.core.supports_256color", return_value=False):
                res = styled("Brand", theme="brand", fallback=True, stream=mock_tty)
                assert ";36m" in res or "\033[36m" in res
    finally:
        reset_theme()

    # 6. Theme with color256 and fallback
    custom_theme = Theme(badge={"color256": 196})
    set_theme(custom_theme)
    try:
        with patch("termtint.core.supports_256color", return_value=False):
            res = styled("Badge", theme="badge", fallback=True, stream=mock_tty)
            assert "\033[31m" in res
    finally:
        reset_theme()

    # 7. Fallback argument validation
    with pytest.raises(TypeError):
        styled("Text", color="red", fallback="not_a_bool")

    # 8. Positional stream as 7th argument
    res = styled("Text", "red", None, None, None, None, mock_tty)
    assert "\033[31m" in res
