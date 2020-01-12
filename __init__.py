bl_info = {
    "name" : "Neltulz - Smart Frame",
    "author" : "Neil V. Moore",
    "description" : 'More ways to "Frame Selection" when pressing the keyboard shortcut',
    "blender" : (2, 80, 0),
    "version" : (1, 0, 13),
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

from . properties           import NTZSMFRM_ignitproperties
from . main_ot              import NTZSMFRM_OT_smartframe
from . misc_ot              import NTZSMFRM_OT_addobjtoexcludedisolateobjs
from . misc_ot              import NTZSMFRM_OT_removeobjfromexcludedisolateobjs
from . misc_ot              import NTZSMFRM_OT_refreshexcludedisolateobjs
from . misc_ot              import NTZSMFRM_OT_clearallexcludedisolateobjs
from . misc_ot              import NTZSMFRM_OT_templateobj
from . misc_ot              import NTZSMFRM_OT_refreshtemplateobjs
from . misc_ot              import NTZSMFRM_OT_untemplateobjs
from . misc_ot              import NTZSMFRM_OT_toggletemplate
from . misc_ot              import NTZSMFRM_OT_templatespecificobj
from . misc_ot              import NTZSMFRM_OT_untemplatespecificobj
from . misc_ot              import NTZSMFRM_OT_clearalltemplatedobjs
from . misc_ot              import NTZSMFRM_OT_viewtoorigin
from . misc_ot              import NTZSMFRM_OT_changetemplateselectionstate
from . misc_ot              import NTZSMFRM_OT_selobj
from . addon_preferences    import NTZSMFRM_OT_addonprefs
from . panels               import NTZSMFRM_PT_frameoptions
from . panels               import NTZSMFRM_PT_isolateoptions
from . panels               import NTZSMFRM_PT_templateoptions
from . panels               import NTZSMFRM_PT_options
from . panels               import NTZSMFRM_PT_sidebarpanel

from . import keymaps

PendingDeprecationWarning

bDebugModeActive = False
if bDebugModeActive:
    print("##################################################################################################################################################################")
    print("REMINDER: DEBUG MODE ACTIVE")
    print("##################################################################################################################################################################")

# -----------------------------------------------------------------------------
#    Store classes in List so that they can be easily registered/unregistered    
# -----------------------------------------------------------------------------  

classes = (
    NTZSMFRM_ignitproperties,
    NTZSMFRM_OT_smartframe,
    NTZSMFRM_OT_addobjtoexcludedisolateobjs,
    NTZSMFRM_OT_removeobjfromexcludedisolateobjs,
    NTZSMFRM_OT_refreshexcludedisolateobjs,
    NTZSMFRM_OT_clearallexcludedisolateobjs,
    NTZSMFRM_OT_templateobj,
    NTZSMFRM_OT_refreshtemplateobjs,
    NTZSMFRM_OT_untemplateobjs,
    NTZSMFRM_OT_toggletemplate,
    NTZSMFRM_OT_templatespecificobj,
    NTZSMFRM_OT_untemplatespecificobj,
    NTZSMFRM_OT_clearalltemplatedobjs,
    NTZSMFRM_OT_viewtoorigin,
    NTZSMFRM_OT_changetemplateselectionstate,
    NTZSMFRM_OT_addonprefs,
    NTZSMFRM_OT_selobj,
    NTZSMFRM_PT_frameoptions,
    NTZSMFRM_PT_isolateoptions,
    NTZSMFRM_PT_templateoptions,
    NTZSMFRM_PT_options,
    NTZSMFRM_PT_sidebarpanel,
)

# -----------------------------------------------------------------------------
#    Register classes from the classes list
# -----------------------------------------------------------------------------    

addon_keymaps = []

#vscode pme workaround from iceythe (part 2 of 2)
def _reg():
    pme = bpy.utils._preferences.addons['pie_menu_editor'].preferences
    for pm in pme.pie_menus:
        if pm.key != 'NONE':
            pm.register_hotkey()
#END vscode pme workaround (part 2 of 2)

def register():

    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # update panel name
    prefs = bpy.context.preferences.addons[__name__].preferences
    addon_preferences.update_panel(prefs, bpy.context)

    #add keymaps from keymaps.py
    keymaps.neltulz_smart_frame_sel_register_keymaps(addon_keymaps)

    #add property group to the scene
    bpy.types.Scene.ntzSmFrm = bpy.props.PointerProperty(type=NTZSMFRM_ignitproperties)

    #vscode pme workaround from iceythe (part 1 of 2)
    #must be appended to def register() so that it is the last thing that executes
    if bDebugModeActive:
        if not bpy.app.timers.is_registered(_reg):
            bpy.app.timers.register(_reg, first_interval=1)
    #END vscode pme workaround (part 1 of 2)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    #remove keymaps
    keymaps.neltulz_smart_frame_sel_unregister_keymaps(addon_keymaps)

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.ntz_smrt_frm.select()