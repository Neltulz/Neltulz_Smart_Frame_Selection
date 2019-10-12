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
            kmi = km.keymap_items.new("object.neltulz_smart_frame_sel", type = "F", ctrl=False, shift=False, alt=False, value = "PRESS")
            kmi.properties.frameSelection = True
            kmi.properties.isolateSelection = False

        #Isolate / Unhide Selection
        if bCreateIsolateKeymap:
            kmi = km.keymap_items.new("object.neltulz_smart_frame_sel", type = "F", ctrl=False, shift=True, alt=False, value = "PRESS")
            kmi.properties.frameSelection = False
            kmi.properties.isolateSelection = True

        #Frame & Isolate
        if bCreateFrameAndIsolateKeymap:
            kmi = km.keymap_items.new("object.neltulz_smart_frame_sel", type = "F", ctrl=True, shift=True, alt=False, value = "PRESS")
            kmi.properties.frameSelection = True
            kmi.properties.isolateSelection = True



    #------------------------------ Object Mode ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Object Mode", space_type="EMPTY")

    createSmartFrameSelKeymap(True, True, True)

    #add list of keymaps
    addon_keymaps.append(km)

    #------------------------------ Mesh Mode ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Mesh", space_type="EMPTY")

    createSmartFrameSelKeymap(True, True, True)

    #add list of keymaps
    addon_keymaps.append(km)

    #------------------------------ Curve Mode ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Curve", space_type="EMPTY")

    createSmartFrameSelKeymap(True, True, True)

    #add list of keymaps
    addon_keymaps.append(km)

    #------------------------------ Surface Mode ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Surface", space_type="EMPTY")

    createSmartFrameSelKeymap(True, False, False)

    #add list of keymaps
    addon_keymaps.append(km)

    #------------------------------ Meta Mode ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Metaball", space_type="EMPTY")

    createSmartFrameSelKeymap(True, True, True)

    #add list of keymaps
    addon_keymaps.append(km)


    #------------------------------ Grease Pencil Mode ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Grease Pencil Stroke Edit Mode", space_type="EMPTY")

    createSmartFrameSelKeymap(True, True, True)

    #add list of keymaps
    addon_keymaps.append(km)

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Grease Pencil Stroke Paint Mode", space_type="EMPTY")

    createSmartFrameSelKeymap(True, True, True)

    #add list of keymaps
    addon_keymaps.append(km)

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Grease Pencil Stroke Sculpt Mode", space_type="EMPTY")

    createSmartFrameSelKeymap(True, True, True)

    #add list of keymaps
    addon_keymaps.append(km)

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Grease Pencil Stroke Weight Mode", space_type="EMPTY")

    createSmartFrameSelKeymap(True, True, True)

    #add list of keymaps
    addon_keymaps.append(km)

    #------------------------------ Armature Mode ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Armature", space_type="EMPTY")

    createSmartFrameSelKeymap(True, True, True)

    #add list of keymaps
    addon_keymaps.append(km)

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Pose", space_type="EMPTY")

    createSmartFrameSelKeymap(True, True, True)

    #add list of keymaps
    addon_keymaps.append(km)

    #------------------------------ Lattice Mode ----------------------------------------------------------------------------

    #create new keymap
    km = wm.keyconfigs.addon.keymaps.new(name="Lattice", space_type="EMPTY")

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