import ctypes

from pymultimonitor.cinterface.constants.DisplayConfigTopology import (
    DisplayConfigTopology,
)
from pymultimonitor.cinterface.constants.SetDisplayConfigFlag import (
    SetDisplayConfigFlag,
)
from pymultimonitor.core.DisplayInfo import DisplayInfo


class DisplayTopology:
    @classmethod
    def _set_display_topology(cls, topology: SetDisplayConfigFlag) -> None:
        error_code = ctypes.windll.user32.SetDisplayConfig(
            0,
            None,
            0,
            None,
            topology.value | SetDisplayConfigFlag.SDC_APPLY.value,
        )
        if error_code != 0:
            raise Exception(f"SetDisplayConfig failed with {error_code=}")

    @classmethod
    def get_display_topology(cls) -> DisplayConfigTopology:
        """
        Get the current display topology (INTERNAL, EXTERNAL, EXTENDED, CLONE)

        :return: :class:`DisplayConfigTopology` object
        """
        _, _, topology_id = DisplayInfo.get_display_info()
        return DisplayConfigTopology(topology_id.value)

    def set_topology_extend(self) -> None:
        """Set display to extended mode"""
        self._set_display_topology(SetDisplayConfigFlag.SDC_TOPOLOGY_EXTEND)

    def set_topology_clone(self) -> None:
        """Set display to clone mode"""
        self._set_display_topology(SetDisplayConfigFlag.SDC_TOPOLOGY_CLONE)

    def set_topology_internal(self) -> None:
        """Set display to internal mode"""
        self._set_display_topology(SetDisplayConfigFlag.SDC_TOPOLOGY_INTERNAL)

    def set_topology_external(self) -> None:
        """Set display to external mode"""
        self._set_display_topology(SetDisplayConfigFlag.SDC_TOPOLOGY_EXTERNAL)
