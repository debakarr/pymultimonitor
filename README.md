# PyMultiMonitor

This module can be used to interact with Windows Display. Currently, it supports:

- Getting and setting current display topology (i.e. CLONE, EXTERNAL, INTERNAL, EXTENDED)
- Getting display name
- Getting and setting current display brightness

## Example

### Getting current display topology

```python
>>> from pymultimonitor.core.DisplayTopology import DisplayTopology
>>> from pymultimonitor.cinterface.constants import DisplayConfigTopology
>>> dt = DisplayTopology()
>>> dt.get_display_topology()
< DisplayConfigTopology.DISPLAYCONFIG_TOPOLOGY_EXTEND: 4 >
>>> dt.get_display_topology() == DisplayConfigTopology.DISPLAYCONFIG_TOPOLOGY_EXTEND
True
```

### Setting display topology

```python
>>> from pymultimonitor.core.DisplayTopology import DisplayTopology
>>> from pymultimonitor.cinterface.constants import DisplayConfigTopology
>>> dt = DisplayTopology()
>>> dt.set_topology_extend()
>>> dt.get_display_topology() == DisplayConfigTopology.DISPLAYCONFIG_TOPOLOGY_EXTEND
True
>>> dt.set_topology_external()
>>> dt.get_display_topology() == DisplayConfigTopology.DISPLAYCONFIG_TOPOLOGY_EXTERNAL
True
```

### Getting current display device friendly name

```python
>>> from pymultimonitor.core.DisplayInfo import DisplayInfo
>>> di = DisplayInfo()
>>> di.get_display_names()
{'\\\\.\\DISPLAY1': 'LG ULTRAWIDE'}
```

### Getting and setting current display brightness for a particular monitor

```python
>>> from pymultimonitor.core.DisplayMonitors import DisplayMonitors
>>> dm = DisplayMonitors()
>>> physical_monitors = dm.get_physical_monitor_handles()
>>> physical_monitors
[PhysicalMonitor(hPhysicalMonitor=1, szPhysicalMonitorDescription='Generic PnP Monitor')]
>>> from pymultimonitor.core.DisplayBrightness import DisplayBrightness
>>> db = DisplayBrightness()
>>> db.get_display_brightness_for_monitor(physical_monitors[0])
Brightness(minimum=0, current=20, maximum=100)
>>> db.set_display_brightness_for_monitor(physical_monitors[0], 50)
```