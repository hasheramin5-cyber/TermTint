"""Tests for termtint._detect and termtint._windows modules."""

import io
import sys
from unittest.mock import MagicMock, patch

import pytest

from termtint._detect import (
    ColorState,
    _detect_color_support,
    get_color_state,
    reset_color_state,
    set_color_state,
    should_color,
)
from termtint._windows import enable_vt_mode


@pytest.fixture(autouse=True)
def reset_detection_state():
    """Reset color detection state before and after each test."""
    reset_color_state()
    yield
    reset_color_state()


def test_color_state_management():
    assert get_color_state() == ColorState.AUTO

    set_color_state(ColorState.ENABLED)
    assert get_color_state() == ColorState.ENABLED
    assert should_color() is True

    set_color_state(ColorState.DISABLED)
    assert get_color_state() == ColorState.DISABLED
    assert should_color() is False

    reset_color_state()
    assert get_color_state() == ColorState.AUTO


def test_no_color_environment(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    reset_color_state()
    assert should_color() is False

    # Empty string should not disable color
    monkeypatch.setenv("NO_COLOR", "")
    reset_color_state()
    with patch("termtint._detect._detect_color_support", return_value=True):
        assert should_color() is True


def test_force_color_environment(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("FORCE_COLOR", "1")
    reset_color_state()
    assert should_color() is True

    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.setenv("CLICOLOR_FORCE", "1")
    reset_color_state()
    assert should_color() is True


def test_non_tty_stream():
    stream = io.StringIO()  # StringIO is non-TTY
    assert should_color(stream) is False


def test_term_dumb_environment(monkeypatch):
    monkeypatch.setenv("TERM", "dumb")
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True
    assert _detect_color_support(mock_tty) is False


def test_windows_environment_detection(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setattr(sys, "platform", "win32")
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True

    # When Windows Terminal env is present
    monkeypatch.setenv("WT_SESSION", "abc-123")
    assert _detect_color_support(mock_tty) is True

    monkeypatch.delenv("WT_SESSION")
    monkeypatch.setenv("ANSICON", "1")
    assert _detect_color_support(mock_tty) is True


def test_enable_vt_mode_non_windows(monkeypatch):
    monkeypatch.setattr(sys, "platform", "linux")
    assert enable_vt_mode() is False


def test_enable_vt_mode_windows_exception(monkeypatch):
    monkeypatch.setattr(sys, "platform", "win32")
    get_handle_path = "ctypes.windll.kernel32.GetStdHandle"
    with patch(get_handle_path, side_effect=Exception("ctypes error")):
        assert enable_vt_mode() is False
