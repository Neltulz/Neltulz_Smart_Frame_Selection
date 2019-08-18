import bpy
from . properties import NeltulzSmartFrameSel_IgnitProperties
from . import misc_functions

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

# -----------------------------------------------------------------------------
#   Panel
# ----------------------------------------------------------------------------- 

class OBJECT_PT_NeltulzSmartFrameSel(Panel):

    bl_idname = "object.neltulz_smart_frame_sel_panel"
    bl_label = "SubD Edge v1.0.1"
    bl_category = "Neltulz - SubD Edge"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):

        layout = self.layout
        scene = context.scene
        obj = context.object

        col = layout.column(align=True)
        #col.label(text="Title:")
        row = col.row(align=True)

        #op = row.operator('object.neltulz_smart_frame_sel', text="BUTTON TEXT")
        #op.PROPERTYNAME=1

        #END Overlay Options (Wireframe, Edge colors, etc)

        # -----------------------------------------------------------------------------
        #   Use Advanced Settings Box
        # -----------------------------------------------------------------------------

        col = layout.column(align=True)
        row = col.row(align=True)

        op = row.operator('object.neltulz_smart_frame_sel', text="Subdivide Edge(s)")

        col.separator()

        col.prop(context.scene.neltulzSmartFrameSel, "advancedSettings", text="Use Advanced Settings" )

        #if scene.neltulzSmartFrameSel.advancedSettings:

            #boxAdvancedOptions = layout.box()
            #boxAdvancedOptions.label(text="Advanced Settings:")

            #box = boxAdvancedOptions.column(align=True)
            
            #row = box.row(align=True)

            #op = row.operator('object.neltulz_smart_frame_sel', text="BUTTON TEXT")
            #op.PROPERTYNAME=1

        #END Use Advanced Settings Box