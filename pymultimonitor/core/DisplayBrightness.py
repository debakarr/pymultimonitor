import ctypes
from ctypes.wintypes import DWORD

from pymultimonitor.output.Brightness import Brightness
from pymultimonitor.output.PhysicalMonitor import PhysicalMonitor


class DisplayBrightness:
    @classmethod
    def get_display_brightness_for_monitor(cls, monitor: PhysicalMonitor) -> Brightness:
        minimum_brightness, current_brightness, maximum_brightness = (
            DWORD(0),
            DWORD(0),
            DWORD(0),
        )
        error_code = ctypes.windll.Dxva2.GetMonitorBrightness(
            monitor.hPhysicalMonitor,
            ctypes.byref(minimum_brightness),
            ctypes.byref(current_brightness),
            ctypes.byref(maximum_brightness),
        )

        if error_code != 0:
            raise Exception(f"GetMonitorBrightness failed with {error_code=}")

        return Brightness(
            minimum_brightness.value, current_brightness.value, maximum_brightness.value
        )

    def set_display_brightness_for_monitor(self, monitor: PhysicalMonitor, value):
        brightness_obj = self.get_display_brightness_for_monitor(monitor)

        if not (brightness_obj.minimum <= value <= brightness_obj.maximum):
            raise Exception(
                f"Brightness value should be in range <{brightness_obj.minimum, brightness_obj.maximum}>"
            )
        ctypes.windll.Dxva2.SetMonitorBrightness(monitor.hPhysicalMonitor, DWORD(value))
