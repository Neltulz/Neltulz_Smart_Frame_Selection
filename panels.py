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
    bl_label = "Smart Frame Selection v1.0.7"
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
        row.prop(context.scene.neltulzSmartFrameSel, "hideFloorOnIsolate", expand=True)
        
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


        #BEGIN Excluded Objects from Isolate Section:

        excludedObjectsSection = layout.row(align=True)
        excludedObjectsSectionCol = excludedObjectsSection.column(align=True)

        numExcludedFromIsolate = len(scene.neltulzSmartFrameSel.excludedIsolateObjects)

        boxExcludedIsolate = excludedObjectsSectionCol.box()
        
        objectText = "objects"
        if numExcludedFromIsolate == 1:
            objectText = "object"
            
        text="Excluded objects from isolate: " + str(numExcludedFromIsolate) + " " + objectText + "."
        boxExcludedIsolate.label(text=text)

        boxCol = boxExcludedIsolate.column(align=True)

        

        if numExcludedFromIsolate > 0:

            if not scene.neltulzSmartFrameSel.hideFullIsolateExclusionList:
                row = boxCol.row(align=True)
                row.prop(context.scene.neltulzSmartFrameSel, "hideFullIsolateExclusionList", text="Show List", toggle=True)
            else:
                row = boxCol.row(align=True)
                row.prop(context.scene.neltulzSmartFrameSel, "hideFullIsolateExclusionList", text="Hide List", toggle=True)

                for item in scene.neltulzSmartFrameSel.excludedIsolateObjects:
                    row = boxCol.row(align=True)

                    op = row.operator('object.neltulz_remove_object_from_excluded_isolate_objects', text="", icon="X")
                    op.objectToRemove = item

                    row.label(text=item)


                


        else: 
            row = boxCol.row(align=True)
            row.label(text="None")

        excludedObjectsSectionCol = excludedObjectsSection.column(align=True)

        op = excludedObjectsSectionCol.operator('object.neltulz_add_object_to_excluded_isolate_objects', text="", icon="ADD")
        op = excludedObjectsSectionCol.operator('object.neltulz_remove_object_from_excluded_isolate_objects', text="", icon="REMOVE")
        op = excludedObjectsSectionCol.operator('object.neltulz_refresh_excluded_isolate_objects', text="", icon="FILE_REFRESH")
        op = excludedObjectsSectionCol.operator('object.neltulz_clear_all_excluded_isolate_objects', text="", icon="TRASH")

        #END Excluded Objects from Isolate Section





        #BEGIN Templated Objects Section:

        templatedObjectsSection = layout.row(align=True)
        templatedObjectsSectionCol = templatedObjectsSection.column(align=True)

        numTemplatedObjects = len(scene.neltulzSmartFrameSel.templatedObjects)

        boxTemplatedObjects = templatedObjectsSectionCol.box()
        
        objectText = "objects"
        if numTemplatedObjects == 1:
            objectText = "object"
            
        text="Templated objects: " + str(numTemplatedObjects) + " " + objectText + "."
        boxTemplatedObjects.label(text=text)

        boxCol = boxTemplatedObjects.column(align=True)

        

        if numTemplatedObjects > 0:

            if not scene.neltulzSmartFrameSel.hideFullTemplateList:
                row = boxCol.row(align=True)
                row.prop(context.scene.neltulzSmartFrameSel, "hideFullTemplateList", text="Show List", toggle=True)
            else:
                row = boxCol.row(align=True)
                row.prop(context.scene.neltulzSmartFrameSel, "hideFullTemplateList", text="Hide List", toggle=True)

                for item in scene.neltulzSmartFrameSel.templatedObjects:
                    row = boxCol.row(align=True)

                    op = row.operator('object.neltulz_smart_frame_sel_remove_templated_objects', text="", icon="X")
                    op.objectToRemove = item

                    row.label(text=item)
                    


                


        else: 
            row = boxCol.row(align=True)
            row.label(text="None")

        templatedObjectsSectionCol = templatedObjectsSection.column(align=True)

        op = templatedObjectsSectionCol.operator('object.neltulz_smart_frame_sel_template', text="", icon="ADD")
        op = templatedObjectsSectionCol.operator('object.neltulz_smart_frame_sel_refresh_template_objects', text="", icon="FILE_REFRESH")
        op = templatedObjectsSectionCol.operator('object.neltulz_smart_frame_sel_clear_all_templated_objects', text="", icon="TRASH")

        #END Templated Objects Section




        #BEGIN Advanced Settings Section
        col = layout.column(align=True)
        col.prop(context.scene.neltulzSmartFrameSel, "useAdvancedSettings", toggle=False)

        if scene.neltulzSmartFrameSel.useAdvancedSettings:
            AdvancedOptionsSection = layout.row(align=True)
            boxExcludedIsolate = AdvancedOptionsSection.box()
            
            boxExcludedIsolate.prop(context.scene.neltulzSmartFrameSel, "hideErrorMessages", toggle=False)

        #END Advanced Settings Section