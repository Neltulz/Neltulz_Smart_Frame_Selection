import bpy

#Show hide section with arrow, optional checkbox, and text
def createShowHide(self, context, scene, properties, showHideBool, optionalCheckboxBool, text, layout):

    if scene is not None:
        data = eval( f"scene.{properties}" )
        boolThing = eval( f"scene.{properties}.{showHideBool}" )
    else:
        data = self
        boolThing = eval( f"self.{showHideBool}")

    if boolThing:
        showHideIcon = "TRIA_DOWN"
    else:
        showHideIcon = "TRIA_RIGHT"

    row = layout.row(align=True)

    downArrow = row.column(align=True)
    downArrow.alignment = "LEFT"
    downArrow.prop(data, showHideBool, text="", icon=showHideIcon, emboss=False )

    if optionalCheckboxBool is not None:
        checkbox = row.column(align=True)
        checkbox.alignment = "LEFT"
        checkbox.prop(data, optionalCheckboxBool, text="" )

    textRow = row.column(align=True)
    textRow.alignment = "LEFT"
    textRow.prop(data, showHideBool, text=text, emboss=False )

    emptySpace = row.column(align=True)
    emptySpace.alignment = "EXPAND"
    emptySpace.prop(data, showHideBool, text=" ", emboss=False)

def createProp(self, context, scene, bEnabled, labelText, data, propItem, scale_y, labelScale, propScale, labelAlign, propAlign, propText, bExpandProp, bUseSlider, layout):

    propRow = layout.row(align=True)

    if not bEnabled:
        propRow.enabled = False

    propRow.scale_y = scale_y

    propRowLabel = propRow.row(align=True)
    propRowLabel.alignment="EXPAND"
    propRowLabel.ui_units_x = labelScale

    propRowLabel1 = propRowLabel.row(align=True)
    propRowLabel1.alignment=labelAlign
    propRowLabel1.scale_x = 1

    propRowLabel1.label(text=labelText)

    propRowItem = propRow.row(align=True)
    propRowItem.alignment=propAlign

    propRowItem1 = propRowItem.row(align=True)
    propRowItem1.alignment=propAlign
    propRowItem1.ui_units_x = propScale
    propRowItem1.scale_x = 100

    propRowItem1.prop(data, propItem, text=propText, expand=bExpandProp, slider=bUseSlider)

def sep(scaleY, layout):
    #custom separator that allows shorter y distance
    sep = layout.column(align=True)
    sep.label(text="",)
    sep.scale_y = scaleY

def mainSmartFramePanel(self, context, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel):
    
    scene = context.scene
    layout = self.layout.column(align=True)

    #determine if panel is inside of a popop/pie menu
    panelInsidePopupOrPie = context.region.type == 'WINDOW'

    if panelInsidePopupOrPie:

        if bUseCompactPopupAndPiePanel:
            layout.ui_units_x = 8
            layout.label(text="Smart Frame")

        else:
            layout.ui_units_x = 13
            layout.label(text="Neltulz - Smart Frame")

    #main frame & isolate buttons
    frameIsolateButtons_section(self, context, scene, panelInsidePopupOrPie, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel, layout)


