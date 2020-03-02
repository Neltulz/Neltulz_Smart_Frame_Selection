import bpy
import bmesh
import numpy

from operator       import itemgetter
from mathutils      import Vector
from itertools      import chain
from itertools      import permutations

def average(lst): 
    return sum(lst) / len(lst) 

# -----------------------------------------------------------------------------
#   Determine which mode is currently Selected (Vert, Edge, Face, etc)
#   Returned: (0=Multiple modes, 1=Vertice Mode, 2=Edge Mode, 3=Face Mode)
# -----------------------------------------------------------------------------

def getSelMode():
    #Create empty list
    tempList = []

    #check current mesh select mode
    for bool in bpy.context.tool_settings.mesh_select_mode:
        tempList.append(bool)
    
    #convert list into a tuple
    currentSelectMode = tuple(tempList)

    return currentSelectMode
# END getSelMode(self, context)

def setSelMode( selBoolTuple):
    bpy.context.tool_settings.mesh_select_mode = selBoolTuple
# END getSelMode(self, context)


def getAllCurvePointsAndHandles(self, context, obj):
    if obj.type == "CURVE":
        curve = obj.data

        #switch to object mode
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

        #switch to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        curvePointList = [p for p in curve.splines.active.bezier_points if p.select_control_point]
        curveHandlesLeftList = [p for p in curve.splines.active.bezier_points if p.select_left_handle]
        curveHandlesRightList = [p for p in curve.splines.active.bezier_points if p.select_right_handle]

        selected_curve_points_and_handles = [curvePointList, curveHandlesLeftList, curveHandlesRightList]

        #switch back to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
            
        return selected_curve_points_and_handles

def hideUnselected_Objs(self, context, scene, addonPrefs, selObjs, activeObj):

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
                    if addonPrefs.useExtremeHideOnIsolate:
                        if obj.hide_viewport == False:
                            obj.hide_viewport = True

                    foundObjectToHide = True

    if foundObjectToHide:
        scene.ntzSmFrm.currentlyBusyIsolating = True

        hideFloorAndAxes(self, context, scene, addonPrefs)

        #hide all but selected
        for obj in bpy.context.scene.objects:
            if 'ntzSmFrm_hidden' in obj:
                obj.hide_set(True) #unhide object

        foundObjectToHide = False #reset

    else:
        scene.ntzSmFrm.currentlyBusyIsolating = True

        hideFloorAndAxes(self, context, scene, addonPrefs)

def hideFloorAndAxes(self, context, scene, addonPrefs):
    #store current floor visibility for use later:
    scene.ntzSmFrm.floorWasPreviouslyVisible = bpy.context.space_data.overlay.show_floor

    #store current axes visibility for use later:
    scene.ntzSmFrm.axis_x_wasPreviouslyVisible = bpy.context.space_data.overlay.show_axis_x
    scene.ntzSmFrm.axis_y_wasPreviouslyVisible = bpy.context.space_data.overlay.show_axis_y
    scene.ntzSmFrm.axis_z_wasPreviouslyVisible = bpy.context.space_data.overlay.show_axis_z

    if addonPrefs.hideFloorOnIsolate:
        bpy.context.space_data.overlay.show_floor = False

    if addonPrefs.hideAxesOnIsolate:
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

def setObjTypeVisibility(self, context, scene, addonPrefs, visibilityCommandList, previousVisibility, visibilitySceneBoolList):
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


def viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjs, activeObj, totalNumVertsSel=0, forceFrameAllVerts=False):

    winAreaRegionInfoList = [] #declare

    self.useZoomAdjust_greenLight = (self.totalVertCount <= addonPrefs.maxVertAllowanceForZoomAdjust) and (totalNumVertsSel <= addonPrefs.maxVertSelectionAllowanceForZoomAdjust)

    if forceFrameAllVerts:
        
        setSelMode( (True, False, False) )

        for obj in bpy.context.objects_in_mode:
            bm = bmesh.from_edit_mesh(obj.data)

            for v in bm.verts:
                v.select = True

            bm.select_flush(True) #force faces to also sorta be selected so that framing is correct with multiple mesh objects in edit mode
            bmesh.update_edit_mesh(obj.data, False, False)

    if self.use_zoomAdjust and self.useZoomAdjust_greenLight:

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

                        allSelVertIDs = [] #declare
                        for obj in bpy.context.objects_in_mode:
                            bm = bmesh.from_edit_mesh(obj.data)

                            for v in bm.verts:
                                if v.select:
                                    selVertIDs = [{"OBJNAME": obj.name, "VERTID": v.index}]
                                    allSelVertIDs = allSelVertIDs + selVertIDs

                        if len(allSelVertIDs) == 1:
                            self.viewSelectMethod = "SINGLE_VERT"
                            _dict = selVertIDs[0]
                            objWithSingleVert = bpy.data.objects[ _dict['OBJNAME'] ]

                        elif len(allSelVertIDs) == 2:
                            self.viewSelectMethod = "EDGE"

                        elif len(allSelVertIDs) > 2:
                            self.viewSelectMethod = "FACE"

            #determine the bounding box size
            if self.viewSelectMethod == "SINGLE_VERT":
                self.viewSelectionWidth = max_dim_from_single_vert_and_adjacent_verts(self, context, scene, addonPrefs, objWithSingleVert)
                
            elif self.viewSelectMethod == "EDGE":
                self.viewSelectionWidth = ( max_dim_from_selection(self, context, scene, addonPrefs) * 1)
                
            elif self.viewSelectMethod == "FACE":
                self.viewSelectionWidth = ( max_dim_from_selection(self, context, scene, addonPrefs) * 1)

            elif self.viewSelectMethod == "OBJ":
                self.viewSelectionWidth = ( max_dim_from_objs_or_empties(self, context, scene, addonPrefs, selObjs) * 1)




    if bUseAll3DAreas:

        # Check for 3D Views
        for win in context.window_manager.windows:
            for area in win.screen.areas:
                if area.type == 'VIEW_3D':
                    
                    if self.use_zoomAdjust and self.useZoomAdjust_greenLight:
                        
                        viewClipStart = area.spaces.active.clip_start
                        viewClipStartList.append(viewClipStart)

                    #view selected
                    winAreaRegionInfo = {'window': win, 'area': area, 'region': area.regions[-1]}
                    winAreaRegionInfoList.append(winAreaRegionInfo)

    else:
        viewClipStartList = [bpy.context.area.spaces.active.clip_start]
        winAreaRegionInfoList = [context.copy()]
    

    for i, winAreaRegionInfo in enumerate(winAreaRegionInfoList):

        if self.use_zoomAdjust and self.useZoomAdjust_greenLight:

            if bUseAll3DAreas:
                area = winAreaRegionInfoList[i]['area']
            else:
                area = bpy.context.area
            
            #determine clip start value for zooming
            clip_start_result = self.viewSelectionWidth + (self.viewSelectionWidth * self.zoomAdjust)
            area.spaces.active.clip_start = clip_start_result

        bpy.ops.view3d.view_selected(winAreaRegionInfo, self.invokeView, use_all_regions=bUseAllRegions)

        if self.use_zoomAdjust and self.useZoomAdjust_greenLight:
            #return clip start values back to their original value after framing
            area.spaces.active.clip_start = viewClipStartList[i]

    
    if forceFrameAllVerts:
        for obj in selObjs:
            bm = bmesh.from_edit_mesh(obj.data)
            for v in bm.verts:
                v.select = False
            
            bm.select_flush(False) #force faces to be deselected
            bmesh.update_edit_mesh(obj.data, False, False)

        setSelMode(self.selModeAtBegin)
    
    


    

