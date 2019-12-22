import bpy
from . properties import NeltulzSmartFrameSel_IgnitProperties
from . import misc_functions
from . misc_layout import createShowHide

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#   Panel
# ----------------------------------------------------------------------------- 

class OBJECT_PT_NeltulzSmartFrameSel(Panel):

    bl_idname = "ntz_smrt_frm.panel"
    bl_label = "Smart Frame v1.0.12"
    bl_category = "Neltulz"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)
        col.scale_y = 1.5
        row = col.row(align=True)
        

        op = row.operator('ntz_smrt_frm.select', text="Frame", icon="SHADING_BBOX")
        op.frameSelection=True
        op.isolateSelection=False


        operatorText = "Isolate"
        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
            operatorText = "Unhide"
        op = row.operator('ntz_smrt_frm.select', text=operatorText, icon="BORDERMOVE")
        op.frameSelection=False
        op.isolateSelection=True



        col = layout.column(align=True)
        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
            col.enabled=False
        op = col.operator('ntz_smrt_frm.select', text="Frame & Isolate")
        op.frameSelection=True
        op.isolateSelection=True

        col = layout.column(align=True)
        op = col.operator('ntz_smrt_frm.viewporttoorigin', text="Viewport to Origin")




        #BEGIN "When Nothing is selected, frame..." section
        optionsSection = layout.column(align=True)

        #create show/hide toggle for options section
        createShowHide(self, context, scene, "neltulzSmartFrameSel", "bShowOptions", None, "Options", optionsSection)

        if scene.neltulzSmartFrameSel.bShowOptions:

            optionsSection.separator()

            optionsSectionRow = optionsSection.row(align=True)

            spacer = optionsSectionRow.column(align=True)
            spacer.label(text=" ")
            spacer.ui_units_x = 1
            
            optionsSectionInner = optionsSectionRow.column(align=True)
            optionsSectionInner.ui_units_x = 10000

            boxFrameOptions = optionsSectionInner.box()
            boxFrameOptions.label(text="When nothing is selected, frame:")

            box = boxFrameOptions.column(align=True)

            row = box.row(align=True)

            if not scene.neltulzSmartFrameSel.showFrameList:
                row.prop(context.scene.neltulzSmartFrameSel, "showFrameList", text="Show List", expand=True, toggle=True)
            else:
                row.prop(context.scene.neltulzSmartFrameSel, "showFrameList", text="Hide List", expand=True, toggle=True)
            
                row = box.row(align=True)

                col = row.column(align=True)

                col.prop(context.scene.neltulzSmartFrameSel, "frameMesh", expand=True, toggle=False)
                col.prop(context.scene.neltulzSmartFrameSel, "frameCurve", expand=True, toggle=False)
                col.prop(context.scene.neltulzSmartFrameSel, "frameSurface", expand=True, toggle=False)
                col.prop(context.scene.neltulzSmartFrameSel, "frameMeta", expand=True, toggle=False)
                col.prop(context.scene.neltulzSmartFrameSel, "frameText", expand=True, toggle=False)
                col.prop(context.scene.neltulzSmartFrameSel, "frameGreasePen", expand=True, toggle=False)
                col.prop(context.scene.neltulzSmartFrameSel, "frameArmature", expand=True, toggle=False)
                

                col = row.column(align=True)
                
                col.prop(context.scene.neltulzSmartFrameSel, "frameLattice", expand=True, toggle=False)
                col.prop(context.scene.neltulzSmartFrameSel, "frameEmpty", expand=True, toggle=False)
                col.prop(context.scene.neltulzSmartFrameSel, "frameLight", expand=True, toggle=False)
                col.prop(context.scene.neltulzSmartFrameSel, "frameLightProbe", expand=True, toggle=False)
                col.prop(context.scene.neltulzSmartFrameSel, "frameCamera", expand=True, toggle=False)
                col.prop(context.scene.neltulzSmartFrameSel, "frameSpeaker", expand=True, toggle=False)

            #END "When Nothing is selected, frame..." section

            #BEGIN Excluded Objects from Isolate Section:

            optionsSectionInner.separator()

            excludedObjectsSection = optionsSectionInner.row(align=True)
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

                        op = row.operator('ntz_smrt_frm.unexcludeobj', text="", icon="X")
                        op.objectToRemove = item

                        row.label(text=item)


                    


            else: 
                row = boxCol.row(align=True)
                row.label(text="None")

            excludedObjectsSectionCol = excludedObjectsSection.column(align=True)

            op = excludedObjectsSectionCol.operator('ntz_smrt_frm.excludeobj', text="", icon="ADD")
            op = excludedObjectsSectionCol.operator('ntz_smrt_frm.unexcludeobj', text="", icon="REMOVE")
            op = excludedObjectsSectionCol.operator('ntz_smrt_frm.refreshexcludedobjlist', text="", icon="FILE_REFRESH")
            op = excludedObjectsSectionCol.operator('ntz_smrt_frm.clearexcludedobjs', text="", icon="TRASH")

            #END Excluded Objects from Isolate Section





            #BEGIN Templated Objects Section:

            optionsSectionInner.separator()

            templatedObjectsSection = optionsSectionInner.row(align=True)
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

                        op = row.operator('ntz_smrt_frm.removetemplatedobj', text="", icon="X")
                        op.objectToRemove = item

                        row.label(text=item)
                        


                    


            else: 
                row = boxCol.row(align=True)
                row.label(text="None")

            templatedObjectsSectionCol = templatedObjectsSection.column(align=True)

            op = templatedObjectsSectionCol.operator('ntz_smrt_frm.convertobjtotemplate', text="", icon="ADD")
            op = templatedObjectsSectionCol.operator('ntz_smrt_frm.refreshtemplatedobjlist', text="", icon="FILE_REFRESH")
            op = templatedObjectsSectionCol.operator('ntz_smrt_frm.clearalltemplatedobjs', text="", icon="TRASH")

            #END Templated Objects Section


            optionsSectionInner.separator()

            col = optionsSectionInner.column(align=True)
            row = col.row(align=True)
            row.prop(context.scene.neltulzSmartFrameSel, "use_all_regions_when_framing", expand=True)

            optionsSectionInner.separator()

            col = optionsSectionInner.column(align=True)
            col.label(text="On Isolate, hide:")

            row = col.row(align=True)

            row.prop(context.scene.neltulzSmartFrameSel, "hideFloorOnIsolate", expand=True, text="Floor", toggle=True, icon="MESH_GRID")

            row.prop(context.scene.neltulzSmartFrameSel, "hideAxesOnIsolate", expand=True, text="Axes", toggle=True, icon="EMPTY_AXIS")

            optionsSectionInner.separator()

            col = optionsSectionInner.column(align=True)
            col.prop(context.scene.neltulzSmartFrameSel, "useExtremeHideOnIsolate", expand=True)