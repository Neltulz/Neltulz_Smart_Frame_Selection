import bpy
import bmesh

from . properties import ntzsf_scene_props
from . import miscFunc

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#    Main Addon Operator
# -----------------------------------------------------------------------------

class opProps():
    tooltip: bpy.props.StringProperty()

    wasInvoked : BoolProperty (
        name="Operator was invoked",
        default = False
    )

    invokeView : StringProperty (
        name="Invoke View Operators",
    )

    selModeAtBegin = (True, False, False)
    totalVertCount = 0
    totalNumVertsSel = 0

    frameMethod_List = [
        ("SEL",         "Selection", "", "", 0),
        ("ORIGIN",      "Origin",    "", "", 1),
    ]

    frameMethod : EnumProperty (
        items=frameMethod_List,
        description="Frame Method",
        default="SEL",
    )

    frameSelection : BoolProperty (
        name="Frame Selection",
        description="Frame selected objects or verts, edges, and faces (Default: True)",
        default = True
    )

    isolateSelection : BoolProperty (
        name="Isolate Selection",
        description="Isolate Selection when Framing (Default: False)",
        default = False
    )

    
    #fetched on invoke from addonPrefs
    use_zoomAdjust : BoolProperty (
        name        = "Use Zoom Adjust",
        description = "Use Zoom Adjust when framing objects, verts, edges, or faces",
        default     = True
    ) 

    #fetched on invoke from addonPrefs
    zoomAdjust : FloatProperty (
        name="Zoom Adjust",
        description="Adjust the zoom amount. (Default: 0)",
        soft_min = -2,
        soft_max = 2,
        default = 0,
    ) 

    resetZoomAdjust : BoolProperty (
        name="Reset Zoom Adjust",
        default = False
    )

    viewSelectMethod : StringProperty (
        name="View Select Method",
        description="Whether the view select method is OBJ, SINGLE_VERT, EDGE, FACE, or OBJ",
        default="NONE",
    )

    viewSelectionWidth : FloatProperty (
        name="View Selection Width",
        description="Width of the selected vert, edge, face, object, or empty",
        default=1,
    )

    useZoomAdjust_greenLight = True

def _draw(self, context):
    addonPrefs = context.preferences.addons[__package__].preferences

    scene = context.scene
    layout = self.layout.column(align=True)

    if self.frameSelection:

        if not self.useZoomAdjust_greenLight:
            layout.label(text="High Vert Count Detected:")
            layout.label(text="Zoom Adjust Disabled")

        else:
            zoomAdjustRow = layout.row(align=True)
            zoomAdjustRow.prop(self, "use_zoomAdjust", text="")
            zoomAdjustSlider = zoomAdjustRow.row(align=True)

            bZoomAdjustUseSlider = True
            if not self.use_zoomAdjust:
                zoomAdjustSlider.enabled = False
                bZoomAdjustUseSlider = False

            zoomAdjustSlider.prop(self, "zoomAdjust", slider=bZoomAdjustUseSlider)

            zoomAdjustSlider.separator()

            resetRow = zoomAdjustSlider.row(align=True)
            if self.zoomAdjust == 0:
                resetRow.active = False

            resetRow.prop(self, "resetZoomAdjust", expand=True, text="", icon="LOOP_BACK", emboss=False)

