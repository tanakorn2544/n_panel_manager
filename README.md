# N-Panel Manager

A Blender addon for organizing and decluttering your N-Panel (sidebar) by grouping tabs and quickly switching between different tool sets.

## Features

- **Group Management**: Create custom groups of N-Panel tabs
- **Quick Filtering**: Click a group button to instantly show only those tabs
- **Search/Filter**: Search tabs by name when editing groups
- **Workflow Presets**: 10 pre-configured presets based on popular addons:
  - Modeling Essentials, Hard Surface, Sculpting
  - Animation & Rigging, Environment, Texturing
  - Rendering, Utility Tools, Retopology, UV Workflow
- **Workspace Auto-Activation**: Link groups to workspaces for automatic switching
- **Persistent State**: Your filtering persists across sessions

## Installation

1. Download/zip the `n_panel_manager` folder
2. In Blender: **Edit > Preferences > Add-ons > Install**
3. Select the zip file and enable the addon

## Usage

### Quick Start
1. Open N-Panel (press `N`) → find **"N-Panel Tool"** tab
2. Click a **Quick Preset** button (e.g., "Modeling Essentials")
3. The addon creates a group with matching installed addons enabled
4. Click the group button to apply filtering

### Manual Group Creation
1. Click **+** in "Manage Groups"
2. Name your group
3. Use the **search box** to find tabs
4. Check/uncheck tabs to include

### Workspace Auto-Activation
1. Select a group → set "Auto-Activate on Workspace"
2. Switching workspaces will auto-apply the linked group

## File Structure

```
n_panel_manager/
├── __init__.py       # Entry point
├── constants.py      # Shared constants
├── preferences.py    # Data structures
├── core.py           # Panel filtering logic
├── operators.py      # Blender operators
├── ui.py             # N-Panel UI
├── presets.py        # Workflow presets
└── drawing.py        # (unused placeholder)
```

## Requirements

- Blender 4.0+

## Known Limitations

- Some addon panels may not move (non-standard registration)
- These simply stay visible - safe behavior

## License

MIT License

## Author

Korn Sensei
