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


def test_non_tty_stream(monkeypatch):
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.delenv("CLICOLOR_FORCE", raising=False)
    stream = io.StringIO()  # StringIO is non-TTY
    assert should_color(stream) is False


def test_term_dumb_environment(monkeypatch):
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.delenv("CLICOLOR_FORCE", raising=False)
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
    import ctypes
    monkeypatch.setattr(sys, "platform", "win32")
    mock_kernel32 = MagicMock()
    mock_kernel32.GetStdHandle.side_effect = Exception("ctypes error")
    mock_windll = MagicMock()
    mock_windll.kernel32 = mock_kernel32

    mock_wintypes = MagicMock()
    monkeypatch.setattr(ctypes, "windll", mock_windll, raising=False)
    monkeypatch.setattr(ctypes, "wintypes", mock_wintypes, raising=False)
    monkeypatch.setitem(sys.modules, "ctypes.wintypes", mock_wintypes)

    assert enable_vt_mode() is False


def test_enable_vt_mode_windows_success(monkeypatch):
    import ctypes
    monkeypatch.setattr(sys, "platform", "win32")
    mock_kernel32 = MagicMock()
    mock_kernel32.GetStdHandle.return_value = 1
    mock_kernel32.GetConsoleMode.return_value = True
    mock_kernel32.SetConsoleMode.return_value = True
    mock_windll = MagicMock()
    mock_windll.kernel32 = mock_kernel32

    mock_wintypes = MagicMock()
    monkeypatch.setattr(ctypes, "windll", mock_windll, raising=False)
    monkeypatch.setattr(ctypes, "wintypes", mock_wintypes, raising=False)
    monkeypatch.setitem(sys.modules, "ctypes.wintypes", mock_wintypes)
    monkeypatch.setattr(ctypes, "byref", lambda x: x)

    assert enable_vt_mode() is True


def test_cached_auto_result_sys_stdout(monkeypatch):
    reset_color_state()
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("FORCE_COLOR", "1")
    # First call caches the auto result for sys.stdout
    assert should_color() is True
    # Second call hits the cached branch
    assert should_color() is True


def test_detect_non_windows_platform(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.delenv("CLICOLOR_FORCE", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setattr(sys, "platform", "linux")
    mock_tty = MagicMock()
    mock_tty.isatty.return_value = True
    assert _detect_color_support(mock_tty) is True


def test_enable_vt_mode_windows_invalid_handles(monkeypatch):
    import ctypes

    monkeypatch.setattr(sys, "platform", "win32")
    mock_kernel32 = MagicMock()
    mock_kernel32.GetStdHandle.return_value = 0
    mock_windll = MagicMock()
    mock_windll.kernel32 = mock_kernel32
    monkeypatch.setattr(ctypes, "windll", mock_windll, raising=False)

    assert enable_vt_mode() is False

    mock_kernel32.GetStdHandle.return_value = -1
    assert enable_vt_mode() is False


def test_enable_vt_mode_windows_get_console_mode_failure(monkeypatch):
    import ctypes

    monkeypatch.setattr(sys, "platform", "win32")
    mock_kernel32 = MagicMock()
    mock_kernel32.GetStdHandle.return_value = 1
    mock_kernel32.GetConsoleMode.return_value = False
    mock_windll = MagicMock()
    mock_windll.kernel32 = mock_kernel32
    mock_wintypes = MagicMock()
    monkeypatch.setattr(ctypes, "windll", mock_windll, raising=False)
    monkeypatch.setattr(ctypes, "wintypes", mock_wintypes, raising=False)
    monkeypatch.setitem(sys.modules, "ctypes.wintypes", mock_wintypes)
    monkeypatch.setattr(ctypes, "byref", lambda x: x)

    assert enable_vt_mode() is False


def test_enable_vt_mode_windows_set_console_mode_failure(monkeypatch):
    import ctypes

    monkeypatch.setattr(sys, "platform", "win32")
    mock_kernel32 = MagicMock()
    mock_kernel32.GetStdHandle.return_value = 1
    mock_kernel32.GetConsoleMode.return_value = True
    mock_kernel32.SetConsoleMode.return_value = False
    mock_windll = MagicMock()
    mock_windll.kernel32 = mock_kernel32
    mock_wintypes = MagicMock()
    monkeypatch.setattr(ctypes, "windll", mock_windll, raising=False)
    monkeypatch.setattr(ctypes, "wintypes", mock_wintypes, raising=False)
    monkeypatch.setitem(sys.modules, "ctypes.wintypes", mock_wintypes)
    monkeypatch.setattr(ctypes, "byref", lambda x: x)

    assert enable_vt_mode() is False

