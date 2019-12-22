import bpy
from . properties import NeltulzSmartFrameSel_IgnitProperties

# -----------------------------------------------------------------------------
#    Keymaps (For Register)
# -----------------------------------------------------------------------------    

def neltulz_smart_frame_sel_register_keymaps(addon_keymaps):

    wm = bpy.context.window_manager

    def createSmartFrameSelKeymap(bCreateFrameKeymap, bCreateIsolateKeymap, bCreateFrameAndIsolateKeymap):
        #Frame
        if bCreateFrameKeymap:
            kmi = km.keymap_items.new("ntz_smrt_frm.select", type = "F", ctrl=False, shift=False, alt=False, value = "PRESS")
            kmi.properties.frameSelection = True
            kmi.properties.isolateSelection = False

        #Isolate / Unhide Selection
        if bCreateIsolateKeymap:
            kmi = km.keymap_items.new("ntz_smrt_frm.select", type = "F", ctrl=False, shift=True, alt=False, value = "PRESS")
            kmi.properties.frameSelection = False
            kmi.properties.isolateSelection = True

        #Frame & Isolate
        if bCreateFrameAndIsolateKeymap:
            kmi = km.keymap_items.new("ntz_smrt_frm.select", type = "F", ctrl=True, shift=True, alt=False, value = "PRESS")
            kmi.properties.frameSelection = True
            kmi.properties.isolateSelection = True

    #------------------------------ 3D View Generic ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="3D View Generic", space_type="VIEW_3D")

    createSmartFrameSelKeymap(True, True, True)

    #add list of keymaps
    addon_keymaps.append(km)

def neltulz_smart_frame_sel_unregister_keymaps(addon_keymaps):
    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    addon_keymaps.clear()