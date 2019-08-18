bl_info = {
    "name" : "Neltulz - Smart Frame Selection",
    "author" : "Neil V. Moore",
    "description" : 'More ways to "Frame Selection" when pressing the keyboard shortcut',
    "blender" : (2, 80, 0),
    "version" : (1, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic",
    "tracker_url": "mailto:neilvmoore@gmail.com",
    "wiki_url": "https://www.logichaos.com/neltulz_blender_addons/neltulz_smart_frame_selection/README_Neltulz_Smart_Frame_Selection"
}

# -----------------------------------------------------------------------------
#   Import Classes and/or functions     
# -----------------------------------------------------------------------------  

import bpy

from . properties import NeltulzSmartFrameSel_IgnitProperties
from . main_ot import OBJECT_OT_NeltulzSmartFrameSel
from . panels import OBJECT_PT_NeltulzSmartFrameSel

from . import keymaps

PendingDeprecationWarning


# -----------------------------------------------------------------------------
#    Store classes in List so that they can be easily registered/unregistered    
# -----------------------------------------------------------------------------  

classes = (
    NeltulzSmartFrameSel_IgnitProperties,
    OBJECT_OT_NeltulzSmartFrameSel,
    OBJECT_PT_NeltulzSmartFrameSel,
)

# -----------------------------------------------------------------------------
#    Register classes from the classes list
# -----------------------------------------------------------------------------    

addon_keymaps = []

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    #add keymaps from keymaps.py
    keymaps.neltulz_smart_frame_sel_register_keymaps(addon_keymaps)

    #add property group to the scene
    bpy.types.Scene.neltulzSmartFrameSel = bpy.props.PointerProperty(type=NeltulzSmartFrameSel_IgnitProperties)

    


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    #remove keymaps
    keymaps.neltulz_smart_frame_sel_unregister_keymaps(addon_keymaps)



if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.neltulz_smart_frame_sel()