def frameIsolateButtons_section(self, context, scene, panelInsidePopupOrPie, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel, layout):

    compactPanelConditions = (panelInsidePopupOrPie and bUseCompactPopupAndPiePanel) or (not panelInsidePopupOrPie and bUseCompactSidebarPanel)

    if compactPanelConditions:
        frameText = "Frm"
        if scene.ntzSmFrm.useExtremeHideOnIsolate:
            isolateText = "E-Iso"
        else:
            isolateText = "Iso"
        scaleY = 1
        frameAndIsolateText = "Frm+Iso"
        templateText = "Tmplt"
        viewOriginText = "View2Ori"
    else:
        frameText = "Frame"
        if scene.ntzSmFrm.useExtremeHideOnIsolate:
            isolateText = "Ext Isolate"
        else:
            isolateText = "Isolate"
        scaleY = 1.5
        frameAndIsolateText = "Frame & Isolate"
        templateText = "Template"
        viewOriginText = "Viewport to Origin"

    frameAndIsolateRow = layout.row(align=True)
    frameAndIsolateRow.scale_y = scaleY


    
    frameRow = frameAndIsolateRow.row(align=True)
    
    frameOpRow = frameRow.column(align=True)
    frameOpRow.alignment="EXPAND"
    frameOpRow.scale_x = 100
    op = frameOpRow.operator('ntz_smrt_frm.select', text=frameText, icon="NONE")
    op.tooltip = "Frame an object, selection of objects, vertice, edge, face, or when all else fails: frame everything"
    op.frameSelection=True
    op.isolateSelection=False

    framePopoverRow = frameRow.row(align=True)
    popover = framePopoverRow.popover(text="", panel="NTZSMFRM_PT_frameoptions", icon="DOWNARROW_HLT")

    frameAndIsolateRow.separator()

    isolateRow = frameAndIsolateRow.row(align=True)

    if scene.ntzSmFrm.currentlyBusyIsolating:
        isolateText = "Unhide"

    isolateOpRow = isolateRow.row(align=True)
    isolateOpRow.alignment="EXPAND"
    isolateOpRow.scale_x = 100
    op = isolateOpRow.operator('ntz_smrt_frm.select', text=isolateText, icon="NONE")
    if scene.ntzSmFrm.useExtremeHideOnIsolate:
        op.tooltip = "Extreme Isolate an object, selection of objects, vertice, edge, face, or when all else fails: extreme isolate everything.  Extreme isolate can improve performance when isolating objects, but take longer to unhide because every object in the viewport must be re-rendered"
    else:
        op.tooltip = "Isolate an object, selection of objects, vertice, edge, face, or when all else fails: isolate everything"
    op.frameSelection=False
    op.isolateSelection=True

    IsolatePopoverRow = isolateRow.row(align=True)
    popover = IsolatePopoverRow.popover(text="", panel="NTZSMFRM_PT_isolateoptions", icon="DOWNARROW_HLT")

    layout.separator()

    #Frame & Isolate AND Template Row
    frameAndIsolateAndTemplateRow = layout.row(align=True)
    frameAndIsolateAndTemplateRow.scale_y = scaleY

    frameAndIsolateRow = frameAndIsolateAndTemplateRow.row(align=True)

    frameAndIsolateOpRow = frameAndIsolateRow.row(align=True)
    frameAndIsolateOpRow.alignment="EXPAND"
    frameAndIsolateOpRow.scale_x = 100

    if scene.ntzSmFrm.currentlyBusyIsolating:
        frameAndIsolateOpRow.enabled=False
    op = frameAndIsolateOpRow.operator('ntz_smrt_frm.select', text=frameAndIsolateText)
    op.tooltip = "Frame and Isolate an object, selection of objects, vertices, edges, or faces, simultaneously, or when all else fails: everything"
    op.frameSelection=True
    op.isolateSelection=True

    frameAndIsolateAndTemplateRow.separator()

    templateRow = frameAndIsolateAndTemplateRow.row(align=True)

    templateOpRow = templateRow.row(align=True)
    templateOpRow.alignment="EXPAND"
    templateOpRow.scale_x = 100

    op = templateOpRow.operator('ntz_smrt_frm.toggletemplate', text=templateText, icon="NONE")
    op.tooltip = "Converts an object to a wireframe with click-through (unselectable) capability for reference purposes"

    if scene.ntzSmFrm.defaultTemplateSelectableState == "UNSELECTABLE":
        op.makeSelectable = False
    elif scene.ntzSmFrm.defaultTemplateSelectableState == "SELECTABLE":
        op.makeSelectable = True

    templatePopoverRow = templateRow.row(align=True)
    popover = templatePopoverRow.popover(text="", panel="NTZSMFRM_PT_templateoptions", icon="DOWNARROW_HLT")

    layout.separator()



    col = layout.column(align=True)
    op = col.operator('ntz_smrt_frm.viewporttoorigin', text=viewOriginText)