def viewAll(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas):
    # Note: Only use this function in object mode - Never edit mode.

    selObjsTemp = [] #declare

    #select all objects except ones excluded from framing
    for obj in scene.objects:

        try:
            frameObjType = addonPrefs.frameObjTypeList2[obj.type]
        except:
            frameObjType = None

        #known object types:
        if frameObjType is not None:

            frameTypeState = getattr(addonPrefs, frameObjType)

            if frameTypeState:
                obj.select_set(True)
                selObjsTemp.append(obj)

        #unknown object type
        else:
            obj.select_set(True)
            selObjsTemp.append(obj)

    #declare an active object for the viewSelected function
    if len(selObjsTemp) > 0:
        activeObjTemp = selObjsTemp[0]
        viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, selObjsTemp, activeObjTemp)
    else:
        view2Origin(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas)



    #deselect all objects
    for obj in scene.objects:
        obj.select_set(False)



def view2Origin(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas):

    #create obj
    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=5, location=(0, 0, 0))
    
    #if empty object type view was disabled, it must be re-enabled temporarily in order to determine the selected object
    emptyViewWasDisabled = False #declare
    if not context.space_data.show_object_viewport_empty:
        emptyViewWasDisabled = True
        context.space_data.show_object_viewport_empty = True

    tempEmptyObj = context.selected_objects[0]

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
        viewSelected(self, context, scene, addonPrefs, modeAtBegin, bUseAllRegions, bUseAll3DAreas, [tempEmptyObj], tempEmptyObj)

    bpy.ops.object.delete(use_global=False, confirm=False)

    if emptyViewWasDisabled:
        context.space_data.show_object_viewport_empty = False

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


def max_dim_from_single_vert_and_adjacent_verts(self, context, scene, addonPrefs, objWithSingleVert):
    
    bm = bmesh.from_edit_mesh(objWithSingleVert.data)
    mat = objWithSingleVert.matrix_world

    #find linked vertices - Source: https://blenderartists.org/t/code-snippet-with-bmesh-find-the-linked-vertices/534077
    selectedVert = [] #declare
    linkedVerts = [] #declare
    for i_0, v_0 in enumerate(bm.verts):
        if v_0.select:
            selectedVert.append( mat @ v_0.co )
        if v_0.select and v_0.is_valid:
            for i_1, e_0 in enumerate(v_0.link_edges):
                linkedVerts.append(mat @ e_0.other_vert(v_0).co)

    all_vcos = [] #declare
    all_vcos.extend(selectedVert)
    all_vcos.extend(linkedVerts)

    it = numpy.fromiter(chain.from_iterable(all_vcos), dtype=float)
    it.shape = (len(all_vcos), 3)
    _min, _max = Vector(it.min(0).tolist()), Vector(it.max(0).tolist())

    if addonPrefs.calcZoomDistanceMethod == "MIN":
        result = min((_max - _min))
    elif addonPrefs.calcZoomDistanceMethod == "MAX": 
        result = max((_max - _min))
    elif addonPrefs.calcZoomDistanceMethod == "AVG":
        result = average((_max - _min))

    if result == 0:
        result = 1

    return result

def max_dim_from_selection(self, context, scene, addonPrefs):

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

    if addonPrefs.calcZoomDistanceMethod == "MIN":
        result = min((_max - _min))
    elif addonPrefs.calcZoomDistanceMethod == "MAX": 
        result = max((_max - _min))
    elif addonPrefs.calcZoomDistanceMethod == "AVG":
        result = average((_max - _min))

    return result

def max_dim_from_objs_or_empties(self, context, scene, addonPrefs, selObjs):
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

    if addonPrefs.calcZoomDistanceMethod == "MIN":
        result = min((_max - _min))
    elif addonPrefs.calcZoomDistanceMethod == "MAX": 
        result = max((_max - _min))
    elif addonPrefs.calcZoomDistanceMethod == "AVG":
        result = average((_max - _min))

    #prevent zero result
    if result == 0:
        result = 1

    return result