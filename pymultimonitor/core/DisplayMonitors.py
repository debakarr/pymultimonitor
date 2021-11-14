import ctypes
from ctypes.wintypes import RECT, DWORD
from dataclasses import dataclass
from typing import List

from pymultimonitor.cinterface.functions.winuser.Winuser import MonitorEnumProc
from pymultimonitor.cinterface.structures.monitorconfiguration.physicalmonitorenumerationapi.PhysicalMonitorStructures import (
    PHYSICAL_MONITOR,
)
from pymultimonitor.output.PhysicalMonitor import PhysicalMonitor


class DisplayMonitors:
    @dataclass
    class MonitorHandle:
        handleToDisplayMonitor: int
        handleToDeviceContext: int
        pointerToRect: RECT

        def __str__(self):
            return (
                f"Handle to display: {self.handleToDisplayMonitor}"
                f"\nHandle to Device context: {self.handleToDeviceContext}"
                f"\nX: {self.pointerToRect.contents.left}, Y: {self.pointerToRect.contents.top}, "
                f"Width: {self.pointerToRect.contents.right - self.pointerToRect.contents.left}, "
                f"Height: {self.pointerToRect.contents.bottom - self.pointerToRect.contents.top}"
            )

    def _get_all_monitor_handles(self) -> List[MonitorHandle]:
        all_monitor_handles = list()

        def callback(hMonitor, hDC, rectPointer, unnamedParam):
            all_monitor_handles.append(self.MonitorHandle(hMonitor, hDC, rectPointer))
            return 1

        ctypes.windll.user32.EnumDisplayMonitors(
            0, 0, MonitorEnumProc(callback), ctypes.c_int(0)
        )
        return all_monitor_handles

    def get_physical_monitor_handles(self) -> List[PhysicalMonitor]:
        all_monitor_handles = self._get_all_monitor_handles()
        physical_monitors = list()
        for monitor_handle in all_monitor_handles:
            count_physical_monitor_element = DWORD()
            ctypes.windll.Dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(
                monitor_handle.handleToDisplayMonitor,
                ctypes.byref(count_physical_monitor_element),
            )

            current_physical_monitors = (
                PHYSICAL_MONITOR * count_physical_monitor_element.value
            )()

            ctypes.windll.Dxva2.GetPhysicalMonitorsFromHMONITOR(
                monitor_handle.handleToDisplayMonitor,
                count_physical_monitor_element,
                current_physical_monitors,
            )
            for physical_monitor in current_physical_monitors:
                if physical_monitor.hPhysicalMonitor is not None:
                    physical_monitors.append(
                        PhysicalMonitor(
                            physical_monitor.hPhysicalMonitor,
                            physical_monitor.szPhysicalMonitorDescription,
                        )
                    )
        return physical_monitors