def _execute(self, context):
    addonPrefs = context.preferences.addons[__package__].preferences

    self.selModeAtBegin = miscFunc.getSelMode()
    
    self.useZoomAdjust_greenLight    = True #reset

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

    if self.frameMethod == "ORIGIN":
        miscFunc.view2Origin(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas)

    elif self.frameMethod == "SEL":
            
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



        #if nothing is selected...
        if len(selObjs) == 0:
            
            if self.frameSelection:
                #set obj type visibility so that certain object types can be excluded when framing
                miscFunc.setObjTypeVisibility(self, context, scene, addonPrefs, visibilityCommandList, previousVisibility, visibilitySceneBoolList)
            
            #if nothing is selected, object mode,, and there is no active object
            if objectMode == "OBJECT" and activeObj == None:

                allSceneObjs = [obj for obj in scene.objects]

                visibleObjsFound = False #declare

                for obj in allSceneObjs:
                    if obj.visible_get():
                        visibleObjsFound = True
                        break

                if visibleObjsFound > 0:

                    if self.frameSelection:
                        miscFunc.viewAll(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas)

                else:

                    if self.frameSelection:
                        #No objects found!
                        miscFunc.view2Origin(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas)

                
                #if user wants to isolate selection...
                if self.isolateSelection:
                    if scene.ntzSmFrm.currentlyBusyIsolating:
                        miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                    else:
                        miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

            #nothing is selected, there might be an active object, and the mode might be object/edit
            else:

                #if user wants to isolate selection...
                if self.isolateSelection:
                    if scene.ntzSmFrm.currentlyBusyIsolating:
                        miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                    else:
                        miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                #user did not want to isolate selection, instead, frame select.
                else:
                    if self.frameSelection:
                        miscFunc.viewAll(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas)

        #if there's something selected...
        elif len(selObjs) > 0:

            if activeObj == None:
                bpy.context.view_layer.objects.active = selObjs[0]
                activeObj = selObjs[0]

            if objectMode == "EDIT":

                if activeObj.type == "MESH":
                    

                    if self.wasInvoked:

                        self.totalVertCount = sum(len(o.evaluated_get(context.evaluated_depsgraph_get()).to_mesh().vertices) for o in context.objects_in_mode)
                        self.totalNumVertsSel = sum(o.data.total_vert_sel for o in context.objects_in_mode)

                    if self.totalVertCount > addonPrefs.maxVertAllowanceForZoomAdjust:

                        if self.frameSelection:

                            if self.totalNumVertsSel == 0:
                                forceFrameAllVerts = True
                            else:
                                forceFrameAllVerts = False

                            miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj, forceFrameAllVerts=forceFrameAllVerts)

                        #isolate missing:
                        if self.isolateSelection:
                            
                            if scene.ntzSmFrm.currentlyBusyIsolating:
                                miscFunc.unhidePreviouslyHidden_VertsEdgesFaces(self, context, scene)
                                miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                            else:
                                if self.totalNumVertsSel > 0:
                                    miscFunc.hideSelected_VertsEdgesFaces(self, context, scene)
                                    miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                    else:

                        if self.totalNumVertsSel > 0:
                            
                            if self.frameSelection:
                                miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj, totalNumVertsSel=self.totalNumVertsSel)

                        else:

                            #no verts selected
                            if self.frameSelection:

                                miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj, forceFrameAllVerts=True)
                        
                        
                        if self.isolateSelection:
                            if scene.ntzSmFrm.currentlyBusyIsolating:
                                miscFunc.unhidePreviouslyHidden_VertsEdgesFaces(self, context, scene)
                                miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                            else:
                                if self.totalNumVertsSel > 0:
                                    miscFunc.hideSelected_VertsEdgesFaces(self, context, scene)
                                    miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                elif activeObj.type == "CURVE":

                    totalNumCurvePointsSel = 0 #declare
                    totalNumCurveHandlesLeft = 0 #declare
                    totalNumCurveHandlesRight = 0 #declare
                    totalNumCurvePointsAndHandles = 0 #declare

                    #get num of selected curve points & handles
                    for obj in selObjs:
                        selectedCurvePointsAndHandles = miscFunc.getSelectedCurvePointsAndHandles(self, context, obj)

                        if selectedCurvePointsAndHandles is not None:
                            totalNumCurvePointsSel += len( selectedCurvePointsAndHandles[0] )
                            totalNumCurveHandlesLeft += len( selectedCurvePointsAndHandles[1] )
                            totalNumCurveHandlesRight += len( selectedCurvePointsAndHandles[2] )
                            totalNumCurvePointsAndHandles = totalNumCurvePointsSel + totalNumCurveHandlesLeft + totalNumCurveHandlesRight

                    if totalNumCurvePointsAndHandles > 0:

                        if self.frameSelection:
                            miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                        if self.isolateSelection:
                            if scene.ntzSmFrm.currentlyBusyIsolating:
                                miscFunc.unhidePreviouslyHidden_CurvePointsAndHandles(self, context, scene)
                                miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                            else:
                                miscFunc.hideSelected_CurvePointsAndHandles(self, context, scene)
                                miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                    else:

                        #no curve points and handles selected
                        if self.frameSelection:

                            bpy.ops.object.mode_set(mode = 'OBJECT')

                            miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                            bpy.ops.object.mode_set(mode = 'EDIT')

                elif activeObj.type == "SURFACE":
                    if self.frameSelection:
                        miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                elif activeObj.type == "META":
                    if self.frameSelection:
                        miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)
                    
                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)
                
                elif activeObj.type == "FONT":
                    if self.frameSelection:
                        miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)
                    
                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                elif activeObj.type == "ARMATURE":
                    if self.frameSelection:
                        miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)
                
                elif activeObj.type == "LATTICE":
                    if self.frameSelection:
                        miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                else:
                    if self.frameSelection:
                        miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)
                    
            elif objectMode == "OBJECT":

                

                #frame selection
                if self.frameSelection:
                    if self.isolateSelection:
                        if not scene.ntzSmFrm.currentlyBusyIsolating:
                            miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)
                    
                    else:
                        miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)
                
                #isolate selection
                if self.isolateSelection:
                    
                    if scene.ntzSmFrm.currentlyBusyIsolating:
                        miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                    else:
                        miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

            elif objectMode == "EDIT_GPENCIL":
                if activeObj.type == "GPENCIL":
                    if self.frameSelection:
                        miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

            elif objectMode == "PAINT_GPENCIL":
                if activeObj.type == "GPENCIL":
                    if self.frameSelection:
                        miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

            elif objectMode == "SCULPT_GPENCIL":
                if activeObj.type == "GPENCIL":
                    if self.frameSelection:
                        miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

                

            elif objectMode == "POSE":
                if activeObj.type == "ARMATURE":
                    if self.frameSelection:
                        miscFunc.viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj)

                    if self.isolateSelection:
                        if scene.ntzSmFrm.currentlyBusyIsolating:
                            miscFunc.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            miscFunc.hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj)

        #re-enable visibility for all objects
        miscFunc.reenableVisibilityForAllObjs(self, context, scene, previousVisibility, visibilityCommandList)
    
    # final steps
    addonPrefs.use_zoomAdjust        = self.use_zoomAdjust  #update
    addonPrefs.zoomAdjust            = self.zoomAdjust      #update

    
    self.wasInvoked                  = False #reset

