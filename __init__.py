bl_info = {
    "name" : "Neltulz - Smart Frame",
    "author" : "Neil V. Moore",
    "description" : 'More ways to "Frame Selection" when pressing the keyboard shortcut',
    "blender" : (2, 80, 0),
    "version" : (1, 0, 16),
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

#scene properties
from . properties          import ntzsf_scene_props

#main operator
from . mainOt              import VIEW3D_OT_ntzsf_smart_frame
from . mainOt              import VIEW3D_OT_ntzsf_isolate
from . mainOt              import VIEW3D_OT_ntzsf_frame_and_isolate
from . mainOt              import VIEW3D_OT_ntzsf_viewport_to_origin

#misc operators
from . miscOt              import VIEW3D_OT_ntzsf_add_obj_to_excluded_isolate_objs
from . miscOt              import VIEW3D_OT_ntzsf_del_obj_from_excluded_isolate_objs
from . miscOt              import VIEW3D_OT_ntzsf_refresh_excluded_isolate_objs
from . miscOt              import VIEW3D_OT_ntzsf_clear_all_excluded_isolate_objs
from . miscOt              import VIEW3D_OT_ntzsf_convert_obj_to_template
from . miscOt              import VIEW3D_OT_ntzsf_refresh_template_objs
from . miscOt              import VIEW3D_OT_ntzsf_untemplate_objs
from . miscOt              import VIEW3D_OT_ntzsf_toggle_template
from . miscOt              import VIEW3D_OT_ntzsf_template_specific_obj
from . miscOt              import VIEW3D_OT_ntzsf_untemplate_specific_obj
from . miscOt              import VIEW3D_OT_ntzsf_clear_all_template_objs
from . miscOt              import VIEW3D_OT_ntzsf_change_template_selection_state
from . miscOt              import VIEW3D_OT_ntzsf_sel_obj_by_name

#addon preferences operator
from . addonPreferences    import VIEW3D_OT_ntzsf_addon_prefs

#panels
from . panels              import VIEW3D_PT_ntzsf_frame_options
from . panels              import VIEW3D_PT_ntzsf_isolate_options
from . panels              import VIEW3D_PT_ntzsf_tmpl_options
from . panels              import VIEW3D_PT_ntzsf_options
from . panels              import VIEW3D_PT_ntzsf_sb_panel

#keymaps
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
    #scene properties
    ntzsf_scene_props,

    #main operator
    VIEW3D_OT_ntzsf_smart_frame,
    VIEW3D_OT_ntzsf_isolate,
    VIEW3D_OT_ntzsf_frame_and_isolate,
    VIEW3D_OT_ntzsf_viewport_to_origin,

    #misc operators
    VIEW3D_OT_ntzsf_add_obj_to_excluded_isolate_objs,
    VIEW3D_OT_ntzsf_del_obj_from_excluded_isolate_objs,
    VIEW3D_OT_ntzsf_refresh_excluded_isolate_objs,
    VIEW3D_OT_ntzsf_clear_all_excluded_isolate_objs,
    VIEW3D_OT_ntzsf_convert_obj_to_template,
    VIEW3D_OT_ntzsf_refresh_template_objs,
    VIEW3D_OT_ntzsf_untemplate_objs,
    VIEW3D_OT_ntzsf_toggle_template,
    VIEW3D_OT_ntzsf_template_specific_obj,
    VIEW3D_OT_ntzsf_untemplate_specific_obj,
    VIEW3D_OT_ntzsf_clear_all_template_objs,
    VIEW3D_OT_ntzsf_change_template_selection_state,
    VIEW3D_OT_ntzsf_sel_obj_by_name,

    #addon preferences operator
    VIEW3D_OT_ntzsf_addon_prefs,

    #panels
    VIEW3D_PT_ntzsf_frame_options,
    VIEW3D_PT_ntzsf_isolate_options,
    VIEW3D_PT_ntzsf_tmpl_options,
    VIEW3D_PT_ntzsf_options,
    VIEW3D_PT_ntzsf_sb_panel,
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
    addonPrefs = bpy.context.preferences.addons[__name__].preferences
    addonPreferences.update_panel(addonPrefs, bpy.context)
    
    #add keymaps from keymaps.py
    keymaps.ntzsfRegKM(addon_keymaps)

    #add property group to the scene
    bpy.types.Scene.ntzSmFrm = bpy.props.PointerProperty(type=ntzsf_scene_props)

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
    keymaps.ntzsfUnregKM(addon_keymaps)

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.view3d.ntzsf_smart_frame()