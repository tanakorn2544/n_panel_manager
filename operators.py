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


class NPANEL_OT_ExportGroups(bpy.types.Operator):
    """Export groups to a JSON file"""
    bl_idname = "npanel.export_groups"
    bl_label = "Export Groups"
    bl_description = "Save groups to a JSON file"
    
    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filter_glob: bpy.props.StringProperty(default='*.json', options={'HIDDEN'})
    
    def execute(self, context):
        import json
        
        prefs = context.preferences.addons[ADDON_ID].preferences
        
        # Build export data
        export_data = {
            "version": "1.0",
            "groups": []
        }
        
        for group in prefs.groups:
            group_data = {
                "name": group.name,
                "workspace_name": group.workspace_name,
                "categories": [
                    {"name": cat.name, "enabled": cat.enabled}
                    for cat in group.categories
                ]
            }
            export_data["groups"].append(group_data)
        
        # Write to file
        filepath = self.filepath
        if not filepath.endswith('.json'):
            filepath += '.json'
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            self.report({'INFO'}, f"Exported {len(prefs.groups)} groups to {filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class NPANEL_OT_ImportGroups(bpy.types.Operator):
    """Import groups from a JSON file"""
    bl_idname = "npanel.import_groups"
    bl_label = "Import Groups"
    bl_description = "Load groups from a JSON file"
    
    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filter_glob: bpy.props.StringProperty(default='*.json', options={'HIDDEN'})
    replace_existing: bpy.props.BoolProperty(
        name="Replace Existing",
        description="Replace all existing groups (unchecked = merge)",
        default=False
    )
    
    def execute(self, context):
        import json
        
        prefs = context.preferences.addons[ADDON_ID].preferences
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {e}")
            return {'CANCELLED'}
        
        # Validate
        if "groups" not in import_data:
            self.report({'ERROR'}, "Invalid file format")
            return {'CANCELLED'}
        
        # Clear existing if replace mode
        if self.replace_existing:
            prefs.groups.clear()
        
        # Get existing group names for merge mode
        existing_names = {g.name for g in prefs.groups}
        
        imported_count = 0
        for group_data in import_data["groups"]:
            name = group_data.get("name", "Imported Group")
            
            # Skip duplicates in merge mode
            if not self.replace_existing and name in existing_names:
                continue
            
            # Create group
            group = prefs.groups.add()
            group.name = name
            group.workspace_name = group_data.get("workspace_name", "")
            
            # Add categories
            for cat_data in group_data.get("categories", []):
                cat = group.categories.add()
                cat.name = cat_data.get("name", "")
                cat.enabled = cat_data.get("enabled", False)
            
            imported_count += 1
        
        self.report({'INFO'}, f"Imported {imported_count} groups")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


classes = (
    NPANEL_OT_AddGroup,
    NPANEL_OT_RemoveGroup,
    NPANEL_OT_ApplyGroup,
    NPANEL_OT_RestoreAll,
    NPANEL_OT_RefreshCategories,
    NPANEL_OT_ApplyPreset,
    NPANEL_OT_ClearSearch,
    NPANEL_OT_ExportGroups,
    NPANEL_OT_ImportGroups,
)

def register_classes():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister_classes():
    for cls in classes:
        bpy.utils.unregister_class(cls)
