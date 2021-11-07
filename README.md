# PyMultiMonitor

This module can be used to interact with Windows Display. Currently, it supports:
- Getting current display topology (i.e. CLONE, EXTERNAL, INTERNAL, EXTENDED)
- Setting display topology
- Getting display name

## Example

### Importing and instantiating `PyMultiMonitor` class

```python
>>> from pymultimonitor.PyMultiMonitor import PyMultiMonitor
>>> pmm = PyMultiMonitor()
```

### Getting current display topology

```python
>>> pmm.get_display_topology()
<DisplayConfigTopology.DISPLAYCONFIG_TOPOLOGY_EXTEND: 4>
>>> from pymultimonitor.constants.DisplayConfigTopology import DisplayConfigTopology
>>> pmm.get_display_topology() == DisplayConfigTopology.DISPLAYCONFIG_TOPOLOGY_EXTEND
True
```

### Setting display topology

```python
>>> pmm.set_topology_extend()
>>> pmm.get_display_topology() == DisplayConfigTopology.DISPLAYCONFIG_TOPOLOGY_EXTEND
True
>>> pmm.set_topology_external()
>>> pmm.get_display_topology() == DisplayConfigTopology.DISPLAYCONFIG_TOPOLOGY_EXTERNAL
True
```

### Getting current display device friendly name

```python
>>> pmm.get_display_names()
{'\\\\.\\DISPLAY1': 'LG ULTRAWIDE'}
```