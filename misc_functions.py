import bpy
import bmesh
from operator import itemgetter
from mathutils import Vector
import numpy
from itertools import chain
from itertools import permutations

def average(lst): 
    return sum(lst) / len(lst) 

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

def getSelectedVerts(self, context, obj, returnMethod):

    if obj.type == "MESH":

        mesh = obj.data

        modeAtBegin = bpy.context.object.mode

        #switch to object mode before getting edgeList
        if modeAtBegin == "EDIT":
            bpy.ops.object.mode_set(mode='OBJECT')

        if returnMethod == "VERTS_ONLY":
            vertList = [v for v in mesh.vertices if v.select]
        elif returnMethod == "VERT_IDS_ONLY":
            vertList = [v.index for v in mesh.vertices if v.select]
        elif returnMethod == "OBJ_NAME_AND_VERT_IDS":
            vertList = [] #declare
            for v in mesh.vertices:
                if v.select:
                    temp = [{"OBJNAME": obj.name, "VERTID": v.index}]
                    vertList = vertList + temp

        if modeAtBegin == "EDIT":
            #switch back to edit mode
            bpy.ops.object.mode_set(mode='EDIT')
            
        return vertList


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

def hideUnselected_Objs(self, context, scene, selObjs, activeObj):

    foundObjectToHide = False #initial declare

    #loop through all objects in scene and put a custom prop so we know which objects to unhide
    for obj in bpy.context.scene.objects:

        if obj not in selObjs:
            if obj.visible_get(): #ensure object is visible, that way later on, user preferred hidden objects don't get revealed accidentally
                if 'ntzSmFrm_isolateExcluded' in obj:
                    pass
                else:
                    obj['ntzSmFrm_hidden'] = 1

                    #should object use extreme hidden to grant a big performance increase?
                    if scene.ntzSmFrm.useExtremeHideOnIsolate:
                        if obj.hide_viewport == False:
                            obj.hide_viewport = True

                    foundObjectToHide = True

    if foundObjectToHide:
        scene.ntzSmFrm.currentlyBusyIsolating = True

        hideFloorAndAxes(self, context, scene)

        #hide all but selected
        for obj in bpy.context.scene.objects:
            if 'ntzSmFrm_hidden' in obj:
                obj.hide_set(True) #unhide object

        foundObjectToHide = False #reset

    else:
        scene.ntzSmFrm.currentlyBusyIsolating = True

        hideFloorAndAxes(self, context, scene)

def hideFloorAndAxes(self, context, scene):
    #store current floor visibility for use later:
    scene.ntzSmFrm.floorWasPreviouslyVisible = bpy.context.space_data.overlay.show_floor

    #store current axes visibility for use later:
    scene.ntzSmFrm.axis_x_wasPreviouslyVisible = bpy.context.space_data.overlay.show_axis_x
    scene.ntzSmFrm.axis_y_wasPreviouslyVisible = bpy.context.space_data.overlay.show_axis_y
    scene.ntzSmFrm.axis_z_wasPreviouslyVisible = bpy.context.space_data.overlay.show_axis_z

    if scene.ntzSmFrm.hideFloorOnIsolate:
        bpy.context.space_data.overlay.show_floor = False

    if scene.ntzSmFrm.hideAxesOnIsolate:
        bpy.context.space_data.overlay.show_axis_x = False
        bpy.context.space_data.overlay.show_axis_y = False
        bpy.context.space_data.overlay.show_axis_z = False

def unhidePreviouslyHidden_Objs(self, context, scene):

    #restore floor visibility
    if scene.ntzSmFrm.floorWasPreviouslyVisible:
        bpy.context.space_data.overlay.show_floor = True

    #restore axes visibility
    if scene.ntzSmFrm.axis_x_wasPreviouslyVisible:
        bpy.context.space_data.overlay.show_axis_x = True

    if scene.ntzSmFrm.axis_y_wasPreviouslyVisible:
        bpy.context.space_data.overlay.show_axis_y = True

    if scene.ntzSmFrm.axis_z_wasPreviouslyVisible:
        bpy.context.space_data.overlay.show_axis_z = True

    #loop through all objects in scene check the custom prop
    for obj in bpy.context.scene.objects:
        if 'ntzSmFrm_hidden' in obj:
            if obj['ntzSmFrm_hidden'] == 1:
                obj.hide_set(False) #unhide object

                
                #Ensure "Show in Viewports" is enabled
                if obj.hide_viewport == True:
                    obj.hide_viewport = False

                del obj['ntzSmFrm_hidden']

    scene.ntzSmFrm.currentlyBusyIsolating = False


