bl_info = {
    "name": "N-Panel Manager",
    "author": "Korn Sensei",
    "version": (0, 0, 1),
    "blender": (4, 0, 0),
    "location": "View3D > N-Panel > N-Panel Tool",
    "description": "Clean up your N-Panel by grouping and hiding tabs.",
    "category": "Interface",
}

import bpy
from . import ui
from . import core
from . import preferences
from . import operators
from . import drawing
from .constants import ADDON_ID
from bpy.app.handlers import persistent

@persistent
def load_handler(dummy):
    """
    Re-apply filtering if it was active.
    """
    try:
        prefs = bpy.context.preferences.addons[ADDON_ID].preferences
        # Initial scan to ensure we have data
        core.PanelScanner.ensure_original_categories_stored()
        
        if prefs.is_filtering and prefs.active_group_index >= 0:
            if prefs.active_group_index < len(prefs.groups):
                group = prefs.groups[prefs.active_group_index]
                print(f"N-Panel Manager: Restoring group '{group.name}'")
                core.PanelManager.apply_group(bpy.context, group.name)
    except Exception as e:
        print(f"N-Panel Manager Load Error: {e}")

_last_workspace = None

@persistent
def workspace_handler(scene):
    global _last_workspace
    try:
        context = bpy.context
        if not context.window or not context.workspace:
            return
            
        current_workspace = context.workspace
        
        if _last_workspace != current_workspace:
            _last_workspace = current_workspace
            
            # Workspace changed, check if we need to switch groups
            prefs = context.preferences.addons[ADDON_ID].preferences
            
            for i, group in enumerate(prefs.groups):
                if group.workspace_name and group.workspace_name == current_workspace.name:
                    print(f"N-Panel Manager: Workspace '{current_workspace.name}' detected. Switching to group '{group.name}'")
                    # We found a match! Apply it.
                    core.PanelManager.apply_group(context, group.name)
                    prefs.active_group_index = i
                    prefs.is_filtering = True
                    return 
                    
    except Exception as e:
        # Avoid spamming errors in depsgraph loop
        pass

def register():
    print("[N-Panel Manager] Starting registration...")
    preferences.register()
    print("[N-Panel Manager] Preferences done. Registering operators...")
    operators.register_classes()
    print("[N-Panel Manager] Operators done. Registering UI...")
    ui.register()
    print("[N-Panel Manager] UI done. Adding handlers...")
    bpy.app.handlers.load_post.append(load_handler)
    bpy.app.handlers.depsgraph_update_post.append(workspace_handler)
    print("[N-Panel Manager] Registering HUD drawing...")
    drawing.register()
    print("[N-Panel Manager] Registration complete!")

def unregister():
    drawing.unregister()
    
    if load_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_handler)
    if workspace_handler in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(workspace_handler)
        
    ui.unregister()
    operators.unregister_classes()
    preferences.unregister()


if __name__ == "__main__":
    register()
