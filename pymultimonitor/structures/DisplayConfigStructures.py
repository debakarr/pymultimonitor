import ctypes
from ctypes.wintypes import (
    UINT,
    DWORD,
    LONG,
    BOOL,
    POINTL,
    LARGE_INTEGER,
    WCHAR,
    USHORT,
)


class DISPLAYCONFIG_RATIONAL(ctypes.Structure):
    _fields_ = [
        ("Numerator", UINT),
        ("Denominator", UINT),
    ]


class LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", DWORD),
        ("HighPart", LONG),
    ]


class DISPLAYCONFIG_PATH_SOURCE_INFO(ctypes.Structure):
    _fields_ = [
        ("adapterId", LUID),
        ("id", UINT),
        ("modeInfoIdx", UINT),
        ("statusFlags", UINT),
    ]


class DISPLAYCONFIG_PATH_TARGET_INFO(ctypes.Structure):
    _fields_ = [
        ("adapterId", LUID),
        ("id", UINT),
        ("modeInfoIdx", UINT),
        ("outputTechnology", UINT),
        ("rotation", UINT),
        ("scaling", UINT),
        ("refreshRate", DISPLAYCONFIG_RATIONAL),
        ("scanLineOrdering", UINT),
        ("targetAvailable", BOOL),
        ("statusFlags", UINT),
    ]


class DISPLAYCONFIG_PATH_INFO(ctypes.Structure):
    _fields_ = [
        ("sourceInfo", DISPLAYCONFIG_PATH_SOURCE_INFO),
        ("targetInfo", DISPLAYCONFIG_PATH_TARGET_INFO),
        ("statusFlags", UINT),
    ]


class DISPLAYCONFIG_2DREGION(ctypes.Structure):
    _fields_ = [
        ("cx", UINT),
        ("cz", UINT),
    ]


class DISPLAYCONFIG_VIDEO_SIGNAL_INFO(ctypes.Structure):
    _fields_ = [
        ("pixelRate", LARGE_INTEGER),
        ("hSyncFreq", DISPLAYCONFIG_RATIONAL),
        ("vSyncFreq", DISPLAYCONFIG_RATIONAL),
        ("activeSize", DISPLAYCONFIG_2DREGION),
        ("totalSize", DISPLAYCONFIG_2DREGION),
        ("videoStandard", UINT),  # union with AdditionalSignalInfo ignored
        ("scanLineOrdering", UINT),
    ]


class DISPLAYCONFIG_SOURCE_MODE(ctypes.Structure):
    _fields_ = [
        ("width", UINT),
        ("height", UINT),
        ("pixelFormat", UINT),
        ("position", POINTL),
    ]


class DISPLAYCONFIG_MODE_INFO_DUMMYUNIONNAME(ctypes.Union):
    _fields_ = [
        ("target", DISPLAYCONFIG_VIDEO_SIGNAL_INFO),
        ("sourceMode", DISPLAYCONFIG_SOURCE_MODE),
        # desktopImageInfo if union ignored
    ]


class DISPLAYCONFIG_MODE_INFO(ctypes.Structure):
    _fields_ = [
        ("infoType", UINT),
        ("id", UINT),
        ("adapterId", LUID),
        ("mode", DISPLAYCONFIG_MODE_INFO_DUMMYUNIONNAME),
    ]


class DISPLAYCONFIG_DEVICE_INFO_HEADER(ctypes.Structure):
    _fields_ = [
        ("type", UINT),
        ("size", UINT),
        ("adapterId", LUID),
        ("id", UINT),
    ]


class DISPLAYCONFIG_SOURCE_DEVICE_NAME(ctypes.Structure):
    _fields_ = [
        ("header", DISPLAYCONFIG_DEVICE_INFO_HEADER),
        ("viewGdiDeviceName", WCHAR * 32),
    ]


class DISPLAYCONFIG_TARGET_DEVICE_NAME(ctypes.Structure):
    _fields_ = [
        ("header", DISPLAYCONFIG_DEVICE_INFO_HEADER),
        ("flags", UINT),
        ("outputTechnology", UINT),
        ("edidManufactureId", USHORT),
        ("edidProductCodeId", USHORT),
        ("connectorInstance", UINT),
        ("monitorFriendlyDeviceName", WCHAR * 64),
        ("monitorDevicePath", WCHAR * 128),
    ]
