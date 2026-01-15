"""
Workflow presets for N-Panel Manager.
Based on popular addons from Superhive, Blender Market, and other platforms.
"""

# Each preset defines a list of tab/category names that are commonly associated
# with that workflow. The addon will match these against installed N-Panel tabs.

PRESETS = {
    "Modeling Essentials": [
        "HardOps", "Hard Ops", "Hardops",
        "BoxCutter", "Box Cutter", "Boxcutter",
        "Mesh Machine", "MESHmachine",
        "Fluent",
        "Random Flow", "RandomFlow",
        "Kit Ops", "KIT OPS", "KitOps",
        "Zen UV", "ZenUV",
        "Quad Remesher",
        "Decal Machine", "DECALmachine",
        "Modifier", "Modifiers",
        "Item", "Tool",
    ],
    
    "Hard Surface": [
        "HardOps", "Hard Ops", "Hardops",
        "BoxCutter", "Box Cutter", "Boxcutter",
        "Mesh Machine", "MESHmachine",
        "Decal Machine", "DECALmachine",
        "Fluent",
        "Random Flow", "RandomFlow",
        "Kit Ops", "KIT OPS", "KitOps",
        "Modifier", "Modifiers",
    ],
    
    "Sculpting": [
        "Sculpt Layers",
        "VK",
        "ZenShaders",
        "Item", "Tool",
        "Brush",
    ],
    
    "Animation & Rigging": [
        "Auto Rig Pro", "AutoRigPro", "ARP",
        "Animation Nodes", "AnimationNodes",
        "Rigify",
        "Mixamo",
        "Simply Cloth",
        "Cinepack",
        "Rig", "Rigging",
        "Animation",
        "Pose",
    ],
    
    "Environment": [
        "Geo-Scatter", "GeoScatter", "Geo Scatter", "Scatter",
        "Botaniq",
        "The Grove", "Grove",
        "True Terrain", "TrueTerrain",
        "True Sky", "TrueSky",
        "Physical Starlight", "Starlight",
        "Tree",
        "Vegetation",
    ],
    
    "Texturing": [
        "Sanctus", "Sanctus Library",
        "Extreme PBR", "ExtremePBR",
        "Fluent Materializer",
        "Realtime Materials",
        "Node Preview",
        "Material", "Materials",
        "Shader", "Shaders",
    ],
    
    "Rendering": [
        "Physical Starlight", "Starlight",
        "Physical Atmosphere",
        "Real Clouds",
        "Real Water",
        "Physical Open Water",
        "HDRI",
        "Light", "Lighting",
    ],
    
    "Utility Tools": [
        "Cablerator",
        "Zen Dock", "ZenDock",
        "Outliner Pro",
        "Node Wrangler",
        "Holt Tools",
        "Batch",
        "Export",
        "Import",
    ],
    
    "Retopology": [
        "Retopoflow", "RetopoFlow",
        "Quad Remesher",
        "Edge Flow", "EdgeFlow",
        "Retopo",
    ],
    
    "UV Workflow": [
        "Zen UV", "ZenUV",
        "UV Packmaster", "UVPackmaster",
        "UV", "UVs",
        "Texel",
    ],
}

def get_preset_names():
    """Return list of preset names."""
    return list(PRESETS.keys())

def get_preset_tabs(preset_name):
    """Return list of tab patterns for a preset."""
    return PRESETS.get(preset_name, [])

def match_preset_to_categories(preset_name, available_categories):
    """
    Match a preset's tab patterns against available categories.
    Returns list of matching category names.
    """
    patterns = get_preset_tabs(preset_name)
    matches = []
    
    for cat in available_categories:
        cat_lower = cat.lower()
        for pattern in patterns:
            if pattern.lower() in cat_lower or cat_lower in pattern.lower():
                if cat not in matches:
                    matches.append(cat)
                break
    
    return matches
