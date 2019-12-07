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
#    Add Object to Excluded Isolate Objects
# -----------------------------------------------------------------------------

class OBJECT_OT_NeltulzAddObjectToExcludedIsolateObjects(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.neltulz_add_object_to_excluded_isolate_objects"
    bl_label = "Neltulz - Add"
    bl_description = 'Add the object to the list of excluded isolated objects'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        sel_objs = [obj for obj in bpy.context.selected_objects]

        for obj in sel_objs:
            scene.neltulzSmartFrameSel.excludedIsolateObjects.add(obj.name)

            obj['neltulzSmartFrameSel_isolateExcluded'] = 1

        #Object added to the "excludedIsolateObjects" list

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
    bl_options = {'REGISTER'}

    objectToRemove : StringProperty(
        name="Object to Remove",
        description="Name of the Object to remove (Default = None)",
        default = "None"
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene

        if self.objectToRemove == "None":
            #User clicked the "-" button.  Remove multiple objects that are selected

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

        else:
            #User clicked the "X" next to an object in the list of excluded objects from isolate.  Remove the single object.
            obj = None
            try:
                obj = bpy.data.objects[self.objectToRemove]
            except:
                pass

            if obj is not None:
                #if object name is in the scene list of excluded isolate objects, then remove it.
                if obj.name in scene.neltulzSmartFrameSel.excludedIsolateObjects:
                    scene.neltulzSmartFrameSel.excludedIsolateObjects.remove(obj.name)

                #check to see if the prop "Neltulz_Isolate_Exlcluded" is on the selected object, if so, remove it.
                for key in obj.keys():
                    if key not in '_RNA_UI':
                        if key == 'neltulzSmartFrameSel_isolateExcluded':
                            del obj[key]

        #removed custom property from object

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
    bl_options = {'REGISTER'}

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

        
        #Refreshed

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
    bl_options = {'REGISTER'}

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


        
        #Cleared

        return {'FINISHED'}
    # END execute()
# END Operator()

# -----------------------------------------------------------------------------
#    Template (Converts object to wireframe with click-through)
# -----------------------------------------------------------------------------

class OBJECT_OT_NeltulzTemplate(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.neltulz_smart_frame_sel_template"
    bl_label = "Neltulz - Template"
    bl_description = 'Converts object to wireframe with click-through'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        sel_objs = [obj for obj in bpy.context.selected_objects]

        for obj in sel_objs:
            scene.neltulzSmartFrameSel.templatedObjects.add(obj.name)

            templateEnabled = False

            for key in obj.keys():
                if key not in '_RNA_UI':
                    if key == 'neltulzSmartFrameSel_template':
                        templateEnabled = True

            if not templateEnabled:
                obj['neltulzSmartFrameSel_originalDisplay'] = obj.display_type
                obj.display_type = 'WIRE'
                obj.hide_select = True
                obj['neltulzSmartFrameSel_template'] = 1
    
        #Templated

        return {'FINISHED'}
    # END execute()
# END Operator()



# -----------------------------------------------------------------------------
#    Refresh Templated Objects List
# -----------------------------------------------------------------------------

class OBJECT_OT_NeltulzRefreshTemplateObjects(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.neltulz_smart_frame_sel_refresh_template_objects"
    bl_label = "Neltulz - Refresh Template Objs"
    bl_description = 'Refresh the list of templated objects'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        objs = [obj for obj in bpy.context.scene.objects]

        scene.neltulzSmartFrameSel.templatedObjects.clear()
        
        for obj in objs:
            for key in obj.keys():
                if key not in '_RNA_UI':
                    if key == 'neltulzSmartFrameSel_template':
                        scene.neltulzSmartFrameSel.templatedObjects.add(obj.name)

        
        #Refreshed Template Objects

        return {'FINISHED'}
    # END execute()
# END Operator()


# -----------------------------------------------------------------------------
#    Remove Templated Object
# -----------------------------------------------------------------------------

class OBJECT_OT_NeltulzRemoveTemplatedObject(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.neltulz_smart_frame_sel_remove_templated_objects"
    bl_label = "Neltulz - Remove Templated Object"
    bl_description = 'Remove the templated object'
    bl_options = {'REGISTER'}

    objectToRemove : StringProperty(
        name="Object to Remove",
        description="Name of the Object to remove (Default = None)",
        default = "None"
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        scene = context.scene

        obj = None
        try:
            obj = bpy.data.objects[self.objectToRemove]
        except:
            pass

        if obj is not None:

            templateEnabled = False
            originalDisplay = "SOLID"

            for key in obj.keys():
                if key not in '_RNA_UI':
                    if key == 'neltulzSmartFrameSel_template':
                        templateEnabled = True
                        del obj['neltulzSmartFrameSel_template']

                    if key == 'neltulzSmartFrameSel_originalDisplay':
                        originalDisplay = obj[key]
                        del obj['neltulzSmartFrameSel_originalDisplay']

            if templateEnabled:
                obj.display_type = originalDisplay
                obj.hide_select = False
                scene.neltulzSmartFrameSel.templatedObjects.remove(self.objectToRemove)
                    



            #Removed Template Object!

        return {'FINISHED'}
    # END execute()
# END Operator()



# -----------------------------------------------------------------------------
#    Clear all Templated Objects
# -----------------------------------------------------------------------------

class OBJECT_OT_NeltulzClearAllTemplatedObjects(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.neltulz_smart_frame_sel_clear_all_templated_objects"
    bl_label = "Neltulz - Clear Templated Objects"
    bl_description = 'Clear the list of templated objects'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        objs = [obj for obj in bpy.context.scene.objects]

        scene.neltulzSmartFrameSel.templatedObjects.clear()

        

        for obj in objs:

            templateEnabled = False
            originalDisplay = "SOLID"

            for key in obj.keys():
                if key not in '_RNA_UI':
                    if key == 'neltulzSmartFrameSel_template':
                        templateEnabled = True
                        del obj['neltulzSmartFrameSel_template']

                    if key == 'neltulzSmartFrameSel_originalDisplay':
                        originalDisplay = obj[key]
                        del obj['neltulzSmartFrameSel_originalDisplay']

            if templateEnabled:
                obj.display_type = originalDisplay
                obj.hide_select = False
                
        #Cleared Template Objects

        return {'FINISHED'}
    # END execute()
# END Operator()



# -----------------------------------------------------------------------------
#    Viewport to Origin
# -----------------------------------------------------------------------------

class OBJECT_OT_NeltulzSmartFrameSelViewportToOrigin(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.neltulz_smart_frame_sel_viewport_to_origin"
    bl_label = "Neltulz - Viewport to Origin"
    bl_description = 'Moves the viewport to the origin'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene

        #use all regions when framing? (Useful for quad view)
        bUseAllRegions = scene.neltulzSmartFrameSel.use_all_regions_when_framing
        
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius=5, location=(0, 0, 0))

        bpy.ops.view3d.view_selected(use_all_regions=bUseAllRegions)

        bpy.ops.object.delete(use_global=False, confirm=False)
        
        #Viewport moved to Origin

        return {'FINISHED'}
    # END execute()
# END Operator()