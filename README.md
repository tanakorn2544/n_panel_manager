# N-Panel Manager

A Blender addon for organizing and decluttering your N-Panel (sidebar) by grouping tabs and quickly switching between different tool sets.

## Features

- **Group Management**: Create custom groups of N-Panel tabs (e.g., "Modeling", "Rigging", "Animation")
- **Quick Filtering**: Click a group button to instantly show only those tabs, hiding the rest
- **Workspace Auto-Activation**: Link groups to workspaces - switching workspace automatically applies the linked group
- **Color Coding**: Assign colors to tabs for visual organization
- **Persistent State**: Your filtering state persists across Blender sessions

## Installation

1. Download or zip the `n_panel_manager` folder
2. In Blender: **Edit > Preferences > Add-ons > Install**
3. Select the zip file and enable the addon

## Usage

### Access the Panel
Open the N-Panel (press `N` in the 3D View) and look for the **"N-Panel Tool"** tab.

### Creating Groups
1. Click the **+** button in the "Manage Groups" section
2. Enter a name for your group (e.g., "Modeling")
3. In the "Edit" section, check the tabs you want to include

### Applying a Group
- Click any group button at the top to instantly filter the N-Panel
- Click **"Show All"** to restore all tabs

### Workspace Auto-Activation
1. Select a group in "Manage Groups"
2. In the "Edit" section, set "Auto-Activate on Workspace"
3. Now switching to that workspace will automatically apply the group

## File Structure

```
n_panel_manager/
├── __init__.py       # Addon entry point
├── constants.py      # Shared constants
├── preferences.py    # Addon preferences & data structures
├── core.py           # Panel scanning & filtering logic
├── operators.py      # Blender operators
├── ui.py             # N-Panel UI
└── drawing.py        # GPU drawing (currently disabled)
```

## Requirements

- Blender 4.0 or later

## Known Limitations

- Some addon panels may fail to move if they use non-standard registration
- Panel ordering is based on Blender's internal order, not customizable

## License

MIT License

## Author

Korn Sensei