def hideSelected_VertsEdgesFaces(self, context, scene):
    bpy.ops.mesh.hide(unselected=True)
    scene.ntzSmFrm.currentlyBusyIsolating = True

def unhidePreviouslyHidden_VertsEdgesFaces(self, context, scene):
    bpy.ops.mesh.reveal(select=False)
    scene.ntzSmFrm.currentlyBusyIsolating = False

def hideSelected_CurvePointsAndHandles(self, context, scene):
    bpy.ops.curve.hide(unselected=True)
    scene.ntzSmFrm.currentlyBusyIsolating = True

def unhidePreviouslyHidden_CurvePointsAndHandles(self, context, scene):
    bpy.ops.curve.reveal()
    scene.ntzSmFrm.currentlyBusyIsolating = False

def setObjTypeVisibility(self, context, scene, visibilityCommandList, previousVisibility, visibilitySceneBoolList):
    #store previousVisibility so that it can be returned to original setting later
    for index, command in enumerate(visibilityCommandList):
        #store previousVisibility so that it can be returned to original setting later
        previousVisibility += list( [ eval(command) ] )

        commandToEval = command + " = " + visibilitySceneBoolList[index]
        eval(compile(commandToEval,'<string>','exec'))

def reenableVisibilityForAllObjs(self, context, scene, previousVisibility, visibilityCommandList):
     for index, boool in enumerate(previousVisibility):
        commandToEval = visibilityCommandList[index] + " = " + str(boool)
        eval(compile(commandToEval,'<string>','exec'))

def getSelObjsFromOutlinerAndViewport(self, context, modeAtBegin):
    #NOTE: modeAtBegin is "OBJECT" or "EDIT" mode

    outlinerBlueHighlightedObjs = set() #declare
    selObjs = set() #declare

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

        outlinerBlueHighlightedObjs = context.selected_objects[:]
        
        # Toggle on hide select for objects not selected in outliner
        for o in hide_select:
            if not o.select_get():
                o.hide_select = True

        for o in sel_org:  # Restore original selection
            o.select_set(True)

        selObjs = set(bpy.context.selected_objects)
        activeObj = bpy.context.view_layer.objects.active
        
        if activeObj is not None:
            if not activeObj in selObjs:
                if modeAtBegin == "EDIT":
                    selObjs.add(activeObj)

        selObjs.union(outlinerBlueHighlightedObjs)

    #if unable to retreive obects from outliner, then retrieve objects normally from sel objs and active object
    else:
        selObjs = bpy.context.selected_objects
        activeObj = bpy.context.view_layer.objects.active
        
        if activeObj is not None:
            if not activeObj in selObjs:
                if modeAtBegin == "EDIT":
                    selObjs.add(activeObj)

    return selObjs


