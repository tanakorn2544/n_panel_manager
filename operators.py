import bpy
from .core import PanelScanner, PanelManager
from .constants import ADDON_ID

class NPANEL_OT_AddGroup(bpy.types.Operator):
    bl_idname = "npanel.add_group"
    bl_label = "Add Group"
    
    name: bpy.props.StringProperty(name="Group Name", default="New Group")
    
    def execute(self, context):
        prefs = context.preferences.addons[ADDON_ID].preferences
        group = prefs.groups.add()
        group.name = self.name
        
        # Populate with current categories
        PanelScanner.ensure_original_categories_stored()
        
        cats = set()
        for cls in PanelScanner.get_all_n_panels():
            cat = getattr(cls, '_npanel_orig_category', getattr(cls, 'bl_category', 'Item'))
            cats.add(cat)
            
        for cat_name in sorted(list(cats)):
            item = group.categories.add()
            item.name = cat_name
            item.enabled = False 
            
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class NPANEL_OT_RemoveGroup(bpy.types.Operator):
    bl_idname = "npanel.remove_group"
    bl_label = "Remove Group"
    
    index: bpy.props.IntProperty()
    
    def execute(self, context):
        prefs = context.preferences.addons[ADDON_ID].preferences
        prefs.groups.remove(self.index)
        return {'FINISHED'}

class NPANEL_OT_ApplyGroup(bpy.types.Operator):
    bl_idname = "npanel.apply_group"
    bl_label = "Apply Group"
    
    group_index: bpy.props.IntProperty()
    
    def execute(self, context):
        prefs = context.preferences.addons[ADDON_ID].preferences
        if self.group_index < 0 or self.group_index >= len(prefs.groups):
            # Restore all
            PanelManager.restore_all(context)
            prefs.active_group_index = -1
            prefs.is_filtering = False
            return {'FINISHED'}
            
        group = prefs.groups[self.group_index]
        PanelManager.apply_group(context, group.name)
        prefs.active_group_index = self.group_index
        prefs.is_filtering = True
        return {'FINISHED'}

class NPANEL_OT_RestoreAll(bpy.types.Operator):
    bl_idname = "npanel.restore_all"
    bl_label = "Show All"
    
    def execute(self, context):
        prefs = context.preferences.addons[ADDON_ID].preferences
        PanelManager.restore_all(context)
        prefs.is_filtering = False
        prefs.active_group_index = -1
        return {'FINISHED'}

class NPANEL_OT_RefreshCategories(bpy.types.Operator):
    bl_idname = "npanel.refresh_categories"
    bl_label = "Refresh Categories"
    
    def execute(self, context):
        # Syncs available categories to all groups
        PanelScanner.ensure_original_categories_stored()
        
        cats = set()
        for cls in PanelScanner.get_all_n_panels():
            cat = getattr(cls, '_npanel_orig_category', getattr(cls, 'bl_category', 'Item'))
            cats.add(cat)
        
        prefs = context.preferences.addons[ADDON_ID].preferences
        for group in prefs.groups:
            existing = {c.name for c in group.categories}
            for cat in cats:
                if cat not in existing:
                    new_item = group.categories.add()
                    new_item.name = cat
                    new_item.enabled = False
        
        return {'FINISHED'}

class NPANEL_OT_ApplyPreset(bpy.types.Operator):
    bl_idname = "npanel.apply_preset"
    bl_label = "Apply Preset"
    bl_description = "Create a group from a workflow preset"
    
    preset_name: bpy.props.StringProperty()
    
    def execute(self, context):
        from .presets import match_preset_to_categories
        from .core import PanelScanner
        
        prefs = context.preferences.addons[ADDON_ID].preferences
        
        # Get all available categories
        PanelScanner.ensure_original_categories_stored()
        cats = set()
        for cls in PanelScanner.get_all_n_panels():
            cat = getattr(cls, '_npanel_orig_category', getattr(cls, 'bl_category', 'Item'))
            cats.add(cat)
        
        # Match preset against available categories
        matches = match_preset_to_categories(self.preset_name, list(cats))
        
        if not matches:
            self.report({'WARNING'}, f"No matching tabs found for '{self.preset_name}'")
            return {'CANCELLED'}
        
        # Create a new group
        group = prefs.groups.add()
        group.name = self.preset_name
        
        # Add all categories, enable only the matched ones
        for cat_name in sorted(list(cats)):
            item = group.categories.add()
            item.name = cat_name
            item.enabled = cat_name in matches
        
        self.report({'INFO'}, f"Created group '{self.preset_name}' with {len(matches)} tabs")
        return {'FINISHED'}

class NPANEL_OT_ClearSearch(bpy.types.Operator):
    bl_idname = "npanel.clear_search"
    bl_label = "Clear Search"
    bl_description = "Clear the search filter"
    
    def execute(self, context):
        prefs = context.preferences.addons[ADDON_ID].preferences
        prefs.search_filter = ""
        return {'FINISHED'}

classes = (
    NPANEL_OT_AddGroup,
    NPANEL_OT_RemoveGroup,
    NPANEL_OT_ApplyGroup,
    NPANEL_OT_RestoreAll,
    NPANEL_OT_RefreshCategories,
    NPANEL_OT_ApplyPreset,
    NPANEL_OT_ClearSearch,
)

def register_classes():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_classes():
    for cls in classes:
        bpy.utils.unregister_class(cls)
