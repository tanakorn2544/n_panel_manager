# N-Panel Manager

A Blender addon for organizing and decluttering your N-Panel (sidebar) by grouping tabs and quickly switching between different tool sets.

![Blender 4.0+](https://img.shields.io/badge/Blender-4.0%2B-orange)
![Version](https://img.shields.io/badge/version-0.0.3-blue)

## Features

### 🎯 Core
- **Group Management** - Create custom groups of N-Panel tabs
- **Quick Filtering** - Click a group to instantly show only those tabs
- **Persistent State** - Filtering persists across sessions

### ⚡ Quick Switch (Shift + Scroll)
- **Shift + Scroll Up/Down** in 3D View to cycle through groups
- Floating overlay appears at bottom of viewport
- Auto-hides after 1.5 seconds
- No clicking needed!

### 📦 Workflow Presets
10 pre-configured presets based on popular addons:

| Preset | Matches |
|--------|---------|
| Modeling Essentials | HardOps, BoxCutter, Mesh Machine, Zen UV |
| Hard Surface | HardOps, BoxCutter, Decal Machine, Fluent |
| Sculpting | Sculpt Layers, VK, ZenShaders |
| Animation & Rigging | Auto Rig Pro, Rigify, Mixamo |
| Environment | Geo-Scatter, Botaniq, The Grove |
| Texturing | Sanctus Library, Extreme PBR |
| Rendering | Physical Starlight, Real Clouds |
| Utility Tools | Cablerator, Zen Dock, Outliner Pro |
| Retopology | Retopoflow, Quad Remesher |
| UV Workflow | Zen UV, UV Packmaster |

### 🔄 Workspace Auto-Activation
- Link groups to workspaces
- Switching workspace auto-applies the linked group

### 💾 Import/Export
- **Export** groups to `.json` files for backup or sharing
- **Import** groups with merge or replace options

## Installation

1. Download/zip the `n_panel_manager` folder
2. **Edit > Preferences > Add-ons > Install**
3. Select zip and enable

## Usage

### Quick Switch (Recommended)
1. Create some groups first (see below)
2. In 3D View: **Shift + Scroll** to cycle groups
3. Overlay shows current selection

### Manual Setup
1. Open N-Panel (`N` key) → **N-Panel Tool** tab
2. Click **+** in "Manage Groups" to create a group
3. Use **search box** to filter tabs
4. Check tabs to include in group
5. Click group button to apply

### Presets
- Click any **Quick Preset** button to auto-create a group
- Matches installed addons automatically

### Import/Export
- Click **Export** to save all groups to a JSON file
- Click **Import** to load groups (choose merge or replace)

## Shortcuts

| Shortcut | Action |
|----------|--------|
| **Shift + Scroll Up** | Next group + show overlay |
| **Shift + Scroll Down** | Previous group + show overlay |

## File Structure

```
n_panel_manager/
├── __init__.py      # Entry point
├── constants.py     # Shared constants
├── preferences.py   # Data structures
├── core.py          # Panel filtering logic
├── operators.py     # Blender operators
├── ui.py            # N-Panel UI
├── presets.py       # Workflow presets
├── overlay.py       # Floating quick-switch overlay
└── drawing.py       # (placeholder)
```

## Changelog

### v0.0.3
- ✨ Added Import/Export groups to JSON files
- ✨ Merge or replace options on import

### v0.0.2
- ✨ Added Shift+Scroll quick switch overlay
- ✨ Added 10 workflow presets
- ✨ Added search filter for tabs

### v0.0.1
- 🎉 Initial release
- Group management
- Workspace auto-activation

## Known Limitations

- Some addon panels can't be moved (non-standard registration)
- These stay visible with "Failed to move" messages - safe behavior

## Author

**Korn Sensei**

## License

MIT License
