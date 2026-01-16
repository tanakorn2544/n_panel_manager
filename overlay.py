"""
Floating quick-switch overlay for N-Panel Manager.
Ctrl + Shift + Scroll to show and cycle through groups.
"""

import bpy
import gpu
from gpu_extras.batch import batch_for_shader
import blf
from .constants import ADDON_ID

# Global state
_draw_handler = None
_is_visible = False
_hide_timer = None


def get_prefs():
    try:
        return bpy.context.preferences.addons[ADDON_ID].preferences
    except:
        return None


def draw_rounded_rect(x, y, width, height, color):
    """Draw a rectangle."""
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    
    vertices = [
        (x, y),
        (x + width, y),
        (x + width, y + height),
        (x, y + height),
    ]
    indices = [(0, 1, 2), (0, 2, 3)]
    
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)


def draw_text(text, x, y, size=14, color=(1, 1, 1, 1)):
    """Draw text at position."""
    font_id = 0
    blf.size(font_id, size)
    blf.color(font_id, *color)
    blf.position(font_id, x, y, 0)
    blf.draw(font_id, text)


def get_text_width(text, size=14):
    """Get width of text."""
    font_id = 0
    blf.size(font_id, size)
    return blf.dimensions(font_id, text)[0]


def draw_overlay_callback():
    """Main draw callback for the floating overlay."""
    global _is_visible
    
    if not _is_visible:
        return
    
    prefs = get_prefs()
    if not prefs or len(prefs.groups) == 0:
        return
    
    # Get region dimensions
    region = bpy.context.region
    if not region:
        return
    
    # Layout settings
    padding = 12
    button_height = 32
    button_spacing = 6
    min_button_width = 90
    
    # Calculate button widths
    button_widths = []
    for group in prefs.groups:
        text_width = get_text_width(group.name, 13)
        button_widths.append(max(min_button_width, text_width + 30))
    
    # Add "Show All" option
    show_all_width = max(min_button_width, get_text_width("Show All", 13) + 30)
    button_widths.append(show_all_width)
    
    total_width = sum(button_widths) + button_spacing * (len(button_widths) - 1) + padding * 2
    total_height = button_height + padding * 2
    
    # Position at bottom center of viewport
    start_x = (region.width - total_width) / 2
    start_y = 60
    
    # Enable blending
    gpu.state.blend_set('ALPHA')
    
    # Draw background panel with border
    border_color = (0.4, 0.4, 0.4, 0.95)
    draw_rounded_rect(start_x - 2, start_y - 2, total_width + 4, total_height + 4, border_color)
    
    bg_color = (0.12, 0.12, 0.12, 0.95)
    draw_rounded_rect(start_x, start_y, total_width, total_height, bg_color)
    
    # Draw buttons
    current_x = start_x + padding
    button_y = start_y + padding
    
    # Determine which index is "active" for display
    # -1 = Show All, 0+ = group index
    if prefs.is_filtering:
        active_idx = prefs.active_group_index
    else:
        active_idx = -1  # Show All
    
    for i, group in enumerate(prefs.groups):
        is_active = (active_idx == i)
        
        # Button color
        if is_active:
            btn_color = (0.55, 0.30, 0.65, 1.0)  # Purple for active
        else:
            btn_color = (0.25, 0.25, 0.25, 0.9)  # Gray for inactive
        
        btn_width = button_widths[i]
        draw_rounded_rect(current_x, button_y, btn_width, button_height, btn_color)
        
        # Draw text
        text = group.name
        if is_active:
            text = "✓ " + text
        
        text_w = get_text_width(text, 13)
        text_x = current_x + (btn_width - text_w) / 2
        text_y = button_y + (button_height - 13) / 2 + 2
        draw_text(text, text_x, text_y, 13, (1, 1, 1, 1))
        
        current_x += btn_width + button_spacing
    
    # Draw "Show All" button
    is_show_all_active = (active_idx == -1)
    if is_show_all_active:
        btn_color = (0.25, 0.55, 0.35, 1.0)  # Green for active
    else:
        btn_color = (0.25, 0.25, 0.25, 0.9)
    
    draw_rounded_rect(current_x, button_y, show_all_width, button_height, btn_color)
    text = "Show All"
    if is_show_all_active:
        text = "✓ " + text
    text_w = get_text_width(text, 13)
    text_x = current_x + (show_all_width - text_w) / 2
    text_y = button_y + (button_height - 13) / 2 + 2
    draw_text(text, text_x, text_y, 13, (1, 1, 1, 1))
    
    gpu.state.blend_set('NONE')