def frameOptions_sectionInner(self, context, scene, layout):

    layout.prop(scene.ntzSmFrm, "bUseSmoothFraming", expand=True)

    layout.separator()

    label = layout.label(text="Calculate Zoom based on:")
    zoomDistanceMethodRow = layout.row(align=True)
    zoomDistanceMethodRow.prop(scene.ntzSmFrm, "calcZoomDistanceMethod", expand=True)

    layout.separator()

    frameObjType_sectionInner(self, context, scene, False, layout)

    layout.separator()

    layout.prop(scene.ntzSmFrm, "use_all_regions_when_framing", expand=True)
    layout.prop(scene.ntzSmFrm, "use_all_3d_areas_when_framing", expand=True)

        

def isolateOptions_sectionInner(self, context, scene, layout):

    excludedObjsFromIsolate_sectionInner(self, context, scene, False, layout)

    layout.label(text="On Isolate, hide:")

    row = layout.row(align=True)

    row.prop(scene.ntzSmFrm, "hideFloorOnIsolate", expand=True, text="Floor", toggle=True, icon="MESH_GRID")

    row.prop(scene.ntzSmFrm, "hideAxesOnIsolate", expand=True, text="Axes", toggle=True, icon="EMPTY_AXIS")

    layout.separator()

    layout.prop(scene.ntzSmFrm, "useExtremeHideOnIsolate", expand=True)






def frameObjType_sectionInner(self, context, scene, bIndent, layout):

    if bIndent:
        row = layout.row(align=True)
        indent = row.column(align=True)
        indent.label(text="", icon="BLANK1")

        frameObjTypeCol = row.column(align=True)
    else:
        frameObjTypeCol = layout

    frameObjTypeCol.label(text="When nothing is selected, frame:")

    grid = frameObjTypeCol.grid_flow(row_major=True, columns=2, align=True)

    for frameObjType in scene.ntzSmFrm.frameObjTypeList:
        grid.prop(scene.ntzSmFrm, frameObjType, expand=True, toggle=True)

    #END "When Nothing is selected, frame..." section

def excludedObjsFromIsolate_sectionInner(self, context, scene, bIndent, layout):

    layout.separator()

    if bIndent:
        row = layout.row(align=True)
        indent = row.column(align=True)
        indent.label(text="", icon="BLANK1")

        excludedObjsFromIsolateCol = row.column(align=True)
    else:
        excludedObjsFromIsolateCol = layout

    excludedObjsFromIsolateCol.label(text="Excluded objects from Isolate:")
    excludedObjectsSection = excludedObjsFromIsolateCol.row(align=True)

    excludedObjectsSectionCol = excludedObjectsSection.column(align=True)

    numExcludedFromIsolate = len(scene.ntzSmFrm.excludedIsolateObjects)


    boxExcludedIsolate = excludedObjectsSectionCol.box()
    
    objectText = "objects"
    if numExcludedFromIsolate == 1:
        objectText = "object"

    text=f"{numExcludedFromIsolate} {objectText}."
    boxExcludedIsolate.label(text=text)

    boxCol = boxExcludedIsolate.column(align=True)

    if numExcludedFromIsolate > 0:

        if not scene.ntzSmFrm.hideFullIsolateExclusionList:
            row = boxCol.row(align=True)
            row.prop(scene.ntzSmFrm, "hideFullIsolateExclusionList", text="Show List", toggle=True)
        else:
            row = boxCol.row(align=True)
            row.prop(scene.ntzSmFrm, "hideFullIsolateExclusionList", text="Hide List", toggle=True)

            for item in scene.ntzSmFrm.excludedIsolateObjects:
                row = boxCol.row(align=True)

                op = row.operator('ntz_smrt_frm.unexcludeobj', text="", icon="X")
                op.objectToUntemplate = item

                row.label(text=item)



    else: 
        row = boxCol.row(align=True)
        row.label(text="None")

    excludedObjectsSectionCol = excludedObjectsSection.column(align=True)

    op = excludedObjectsSectionCol.operator('ntz_smrt_frm.excludeobj', text="", icon="ADD")
    op = excludedObjectsSectionCol.operator('ntz_smrt_frm.unexcludeobj', text="", icon="REMOVE")
    op = excludedObjectsSectionCol.operator('ntz_smrt_frm.refreshexcludedobjlist', text="", icon="FILE_REFRESH")
    op = excludedObjectsSectionCol.operator('ntz_smrt_frm.clearexcludedobjs', text="", icon="TRASH")