def _invoke(self, context, event):
    addonPrefs = context.preferences.addons[__package__].preferences

    scene = context.scene
    self.wasInvoked = True

    if addonPrefs.bUseSmoothFraming:
        self.invokeView = "INVOKE_DEFAULT"
    else:
        self.invokeView = "EXEC_DEFAULT"

    self.use_zoomAdjust = addonPrefs.use_zoomAdjust
    self.zoomAdjust     = addonPrefs.zoomAdjust

class VIEW3D_OT_ntzsf_smart_frame(Operator, opProps):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_smart_frame"
    bl_label = "NTZSF : Frame"
    bl_description = 'Smart Frame selected objects / faces / edges / vertices'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    @classmethod
    def description(cls, context, properties):
        return properties.tooltip

    def draw(self, context):
        _draw(self, context)

    def execute(self, context):
        _execute(self, context)
        return {'FINISHED'}
    # END execute()

    def invoke(self, context, event):
        _invoke(self, context, event)
        return self.execute(context)
    #END invoke()
    
# END Operator()

class VIEW3D_OT_ntzsf_isolate(Operator, opProps):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_isolate"
    bl_label = "NTZSF : Isolate"
    bl_description = 'Isolate selected objects / faces / edges / vertices'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    @classmethod
    def description(cls, context, properties):
        return properties.tooltip

    def draw(self, context):
        _draw(self, context)

    def execute(self, context):
        _execute(self, context)
        return {'FINISHED'}
    # END execute()

    def invoke(self, context, event):
        _invoke(self, context, event)
        return self.execute(context)
    #END invoke()
    
# END Operator()

class VIEW3D_OT_ntzsf_frame_and_isolate(Operator, opProps):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_frame_and_isolate"
    bl_label = "NTZSF : Frame & Isolate"
    bl_description = 'Frame & Isolate selected objects / faces / edges / vertices'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    @classmethod
    def description(cls, context, properties):
        return properties.tooltip

    def draw(self, context):
        _draw(self, context)

    def execute(self, context):
        _execute(self, context)
        return {'FINISHED'}
    # END execute()

    def invoke(self, context, event):
        _invoke(self, context, event)
        return self.execute(context)
    #END invoke()
    
# END Operator()

class VIEW3D_OT_ntzsf_viewport_to_origin(Operator, opProps):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_viewport_to_origin"
    bl_label = "NTZSF : Viewport to Origin"
    bl_description = 'Move the viewport to the origin'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    @classmethod
    def description(cls, context, properties):
        return properties.tooltip

    def draw(self, context):
        _draw(self, context)

    def execute(self, context):
        _execute(self, context)
        return {'FINISHED'}
    # END execute()

    def invoke(self, context, event):
        _invoke(self, context, event)
        return self.execute(context)
    #END invoke()
    
# END Operator()
