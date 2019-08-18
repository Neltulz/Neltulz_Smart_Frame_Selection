import bpy
from . properties import NeltulzSmartFrameSel_IgnitProperties
from . import misc_functions

# -----------------------------------------------------------------------------
#    Main Addon Operator
# -----------------------------------------------------------------------------    

class OBJECT_OT_NeltulzSmartFrameSel(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.neltulz_smart_frame_sel"
    bl_label = "Neltulz - Smart Frame Selection"
    bl_description = 'More ways to "Frame Selection" when pressing the keyboard shortcut'

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        if bpy.context.object.mode == "EDIT":

            totalNumVertsSel = 0

            obj_sel = bpy.context.selected_objects
            for obj in obj_sel:
                selectedVerts = misc_functions.getSelectedVerts(self, context, obj)
                totalNumVertsSel += len( selectedVerts )

            
            if totalNumVertsSel > 0:
                
                if totalNumVertsSel == 1:
                    #self.report({'INFO'}, 'edit mode: object selected: SINGLE vert selected' )
                    
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
                    bpy.ops.view3d.view_selected(use_all_regions=False)
            else:
                #self.report({'INFO'}, 'edit mode: object selected: NO verts selected' )
                bpy.ops.view3d.view_all(center=False)



        if bpy.context.object.mode == "OBJECT":

            obj = context.object

            if context.selected_objects:
                #self.report({'INFO'}, 'object mode: object selected' )
                bpy.ops.view3d.view_selected(use_all_regions=False)
            else:
                #self.report({'INFO'}, 'object mode: nothing selected' )
                bpy.ops.view3d.view_all(center=False)

        return {'FINISHED'}
    # END execute()
# END Operator()







