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
    if obj.type == "MESH":
        mesh = obj.data

        #switch to object mode before getting edgeList
        bpy.ops.object.mode_set(mode='OBJECT')

        edgeList = [e for e in mesh.edges if e.select]

        #switch back to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
            
        return edgeList

def getSelectedVerts(self, context, obj):

    if obj.type == "MESH":

        mesh = obj.data

        #switch to object mode before getting edgeList
        bpy.ops.object.mode_set(mode='OBJECT')

        vertList = [v for v in mesh.vertices if v.select]

        #switch back to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
            
        return vertList

def getAllVerts(self, context, obj):
    if obj.type == "MESH":
        mesh = obj.data

        #switch to object mode before getting edgeList
        bpy.ops.object.mode_set(mode='OBJECT')

        vertList = [v for v in mesh.vertices]

        #switch back to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
            
        return vertList

def getAllVertIDs(self, context, obj):
    if obj.type == "MESH":
        mesh = obj.data

        #switch to object mode before getting edgeList
        bpy.ops.object.mode_set(mode='OBJECT')

        vertIDList = [v.index for v in mesh.vertices]

        #switch back to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
            
        return vertIDList

def getAllEdges(self, context, obj):
    if obj.type == "MESH":
        mesh = obj.data

        #switch to object mode before getting edgeList
        bpy.ops.object.mode_set(mode='OBJECT')

        edgeList = [e for e in mesh.edges]

        #switch back to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
            
        return edgeList

def getAllCurvePointsAndHandles(self, context, obj):
    if obj.type == "CURVE":
        curve = obj.data

        #switch to object mode before getting edgeList
        bpy.ops.object.mode_set(mode='OBJECT')

        curvePointList = [p for p in curve.splines.active.bezier_points]
        curveHandlesLeft = [p for p in curve.splines.active.bezier_points]
        curveHandlesRight = [p for p in curve.splines.active.bezier_points]

        all_curve_points_and_handles = [curvePointList, curveHandlesLeft, curveHandlesRight]

        #switch back to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
            
        return all_curve_points_and_handles

def getSelectedCurvePointsAndHandles(self, context, obj):
    if obj.type == "CURVE":
        curve = obj.data

        #switch to object mode before getting edgeList
        bpy.ops.object.mode_set(mode='OBJECT')

        curvePointList = [p for p in curve.splines.active.bezier_points if p.select_control_point]
        curveHandlesLeftList = [p for p in curve.splines.active.bezier_points if p.select_left_handle]
        curveHandlesRightList = [p for p in curve.splines.active.bezier_points if p.select_right_handle]

        selected_curve_points_and_handles = [curvePointList, curveHandlesLeftList, curveHandlesRightList]

        #switch back to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
            
        return selected_curve_points_and_handles

def hideUnselected_Objs(self, context, scene, obj_sel, active_obj):

    foundObjectToHide = False #initial declare

    #loop through all objects in scene and put a custom prop so we know which objects to unhide
    for obj in bpy.context.scene.objects:

        if obj not in obj_sel:
            if obj.visible_get(): #ensure object is visible, that way later on, user preferred hidden objects don't get revealed accidentally
                if 'neltulzSmartFrameSel_isolateExcluded' in obj:
                    pass
                else:
                    obj['neltulzSmartFrameSel_hidden'] = 1

                    #should object use extreme hidden to grant a big performance increase?
                    if scene.neltulzSmartFrameSel.useExtremeHideOnIsolate:
                        if obj.hide_viewport == False:
                            obj.hide_viewport = True

                    foundObjectToHide = True

    if foundObjectToHide:
        scene.neltulzSmartFrameSel.currentlyBusyIsolating = True

        hideFloorAndAxes(self, context, scene)

        #hide all but selected
        for obj in bpy.context.scene.objects:
            if 'neltulzSmartFrameSel_hidden' in obj:
                obj.hide_set(True) #unhide object

        foundObjectToHide = False #reset

    else:
        scene.neltulzSmartFrameSel.currentlyBusyIsolating = True

        hideFloorAndAxes(self, context, scene)

def hideFloorAndAxes(self, context, scene):
    #store current floor visibility for use later:
    scene.neltulzSmartFrameSel.floorWasPreviouslyVisible = bpy.context.space_data.overlay.show_floor

    #store current axes visibility for use later:
    scene.neltulzSmartFrameSel.axis_x_wasPreviouslyVisible = bpy.context.space_data.overlay.show_axis_x
    scene.neltulzSmartFrameSel.axis_y_wasPreviouslyVisible = bpy.context.space_data.overlay.show_axis_y
    scene.neltulzSmartFrameSel.axis_z_wasPreviouslyVisible = bpy.context.space_data.overlay.show_axis_z

    if scene.neltulzSmartFrameSel.hideFloorOnIsolate:
        bpy.context.space_data.overlay.show_floor = False

    if scene.neltulzSmartFrameSel.hideAxesOnIsolate:
        bpy.context.space_data.overlay.show_axis_x = False
        bpy.context.space_data.overlay.show_axis_y = False
        bpy.context.space_data.overlay.show_axis_z = False

def unhidePreviouslyHidden_Objs(self, context, scene):

    #restore floor visibility
    if scene.neltulzSmartFrameSel.floorWasPreviouslyVisible:
        bpy.context.space_data.overlay.show_floor = True

    #restore axes visibility
    if scene.neltulzSmartFrameSel.axis_x_wasPreviouslyVisible:
        bpy.context.space_data.overlay.show_axis_x = True

    if scene.neltulzSmartFrameSel.axis_y_wasPreviouslyVisible:
        bpy.context.space_data.overlay.show_axis_y = True

    if scene.neltulzSmartFrameSel.axis_z_wasPreviouslyVisible:
        bpy.context.space_data.overlay.show_axis_z = True

    #loop through all objects in scene check the custom prop
    for obj in bpy.context.scene.objects:
        if 'neltulzSmartFrameSel_hidden' in obj:
            if obj['neltulzSmartFrameSel_hidden'] == 1:
                obj.hide_set(False) #unhide object

                
                #Ensure "Show in Viewports" is enabled
                if obj.hide_viewport == True:
                    obj.hide_viewport = False

                del obj['neltulzSmartFrameSel_hidden']

    scene.neltulzSmartFrameSel.currentlyBusyIsolating = False


def hideSelected_VertsEdgesFaces(self, context, scene):
    bpy.ops.mesh.hide(unselected=True)
    scene.neltulzSmartFrameSel.currentlyBusyIsolating = True

def unhidePreviouslyHidden_VertsEdgesFaces(self, context, scene):
    bpy.ops.mesh.reveal(select=False)
    scene.neltulzSmartFrameSel.currentlyBusyIsolating = False

def hideSelected_CurvePointsAndHandles(self, context, scene):
    bpy.ops.curve.hide(unselected=True)
    scene.neltulzSmartFrameSel.currentlyBusyIsolating = True

def unhidePreviouslyHidden_CurvePointsAndHandles(self, context, scene):
    bpy.ops.curve.reveal()
    scene.neltulzSmartFrameSel.currentlyBusyIsolating = False