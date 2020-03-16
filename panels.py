import bpy
from . properties import ntzsf_scene_props
from . import miscFunc
from . import miscLay

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup, Menu)

# -----------------------------------------------------------------------------
#   Panel
# ----------------------------------------------------------------------------- 

class VIEW3D_PT_ntzsf_frame_options(Panel):
    bl_label = "Neltulz - Frame Options"
    bl_idname = "VIEW3D_PT_ntzsf_frame_options"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.ui_units_x = 15

        frameOptionsSection = layout.column(align=True)

        addonPrefs = context.preferences.addons[__package__].preferences

        miscLay.frameOptions_sectionInner(self, context, scene, addonPrefs, frameOptionsSection)

    #END draw()


class VIEW3D_PT_ntzsf_isolate_options(Panel):
    bl_label = "Neltulz - Isolate Options"
    bl_idname = "VIEW3D_PT_ntzsf_isolate_options"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.ui_units_x = 15

        isolateOptionsSection = layout.column(align=True)

        addonPrefs = context.preferences.addons[__package__].preferences

        miscLay.isolateOptions_sectionInner(self, context, scene, addonPrefs, isolateOptionsSection)

    #END draw()

class VIEW3D_PT_ntzsf_tmpl_options(Panel):
    bl_label = "Neltulz - Isolate Options"
    bl_idname = "VIEW3D_PT_ntzsf_tmpl_options"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.ui_units_x = 15

        templateOptionsSection = layout.column(align=True)

        addonPrefs = bpy.context.preferences.addons[__package__].preferences

        miscLay.templateOptions_section(self, context, scene, addonPrefs, False, templateOptionsSection)

    #END draw()

class VIEW3D_PT_ntzsf_options(Panel):
    bl_label = "Neltulz - Options"
    bl_idname = "VIEW3D_PT_ntzsf_options"
    bl_category = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.ui_units_x = 12

        optionsSection = layout.column(align=True)

        miscLay.options_sectionInner(self, context, scene, True, False, False, False, optionsSection)

    #END draw()



class VIEW3D_PT_ntzsf_sb_panel(Panel):
    bl_label = "Smart Frame v1.0.16"
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
        miscLay.mainSmartFramePanel(self, context, self.bUseCompactSidebarPanel, self.bUseCompactPopupAndPiePanel)
    #END draw()