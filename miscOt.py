import bpy
from . properties import ntzsf_scene_props
from . import miscFunc

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#    Add Object to Excluded Isolate Objects
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_add_obj_to_excluded_isolate_objs(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_add_obj_to_excluded_isolate_objs"
    bl_label = 'NTZSF : Add obj to "Isolate Exclusion List"'
    bl_description = 'Add the object to the list of excluded isolated objects'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        selObjs = [obj for obj in bpy.context.selected_objects]

        for obj in selObjs:
            scene.ntzSmFrm.excludedIsolateObjects.add(obj.name)

            obj['ntzSmFrm_isolateExcluded'] = 1

        #Object added to the "excludedIsolateObjects" list

        return {'FINISHED'}
    # END execute()
# END Operator()

# -----------------------------------------------------------------------------
#    Remove Object From Excluded Isolate Objects
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_del_obj_from_excluded_isolate_objs(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_del_obj_from_excluded_isolate_objs"
    bl_label = 'NTZSF : Remove obj from "Isolate Exclusion List"'
    bl_description = 'Remove the object from the excluded isolated objects'
    bl_options = {'REGISTER', 'UNDO'}

    objectToUntemplate : StringProperty(
        name="Object to Remove",
        description="Name of the Object to remove (Default = None)",
        default = "None"
    )

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        pass
    #END draw()

    def execute(self, context):

        scene = context.scene

        if self.objectToUntemplate == "None":
            #User clicked the "-" button.  Remove multiple objects that are selected

            selObjs = [obj for obj in bpy.context.selected_objects]

            for obj in selObjs:

                #if object name is in the scene list of excluded isolate objects, then remove it.
                if obj.name in scene.ntzSmFrm.excludedIsolateObjects:
                    scene.ntzSmFrm.excludedIsolateObjects.remove(obj.name)

                #check to see if the prop "Neltulz_Isolate_Exlcluded" is on the selected object, if so, remove it.
                try:
                    obj.pop('ntzSmFrm_isolateExcluded')
                except:
                    pass
        else:
            #User clicked the "X" next to an object in the list of excluded objects from isolate.  Remove the single object.
            obj = None
            try:
                obj = bpy.data.objects[self.objectToUntemplate]
            except:
                pass

            if obj is not None:
                #if object name is in the scene list of excluded isolate objects, then remove it.
                if obj.name in scene.ntzSmFrm.excludedIsolateObjects:
                    scene.ntzSmFrm.excludedIsolateObjects.remove(obj.name)

                #check to see if the prop "Neltulz_Isolate_Exlcluded" is on the selected object, if so, remove it.
                try:
                    obj.pop('ntzSmFrm_isolateExcluded')
                except:
                    pass

        #removed custom property from object

        return {'FINISHED'}
    # END execute()
# END Operator()

# -----------------------------------------------------------------------------
#    Refresh Excluded Isolate Objects
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_refresh_excluded_isolate_objs(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_refresh_excluded_isolate_objs"
    bl_label = 'NTZSF : Refresh "Isolate Exclusion List"'
    bl_description = 'Refresh the list of excluded isolated objects.  Useful if you have renamed objects and the list no longer matches'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        objs = [obj for obj in bpy.context.scene.objects]

        scene.ntzSmFrm.excludedIsolateObjects.clear()
        
        for obj in objs:

            try:
                if obj['ntzSmFrm_isolateExcluded']:
                    scene.ntzSmFrm.excludedIsolateObjects.add(obj.name)
            except:
                pass
                        

        
        #Refreshed

        return {'FINISHED'}
    # END execute()
# END Operator()


# -----------------------------------------------------------------------------
#    Clear all Excluded Isolate Objects
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_clear_all_excluded_isolate_objs(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_clear_all_excluded_isolate_objs"
    bl_label = 'NTZSF : Clear "Isolate Exclusion List"'
    bl_description = 'Clear the list of excluded isolated objects.'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        objs = [obj for obj in bpy.context.scene.objects]

        scene.ntzSmFrm.excludedIsolateObjects.clear()

        for obj in objs:
            try:
                obj.pop('ntzSmFrm_isolateExcluded')
            except:
                pass


        
        #Cleared

        return {'FINISHED'}
    # END execute()
# END Operator()

# -----------------------------------------------------------------------------
#    Template (Converts object to wireframe with click-through)
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_convert_obj_to_template(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_convert_obj_to_template"
    bl_label = 'NTZSF : Add obj to "Templated Obj List"'
    bl_description = 'Converts object to wireframe with click-through'
    bl_options = {'REGISTER', 'UNDO'}

    makeSelectable : BoolProperty (
        name="Make Template Selectable",
        description="Make the template object selectable (Default = False)",
        default = False
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        activeObj = bpy.context.view_layer.objects.active
        
        modeAtBegin = "Unknown" #declare
        try:
            #try to determine objectMode
            modeAtBegin = bpy.context.object.mode
        except:
            modeAtBegin = "OBJECT"

        selObjs = miscFunc.getSelObjsFromOutlinerAndViewport(self, context, modeAtBegin)

        for obj in selObjs:
            scene.ntzSmFrm.templatedObjects.add(obj.name)

            templateEnabled = False

            try:
                if obj['ntzSmFrm_template']:
                    objIsTemplate = True
            except:
                pass

            if not templateEnabled:
                obj['ntzSmFrm_originalDisplay'] = obj.display_type
                obj.display_type = 'WIRE'
                obj.hide_select = True
                obj['ntzSmFrm_template'] = 1
    
        #Templated

        return {'FINISHED'}
    # END execute()
# END Operator()


# -----------------------------------------------------------------------------
#    Toggle Template of objects highlighted in outliner
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_toggle_template(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_toggle_template"
    bl_label = 'NTZSF : Template'
    bl_description = 'Toggles object(s) between template and non template'
    bl_options = {'REGISTER', 'UNDO'}

    tooltip: bpy.props.StringProperty()

    makeSelectable : BoolProperty (
        name="Make Template Selectable",
        description="Make the template object selectable (Default = False)",
        default = False
    )

    @classmethod
    def poll(cls, context):
        return True

    @classmethod
    def description(cls, context, properties):
        return properties.tooltip

    
    def draw(self, context):
        scene = context.scene
        lay = self.layout.column(align=True)

        lay.prop(self, 'makeSelectable')
    #END draw()

    def execute(self, context):

        scene = context.scene

        modeAtBegin = "Unknown" #declare
        
        try:
            #try to determine objectMode
            modeAtBegin = bpy.context.object.mode
        except:
            modeAtBegin = "OBJECT"

        selObjs = miscFunc.getSelObjsFromOutlinerAndViewport(self, context, modeAtBegin)

        if modeAtBegin == "OBJECT":
            if len(selObjs) > 0:
                for obj in selObjs:
                    bpy.context.view_layer.objects.active = obj
                    break
        
        for obj in selObjs:
            objIsTemplate = False #declare

            try:
                if obj['ntzSmFrm_template']:
                    objIsTemplate = True
            except:
                pass
            
            if objIsTemplate:
                bpy.ops.view3d.ntzsf_untemplate_specific_obj(objectToUntemplate = f"{obj.name}" )
            else:
                bpy.ops.view3d.ntzsf_template_specific_obj(objectToTemplate = f"{obj.name}", makeSelectable = self.makeSelectable )

    
        #Templated

        return {'FINISHED'}
    # END execute()


    def invoke(self, context, event):

        addonPrefs = context.preferences.addons[__package__].preferences

        if addonPrefs.defaultTemplateSelectableState == "UNSELECTABLE":
            self.makeSelectable = False
        elif addonPrefs.defaultTemplateSelectableState == "SELECTABLE":
            self.makeSelectable = True
        
        return self.execute(context)
    #END invoke()
# END Operator()


# -----------------------------------------------------------------------------
#    Refresh Templated Objects List
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_refresh_template_objs(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_refresh_template_objs"
    bl_label = 'NTZSF : Refresh "Templated Obj List"'
    bl_description = 'Refresh the list of templated objects'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        objs = [obj for obj in bpy.context.scene.objects]

        scene.ntzSmFrm.templatedObjects.clear()
        
        for obj in objs:

            try:
                if obj['ntzSmFrm_template']:
                    scene.ntzSmFrm.templatedObjects.add(obj.name)
            except:
                pass
                        

        
        #Refreshed Template Objects

        return {'FINISHED'}
    # END execute()
# END Operator()


# -----------------------------------------------------------------------------
#    Un-Template Highlighted Objects in the Outliner
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_untemplate_objs(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_untemplate_objs"
    bl_label = 'NTZSF : Remove obj from "Templated Obj List"'
    bl_description = 'Remove the templated object'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene
        selObjsInOutliner = [] #declare

        # Select objects in outliner
        area = None #declare
        try:
            #check for outliner in the main window
            area = next(a for a in context.screen.areas if a.type == 'OUTLINER')
        except:
            try:
                #check for outliner in other windows
                area = next(a for w in context.window_manager.windows
                            for a in w.screen.areas if a.type == 'OUTLINER')
            except:
                pass
        
        if area is not None:
            sel_org = context.selected_objects[:]
            objs = context.view_layer.objects

            hide_select = {o for o in objs if o.hide_select}
            for o in hide_select:  # Toggle off hide select
                o.hide_select = False

            for o in sel_org:  # Deselect all selected
                o.select_set(False)

            bpy.ops.outliner.object_operation({'area': area}, type='SELECT')

            selObjsInOutliner = context.selected_objects[:]
            
            # Toggle on hide select for objects not selected in outliner
            for o in hide_select:
                if not o.select_get():
                    o.hide_select = True

            for o in sel_org:  # Restore original selection
                o.select_set(True)


        # BEGIN code that un-templates the object

        for obj in selObjsInOutliner:
            templateEnabled = obj.pop("ntzSmFrm_template", False)
            originalDisplay = obj.pop('ntzSmFrm_originalDisplay', "SOLID")

            if templateEnabled:
                obj.display_type = originalDisplay
                obj.hide_select = False
                scene.ntzSmFrm.templatedObjects.discard( f"{obj.name}" )

        # END code that un-templates the object

        return {'FINISHED'}
    # END execute()
# END Operator()

# -----------------------------------------------------------------------------
#    Template Specific Obj
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_template_specific_obj(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_template_specific_obj"
    bl_label = 'NTZSF : Add specific obj from "Templated Obj List"'
    bl_description = 'Add specific object from templated object list'
    bl_options = {'REGISTER', 'UNDO'}

    objectToTemplate : StringProperty(
        name="Object to Template",
        description="Name of the Object to Template (Default = None)",
        default = "None"
    )

    makeSelectable : BoolProperty (
        name="Make Template Selectable",
        description="Make the template object selectable (Default = False)",
        default = False
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scene = context.scene

        # BEGIN code that templates the object

        obj = None #declare
        try:
            obj = bpy.data.objects[self.objectToTemplate]
        except:
            pass
        
        if obj is not None:
            scene.ntzSmFrm.templatedObjects.add(obj.name)

            templateEnabled = False

            try:
                if obj['ntzSmFrm_template']:
                    templateEnabled = True
            except:
                pass

            if not templateEnabled:
                obj['ntzSmFrm_originalDisplay'] = obj.display_type
                obj.display_type = 'WIRE'
                
                obj.hide_select = not(self.makeSelectable)
                obj['ntzSmFrm_template'] = 1

        # END code that templates the object


        return {'FINISHED'}
    # END execute()
# END Operator()


# -----------------------------------------------------------------------------
#    Un-Template Specific Obj
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_untemplate_specific_obj(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_untemplate_specific_obj"
    bl_label = 'NTZSF : Remove specific obj from "Templated Obj List"'
    bl_description = 'Remove specific object from templated object list'
    bl_options = {'REGISTER', 'UNDO'}

    objectToUntemplate : StringProperty(
        name="Object to Remove",
        description="Name of the Object to remove (Default = None)",
        default = "None"
    )

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        pass
    #END draw()

    def execute(self, context):
        scene = context.scene

        # BEGIN code that un-templates the object

        obj = None #declare
        try:
            obj = bpy.data.objects[self.objectToUntemplate]
        except:
            pass
        
        if obj is not None:
            templateEnabled = obj.pop("ntzSmFrm_template", False)
            originalDisplay = obj.pop('ntzSmFrm_originalDisplay', "SOLID")

            if templateEnabled:
                obj.display_type = originalDisplay
                obj.hide_select = False
                scene.ntzSmFrm.templatedObjects.discard( self.objectToUntemplate )

        # END code that un-templates the object


        return {'FINISHED'}
    # END execute()
# END Operator()



# -----------------------------------------------------------------------------
#    Clear all Templated Objects
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_clear_all_template_objs(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_clear_all_template_objs"
    bl_label = 'NTZSF : Clear "Templated Obj List"'
    bl_description = 'Clear the list of templated objects'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        objs = [obj for obj in bpy.context.scene.objects]

        scene.ntzSmFrm.templatedObjects.clear()

        

        for obj in objs:

            templateEnabled = obj.pop("ntzSmFrm_template", False)
            originalDisplay = obj.pop('ntzSmFrm_originalDisplay', "SOLID")

            if templateEnabled:
                obj.display_type = originalDisplay
                obj.hide_select = False
                
        #Cleared Template Objects

        return {'FINISHED'}
    # END execute()
# END Operator()


# -----------------------------------------------------------------------------
#    Make all existing template objects selectable
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_change_template_selection_state(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_change_template_selection_state"
    bl_label = 'NTZSF : Change All Template Selection State'
    bl_description = 'Change All Template Selection State'
    bl_options = {'REGISTER', 'UNDO'}

    makeSelectable : BoolProperty(
        name="Make All Objects Selectable",
        description="Make All Objects Selectable",
        default = True
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        #refresh templated obj list
        bpy.ops.view3d.ntzsf_refresh_template_objs()

        scene = context.scene
        objs = [obj for obj in bpy.context.scene.objects]

        for obj in objs:
            
            templateEnabled = False
            try:
                if obj['ntzSmFrm_template']:
                    templateEnabled = True
            except:
                pass

            if templateEnabled:
                if self.makeSelectable:
                    obj.hide_select = False
                else:
                    obj.hide_select = True
                
        #Cleared Template Objects

        return {'FINISHED'}
    # END execute()
# END Operator()

# -----------------------------------------------------------------------------
#    Select Object by Name
# -----------------------------------------------------------------------------

class VIEW3D_OT_ntzsf_sel_obj_by_name(Operator):
    """Tooltip"""
    bl_idname = "view3d.ntzsf_sel_obj_by_name"
    bl_label = 'NTZSF : Select Object'
    bl_description = 'Selects and object by name'
    bl_options = {'REGISTER', 'UNDO'}

    objToSelect : StringProperty(
        name="Object to Select",
        description="Name of the Object to Select (Default = None)",
        default = "None"
    )

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        pass
    #END draw()

    def execute(self, context):

        scene = context.scene

        modeAtBegin = "Unknown" #declare
        try:
            #try to determine objectMode
            modeAtBegin = bpy.context.object.mode
        except:
            modeAtBegin = "OBJECT"


        obj = None
        try:
            obj = bpy.data.objects[self.objToSelect] 
        except:
            pass

        if obj is not None:

            if modeAtBegin == "EDIT":
                bpy.ops.object.mode_set(mode = 'OBJECT') #switch to object mode

            bpy.ops.object.select_all(action='DESELECT') #deselect all objs
            obj.select_set(True) #select object
            bpy.context.view_layer.objects.active = obj #set obj as active obj


        return {'FINISHED'}
    # END execute()
# END Operator()