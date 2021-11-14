import ctypes
from ctypes.wintypes import HANDLE, WCHAR


class PHYSICAL_MONITOR(ctypes.Structure):
    """https://docs.microsoft.com/en-us/windows/win32/api/physicalmonitorenumerationapi/ns-physicalmonitorenumerationapi-physical_monitor"""

    _fields_ = [
        ("hPhysicalMonitor", HANDLE),
        ("szPhysicalMonitorDescription", WCHAR * 128),
    ]
