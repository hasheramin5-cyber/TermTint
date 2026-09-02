"""Windows console Virtual Terminal processing support."""

import sys


def enable_vt_mode() -> bool:
    """Enable Virtual Terminal Processing on Windows 10/11 console.

    Returns:
        bool: True if VT processing was successfully enabled or supported,
              False otherwise.
    """
    if sys.platform != "win32":
        return False

    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32

        # Win32 Constants
        STD_OUTPUT_HANDLE = -11
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

        handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        if handle == 0 or handle == -1:
            return False

        mode = wintypes.DWORD()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False

        new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
        if kernel32.SetConsoleMode(handle, new_mode):
            return True
        return False
    except Exception:
        return False
