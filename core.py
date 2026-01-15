import bpy
from .constants import ADDON_ID

class PanelScanner:
    @staticmethod
    def get_all_n_panels():
        """Yields all UI panel classes in VIEW_3D."""
        for cls in bpy.types.Panel.__subclasses__():
            if getattr(cls, 'bl_space_type', '') == 'VIEW_3D' and \
               getattr(cls, 'bl_region_type', '') == 'UI':
                 # Exclude our own panel to prevent hiding it
                 if cls.__name__ == "NPANEL_PT_Main":
                     continue
                 yield cls

    @staticmethod
    def get_current_categories():
        """Returns set of currently visible categories."""
        cats = set()
        for cls in PanelScanner.get_all_n_panels():
            # We care about the CURRENT name
            cat = getattr(cls, 'bl_category', 'Item')
            cats.add(cat)
        return sorted(list(cats))
    
    @staticmethod
    def ensure_original_categories_stored():
        """Iterates all panels and stores their original bl_category if not already stored."""
        for cls in PanelScanner.get_all_n_panels():
            if not hasattr(cls, '_npanel_orig_category'):
                # If we are already running and they are hidden, this might be risky.
                # But assuming this runs FIRST before any hiding, we are good.
                # TODO: If we reload, we might lose this. 
                # Ideally we persist this, but for now runtime is okay.
                cls._npanel_orig_category = getattr(cls, 'bl_category', 'Item')

class PanelManager:
    @staticmethod
    def apply_group(context, group_name):
        """
        Enables only categories in the group. 
        Everything else moves to '_Hidden_'.
        """
        PanelScanner.ensure_original_categories_stored()
        
        prefs = context.preferences.addons[ADDON_ID].preferences
        group = next((g for g in prefs.groups if g.name == group_name), None)
        
        if not group:
            print(f"Group {group_name} not found")
            return

        # Get allowed categories logic
        # 'categories' collection in group defines what is allowed.
        # But wait, we need to know what constitutes "Allowed".
        # Let's say we rely on the implementation where we add strings to the Group.
        allowed_cats = {c.name for c in group.categories if c.enabled}

        count_moved = 0
        
        for cls in PanelScanner.get_all_n_panels():
            orig = getattr(cls, '_npanel_orig_category', getattr(cls, 'bl_category', 'Item'))
            
            # Logic: Is this category in our allowed list?
            should_show = (orig in allowed_cats)
            
            target_cat = orig if should_show else " Hidden"
            
            current_cat = getattr(cls, 'bl_category', 'Item')
            
            if current_cat != target_cat:
                # We need to move it
                try:
                    bpy.utils.unregister_class(cls)
                    cls.bl_category = target_cat
                    bpy.utils.register_class(cls)
                    count_moved += 1
                except Exception as e:
                    print(f"Failed to move {cls.__name__}: {e}")
        
        print(f"PanelManager: Processed panels. Moved {count_moved} panels.")
        
    @staticmethod
    def restore_all(context):
        """Restores all panels to original categories."""
        PanelScanner.ensure_original_categories_stored()
        
        count = 0
        for cls in PanelScanner.get_all_n_panels():
            orig = getattr(cls, '_npanel_orig_category', None)
            if orig:
                current = getattr(cls, 'bl_category', 'Item')
                if current != orig:
                    try:
                        bpy.utils.unregister_class(cls)
                        cls.bl_category = orig
                        bpy.utils.register_class(cls)
                        count += 1
                    except:
                        pass
        print(f"PanelManager: Restored {count} panels.")
