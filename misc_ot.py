import bpy
from . properties import NTZSMFRM_ignitproperties
from . import misc_functions

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#    Add Object to Excluded Isolate Objects
# -----------------------------------------------------------------------------

class NTZSMFRM_OT_addobjtoexcludedisolateobjs(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.excludeobj"
    bl_label = 'Neltulz - Smart Frame : Add obj to "Isolate Exclusion List"'
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

class NTZSMFRM_OT_removeobjfromexcludedisolateobjs(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.unexcludeobj"
    bl_label = 'Neltulz - Smart Frame : Remove obj from "Isolate Exclusion List"'
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

class NTZSMFRM_OT_refreshexcludedisolateobjs(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.refreshexcludedobjlist"
    bl_label = 'Neltulz - Smart Frame : Refresh "Isolate Exclusion List"'
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

class NTZSMFRM_OT_clearallexcludedisolateobjs(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.clearexcludedobjs"
    bl_label = 'Neltulz - Smart Frame : Clear "Isolate Exclusion List"'
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

class NTZSMFRM_OT_templateobj(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.convertobjtotemplate"
    bl_label = 'Neltulz - Smart Frame : Add obj to "Templated Obj List"'
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

        selObjs = misc_functions.getSelObjsFromOutlinerAndViewport(self, context, modeAtBegin)

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

class NTZSMFRM_OT_toggletemplate(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.toggletemplate"
    bl_label = 'Neltulz - Smart Frame : Toggle template of object(s)'
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

        selObjs = misc_functions.getSelObjsFromOutlinerAndViewport(self, context, modeAtBegin)

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
                bpy.ops.ntz_smrt_frm.untemplatespecificobj(objectToUntemplate = f"{obj.name}" )
            else:
                bpy.ops.ntz_smrt_frm.templatespecificobj(objectToTemplate = f"{obj.name}", makeSelectable = self.makeSelectable )

    
        #Templated

        return {'FINISHED'}
    # END execute()
# END Operator()


# -----------------------------------------------------------------------------
#    Refresh Templated Objects List
# -----------------------------------------------------------------------------

class NTZSMFRM_OT_refreshtemplateobjs(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.refreshtemplatedobjlist"
    bl_label = 'Neltulz - Smart Frame : Refresh "Templated Obj List"'
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

class NTZSMFRM_OT_untemplateobjs(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.untemplateobjs"
    bl_label = 'Neltulz - Smart Frame : Remove obj from "Templated Obj List"'
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

class NTZSMFRM_OT_templatespecificobj(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.templatespecificobj"
    bl_label = 'Neltulz - Smart Frame : Add specific obj from "Templated Obj List"'
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

class NTZSMFRM_OT_untemplatespecificobj(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.untemplatespecificobj"
    bl_label = 'Neltulz - Smart Frame : Remove specific obj from "Templated Obj List"'
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

class NTZSMFRM_OT_clearalltemplatedobjs(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.clearalltemplatedobjs"
    bl_label = 'Neltulz - Smart Frame : Clear "Templated Obj List"'
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

class NTZSMFRM_OT_changetemplateselectionstate(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.changetemplateselectionstate"
    bl_label = 'Neltulz - Smart Frame : Change All Template Selection State'
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
        bpy.ops.ntz_smrt_frm.refreshtemplatedobjlist()

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
#    Viewport to Origin
# -----------------------------------------------------------------------------

class NTZSMFRM_OT_viewtoorigin(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.viewporttoorigin"
    bl_label = 'Neltulz - Smart Frame : Viewport to Origin'
    bl_description = 'Moves the viewport to the origin'
    bl_options = {'REGISTER', 'UNDO'}

    wasInvoked : BoolProperty(
        name="Operator was invoked",
        default = False
    )

    invokeView : StringProperty(
        name="Invoke View Operators",
    )

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        pass
    #END draw()

    def execute(self, context):

        if not self.wasInvoked:
            self.invokeView = "EXEC_DEFAULT"

        scene = context.scene

        addonPrefs = context.preferences.addons[__package__].preferences

        modeAtBegin = "Unknown"
        selObjs = bpy.context.selected_objects
        activeObj = bpy.context.view_layer.objects.active
        
        try:
            #try to determine objectMode
            modeAtBegin = bpy.context.object.mode
        except:
            modeAtBegin = "OBJECT"

        
        if activeObj is not None:
            if not activeObj in selObjs:
                if modeAtBegin == "EDIT":
                    selObjs.append(activeObj)

        if modeAtBegin != "OBJECT":
            bpy.ops.object.mode_set(mode = 'OBJECT')

        #use all regions when framing? (Useful for quad view)
        bUseAllRegions = addonPrefs.useAllRegionsWhenFraming
        bUseAll3DAreas = addonPrefs.useAll3DAreasWhenFraming
        
        misc_functions.view2Origin(self, context, bUseAllRegions, bUseAll3DAreas)

        if len(selObjs) > 0:
            bpy.context.view_layer.objects.active = selObjs[0]
            selObjs[0].select_set(True)

            if modeAtBegin == "EDIT":
                bpy.ops.object.mode_set(mode = 'EDIT')

        #final step
        if self.wasInvoked:
            self.wasInvoked = False

        return {'FINISHED'}
    # END execute()

    def invoke(self, context, event):
        scene = context.scene

        addonPrefs = context.preferences.addons[__package__].preferences

        self.wasInvoked = True

        if addonPrefs.bUseSmoothFraming:
            self.invokeView = "INVOKE_DEFAULT"
        else:
            self.invokeView = "EXEC_DEFAULT"
        
        return self.execute(context)
    #END invoke()
    
# END Operator()


# -----------------------------------------------------------------------------
#    Select Object by Name
# -----------------------------------------------------------------------------

class NTZSMFRM_OT_selobj(Operator):
    """Tooltip"""
    bl_idname = "ntz_smrt_frm.selobj"
    bl_label = 'Neltulz - Smart Frame : Select Object'
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