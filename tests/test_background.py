"""Tests for TermTint background color support across all APIs."""

import io
from unittest.mock import patch

import pytest

from termtint import (
    Style,
    Theme,
    colored,
    enable_color,
    print_256,
    print_blue,
    print_green,
    print_red,
    print_rgb,
    reset_color_state,
    styled,
)


@pytest.fixture(autouse=True)
def setup_color():
    """Ensure color output is enabled for predictable test assertion."""
    enable_color()
    yield
    reset_color_state()


class TestColoredBackground:
    """Test background color features in colored()."""

    def test_named_background_only(self):
        result = colored("hello", bg="blue")
        assert result == "\033[44mhello\033[0m"

    def test_foreground_and_background(self):
        result = colored("hello", "white", bg="red")
        assert result == "\033[37;41mhello\033[0m"

    def test_foreground_background_and_style(self):
        result = colored("alert", "yellow", style="bold", bg="black")
        assert result == "\033[1;33;40malert\033[0m"

    def test_all_standard_background_colors(self):
        expected_codes = {
            "black": "40",
            "red": "41",
            "green": "42",
            "yellow": "43",
            "blue": "44",
            "magenta": "45",
            "cyan": "46",
            "white": "47",
        }
        for name, code in expected_codes.items():
            assert colored("text", bg=name) == f"\033[{code}mtext\033[0m"
            assert colored("text", bg=name.upper()) == f"\033[{code}mtext\033[0m"

    def test_rgb_background(self):
        result = colored("text", bg_rgb=(10, 20, 30))
        assert result == "\033[48;2;10;20;30mtext\033[0m"

        both = colored("text", rgb=(255, 255, 255), bg_rgb=(0, 0, 100))
        assert both == "\033[38;2;255;255;255;48;2;0;0;100mtext\033[0m"

    def test_color256_background(self):
        result = colored("text", bg_color256=198)
        assert result == "\033[48;5;198mtext\033[0m"

        both = colored("text", color256=15, bg_color256=24)
        assert both == "\033[38;5;15;48;5;24mtext\033[0m"

    def test_invalid_background_errors(self):
        with pytest.raises(ValueError, match="Invalid background color 'purple'"):
            colored("text", bg="purple")

        with pytest.raises(TypeError, match="Named background color must be a string"):
            colored("text", bg=123)

        with pytest.raises(TypeError, match="Named background color must be a string"):
            colored("text", bg=True)

        with pytest.raises(
            ValueError, match="Only one of 'bg', 'bg_rgb', or 'bg_color256'"
        ):
            colored("text", bg="red", bg_rgb=(1, 2, 3))

    def test_invalid_bg_rgb_errors(self):
        with pytest.raises(TypeError, match="Background RGB must be a sequence"):
            colored("text", bg_rgb=123)

        with pytest.raises(TypeError, match="Background RGB must be a tuple or list"):
            colored("text", bg_rgb="red")

        with pytest.raises(TypeError, match="Background RGB must be a tuple or list"):
            colored("text", bg_rgb=True)

        with pytest.raises(
            ValueError, match="Background RGB must contain exactly 3 components"
        ):
            colored("text", bg_rgb=(1, 2))

        with pytest.raises(
            ValueError, match="Background RGB must contain exactly 3 components"
        ):
            colored("text", bg_rgb=(1, 2, 3, 4))

        with pytest.raises(
            TypeError, match="Background RGB component at index 0 must be an integer"
        ):
            colored("text", bg_rgb=("255", 0, 0))

        with pytest.raises(
            TypeError, match="Background RGB component at index 1 must be an integer"
        ):
            colored("text", bg_rgb=(255, True, 0))

        with pytest.raises(
            ValueError,
            match="Background RGB component at index 2 must be between 0 and 255",
        ):
            colored("text", bg_rgb=(0, 0, 256))

    def test_invalid_bg_color256_errors(self):
        with pytest.raises(TypeError, match="Background color256 must be an integer"):
            colored("text", bg_color256="100")

        with pytest.raises(TypeError, match="Background color256 must be an integer"):
            colored("text", bg_color256=True)

        with pytest.raises(
            ValueError, match="Background color256 must be between 0 and 255"
        ):
            colored("text", bg_color256=256)

        with pytest.raises(
            ValueError, match="Background color256 must be between 0 and 255"
        ):
            colored("text", bg_color256=-1)


