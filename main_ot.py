import bpy
from . properties import NTZSMFRM_ignitproperties
from . import misc_functions

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#    Main Addon Operator
# -----------------------------------------------------------------------------    

class NTZSMFRM_OT_smartframe(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.select"
    bl_label = "Neltulz - Smart Frame"
    bl_description = 'Smart Frame'
    bl_options = {'REGISTER', 'UNDO'}

    tooltip: bpy.props.StringProperty()

    wasInvoked : BoolProperty(
        name="Operator was invoked",
        default = False
    )

    invokeView : StringProperty(
        name="Invoke View Operators",
    )

    frameSelection : BoolProperty(
        name="Frame Selection",
        description="Frame selected objects or verts, edges, and faces (Default: True)",
        default = True
    )

    isolateSelection : BoolProperty(
        name="Isolate Selection",
        description="Isolate Selection when Framing (Default: False)",
        default = False
    )

    use_zoomAdjust : BoolProperty (
        name        = "Use Zoom Adjust",
        description = "Use Zoom Adjust when framing objects, verts, edges, or faces",
        default     = True
    )

    zoomAdjust : FloatProperty(
        name="Zoom Adjust",
        description="Adjust the zoom amount. (Default: 0)",
        soft_min = -2,
        soft_max = 2,
        default = 0,
    )

    resetZoomAdjust : BoolProperty(
        name="Reset Zoom Adjust",
        default = False
    )



    viewSelectMethod : StringProperty(
        name="View Select Method",
        description="Whether the view select method is OBJ, SINGLE_VERT, EDGE, FACE, or OBJ",
        default="NONE",
    )

    viewSelectionWidth : FloatProperty(
        name="View Selection Width",
        description="Width of the selected vert, edge, face, object, or empty",
        default=1,
    )

    @classmethod
    def poll(cls, context):
        return True

    @classmethod
    def description(cls, context, properties):
        return properties.tooltip

    def draw(self, context):
        scene = context.scene
        layout = self.layout.column(align=True)

        zoomAdjustRow = layout.row(align=True)
        zoomAdjustRow.prop(self, "use_zoomAdjust", text="")
        zoomAdjustSlider = zoomAdjustRow.row(align=True)

        bZoomAdjustUseSlider = True
        if not self.use_zoomAdjust:
            zoomAdjustSlider.enabled = False
            bZoomAdjustUseSlider = False

        zoomAdjustSlider.prop(self, "zoomAdjust", slider=bZoomAdjustUseSlider)

        zoomAdjustRow.prop(self, "resetZoomAdjust", expand=True, text="", icon="LOOP_BACK")
    #END draw()

    def execute(self, context):

        addonPrefs = context.preferences.addons[__package__].preferences
        
        if not self.wasInvoked:
            self.invokeView = "EXEC_DEFAULT"
            

        scene = context.scene
        
        if self.resetZoomAdjust:
            self.resetZoomAdjust = False

            self.zoomAdjust = 0

        modeAtBegin = "Unknown"
        try:
            #try to determine objectMode
            modeAtBegin = bpy.context.object.mode
        except:
            modeAtBegin = "OBJECT"

        showErrorMessages = True #declare
        if scene.ntzSmFrm.useAdvancedSettings:
            if scene.ntzSmFrm.hideErrorMessages:
                showErrorMessages = False

        #use all regions when framing? (Useful for quad view)
        bUseAllRegions = addonPrefs.useAllRegionsWhenFraming
        bUseAll3DAreas = addonPrefs.useAll3DAreasWhenFraming

        objectMode = "Unknown"
        selObjs = bpy.context.selected_objects
        activeObj = bpy.context.view_layer.objects.active
        

        try:
            #try to determine objectMode
            objectMode = bpy.context.object.mode
        except:
            objectMode = "OBJECT"

        if activeObj is not None:
            if not activeObj in selObjs:
                if objectMode == "EDIT":
                    activeObj.select_set(True)
                    selObjs.append(activeObj)

        visibilityCommandList = [
            "context.space_data.show_object_viewport_mesh",
            "context.space_data.show_object_viewport_curve",
            "context.space_data.show_object_viewport_surf",
            "context.space_data.show_object_viewport_meta",
            "context.space_data.show_object_viewport_font",
            "context.space_data.show_object_viewport_grease_pencil",
            "context.space_data.show_object_viewport_armature",
            "context.space_data.show_object_viewport_lattice",
            "context.space_data.show_object_viewport_empty",
            "context.space_data.show_object_viewport_light",
            "context.space_data.show_object_viewport_light_probe",
            "context.space_data.show_object_viewport_camera",
            "context.space_data.show_object_viewport_speaker",
        ]

        visibilitySceneBoolList = [
            "addonPrefs.frameMesh",
            "addonPrefs.frameCurve",
            "addonPrefs.frameSurface",
            "addonPrefs.frameMeta",
            "addonPrefs.frameText",
            "addonPrefs.frameGreasePen",
            "addonPrefs.frameArmature",
            "addonPrefs.frameLattice",
            "addonPrefs.frameEmpty",
            "addonPrefs.frameLight",
            "addonPrefs.frameLightProbe",
            "addonPrefs.frameCamera",
            "addonPrefs.frameSpeaker",
        ]

        previousVisibility = list()

        if self.frameSelection:
            #set obj type visibility so that certain object types can be excluded when framing
            misc_functions.setObjTypeVisibility(self, context, scene, addonPrefs, visibilityCommandList, previousVisibility, visibilitySceneBoolList)

        #if nothing is selected...
        if len(selObjs) == 0:

            if objectMode == "OBJECT" and activeObj == None:

                allSceneObjs = [obj for obj in scene.objects]

                visibleObjsFound = False #declare

                for obj in allSceneObjs:
                    if obj.visible_get():
                        visibleObjsFound = True
                        break

                if visibleObjsFound > 0:

                    if self.frameSelection:
                        misc_functions.viewAll(self, context, bUseAll3DAreas)

                else:

                    if self.frameSelection:
                        #No objects found!
                        bpy.ops.ntz_smrt_frm.viewporttoorigin()

                
                #if user wants to isolate selection...
                if self.isolateSelection:
                    if scene.ntzSmFrm.currentlyBusyIsolating:
                        misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                    else:
                        misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

            else:

                #if user wants to isolate selection...
                if self.isolateSelection:
                    if scene.ntzSmFrm.currentlyBusyIsolating:
                        misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                    else:
                        misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                #user did not want to isolate selection, instead, frame select.
                else:
                    if self.frameSelection:
                        misc_functions.viewAll(self, context, bUseAll3DAreas)

        #if there's something selected...
        elif len(selObjs) > 0:

            if activeObj == None:
                bpy.context.view_layer.objects.active = selObjs[0]
                activeObj = selObjs[0]

            if objectMode == "EDIT":

                if activeObj.type == "MESH":

                    totalNumVertsSel = 0 #declare

                    #get num of selected verts
                    for obj in selObjs:
                        selectedVerts = misc_functions.getSelectedVerts(self, context, obj, "VERTS_ONLY")

                        if selectedVerts is not None:
                            totalNumVertsSel += len( selectedVerts )

                    
                    if totalNumVertsSel > 0:
                        
                        if self.frameSelection:
                            misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    else:

                        #no verts selected
                        if self.frameSelection:

                            bpy.ops.object.mode_set(mode = 'OBJECT')

                            misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                            bpy.ops.object.mode_set(mode = 'EDIT')
                    
                    
                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_VertsEdgesFaces(self, context, scene)
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            if totalNumVertsSel > 0:
                                misc_functions.hideSelected_VertsEdgesFaces(self, context, scene)
                                misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                elif activeObj.type == "CURVE":

                    totalNumCurvePointsSel = 0 #declare
                    totalNumCurveHandlesLeft = 0 #declare
                    totalNumCurveHandlesRight = 0 #declare
                    totalNumCurvePointsAndHandles = 0 #declare

                    #get num of selected curve points & handles
                    for obj in selObjs:
                        selectedCurvePointsAndHandles = misc_functions.getSelectedCurvePointsAndHandles(self, context, obj)

                        if selectedCurvePointsAndHandles is not None:
                            totalNumCurvePointsSel += len( selectedCurvePointsAndHandles[0] )
                            totalNumCurveHandlesLeft += len( selectedCurvePointsAndHandles[1] )
                            totalNumCurveHandlesRight += len( selectedCurvePointsAndHandles[2] )
                            totalNumCurvePointsAndHandles = totalNumCurvePointsSel + totalNumCurveHandlesLeft + totalNumCurveHandlesRight

                    if totalNumCurvePointsAndHandles > 0:

                        if self.frameSelection:
                            misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                        if self.isolateSelection:
                            if scene.ntzSmFrm.currentlyBusyIsolating:
                                misc_functions.unhidePreviouslyHidden_CurvePointsAndHandles(self, context, scene)
                                misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                            else:
                                misc_functions.hideSelected_CurvePointsAndHandles(self, context, scene)
                                misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                    else:

                        #no curve points and handles selected
                        if self.frameSelection:

                            bpy.ops.object.mode_set(mode = 'OBJECT')

                            misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                            bpy.ops.object.mode_set(mode = 'EDIT')

                elif activeObj.type == "SURFACE":
                    if self.frameSelection:
                        misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                elif activeObj.type == "META":
                    if self.frameSelection:
                        misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)
                    
                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)
                
                elif activeObj.type == "FONT":
                    if self.frameSelection:
                        misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)
                    
                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                elif activeObj.type == "ARMATURE":
                    if self.frameSelection:
                        misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)
                
                elif activeObj.type == "LATTICE":
                    if self.frameSelection:
                        misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                else:
                    if self.frameSelection:
                        misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)
                    
            elif objectMode == "OBJECT":

                #frame selection
                if self.frameSelection:
                    if self.isolateSelection:
                        if not scene.ntzSmFrm.currentlyBusyIsolating:
                            misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)
                    
                    else:
                        misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)
                
                #isolate selection
                if self.isolateSelection:
                    
                    if scene.ntzSmFrm.currentlyBusyIsolating:
                        misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                    else:
                        misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

            elif objectMode == "EDIT_GPENCIL":
                if activeObj.type == "GPENCIL":
                    if self.frameSelection:
                        misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

            elif objectMode == "PAINT_GPENCIL":
                if activeObj.type == "GPENCIL":
                    if self.frameSelection:
                        misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

            elif objectMode == "SCULPT_GPENCIL":
                if activeObj.type == "GPENCIL":
                    if self.frameSelection:
                        misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                

            elif objectMode == "POSE":
                if activeObj.type == "ARMATURE":
                    if self.frameSelection:
                        misc_functions.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

        #re-enable visibility for all objects
        misc_functions.reenableVisibilityForAllObjs(self, context, scene, previousVisibility, visibilityCommandList)
        
        #final step
        if self.wasInvoked:
            self.wasInvoked = False

        return {'FINISHED'}
    # END execute()

    def invoke(self, context, event):

        addonPrefs = context.preferences.addons[__package__].preferences

        scene = context.scene
        self.wasInvoked = True

        if addonPrefs.bUseSmoothFraming:
            self.invokeView = "INVOKE_DEFAULT"
        else:
            self.invokeView = "EXEC_DEFAULT"
        
        return self.execute(context)
    #END invoke()
    
# END Operator()







