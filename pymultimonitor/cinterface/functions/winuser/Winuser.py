import ctypes
from ctypes.wintypes import RECT

MonitorEnumProc = ctypes.WINFUNCTYPE(
    ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_double
)