class TestStyledBackground:
    """Test background color features in styled()."""

    def test_styled_named_bg(self):
        res = styled("Header", bg="green", style=["bold", "underline"])
        assert res == "\033[1;4;42mHeader\033[0m"

    def test_styled_fg_and_bg(self):
        res = styled("Warning", color="yellow", bg="red", style="bold")
        assert res == "\033[1;33;41mWarning\033[0m"

    def test_styled_rgb_bg(self):
        res = styled("Custom", bg_rgb=(10, 20, 30))
        assert res == "\033[48;2;10;20;30mCustom\033[0m"

    def test_styled_256_bg(self):
        res = styled("Custom", bg_color256=208)
        assert res == "\033[48;5;208mCustom\033[0m"

    def test_styled_theme_conflict_with_bg(self):
        with pytest.raises(ValueError, match="Cannot specify 'theme' together with"):
            styled("text", theme="success", bg="blue")

        with pytest.raises(ValueError, match="Cannot specify 'theme' together with"):
            styled("text", theme="success", bg_rgb=(1, 2, 3))

        with pytest.raises(ValueError, match="Cannot specify 'theme' together with"):
            styled("text", theme="success", bg_color256=50)

    def test_styled_bg_mutual_exclusivity(self):
        with pytest.raises(
            ValueError, match="Only one of 'bg', 'bg_rgb', or 'bg_color256'"
        ):
            styled("text", bg="blue", bg_color256=12)

    def test_styled_bg_validation_errors(self):
        with pytest.raises(TypeError, match="Named background color must be a string"):
            styled("text", bg=123)

        with pytest.raises(TypeError, match="Named background color must be a string"):
            styled("text", bg=True)

        with pytest.raises(ValueError, match="Invalid background color 'unknown'"):
            styled("text", bg="unknown")

    def test_styled_bg_fallback_truecolor_to_256(self):
        stream = io.StringIO()
        with (
            patch("termtint.core.supports_truecolor", return_value=False),
            patch("termtint.core.supports_256color", return_value=True),
        ):
            res = styled("text", bg_rgb=(255, 0, 0), fallback=True, stream=stream)
            # RGB (255, 0, 0) maps to 256-color index 196
            assert res == "\033[48;5;196mtext\033[0m"

    def test_styled_bg_fallback_truecolor_to_ansi(self):
        stream = io.StringIO()
        with (
            patch("termtint.core.supports_truecolor", return_value=False),
            patch("termtint.core.supports_256color", return_value=False),
        ):
            res = styled("text", bg_rgb=(255, 0, 0), fallback=True, stream=stream)
            # Degrades to red background (ANSI 41)
            assert res == "\033[41mtext\033[0m"

    def test_styled_bg_fallback_256_to_ansi(self):
        stream = io.StringIO()
        with patch("termtint.core.supports_256color", return_value=False):
            res = styled("text", bg_color256=196, fallback=True, stream=stream)
            # Color 196 degrades to red background (ANSI 41)
            assert res == "\033[41mtext\033[0m"


