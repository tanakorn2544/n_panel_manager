"""
Quick-switch popup for N-Panel Manager.
Provides a floating grid UI for fast group switching.
Trigger: Ctrl + Shift + Scroll Wheel in 3D View
"""

import bpy
import gpu
from gpu_extras.batch import batch_for_shader
import blf
from .constants import ADDON_ID


class NPANEL_OT_QuickSwitch(bpy.types.Operator):
    """Quick switch between N-Panel groups with Ctrl+Shift+Scroll"""
    bl_idname = "npanel.quick_switch"
    bl_label = "Quick Switch Groups"
    bl_options = {'REGISTER'}
    
    direction: bpy.props.IntProperty(default=0)  # 1 = next, -1 = previous
    
    def execute(self, context):
        prefs = context.preferences.addons[ADDON_ID].preferences
        
        if len(prefs.groups) == 0:
            self.report({'WARNING'}, "No groups created yet")
            return {'CANCELLED'}
        
        # Calculate new index
        current = prefs.active_group_index if prefs.is_filtering else -1
        new_index = current + self.direction
        
        # Wrap around
        if new_index >= len(prefs.groups):
            new_index = -1  # Show All
        elif new_index < -1:
            new_index = len(prefs.groups) - 1
        
        # Apply group or restore all
        if new_index == -1:
            from .core import PanelManager
            PanelManager.restore_all(context)
            prefs.is_filtering = False
            prefs.active_group_index = -1
            self.report({'INFO'}, "Show All")
        else:
            from .core import PanelManager
            group = prefs.groups[new_index]
            PanelManager.apply_group(context, group.name)
            prefs.active_group_index = new_index
            prefs.is_filtering = True
            self.report({'INFO'}, f"Switched to: {group.name}")
        
        return {'FINISHED'}


class NPANEL_OT_QuickSwitchPopup(bpy.types.Operator):
    """Show quick switch popup for N-Panel groups"""
    bl_idname = "npanel.quick_switch_popup"
    bl_label = "Quick Switch Popup"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        prefs = context.preferences.addons[ADDON_ID].preferences
        
        if len(prefs.groups) == 0:
            self.report({'WARNING'}, "No groups created yet")
            return {'CANCELLED'}
        
        # Show popup
        return context.window_manager.invoke_popup(self, width=300)
    
    def draw(self, context):
        layout = self.layout
        prefs = context.preferences.addons[ADDON_ID].preferences
        
        # Header
        row = layout.row()
        row.label(text="Quick Switch", icon='ARROW_LEFTRIGHT')
        
        layout.separator()
        
        # Grid of groups
        grid = layout.grid_flow(row_major=True, columns=3, even_columns=True, align=True)
        
        for i, group in enumerate(prefs.groups):
            is_active = prefs.is_filtering and prefs.active_group_index == i
            
            op = grid.operator(
                "npanel.apply_group",
                text=group.name,
                icon='CHECKMARK' if is_active else 'BLANK1',
                depress=is_active
            )
            op.group_index = i
        
        layout.separator()
        
        # Show All button
        row = layout.row()
        row.scale_y = 1.3
        is_showing_all = not prefs.is_filtering
        row.operator(
            "npanel.restore_all",
            text="Show All",
            icon='LOOP_BACK',
            depress=is_showing_all
        )


# Keymap
addon_keymaps = []


def register_keymaps():
    """Register keymaps for quick switch."""
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:
        # 3D View keymap
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        
        # Shift + Scroll Up = Next group
        kmi = km.keymap_items.new(
            'npanel.quick_switch',
            'WHEELUPMOUSE',
            'PRESS',
            shift=True,
            ctrl=True
        )
        kmi.properties.direction = 1
        addon_keymaps.append((km, kmi))
        
        # Shift + Scroll Down = Previous group
        kmi = km.keymap_items.new(
            'npanel.quick_switch',
            'WHEELDOWNMOUSE',
            'PRESS',
            shift=True,
            ctrl=True
        )
        kmi.properties.direction = -1
        addon_keymaps.append((km, kmi))
        
        # Shift + ` (backtick) = Show popup
        kmi = km.keymap_items.new(
            'npanel.quick_switch_popup',
            'ACCENT_GRAVE',
            'PRESS',
            shift=True
        )
        addon_keymaps.append((km, kmi))


def unregister_keymaps():
    """Unregister keymaps."""
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


classes = (
    NPANEL_OT_QuickSwitch,
    NPANEL_OT_QuickSwitchPopup,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_keymaps()
    print("[N-Panel Manager] Quick switch registered (Ctrl+Shift+Scroll)")


def unregister():
    unregister_keymaps()
    for cls in classes:
        bpy.utils.unregister_class(cls)