def viewSelected(self, context, scene, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj):


    winAreaRegionInfoList = [] #declare

    if self.use_zoomAdjust:

        viewClipStartList = [] #declare
        self.viewSelectMethod = "NONE" #declare
        allSelVerts = [] #declare
        minEdgeLength = 0 #declare

        objWithSingleVert = None

 

        if self.wasInvoked:
            #determine which view select method to use
            if activeObj is not None:
                self.viewSelectMethod = "OBJ"

                if activeObj.type == "MESH":
                    if modeAtBegin == "EDIT":

                        #get list of selected verts
                        for obj in selObjs:
                            if obj.type == "MESH":
                                verts = getSelectedVerts(self, context, obj, "OBJ_NAME_AND_VERT_IDS")
                                allSelVerts = allSelVerts + verts
                                if len(allSelVerts) >= 1:
                                    objWithSingleVert = obj
                                    break

                        if len(allSelVerts) == 1:
                            self.viewSelectMethod = "SINGLE_VERT"

                        elif len(allSelVerts) == 2:
                            self.viewSelectMethod = "EDGE"

                        elif len(allSelVerts) > 2:
                            self.viewSelectMethod = "FACE"

            #determine the bounding box size
            if self.viewSelectMethod == "SINGLE_VERT":
                self.viewSelectionWidth = max_dim_from_single_vert_and_adjacent_verts(self, context, scene, allSelVerts, objWithSingleVert)
                
            elif self.viewSelectMethod == "EDGE":
                self.viewSelectionWidth = ( max_dim_from_selection(self, context, scene) * 1)
                
            elif self.viewSelectMethod == "FACE":
                self.viewSelectionWidth = ( max_dim_from_selection(self, context, scene) * 1)

            elif self.viewSelectMethod == "OBJ":
                self.viewSelectionWidth = ( max_dim_from_objs_or_empties(self, context, scene, selObjs) * 1)




    if bUseAll3DAreas:

        # Check for 3D Views
        for win in context.window_manager.windows:
            for area in win.screen.areas:
                if area.type == 'VIEW_3D':
                    
                    if self.use_zoomAdjust:
                        
                        viewClipStart = area.spaces.active.clip_start
                        viewClipStartList.append(viewClipStart)

                    #view selected
                    winAreaRegionInfo = {'window': win, 'area': area, 'region': area.regions[-1]}
                    winAreaRegionInfoList.append(winAreaRegionInfo)

    else:
        viewClipStartList = [bpy.context.area.spaces.active.clip_start]
        winAreaRegionInfoList = [context.copy()]
    

    for i, winAreaRegionInfo in enumerate(winAreaRegionInfoList):

        if self.use_zoomAdjust:

            if bUseAll3DAreas:
                area = winAreaRegionInfoList[i]['area']
            else:
                area = bpy.context.area
            
            #determine clip start value for zooming
            clip_start_result = self.viewSelectionWidth + (self.viewSelectionWidth * self.zoomAdjust)
            area.spaces.active.clip_start = clip_start_result

        bpy.ops.view3d.view_selected(winAreaRegionInfo, self.invokeView, use_all_regions=bUseAllRegions)

        if self.use_zoomAdjust:
            #return clip start values back to their original value after framing
            area.spaces.active.clip_start = viewClipStartList[i]


    
   
def viewAll(self, context, bUseAll3DAreas):

    winAreaRegionInfoList = []

    if bUseAll3DAreas:
        # Check for 3D Views
        for win in context.window_manager.windows:
            for area in win.screen.areas:
                if area.type == 'VIEW_3D':

                    winAreaRegionInfo = {'window': win, 'area': area, 'region': area.regions[-1]}
                    winAreaRegionInfoList.append(winAreaRegionInfo)
                    
    else:
        winAreaRegionInfoList = [context.copy()]

    for winAreaRegionInfo in winAreaRegionInfoList:

        #view all
        bpy.ops.view3d.view_all(winAreaRegionInfo, self.invokeView, center=False)


def view2Origin(self, context, bUseAllRegions, bUseAll3DAreas):

    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=5, location=(0, 0, 0))

    winAreaRegionInfoList = []

    # Check for 3D Views

    if bUseAll3DAreas:    
        for win in context.window_manager.windows:
            for area in win.screen.areas:
                if area.type == 'VIEW_3D':

                    winAreaRegionInfo = {'window': win, 'area': area, 'region': area.regions[-1]}
                    winAreaRegionInfoList.append(winAreaRegionInfo)

    else:
        winAreaRegionInfoList = [context.copy()]

    for winAreaRegionInfo in winAreaRegionInfoList:

        #view to origin
        bpy.ops.view3d.view_selected(winAreaRegionInfo, self.invokeView, use_all_regions=bUseAllRegions)

    bpy.ops.object.delete(use_global=False, confirm=False)