class TestStyleObjectBackground:
    """Test background color features on Style class."""

    def test_style_init_properties(self):
        st = Style(color="white", bg="blue", style="bold")
        assert st.color == "white"
        assert st.bg == "blue"
        assert st.bg_rgb is None
        assert st.bg_color256 is None
        assert st.style == ("bold",)

    def test_style_bg_rgb_properties(self):
        st = Style(bg_rgb=(10, 20, 30))
        assert st.bg is None
        assert st.bg_rgb == (10, 20, 30)
        assert st.bg_color256 is None

    def test_style_bg_color256_properties(self):
        st = Style(bg_color256=142)
        assert st.bg is None
        assert st.bg_rgb is None
        assert st.bg_color256 == 142

    def test_style_with_bg_methods(self):
        base = Style(color="cyan")

        s_bg = base.with_bg("red")
        assert s_bg.bg == "red"
        assert s_bg.color == "cyan"

        s_rgb = s_bg.with_bg_rgb((1, 2, 3))
        assert s_rgb.bg is None
        assert s_rgb.bg_rgb == (1, 2, 3)

        s_256 = s_rgb.with_bg_color256(77)
        assert s_256.bg_rgb is None
        assert s_256.bg_color256 == 77

    def test_style_to_dict(self):
        st = Style(color="green", bg="black", style="bold")
        assert st.to_dict() == {"color": "green", "bg": "black", "style": ["bold"]}

        st_rgb = Style(bg_rgb=(1, 2, 3))
        assert st_rgb.to_dict() == {"bg_rgb": (1, 2, 3)}

        st_256 = Style(bg_color256=100)
        assert st_256.to_dict() == {"bg_color256": 100}

    def test_style_apply_rendering(self):
        st = Style(color="white", bg="magenta")
        assert st.apply("Badge") == "\033[37;45mBadge\033[0m"
        assert st("Badge") == "\033[37;45mBadge\033[0m"

    def test_style_addition_background_override(self):
        s1 = Style(color="white", bg="blue")
        s2 = Style(bg="red", style="bold")

        combined = s1 + s2
        assert combined.color == "white"
        assert combined.bg == "red"
        assert combined.style == ("bold",)

    def test_style_addition_cross_type_background(self):
        s1 = Style(bg="blue")
        s2 = Style(bg_rgb=(10, 20, 30))

        comb = s1 + s2
        assert comb.bg is None
        assert comb.bg_rgb == (10, 20, 30)

        s3 = Style(bg_color256=99)
        comb2 = s2 + s3
        assert comb2.bg_rgb is None
        assert comb2.bg_color256 == 99

    def test_style_repr_and_equality(self):
        st1 = Style(color="red", bg="yellow")
        st2 = Style(color="red", bg="yellow")
        st3 = Style(color="red", bg="blue")

        assert st1 == st2
        assert st1 != st3
        assert hash(st1) == hash(st2)
        assert repr(st1) == "Style(color='red', bg='yellow')"

        st_rgb = Style(bg_rgb=(1, 2, 3))
        assert repr(st_rgb) == "Style(bg_rgb=(1, 2, 3))"

        st_256 = Style(bg_color256=5)
        assert repr(st_256) == "Style(bg_color256=5)"

    def test_style_fallback_rendering(self):
        stream = io.StringIO()
        st = Style(bg_rgb=(255, 0, 0), fallback=True)
        with (
            patch("termtint.style.supports_truecolor", return_value=False),
            patch("termtint.style.supports_256color", return_value=True),
        ):
            assert st.apply("text", stream=stream) == "\033[48;5;196mtext\033[0m"

        with (
            patch("termtint.style.supports_truecolor", return_value=False),
            patch("termtint.style.supports_256color", return_value=False),
        ):
            assert st.apply("text", stream=stream) == "\033[41mtext\033[0m"

        st_256 = Style(bg_color256=196, fallback=True)
        with patch("termtint.style.supports_256color", return_value=False):
            assert st_256.apply("text", stream=stream) == "\033[41mtext\033[0m"


