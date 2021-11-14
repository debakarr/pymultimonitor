import ctypes
from ctypes.wintypes import DWORD, UINT
from typing import Tuple, Dict

from pymultimonitor.cinterface.constants.DisplayConfigDeviceInfo import (
    DisplayConfigDeviceInfo,
)
from pymultimonitor.cinterface.constants.DisplayModeInfo import DisplayModeInfo
from pymultimonitor.cinterface.constants.QueryDisplayConfigFlag import (
    QueryDisplayConfigFlag,
)
from pymultimonitor.cinterface.structures.displaydevicesreference.wingdi.DisplayConfigStructures import (
    DISPLAYCONFIG_PATH_INFO,
    DISPLAYCONFIG_MODE_INFO,
    DISPLAYCONFIG_SOURCE_DEVICE_NAME,
    LUID,
    DISPLAYCONFIG_TARGET_DEVICE_NAME,
)


class DisplayInfo:
    @classmethod
    def _get_display_info(cls) -> Tuple[ctypes.Array, ctypes.Array, ctypes.c_uint]:
        count_path_elements = DWORD()
        count_mode_elements = DWORD()
        current_topology_id = UINT()

        error_code = ctypes.windll.user32.GetDisplayConfigBufferSizes(
            QueryDisplayConfigFlag.QDC_DATABASE_CURRENT.value,
            ctypes.byref(count_path_elements),
            ctypes.byref(count_mode_elements),
        )
        if error_code != 0:
            raise Exception(f"GetDisplayConfigBufferSizes failed with {error_code=}")

        display_paths = (DISPLAYCONFIG_PATH_INFO * count_path_elements.value)()
        display_modes = (DISPLAYCONFIG_MODE_INFO * count_mode_elements.value)()

        error_code = ctypes.windll.user32.QueryDisplayConfig(
            QueryDisplayConfigFlag.QDC_DATABASE_CURRENT.value,
            ctypes.byref(count_path_elements),
            display_paths,
            ctypes.byref(count_mode_elements),
            display_modes,
            ctypes.byref(current_topology_id),
        )
        if error_code != 0:
            raise Exception(f"QueryDisplayConfig failed with {error_code=}")

        return display_paths, display_modes, current_topology_id

    @classmethod
    def _get_display_device_info(
        cls,
        adapter_id: LUID,
        source_id: ctypes.c_uint,
        source_type: DisplayConfigDeviceInfo,
    ):
        if (
            source_type
            == DisplayConfigDeviceInfo.DISPLAYCONFIG_DEVICE_INFO_GET_SOURCE_NAME
        ):
            request = DISPLAYCONFIG_SOURCE_DEVICE_NAME()
            request.header.size = ctypes.sizeof(DISPLAYCONFIG_SOURCE_DEVICE_NAME)
        else:
            request = DISPLAYCONFIG_TARGET_DEVICE_NAME()
            request.header.size = ctypes.sizeof(DISPLAYCONFIG_TARGET_DEVICE_NAME)

        request.header.type = source_type.value
        request.header.adapterId = adapter_id
        request.header.id = source_id
        error_code = ctypes.windll.user32.DisplayConfigGetDeviceInfo(
            ctypes.byref(request)
        )

        if error_code != 0:
            raise Exception(f"DisplayConfigGetDeviceInfo failed with {error_code=}")

        return request

    def get_display_names(self) -> Dict[str, str]:
        """
        Get Friendly name for each display.

        :return: Dictionary containing the display ID and friendly name
        """
        _, display_modes, _ = self._get_display_info()
        adapter_ids = set()
        adapter_friendly_names_map = dict()
        adapter_gdi_name_map = dict()

        for display_mode in display_modes:
            adapter_id = (
                f"{display_mode.adapterId.LowPart}-{display_mode.adapterId.HighPart}"
            )
            adapter_ids.add(adapter_id)
            if (
                display_mode.infoType
                == DisplayModeInfo.DISPLAYCONFIG_MODE_INFO_TYPE_SOURCE
            ):
                display_device_info = self._get_display_device_info(
                    display_mode.adapterId,
                    display_mode.id,
                    DisplayConfigDeviceInfo.DISPLAYCONFIG_DEVICE_INFO_GET_SOURCE_NAME,
                )
                adapter_gdi_name_map[adapter_id] = display_device_info.viewGdiDeviceName
            elif (
                display_mode.infoType
                == DisplayModeInfo.DISPLAYCONFIG_MODE_INFO_TYPE_TARGET
            ):
                display_device_info = self._get_display_device_info(
                    display_mode.adapterId,
                    display_mode.id,
                    DisplayConfigDeviceInfo.DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_NAME,
                )
                adapter_friendly_names_map[
                    adapter_id
                ] = display_device_info.monitorFriendlyDeviceName
            else:
                raise Exception(
                    f"Invalid display mode info type: {display_mode.infoType}"
                )

        friendly_name_map = dict()

        for adapter_id in adapter_ids:
            friendly_name_map[
                adapter_gdi_name_map[adapter_id]
            ] = adapter_friendly_names_map[adapter_id]

        return friendly_name_map
