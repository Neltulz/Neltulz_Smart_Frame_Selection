import bpy
from . properties import NeltulzSmartFrameSel_IgnitProperties

# -----------------------------------------------------------------------------
#    Keymaps (For Register)
# -----------------------------------------------------------------------------    

def neltulz_smart_frame_sel_register_keymaps(addon_keymaps):

    wm = bpy.context.window_manager

    def createSmartFrameSelKeymap():
        #create shortcuts for keymap
        kmi = km.keymap_items.new("object.neltulz_smart_frame_sel", type = "F", ctrl=False, shift=False, alt=False, value = "PRESS")
        #kmi.properties.PROPERTYNAME = 1

    #------------------------------ Object Mode ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Object Mode", space_type="EMPTY")

    createSmartFrameSelKeymap()

    #add list of keymaps
    addon_keymaps.append(km)

    #------------------------------ Mesh Mode ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Mesh", space_type="EMPTY")

    createSmartFrameSelKeymap()

    #add list of keymaps
    addon_keymaps.append(km)



def neltulz_smart_frame_sel_unregister_keymaps(addon_keymaps):
    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    addon_keymaps.clear()