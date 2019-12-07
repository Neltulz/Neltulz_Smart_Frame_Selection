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
#    Main Addon Operator
# -----------------------------------------------------------------------------    

class OBJECT_OT_NeltulzSmartFrameSel(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.neltulz_smart_frame_sel"
    bl_label = "Neltulz - Smart Frame Selection"
    bl_description = 'More ways to "Frame Selection" when pressing the keyboard shortcut'
    bl_options = {'REGISTER', 'UNDO'}

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

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene

        showErrorMessages = True #declare
        if scene.neltulzSmartFrameSel.useAdvancedSettings:
            if scene.neltulzSmartFrameSel.hideErrorMessages:
                showErrorMessages = False

        #use all regions when framing? (Useful for quad view)
        bUseAllRegions = scene.neltulzSmartFrameSel.use_all_regions_when_framing

        objectMode = "Unknown"
        obj_sel = bpy.context.selected_objects
        active_obj = bpy.context.view_layer.objects.active
        
        #if there are no "yellow" selected objects, force the first selected object to become the active object
        if not active_obj in obj_sel:
            if len(obj_sel) > 0: #required to prevent error when no objects are selected in the scene
                context.view_layer.objects.active = obj_sel[0]
                active_obj = obj_sel[0]
        
        try:
            #try to determine objectMode
            objectMode = bpy.context.object.mode
        except:
            #Object Mode is unknown
            for obj in bpy.data.objects:
                active_obj = obj
                break

        visibilityCommandList = [
            "bpy.context.space_data.show_object_viewport_mesh",
            "bpy.context.space_data.show_object_viewport_curve",
            "bpy.context.space_data.show_object_viewport_surf",
            "bpy.context.space_data.show_object_viewport_meta",
            "bpy.context.space_data.show_object_viewport_font",
            "bpy.context.space_data.show_object_viewport_grease_pencil",
            "bpy.context.space_data.show_object_viewport_armature",
            "bpy.context.space_data.show_object_viewport_lattice",
            "bpy.context.space_data.show_object_viewport_empty",
            "bpy.context.space_data.show_object_viewport_light",
            "bpy.context.space_data.show_object_viewport_light_probe",
            "bpy.context.space_data.show_object_viewport_camera",
            "bpy.context.space_data.show_object_viewport_speaker",
        ]

        visibilitySceneBoolList = [
            "scene.neltulzSmartFrameSel.frameMesh",
            "scene.neltulzSmartFrameSel.frameCurve",
            "scene.neltulzSmartFrameSel.frameSurface",
            "scene.neltulzSmartFrameSel.frameMeta",
            "scene.neltulzSmartFrameSel.frameText",
            "scene.neltulzSmartFrameSel.frameGreasePen",
            "scene.neltulzSmartFrameSel.frameArmature",
            "scene.neltulzSmartFrameSel.frameLattice",
            "scene.neltulzSmartFrameSel.frameEmpty",
            "scene.neltulzSmartFrameSel.frameLight",
            "scene.neltulzSmartFrameSel.frameLightProbe",
            "scene.neltulzSmartFrameSel.frameCamera",
            "scene.neltulzSmartFrameSel.frameSpeaker",
        ]

        previousVisibility = list()

        


        #if nothing is selected...
        if len(obj_sel) == 0:

            if objectMode == "Unknown" and active_obj == None:
                if len(bpy.context.scene.objects) <= 0:

                    if self.frameSelection:
                        #No objects found!
                        bpy.ops.object.neltulz_smart_frame_sel_viewport_to_origin()

                    
            
            else:
                for index, command in enumerate(visibilityCommandList):
                    #store previousVisibility so that it can be returned to original setting later
                    previousVisibility += list( [ eval(command) ] )

                    commandToEval = command + " = " + visibilitySceneBoolList[index]
                    eval(compile(commandToEval,'<string>','exec'))



                #if user wants to isolate selection...
                if self.isolateSelection:
                    if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                        misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                    else:
                        misc_functions.hideUnselected_Objs(self, context, scene,  obj_sel, active_obj)

                #user did not want to isolate selection, instead, frame select.
                else:
                    if self.frameSelection:
                        bpy.ops.view3d.view_all(center=False)


        #if there's something selected...
        elif len(obj_sel) > 0:

            if bpy.context.object.mode == "EDIT":

                if active_obj.type == "MESH":

                    totalNumVertsSel = 0 #declare

                    #get num of selected verts
                    for obj in obj_sel:
                        selectedVerts = misc_functions.getSelectedVerts(self, context, obj)

                        if selectedVerts is not None:
                            totalNumVertsSel += len( selectedVerts )

                    
                    if totalNumVertsSel > 0:
                        
                        if self.frameSelection:
                            bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                        '''
                        #OLD ZOOM CODE FOR WHEN ONLY 1 VERT IS SELECTED.  DISABLED UNTIL FURTHER NOTICE BECAUSE IT'S PROBLEMATIC FOR OBJECTS THAT ARE VERY SMALL OR VERY LARGE.
                        if totalNumVertsSel == 1:
                            #self.report({'INFO'}, 'edit mode: object selected: SINGLE vert selected' )
                            if self.frameSelection:
                                bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                                # get view3d camera and zoom out! Note: This does not mess up the camera orbit.
                                # source: https://blenderartists.org/t/how-to-access-the-view-3d-camera/601372/7
                                # answer by user: system
                                for area in bpy.context.screen.areas:
                                    if area.type == 'VIEW_3D':
                                        rv3d = area.spaces[0].region_3d
                                        if rv3d is not None:
                                            rv3d.view_distance = 0.5
                            
                        else:
                            #self.report({'INFO'}, 'edit mode: object selected: multiple verts selected' )
                            if self.frameSelection:
                                bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)
                        '''

                        

                    else:
                        #no verts selected
                        if self.frameSelection:

                            bpy.ops.object.mode_set(mode = 'OBJECT')

                            bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                            bpy.ops.object.mode_set(mode = 'EDIT')
                    
                    
                    if self.isolateSelection:
                        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_VertsEdgesFaces(self, context, scene)
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            if totalNumVertsSel > 0:
                                misc_functions.hideSelected_VertsEdgesFaces(self, context, scene)
                                misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)

                elif active_obj.type == "CURVE":

                    totalNumCurvePointsSel = 0 #declare
                    totalNumCurveHandlesLeft = 0 #declare
                    totalNumCurveHandlesRight = 0 #declare
                    totalNumCurvePointsAndHandles = 0 #declare

                    #get num of selected curve points & handles
                    for obj in obj_sel:
                        selectedCurvePointsAndHandles = misc_functions.getSelectedCurvePointsAndHandles(self, context, obj)

                        if selectedCurvePointsAndHandles is not None:
                            totalNumCurvePointsSel += len( selectedCurvePointsAndHandles[0] )
                            totalNumCurveHandlesLeft += len( selectedCurvePointsAndHandles[1] )
                            totalNumCurveHandlesRight += len( selectedCurvePointsAndHandles[2] )
                            totalNumCurvePointsAndHandles = totalNumCurvePointsSel + totalNumCurveHandlesLeft + totalNumCurveHandlesRight

                    if totalNumCurvePointsAndHandles > 0:

                        if self.frameSelection:
                            bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                        if self.isolateSelection:
                            if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                                misc_functions.unhidePreviouslyHidden_CurvePointsAndHandles(self, context, scene)
                                misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                            else:
                                misc_functions.hideSelected_CurvePointsAndHandles(self, context, scene)
                                misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)

                    else:

                        #no curve points and handles selected
                        if self.frameSelection:

                            bpy.ops.object.mode_set(mode = 'OBJECT')

                            bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                            bpy.ops.object.mode_set(mode = 'EDIT')

                elif active_obj.type == "SURFACE":
                    if self.frameSelection:
                        bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                    if self.isolateSelection:
                        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)

                elif active_obj.type == "META":
                    if self.frameSelection:
                        bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)
                    
                    if self.isolateSelection:
                        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)
                
                elif active_obj.type == "FONT":
                    if self.frameSelection:
                        bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)
                    
                    if self.isolateSelection:
                        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)

                elif active_obj.type == "ARMATURE":
                    if self.frameSelection:
                        bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                    if self.isolateSelection:
                        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)
                
                elif active_obj.type == "LATTICE":
                    if self.frameSelection:
                        bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                    if self.isolateSelection:
                        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)

                else:
                    if self.frameSelection:
                        bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                    if self.isolateSelection:
                        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)
                    
            elif bpy.context.object.mode == "OBJECT":

                #frame selection
                if self.frameSelection:
                    if self.isolateSelection:
                        if not scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)
                    
                    else:
                        bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)
                
                #isolate selection
                if self.isolateSelection:
                    
                    if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                        misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                    else:
                        misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)

            elif bpy.context.object.mode == "EDIT_GPENCIL":
                if active_obj.type == "GPENCIL":
                    if self.frameSelection:
                        bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                    if self.isolateSelection:
                        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)

            elif bpy.context.object.mode == "PAINT_GPENCIL":
                if active_obj.type == "GPENCIL":
                    if self.frameSelection:
                        bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                    if self.isolateSelection:
                        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)

            elif bpy.context.object.mode == "SCULPT_GPENCIL":
                if active_obj.type == "GPENCIL":
                    if self.frameSelection:
                        bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                    if self.isolateSelection:
                        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)

                

            elif bpy.context.object.mode == "POSE":
                if active_obj.type == "ARMATURE":
                    if self.frameSelection:
                        bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

                    if self.isolateSelection:
                        if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                        else:
                            misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)

        #re-enable visibility for all objects
        if len(obj_sel) == 0:

            for index, boool in enumerate(previousVisibility):
                commandToEval = visibilityCommandList[index] + " = " + str(boool)
                eval(compile(commandToEval,'<string>','exec'))


        return {'FINISHED'}
    # END execute()
# END Operator()







