import bpy
from . properties import NeltulzSmartFrameSel_IgnitProperties
from . import misc_functions

# -----------------------------------------------------------------------------
#    Add Object to Excluded Isolate Objects
# -----------------------------------------------------------------------------

class OBJECT_OT_NeltulzAddObjectToExcludedIsolateObjects(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.neltulz_add_object_to_excluded_isolate_objects"
    bl_label = "Neltulz - Add"
    bl_description = 'Add the object to the list of excluded isolated objects'

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        sel_objs = [obj for obj in bpy.context.selected_objects]

        for obj in sel_objs:
            scene.neltulzSmartFrameSel.excludedIsolateObjects.add(obj.name)

            obj['neltulzSmartFrameSel_isolateExcluded'] = 1

        print('Added!')

        return {'FINISHED'}
    # END execute()
# END Operator()

# -----------------------------------------------------------------------------
#    Remove Object From Excluded Isolate Objects
# -----------------------------------------------------------------------------

class OBJECT_OT_NeltulzRemoveObjectFromExcludedIsolateObjects(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.neltulz_remove_object_from_excluded_isolate_objects"
    bl_label = "Neltulz - Remove"
    bl_description = 'Remove the object from the excluded isolated objects'

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        sel_objs = [obj for obj in bpy.context.selected_objects]

        for obj in sel_objs:

            #if object name is in the scene list of excluded isolate objects, then remove it.
            if obj.name in scene.neltulzSmartFrameSel.excludedIsolateObjects:
                scene.neltulzSmartFrameSel.excludedIsolateObjects.remove(obj.name)

            #check to see if the prop "Neltulz_Isolate_Exlcluded" is on the selected object, if so, remove it.
            for key in obj.keys():
                if key not in '_RNA_UI':
                    if key == 'neltulzSmartFrameSel_isolateExcluded':
                        del obj[key]

        print('Removed!')

        return {'FINISHED'}
    # END execute()
# END Operator()

# -----------------------------------------------------------------------------
#    Refresh Excluded Isolate Objects
# -----------------------------------------------------------------------------

class OBJECT_OT_NeltulzRefreshExcludedIsolateObjects(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.neltulz_refresh_excluded_isolate_objects"
    bl_label = "Neltulz - Refresh"
    bl_description = 'Refresh the list of excluded isolated objects.  Useful if you have renamed objects and the list no longer matches'

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        objs = [obj for obj in bpy.context.scene.objects]

        scene.neltulzSmartFrameSel.excludedIsolateObjects.clear()
        
        for obj in objs:
            for key in obj.keys():
                if key not in '_RNA_UI':
                    if key == 'neltulzSmartFrameSel_isolateExcluded':
                        scene.neltulzSmartFrameSel.excludedIsolateObjects.add(obj.name)

        
        print('Refreshed!')

        return {'FINISHED'}
    # END execute()
# END Operator()


# -----------------------------------------------------------------------------
#    Clear all Excluded Isolate Objects
# -----------------------------------------------------------------------------

class OBJECT_OT_NeltulzClearAllExcludedIsolateObjects(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.neltulz_clear_all_excluded_isolate_objects"
    bl_label = "Neltulz - Clear"
    bl_description = 'Clear the list of excluded isolated objects.'

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        objs = [obj for obj in bpy.context.scene.objects]

        scene.neltulzSmartFrameSel.excludedIsolateObjects.clear()

        for obj in objs:
            for key in obj.keys():
                if key not in '_RNA_UI':
                    if key == 'neltulzSmartFrameSel_isolateExcluded':
                        del obj[key]


        
        print('Cleared!')

        return {'FINISHED'}
    # END execute()
# END Operator()