class TestThemeBackground:
    """Test background color features in Theme."""

    def test_theme_role_with_bg(self):
        th = Theme(
            {
                "highlight": {"color": "black", "bg": "yellow", "style": "bold"},
                "badge": {"bg_rgb": (10, 20, 30)},
                "tag": {"bg_color256": 120},
            }
        )

        assert th.styled("Important", "highlight") == "\033[1;30;43mImportant\033[0m"
        assert th.styled("Data", "badge") == "\033[48;2;10;20;30mData\033[0m"
        assert th.styled("Tag", "tag") == "\033[48;5;120mTag\033[0m"

    def test_theme_get_style_with_bg(self):
        th = Theme(
            {
                "badge": {"color": "white", "bg": "blue", "style": "underline"},
            }
        )
        st = th.get_style("badge")
        assert st.color == "white"
        assert st.bg == "blue"
        assert st.style == ("underline",)
        assert st("Click") == "\033[4;37;44mClick\033[0m"

    def test_theme_from_role(self):
        th = Theme({"notice": {"bg": "cyan"}})
        st = Style.from_role("notice", theme=th)
        assert st.bg == "cyan"
        assert st("Info") == "\033[46mInfo\033[0m"

    def test_theme_role_validation_errors(self):
        with pytest.raises(
            ValueError, match="Theme role 'bad' cannot specify more than one of 'bg'"
        ):
            Theme({"bad": {"bg": "red", "bg_rgb": (1, 2, 3)}})

        with pytest.raises(TypeError, match="Role 'bad' bg must be a string"):
            Theme({"bad": {"bg": 123}})

        with pytest.raises(ValueError, match="Invalid background color 'unknown'"):
            Theme({"bad": {"bg": "unknown"}})

    def test_theme_extend_with_bg(self):
        base = Theme({"info": {"color": "blue"}})
        extended = base.extend({"info": {"color": "blue", "bg": "yellow"}})
        assert extended.styled("Note", "info") == "\033[34;43mNote\033[0m"


class TestPrintHelpersBackground:
    """Test print helper functions with background color parameters."""

    def test_print_color_with_bg(self):
        buf = io.StringIO()
        print_green("Success", bg="black", file=buf)
        assert buf.getvalue() == "\033[32;40mSuccess\033[0m\n"

        buf2 = io.StringIO()
        print_red("Danger", style="bold", bg="yellow", file=buf2)
        assert buf2.getvalue() == "\033[1;31;43mDanger\033[0m\n"

        buf3 = io.StringIO()
        print_blue("Info", bg="white", file=buf3)
        assert buf3.getvalue() == "\033[34;47mInfo\033[0m\n"

    def test_print_rgb_with_bg(self):
        buf = io.StringIO()
        print_rgb((255, 255, 255), "TrueColor", bg="blue", file=buf)
        assert buf.getvalue() == "\033[38;2;255;255;255;44mTrueColor\033[0m\n"

        buf2 = io.StringIO()
        print_rgb(
            (255, 255, 255),
            "FullRGB",
            bg_rgb=(0, 0, 128),
            file=buf2,
        )
        assert buf2.getvalue() == "\033[38;2;255;255;255;48;2;0;0;128mFullRGB\033[0m\n"

    def test_print_256_with_bg(self):
        buf = io.StringIO()
        print_256(15, "Palette", bg="black", file=buf)
        assert buf.getvalue() == "\033[38;5;15;40mPalette\033[0m\n"

        buf2 = io.StringIO()
        print_256(15, "Dual256", bg_color256=24, file=buf2)
        assert buf2.getvalue() == "\033[38;5;15;48;5;24mDual256\033[0m\n"


