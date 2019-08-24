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
    bl_label = "Smart Frame Selection v1.0.3"
    bl_category = "Smart Frame Sel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)
        row = col.row(align=True)
    

        
        col = layout.column(align=True)
        col.label(text="When nothing is selected:")
        row = col.row(align=True)

        row.prop(context.scene.neltulzSmartFrameSel, "frameOnlyMesh", expand=True)


        col = layout.column(align=True)
        row = col.row(align=True)
        

        if not scene.neltulzSmartFrameSel.frameOnlyMesh:

            boxAdvancedOptions = layout.box()
            boxAdvancedOptions.label(text="When nothing is selected:")

            box = boxAdvancedOptions.column(align=True)
            
            col = box.column(align=True)

            col.prop(context.scene.neltulzSmartFrameSel, "frameMesh", expand=True)
            col.prop(context.scene.neltulzSmartFrameSel, "frameCurve", expand=True)
            col.prop(context.scene.neltulzSmartFrameSel, "frameSurface", expand=True)
            col.prop(context.scene.neltulzSmartFrameSel, "frameMeta", expand=True)
            col.prop(context.scene.neltulzSmartFrameSel, "frameText", expand=True)
            col.prop(context.scene.neltulzSmartFrameSel, "frameGreasePen", expand=True)
            col.prop(context.scene.neltulzSmartFrameSel, "frameArmature", expand=True)
            col.prop(context.scene.neltulzSmartFrameSel, "frameLattice", expand=True)
            col.prop(context.scene.neltulzSmartFrameSel, "frameEmpty", expand=True)
            col.prop(context.scene.neltulzSmartFrameSel, "frameLight", expand=True)
            col.prop(context.scene.neltulzSmartFrameSel, "frameLightProbe", expand=True)
            col.prop(context.scene.neltulzSmartFrameSel, "frameCamera", expand=True)
            col.prop(context.scene.neltulzSmartFrameSel, "frameSpeaker", expand=True)

        col = layout.column(align=True)
        row = col.row(align=True)
        
        col = layout.column(align=True)

        op = col.operator('object.neltulz_smart_frame_sel', text="Frame")
        op.frameSelection=True
        op.isolateSelection=False


        col = layout.column(align=True)
        operatorText = "Isolate"
        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
            operatorText = "Unhide"
        op = col.operator('object.neltulz_smart_frame_sel', text=operatorText)
        op.frameSelection=False
        op.isolateSelection=True

        col = layout.column(align=True)
        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
            col.enabled=False
        op = col.operator('object.neltulz_smart_frame_sel', text="Frame & Isolate")
        op.frameSelection=True
        op.isolateSelection=True