def templateOptions_section(self, context, scene,  bIndent, layout):

    layout.separator()

    if bIndent:
        row = layout.row(align=True)
        indent = row.column(align=True)
        indent.label(text="", icon="BLANK1")

        templatedObjsCol = row.column(align=True)
    else:
        templatedObjsCol = layout

    templatedObjsCol.label(text="Default Template Selectable State")
    prop = templatedObjsCol.prop(scene.ntzSmFrm, 'defaultTemplateSelectableState', text="", toggle=True)

    templatedObjsCol.separator()

    templateSelectableCol = templatedObjsCol.column(align=True)
    templateSelectableCol.scale_y = 1.25
    templateSelectableCol.label(text="Make All Template Objects:")
    templateSelectableRow = templateSelectableCol.row(align=True)
    op = templateSelectableRow.operator('ntz_smrt_frm.changetemplateselectionstate', text="Selectable", icon="NONE")
    op.makeSelectable = True

    op = templateSelectableRow.operator('ntz_smrt_frm.changetemplateselectionstate', text="Un-selectable", icon="NONE")
    op.makeSelectable = False

    templatedObjsCol.separator()

    templatedObjsCol.label(text="Templated objects:")

    templatedObjectsSection = templatedObjsCol.row(align=True)
    templatedObjectsSectionCol = templatedObjectsSection.column(align=True)

    numTemplatedObjects = len(scene.ntzSmFrm.templatedObjects)

    boxTemplatedObjects = templatedObjectsSectionCol.box()
    
    objectText = "objects"
    if numTemplatedObjects == 1:
        objectText = "object"
        
    text=f"{numTemplatedObjects} {objectText}."
    boxTemplatedObjects.label(text=text)

    boxCol = boxTemplatedObjects.column(align=True)

    

    if numTemplatedObjects > 0:

        if not scene.ntzSmFrm.hideFullTemplateList:
            row = boxCol.row(align=True)
            row.prop(scene.ntzSmFrm, "hideFullTemplateList", text="Show List", toggle=True)
        else:
            row = boxCol.row(align=True)
            row.prop(scene.ntzSmFrm, "hideFullTemplateList", text="Hide List", toggle=True)

            for item in scene.ntzSmFrm.templatedObjects:
                row = boxCol.row(align=True)

                op = row.operator('ntz_smrt_frm.untemplatespecificobj', text="", icon="X")
                op.objectToUntemplate = item

                op = row.operator('ntz_smrt_frm.selobj', text=item, icon="NONE", emboss=True)
                op.objToSelect = item

                selectState = bpy.data.objects[item]

                row.prop(bpy.data.objects[item], "hide_select", text="", emboss=False, invert_checkbox=True)



    else: 
        row = boxCol.row(align=True)
        row.label(text="None")

    templatedObjectsSectionCol = templatedObjectsSection.column(align=True)

    op = templatedObjectsSectionCol.operator('ntz_smrt_frm.convertobjtotemplate', text="", icon="ADD")

    if scene.ntzSmFrm.defaultTemplateSelectableState == "UNSELECTABLE":
        op.makeSelectable = False
    elif scene.ntzSmFrm.defaultTemplateSelectableState == "SELECTABLE":
        op.makeSelectable = True

    removeOpRow = templatedObjectsSectionCol.row(align=True)
    activeObj = bpy.context.view_layer.objects.active


    if activeObj is None:
        removeOpRow.enabled = False
    op = removeOpRow.operator('ntz_smrt_frm.untemplateobjs', text="", icon="REMOVE")

    op = templatedObjectsSectionCol.operator('ntz_smrt_frm.refreshtemplatedobjlist', text="", icon="FILE_REFRESH")
    op = templatedObjectsSectionCol.operator('ntz_smrt_frm.clearalltemplatedobjs', text="", icon="TRASH")