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
        #only permit the script to run when there are more than 0 objects in the scene.  Prevents error!
        return len(bpy.context.scene.objects) > 0

    def execute(self, context):

        scene = context.scene

        obj_sel = bpy.context.selected_objects

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

        if len(obj_sel) == 0:

            if scene.neltulzSmartFrameSel.frameOnlyMesh:
                for command in visibilityCommandList:

                    if command is "bpy.context.space_data.show_object_viewport_mesh":
                        previousVisibility += list( [ True ] )

                    else:
                        #store previousVisibility so that it can be returned to original setting later
                        previousVisibility += list( [ eval(command) ] )

                        commandToEval = command + " = False"
                        eval(compile(commandToEval,'<string>','exec'))

            else:
                for index, command in enumerate(visibilityCommandList):
                    #store previousVisibility so that it can be returned to original setting later
                    previousVisibility += list( [ eval(command) ] )

                    commandToEval = command + " = " + visibilitySceneBoolList[index]
                    eval(compile(commandToEval,'<string>','exec'))

            


        if bpy.context.object.mode == "EDIT":

            totalNumVertsSel = 0

            #get num of selected verts
            for obj in obj_sel:
                selectedVerts = misc_functions.getSelectedVerts(self, context, obj)
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
                #self.report({'INFO'}, 'edit mode: object selected: NO verts selected' )
                if self.frameSelection:
                    bpy.ops.mesh.select_all(action='SELECT')

                    bpy.ops.view3d.view_selected(use_all_regions=False)
                    #bpy.ops.view3d.view_all(center=False)

                    bpy.ops.mesh.select_all(action='DESELECT')
            
            
            if self.isolateSelection:
                if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                    misc_functions.unhidePreviouslyHidden_VertsEdgesFaces(self, context, scene)
                    misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                else:
                    if totalNumVertsSel > 0:
                        misc_functions.hideSelected_VertsEdgesFaces(self, context, scene)
                        misc_functions.hideUnselected_Objs(self, context, scene, obj_sel)
                


        if bpy.context.object.mode == "OBJECT":
            

            if len(obj_sel) > 0:
                #Object is selected
                if self.frameSelection:
                    if self.isolateSelection:
                        if not scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                            bpy.ops.view3d.view_selected(use_all_regions=False)
                    
                    else:
                        bpy.ops.view3d.view_selected(use_all_regions=False)
                
                if self.isolateSelection:
                    
                    if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                        misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                    else:
                        misc_functions.hideUnselected_Objs(self, context, scene, obj_sel)


            else:

                if self.isolateSelection:
                    if scene.neltulzSmartFrameSel.currentlyBusyIsolating:
                        misc_functions.unhidePreviouslyHidden_Objs(self, context, scene)

                else:
                    if self.frameSelection:
                        bpy.ops.view3d.view_all(center=False)

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







