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

        
        obj_sel = bpy.context.selected_objects
        active_obj = bpy.context.view_layer.objects.active
        
        #if there are no "yellow" selected objects, force the first selected object to become the active object
        if not active_obj in obj_sel:
            if len(obj_sel) > 0: #required to prevent error when no objects are selected in the scene
                context.view_layer.objects.active = obj_sel[0]
                active_obj = obj_sel[0]
        

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
            
            # if "Frame Only Mesh Objects" is checked in the side panel, then loop through all the object visibility commands.
            # store previous visibility, and hide visibility for all but Mesh Objects
            if scene.neltulzSmartFrameSel.frameOnlyMesh:
                for command in visibilityCommandList:

                    if command is "bpy.context.space_data.show_object_viewport_mesh":
                        previousVisibility += list( [ True ] )

                    else:
                        #store previousVisibility so that it can be returned to original setting later
                        previousVisibility += list( [ eval(command) ] )

                        #disable visibility
                        commandToEval = command + " = False"
                        eval(compile(commandToEval,'<string>','exec'))

            # otherwise, the user wants more specific control over what's framed, so, loop through each object visibility command,
            # store previous visibility, and hide all except the ones the user specifically checkmarked
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
                        
                        if totalNumVertsSel == 1:
                            #self.report({'INFO'}, 'edit mode: object selected: SINGLE vert selected' )
                            if self.frameSelection:
                                bpy.ops.view3d.view_selected(use_all_regions=False)

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
                                bpy.ops.view3d.view_selected(use_all_regions=False)

                        

                    else:
                        #no verts selected
                        if self.frameSelection:

                            bpy.ops.object.mode_set(mode = 'OBJECT')

                            bpy.ops.view3d.view_selected(use_all_regions=False)

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

                    #print( "Total Selected Curve Points: " + str(totalNumCurvePointsSel) )
                    #print( "Total Selected Curve Handles (LEFT): " + str(totalNumCurveHandlesLeft) )
                    #print( "Total Selected Curve Handles (RIGHT): " + str(totalNumCurveHandlesRight) )
                    #print( "Total Selected Curve Points & Handles: " + str(totalNumCurvePointsAndHandles) )

                    if totalNumCurvePointsAndHandles > 0:

                        if self.frameSelection:
                            bpy.ops.view3d.view_selected(use_all_regions=False)

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

                            bpy.ops.view3d.view_selected(use_all_regions=False)

                            bpy.ops.object.mode_set(mode = 'EDIT')

                else:
                    if showErrorMessages:
                        errorPartOne = 'Neltulz Smart Frame Selection:\n\n"'
                        errorPartTwo = '" is currently unsupported on "' + str(active_obj.type) + '" object type while in "EDIT" mode\n\nSorry about that! I hope to have this implemented sometime in the future!\n\nIf this is a super important feature you need, please pester Neil at neilvmoore@gmail.com\n\nOr visit: https://blenderartists.org/t/neltulz-smart-frame-selection to submit a feature request!\n\nThanks!\n\n'
                        error_supported_object_type_list = 'Current Supported Object Types: "MESH", "CURVE"'
                        unsupported_object_type_error = False
                        unsupported_object_type_error_operator = []

                        if self.frameSelection:
                            unsupported_object_type_error = True
                            unsupported_object_type_error_operator.append("Frame")
                            
                        
                        if self.isolateSelection:
                            unsupported_object_type_error = True
                            unsupported_object_type_error_operator.append("Isolate")

                        if unsupported_object_type_error:
                            
                            operator_used = ""
                            if len(unsupported_object_type_error_operator) == 1:
                                operator_used = unsupported_object_type_error_operator[0]
                            else:
                                operator_used = unsupported_object_type_error_operator[0] + " & " + unsupported_object_type_error_operator[1]

                            self.report({'ERROR'}, errorPartOne + operator_used + errorPartTwo + error_supported_object_type_list )

            
            elif bpy.context.object.mode == "OBJECT":

                #frame selection
                if self.frameSelection:
                    if self.isolateSelection:
                        if not scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            bpy.ops.view3d.view_selected(use_all_regions=False)
                    
                    else:
                        bpy.ops.view3d.view_selected(use_all_regions=False)
                
                #isolate selection
                if self.isolateSelection:
                    
                    if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                        misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                    else:
                        misc_functions.hideUnselected_Objs(self, context, scene, obj_sel, active_obj)





        #re-enable visibility for all objects
        if len(obj_sel) == 0:
            if scene.neltulzSmartFrameSel.frameOnlyMesh:
                for index, boool in enumerate(previousVisibility):

                    if visibilityCommandList[index] is "bpy.context.space_data.show_object_viewport_mesh":
                        pass

                    else:
                        commandToEval = visibilityCommandList[index] + " = " + str(boool)
                        eval(compile(commandToEval,'<string>','exec'))
            
            else:
                for index, boool in enumerate(previousVisibility):
                    commandToEval = visibilityCommandList[index] + " = " + str(boool)
                    eval(compile(commandToEval,'<string>','exec'))


        return {'FINISHED'}
    # END execute()
# END Operator()







