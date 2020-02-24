import bpy
from . properties import NTZSMFRM_ignitproperties
from . import misc_functions
from . import misc_layout

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup, Menu)

# -----------------------------------------------------------------------------
#   Panel
# ----------------------------------------------------------------------------- 

class NTZSMFRM_PT_frameoptions(Panel):
    bl_label = "Neltulz - Frame Options"
    bl_idname = "NTZSMFRM_PT_frameoptions"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.ui_units_x = 15

        frameOptionsSection = layout.column(align=True)

        addonPrefs = context.preferences.addons[__package__].preferences

        misc_layout.frameOptions_sectionInner(self, context, scene, addonPrefs, frameOptionsSection)

    #END draw()


class NTZSMFRM_PT_isolateoptions(Panel):
    bl_label = "Neltulz - Isolate Options"
    bl_idname = "NTZSMFRM_PT_isolateoptions"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.ui_units_x = 15

        isolateOptionsSection = layout.column(align=True)

        addonPrefs = context.preferences.addons[__package__].preferences

        misc_layout.isolateOptions_sectionInner(self, context, scene, addonPrefs, isolateOptionsSection)

    #END draw()

class NTZSMFRM_PT_templateoptions(Panel):
    bl_label = "Neltulz - Isolate Options"
    bl_idname = "NTZSMFRM_PT_templateoptions"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.ui_units_x = 15

        templateOptionsSection = layout.column(align=True)

        addonPrefs = bpy.context.preferences.addons[__package__].preferences

        misc_layout.templateOptions_section(self, context, scene, addonPrefs, False, templateOptionsSection)

    #END draw()

class NTZSMFRM_PT_options(Panel):
    bl_label = "Neltulz - Options"
    bl_idname = "NTZSMFRM_PT_options"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.ui_units_x = 12

        optionsSection = layout.column(align=True)

        misc_layout.options_sectionInner(self, context, scene, True, False, False, False, optionsSection)

    #END draw()



class NTZSMFRM_PT_sidebarpanel(Panel):
    bl_label = "Smart Frame v1.0.14"
    bl_category = "Neltulz"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bUseCompactSidebarPanel = BoolProperty(
        name="Use Compact Panel",
        description="Use Compact Panel",
        default = False
    )

    bUseCompactPopupAndPiePanel = BoolProperty(
        name="Use Compact Popup & Pie Panel",
        description="Use Compact Popup & Pie Panel",
        default = True
    )

    def draw(self, context):
        misc_layout.mainSmartFramePanel(self, context, self.bUseCompactSidebarPanel, self.bUseCompactPopupAndPiePanel)
    #END draw()