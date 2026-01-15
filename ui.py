import bpy
from .constants import ADDON_ID

class NPANEL_PT_Main(bpy.types.Panel):
    bl_label = "N-Panel Manager"
    bl_idname = "NPANEL_PT_Main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'N-Panel Tool'

    def draw(self, context):
        layout = self.layout
        
        # Safety check: addon might not be fully registered yet
        try:
            prefs = context.preferences.addons[ADDON_ID].preferences
        except KeyError:
            layout.label(text="Addon not fully loaded. Please restart Blender.", icon='ERROR')
            return
        
        # ============================================================
        # HUD-STYLE STATUS HEADER
        # ============================================================
        header_box = layout.box()
        header_row = header_box.row(align=True)
        header_row.scale_y = 1.5  # Larger, more prominent
        
        if prefs.is_filtering and prefs.active_group_index >= 0 and prefs.active_group_index < len(prefs.groups):
            active_group = prefs.groups[prefs.active_group_index]
            header_row.alert = True
            header_row.label(text=f"▸ {active_group.name}", icon='FILTER')
            header_row.operator("npanel.restore_all", text="Show All", icon='LOOP_BACK')
        else:
            header_row.label(text="▸ All Tabs Visible", icon='HIDE_OFF')

        layout.separator()
        
        # ============================================================
        # DASHBOARD GRID (Quick Group Switches)
        # ============================================================
        if prefs.groups:
            grid = layout.grid_flow(row_major=True, columns=2, even_columns=True, even_rows=True, align=True)
            
            for index, group in enumerate(prefs.groups):
                is_active = (prefs.is_filtering and prefs.active_group_index == index)
                
                col = grid.column(align=True)
                col.scale_y = 1.4  # Larger buttons
                
                if is_active:
                    col.alert = True
                
                op = col.operator("npanel.apply_group", text=group.name, icon='CHECKMARK' if is_active else 'BLANK1', depress=is_active)
                op.group_index = index
        else:
            layout.label(text="No groups yet. Add one below.", icon='INFO')
            
        layout.separator()

        # ============================================================
        # COLLAPSED: MANAGE GROUPS (Less Prominent)
        # ============================================================
        manage_box = layout.box()
        manage_row = manage_box.row()
        manage_row.label(text="Manage Groups", icon='PREFERENCES')
        
        row = manage_box.row()
        row.template_list("UI_UL_list", "npanel_groups", prefs, "groups", prefs, "active_group_index", rows=3)
        
        col = row.column(align=True)
        col.operator("npanel.add_group", text="", icon='ADD')
        col.operator("npanel.remove_group", text="", icon='REMOVE').index = prefs.active_group_index
        col.separator()
        col.operator("npanel.refresh_categories", text="", icon='FILE_REFRESH')
        
        # ============================================================
        # EDIT SELECTED GROUP (If one is selected)
        # ============================================================
        if prefs.groups and 0 <= prefs.active_group_index < len(prefs.groups):
            group = prefs.groups[prefs.active_group_index]
            
            edit_box = layout.box()
            edit_box.label(text=f"Edit: {group.name}", icon='GREASEPENCIL')
            
            edit_box.prop(group, "name", text="Name")
            edit_box.prop_search(group, "workspace_name", bpy.data, "workspaces", text="Auto-Activate on Workspace")
            
            edit_box.separator()
            edit_box.label(text="Included Tabs:")
            
            col = edit_box.column(align=True)
            for cat in group.categories:
                row = col.row(align=True)
                row.prop(cat, "enabled", text="")
                row.label(text=cat.name)

def register():
    bpy.utils.register_class(NPANEL_PT_Main)

def unregister():
    bpy.utils.unregister_class(NPANEL_PT_Main)
