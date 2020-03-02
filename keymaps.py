import bpy
from . properties import ntzsf_scene_props

# -----------------------------------------------------------------------------
#    Keymaps (For Register)
# -----------------------------------------------------------------------------    

def ntzsfRegKM(addon_keymaps):

    wm = bpy.context.window_manager


    #------------------------------ 3D View ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")

    #Frame
    kmi = km.keymap_items.new("view3d.ntzsf_smart_frame", type = "F", ctrl=False, shift=False, alt=False, value = "PRESS")
    kmi.properties.tooltip = "Frame an object, selection of objects, vertice, edge, face, or when all else fails: frame everything"
    kmi.properties.frameSelection = True
    kmi.properties.isolateSelection = False
    kmi.properties.frameMethod = "SEL"

    #Isolate / Unhide Selection
    kmi = km.keymap_items.new("view3d.ntzsf_isolate", type = "F", ctrl=False, shift=True, alt=False, value = "PRESS")
    kmi.properties.tooltip = "Isolate an object, selection of objects, vertice, edge, face, or when all else fails: isolate everything"
    kmi.properties.frameSelection = False
    kmi.properties.isolateSelection = True
    kmi.properties.frameMethod = "SEL"

    #Frame & Isolate
    kmi = km.keymap_items.new("view3d.ntzsf_frame_and_isolate", type = "F", ctrl=True, shift=True, alt=False, value = "PRESS")
    kmi.properties.tooltip = "Frame and Isolate an object, selection of objects, vertices, edges, or faces, simultaneously, or when all else fails: everything"
    kmi.properties.frameSelection = True
    kmi.properties.isolateSelection = True
    kmi.properties.frameMethod = "SEL"
    
    #Viewport to Origin
    kmi = km.keymap_items.new("view3d.ntzsf_viewport_to_origin", type = "R", ctrl=True, shift=True, alt=False, value = "PRESS")
    kmi.properties.tooltip = "Move the viewport to the origin"
    kmi.properties.frameSelection = True
    kmi.properties.isolateSelection = False
    kmi.properties.frameMethod = "ORIGIN"
    
    #Template Object
    kmi = km.keymap_items.new("view3d.ntzsf_toggle_template", type = "T", ctrl=True, shift=True, alt=False, value = "PRESS")
    kmi.properties.tooltip = "Converts an object to a wireframe with click-through (unselectable) capability for reference purposes"

    #add list of keymaps
    addon_keymaps.append(km)

def ntzsfUnregKM(addon_keymaps):
    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    addon_keymaps.clear()