def hide_overlay():
    """Hide the overlay after delay."""
    global _is_visible
    _is_visible = False
    
    # Force redraw
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
    
    return None  # Don't repeat timer


class NPANEL_OT_ScrollSwitch(bpy.types.Operator):
    """Quick switch groups with Ctrl+Shift+Scroll"""
    bl_idname = "npanel.scroll_switch"
    bl_label = "Scroll Switch Groups"
    bl_options = {'INTERNAL'}
    
    direction: bpy.props.IntProperty(default=0)  # 1 = next, -1 = previous
    
    def execute(self, context):
        global _is_visible, _hide_timer
        
        prefs = get_prefs()
        if not prefs:
            return {'CANCELLED'}
        
        if len(prefs.groups) == 0:
            self.report({'WARNING'}, "No groups created yet")
            return {'CANCELLED'}
        
        # Show overlay
        _is_visible = True
        
        # Cancel existing timer
        if _hide_timer is not None:
            try:
                bpy.app.timers.unregister(_hide_timer)
            except:
                pass
        
        # Set timer to hide overlay after 1.5 seconds
        _hide_timer = hide_overlay
        bpy.app.timers.register(_hide_timer, first_interval=1.5)
        
        # Calculate current index
        # -1 = Show All, 0 to N-1 = groups
        if prefs.is_filtering:
            current = prefs.active_group_index
        else:
            current = -1  # Show All
        
        # Calculate new index
        new_index = current + self.direction
        max_index = len(prefs.groups) - 1
        
        # Wrap around: -1 (Show All) <-> 0 <-> ... <-> max_index <-> -1
        if new_index > max_index:
            new_index = -1  # Wrap to Show All
        elif new_index < -1:
            new_index = max_index  # Wrap to last group
        
        # Apply the selection
        from .core import PanelManager
        
        if new_index == -1:
            # Show All
            PanelManager.restore_all(context)
            prefs.is_filtering = False
            prefs.active_group_index = -1
            self.report({'INFO'}, "Show All")
        else:
            # Apply group
            group = prefs.groups[new_index]
            PanelManager.apply_group(context, group.name)
            prefs.active_group_index = new_index
            prefs.is_filtering = True
            self.report({'INFO'}, f"Group: {group.name}")
        
        # Force redraw
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        
        return {'FINISHED'}


# Keymap
addon_keymaps = []


def register():
    global _draw_handler
    
    bpy.utils.register_class(NPANEL_OT_ScrollSwitch)
    
    # Add draw handler
    _draw_handler = bpy.types.SpaceView3D.draw_handler_add(
        draw_overlay_callback, (), 'WINDOW', 'POST_PIXEL'
    )
    
    # Add keymaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        
        # Shift + Scroll Up = Next group
        kmi = km.keymap_items.new(
            'npanel.scroll_switch',
            'WHEELUPMOUSE',
            'PRESS',
            shift=True,
            ctrl=True
        )
        kmi.properties.direction = 1
        addon_keymaps.append((km, kmi))
        
        # Shift + Scroll Down = Previous group
        kmi = km.keymap_items.new(
            'npanel.scroll_switch',
            'WHEELDOWNMOUSE',
            'PRESS',
            shift=True,
            ctrl=True
        )
        kmi.properties.direction = -1
        addon_keymaps.append((km, kmi))
    
    print("[N-Panel Manager] Scroll overlay registered (Ctrl+Shift+Scroll)")


def unregister():
    global _draw_handler, _is_visible, _hide_timer
    
    _is_visible = False
    
    # Cancel timer
    if _hide_timer is not None:
        try:
            bpy.app.timers.unregister(_hide_timer)
        except:
            pass
    
    # Remove keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    # Remove draw handler
    if _draw_handler:
        bpy.types.SpaceView3D.draw_handler_remove(_draw_handler, 'WINDOW')
        _draw_handler = None
    
    bpy.utils.unregister_class(NPANEL_OT_ScrollSwitch)