class TestThemeFallbackAndStyleValidation:
    """Test theme role background fallbacks and Style validation branches."""

    def test_theme_bg_fallback_in_styled(self):
        stream = io.StringIO()
        th = Theme(
            {
                "hdr": {"bg": "blue"},
                "rgb_role": {"bg_rgb": (255, 0, 0)},
                "c256_role": {"bg_color256": 196},
            }
        )

        with patch("termtint.theme.get_theme", return_value=th):
            # bg role
            assert styled("Text", theme="hdr") == "\033[44mText\033[0m"

            # bg_rgb with truecolor supported
            with patch("termtint.core.supports_truecolor", return_value=True):
                assert (
                    styled("Text", theme="rgb_role", fallback=True, stream=stream)
                    == "\033[48;2;255;0;0mText\033[0m"
                )

            # bg_rgb with truecolor unsupported, 256color supported
            with (
                patch("termtint.core.supports_truecolor", return_value=False),
                patch("termtint.core.supports_256color", return_value=True),
            ):
                assert (
                    styled("Text", theme="rgb_role", fallback=True, stream=stream)
                    == "\033[48;5;196mText\033[0m"
                )

            # bg_rgb with truecolor unsupported, 256color unsupported
            with (
                patch("termtint.core.supports_truecolor", return_value=False),
                patch("termtint.core.supports_256color", return_value=False),
            ):
                assert (
                    styled("Text", theme="rgb_role", fallback=True, stream=stream)
                    == "\033[41mText\033[0m"
                )

            # bg_color256 with 256color supported
            with patch("termtint.core.supports_256color", return_value=True):
                assert (
                    styled("Text", theme="c256_role", fallback=True, stream=stream)
                    == "\033[48;5;196mText\033[0m"
                )

            # bg_color256 with 256color unsupported
            with patch("termtint.core.supports_256color", return_value=False):
                assert (
                    styled("Text", theme="c256_role", fallback=True, stream=stream)
                    == "\033[41mText\033[0m"
                )

    def test_styled_bg_supported_fallback_paths(self):
        stream = io.StringIO()
        with patch("termtint.core.supports_truecolor", return_value=True):
            res = styled("Text", bg_rgb=(1, 2, 3), fallback=True, stream=stream)
            assert res == "\033[48;2;1;2;3mText\033[0m"

        with patch("termtint.core.supports_256color", return_value=True):
            res2 = styled("Text", bg_color256=45, fallback=True, stream=stream)
            assert res2 == "\033[48;5;45mText\033[0m"

    def test_style_bg_validation_errors(self):
        with pytest.raises(TypeError, match="Named background color must be a string"):
            Style(bg=123)

        with pytest.raises(TypeError, match="Named background color must be a string"):
            Style(bg=True)

        with pytest.raises(ValueError, match="Invalid background color 'bad_color'"):
            Style(bg="bad_color")

        with pytest.raises(
            ValueError, match="Only one of 'bg', 'bg_rgb', or 'bg_color256'"
        ):
            Style(bg="red", bg_color256=10)

    def test_style_theme_bg_fallback_rendering(self):
        stream = io.StringIO()
        th = Theme(
            {
                "hdr": {"bg": "cyan"},
                "rgb_role": {"bg_rgb": (255, 0, 0)},
                "c256_role": {"bg_color256": 196},
            }
        )

        with patch("termtint.theme.get_theme", return_value=th):
            st_hdr = Style(theme="hdr")
            assert st_hdr.apply("Text", stream=stream) == "\033[46mText\033[0m"

            st_rgb = Style(theme="rgb_role", fallback=True)
            with patch("termtint.style.supports_truecolor", return_value=True):
                assert (
                    st_rgb.apply("Text", stream=stream)
                    == "\033[48;2;255;0;0mText\033[0m"
                )

            with (
                patch("termtint.style.supports_truecolor", return_value=False),
                patch("termtint.style.supports_256color", return_value=True),
            ):
                assert (
                    st_rgb.apply("Text", stream=stream) == "\033[48;5;196mText\033[0m"
                )

            with (
                patch("termtint.style.supports_truecolor", return_value=False),
                patch("termtint.style.supports_256color", return_value=False),
            ):
                assert st_rgb.apply("Text", stream=stream) == "\033[41mText\033[0m"

            st_256 = Style(theme="c256_role", fallback=True)
            with patch("termtint.style.supports_256color", return_value=True):
                assert (
                    st_256.apply("Text", stream=stream) == "\033[48;5;196mText\033[0m"
                )

            with patch("termtint.style.supports_256color", return_value=False):
                assert st_256.apply("Text", stream=stream) == "\033[41mText\033[0m"

    def test_style_bg_supported_fallback_paths(self):
        stream = io.StringIO()
        st_rgb = Style(bg_rgb=(10, 20, 30), fallback=True)
        with patch("termtint.style.supports_truecolor", return_value=True):
            assert (
                st_rgb.apply("Text", stream=stream) == "\033[48;2;10;20;30mText\033[0m"
            )

        st_256 = Style(bg_color256=88, fallback=True)
        with patch("termtint.style.supports_256color", return_value=True):
            assert st_256.apply("Text", stream=stream) == "\033[48;5;88mText\033[0m"
