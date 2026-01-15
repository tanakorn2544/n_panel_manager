import bpy
from bpy.props import StringProperty, CollectionProperty, BoolProperty, PointerProperty
from bpy.types import PropertyGroup, AddonPreferences
from .constants import ADDON_ID

class IncludedCategory(PropertyGroup):
    name: StringProperty(name="Category Name")
    enabled: BoolProperty(name="Enabled", default=True)
    color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        size=3,
        min=0.0, max=1.0,
        default=(0.8, 0.8, 0.8)
    )

class PanelGroup(PropertyGroup):
    name: StringProperty(name="Group Name")
    # We use a collection to store which categories are "in" this group
    categories: CollectionProperty(type=IncludedCategory)
    
    # Store workspace name as string (data-block pointers not allowed in AddonPrefs)
    workspace_name: StringProperty(name="Linked Workspace", default="")

class NPANEL_Preferences(AddonPreferences):
    bl_idname = ADDON_ID

    groups: CollectionProperty(type=PanelGroup)
    active_group_index: bpy.props.IntProperty()
    
    # Store global state of whether we are currently "Filtering"
    is_filtering: BoolProperty(name="Is Filtering", default=False)
    
    # HUD Settings
    show_hud: BoolProperty(
        name="Show Color HUD",
        description="Display a color-coded HUD bar at the top of the 3D View",
        default=True
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="N-Panel Manager Preferences")
        layout.prop(self, "show_hud")
        
def register():
    print(f"[N-Panel Manager] Registering IncludedCategory...")
    bpy.utils.register_class(IncludedCategory)
    print(f"[N-Panel Manager] Registering PanelGroup...")
    bpy.utils.register_class(PanelGroup)
    print(f"[N-Panel Manager] Registering NPANEL_Preferences with bl_idname='{ADDON_ID}'...")
    bpy.utils.register_class(NPANEL_Preferences)
    print(f"[N-Panel Manager] Preferences registered successfully!")

def unregister():
    bpy.utils.unregister_class(NPANEL_Preferences)
    bpy.utils.unregister_class(PanelGroup)
    bpy.utils.unregister_class(IncludedCategory)