def bbox_from_selection():
    #returns the bounding box of a selection.  Special thanks and Source: iceythe
    all_vcos = []
    # Get all vert cos from objects in edit mode
    for o in bpy.context.objects_in_mode_unique_data:
        bm = bmesh.from_edit_mesh(o.data)
        mat = o.matrix_world
        all_vcos.extend([mat @ v.co for v in bm.verts if v.select])

    (x1, y1, z1,
     x2, y2, z2) = [func(all_vcos, key=itemgetter(i))[i]
                    for func in (min, max) for i in range(3)]

    bbox = (
        (x1, y1, z1), (x1, y1, z2),
        (x2, y1, z2), (x2, y1, z1),

        # mirror other size
        (x1, y2, z1), (x1, y2, z2),
        (x2, y2, z2), (x2, y2, z1))

    bbox_vecs = [Vector(i) for i in bbox]


    return bbox_vecs

def max_dim_from_single_vert_and_adjacent_verts(self, context, scene, allSelVerts, objWithSingleVert):
    startVert = allSelVerts[0]
    matrix = objWithSingleVert.matrix_world

    startVertWorldLoc = matrix @ objWithSingleVert.data.vertices[int(startVert['VERTID'])].co
    

    bpy.ops.mesh.select_more()

    adjacentVerts = getSelectedVerts(self, context, objWithSingleVert, "OBJ_NAME_AND_VERT_IDS")
    adjacentVerts.remove(startVert)

    edgeLengths = [] #declare

    for v in adjacentVerts:
        vWorldLoc = matrix @ objWithSingleVert.data.vertices[int(v['VERTID'])].co

        distance = (vWorldLoc - startVertWorldLoc).length

        edgeLengths.append(distance)

    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT') # switch to object mode before re-selecting the vert
    objWithSingleVert.data.vertices[ int(startVert['VERTID']) ].select = True
    bpy.ops.object.mode_set(mode='EDIT') # switch back to edit mode

    if scene.ntzSmFrm.calcZoomDistanceMethod == "MIN":
        result = min(edgeLengths)
    elif scene.ntzSmFrm.calcZoomDistanceMethod == "MAX": 
        result = max(edgeLengths)
    elif scene.ntzSmFrm.calcZoomDistanceMethod == "AVG":
        result = average(edgeLengths)

    return result

def max_dim_from_selection(self, context, scene):

    scene = context.scene

    #Get max dimension from selection - Special thanks & source: iceythe

    all_vcos = []
    # Get all vert cos from objects in edit mode
    for o in bpy.context.objects_in_mode_unique_data:
        bm = bmesh.from_edit_mesh(o.data)
        mat = o.matrix_world
        all_vcos.extend([(mat @ v.co)[:] for v in bm.verts if v.select])

    it = numpy.fromiter(chain.from_iterable(all_vcos), dtype=float)
    it.shape = (len(all_vcos), 3)
    _min, _max = Vector(it.min(0).tolist()), Vector(it.max(0).tolist())

    if scene.ntzSmFrm.calcZoomDistanceMethod == "MIN":
        result = min((_max - _min))
    elif scene.ntzSmFrm.calcZoomDistanceMethod == "MAX": 
        result = max((_max - _min))
    elif scene.ntzSmFrm.calcZoomDistanceMethod == "AVG":
        result = average((_max - _min))

    return result

def max_dim_from_objs_or_empties(self, context, scene, selObjs):
    scene = context.scene

    #Get max dimension from objects and empties - Special thanks & source: iceythe
    all_vcos = []
    for o in selObjs:
        mat_w = o.matrix_world
        if o.type == 'EMPTY':
            size = o.empty_display_size
            all_vcos.extend([mat_w @ Vector(point) for point in
                            permutations((-size, size) * 2, 3)])
            continue
        all_vcos.extend([mat_w @ Vector(point[:])
                        for point in o.bound_box[:]])

    it = numpy.fromiter(chain.from_iterable((all_vcos)), dtype=float)
    it.shape = (len(all_vcos), 3)
    _min, _max = Vector(it.min(0).tolist()), Vector(it.max(0).tolist())

    if scene.ntzSmFrm.calcZoomDistanceMethod == "MIN":
        result = min((_max - _min))
    elif scene.ntzSmFrm.calcZoomDistanceMethod == "MAX": 
        result = max((_max - _min))
    elif scene.ntzSmFrm.calcZoomDistanceMethod == "AVG":
        result = average((_max - _min))

    return result