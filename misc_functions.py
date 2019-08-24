import bpy
        

# -----------------------------------------------------------------------------
#   Determine which mode is currently Selected (Vert, Edge, Face, etc)
#   Returned: (0=Multiple modes, 1=Vertice Mode, 2=Edge Mode, 3=Face Mode)
# -----------------------------------------------------------------------------

def getCurrentSelectMode(self, context):
    #Create empty list
    tempList = []

    #check current mesh select mode
    for bool in bpy.context.tool_settings.mesh_select_mode:
        tempList.append(bool)
    
    #convert list into a tuple
    tempTuple = tuple(tempList)

    currentSelectMode = int()

    
    if tempTuple == (True, False, False):       
        currentSelectMode = 1
    elif tempTuple == (False, True, False):
        currentSelectMode = 2
    elif tempTuple == (False, False, True):
        currentSelectMode = 3
    else:
        pass #(defaults currentSelectMode to 0)

    return currentSelectMode
# END getCurrentSelectMode(self, context)


def getSelectedEdges(self, context, obj):
    mesh = obj.data

    #switch to object mode before getting edgeList
    bpy.ops.object.mode_set(mode='OBJECT')

    edgeList = [e for e in mesh.edges if e.select]

    #switch back to edit mode
    bpy.ops.object.mode_set(mode='EDIT')
        
    return edgeList

def getSelectedVerts(self, context, obj):
    mesh = obj.data

    #switch to object mode before getting edgeList
    bpy.ops.object.mode_set(mode='OBJECT')

    vertList = [v for v in mesh.vertices if v.select]

    #switch back to edit mode
    bpy.ops.object.mode_set(mode='EDIT')
        
    return vertList

def getAllEdges(self, context, obj):
    mesh = obj.data

    #switch to object mode before getting edgeList
    bpy.ops.object.mode_set(mode='OBJECT')

    edgeList = [e for e in mesh.edges]

    #switch back to edit mode
    bpy.ops.object.mode_set(mode='EDIT')
        
    return edgeList

def hideUnselected_Objs(self, context, scene, obj_sel):

    foundObjectToHide = False #initial declare

    #loop through all objects in scene and put a custom prop so we know which objects to unhide
    for obj in bpy.context.scene.objects:
        if obj not in obj_sel:
            obj['neltulzSmartFrameSel_hidden'] = 1
            foundObjectToHide = True
            
    if foundObjectToHide:
        scene.neltulzSmartFrameSel.currentlyBusyIsolating = True

        #hide all but selected
        bpy.ops.object.hide_view_set(unselected=True)

        foundObjectToHide = False #reset

    

def unhidePreviouslyHidden_Objs(self, context, scene):
    #loop through all objects in scene check the custom prop
    for obj in bpy.context.scene.objects:
        if 'neltulzSmartFrameSel_hidden' in obj:
            if obj['neltulzSmartFrameSel_hidden'] == 1:
                obj.hide_set(False) #unhide object
                del obj['neltulzSmartFrameSel_hidden']

    scene.neltulzSmartFrameSel.currentlyBusyIsolating = False


def hideSelected_VertsEdgesFaces(self, context, scene):
    bpy.ops.mesh.hide(unselected=True)
    scene.neltulzSmartFrameSel.currentlyBusyIsolating = True

def unhidePreviouslyHidden_VertsEdgesFaces(self, context, scene):
    bpy.ops.mesh.reveal(select=False)
    scene.neltulzSmartFrameSel.currentlyBusyIsolating = False