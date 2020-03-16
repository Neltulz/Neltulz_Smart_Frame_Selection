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

def createProp(self, context, scene, bEnabled, labelText, data, propItem, scale_y, labelWidth, propWidth, labelJustify, propJustify, propText, bExpandProp, bUseSlider, layout):

    propRow = layout.row(align=True)

    if not bEnabled:
        propRow.enabled = False

    propRow.scale_y = scale_y

    propRowLabel = propRow.row(align=True)
    propRowLabel.alignment="EXPAND"
    propRowLabel.ui_units_x = labelWidth

    propRowLabel1 = propRowLabel.row(align=True)
    propRowLabel1.alignment=labelJustify
    propRowLabel1.scale_x = 1

    propRowLabel1.label(text=labelText)

    propRowItem = propRow.row(align=True)
    propRowItem.alignment=propJustify

    propRowItem1 = propRowItem.row(align=True)
    propRowItem1.alignment=propJustify
    propRowItem1.ui_units_x = propWidth
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
    addonPrefs = context.preferences.addons[__package__].preferences

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
    frameIsolateButtons_section(self, context, scene, addonPrefs, panelInsidePopupOrPie, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel, layout)


def frameIsolateButtons_section(self, context, scene, addonPrefs, panelInsidePopupOrPie, bUseCompactSidebarPanel, bUseCompactPopupAndPiePanel, layout):

    compactPanelConditions = (panelInsidePopupOrPie and bUseCompactPopupAndPiePanel) or (not panelInsidePopupOrPie and bUseCompactSidebarPanel)

    if compactPanelConditions:
        frameText = "Frm"
        if addonPrefs.useExtremeHideOnIsolate:
            isolateText = "E-Iso"
            isolateIcon="NONE"
        else:
            isolateText = "Iso"
            isolateIcon="NONE"
        scaleY = 1
        frameAndIsolateText = "Frm+Iso"
        templateText = "Tmplt"
        viewOriginText = "View2Ori"
    else:
        frameText = "Frame"
        if addonPrefs.useExtremeHideOnIsolate:
            isolateText = "Ext Isolate"
            isolateIcon="ERROR"
        else:
            isolateIcon="NONE"
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
    op = frameOpRow.operator('view3d.ntzsf_smart_frame', text=frameText, icon="NONE")
    op.tooltip              = "Frame an object, selection of objects, vertice, edge, face, or when all else fails: frame everything"
    op.frameSelection       = True
    op.isolateSelection     = False
    op.frameMethod          = "SEL"

    framePopoverRow = frameRow.row(align=True)
    popover = framePopoverRow.popover(text="", panel="VIEW3D_PT_ntzsf_frame_options", icon="DOWNARROW_HLT")

    frameAndIsolateRow.separator()

    isolateRow = frameAndIsolateRow.row(align=True)

    if scene.ntzSmFrm.currentlyBusyIsolating:
        isolateText = "Unhide"

    isolateOpRow = isolateRow.row(align=True)
    isolateOpRow.alignment="EXPAND"
    isolateOpRow.scale_x = 100
    op = isolateOpRow.operator('view3d.ntzsf_isolate', text=isolateText, icon=isolateIcon)
    op.tooltip              = "Isolate an object, selection of objects, vertice, edge, face, or when all else fails: isolate everything"
    op.frameSelection       = False
    op.isolateSelection     = True
    op.frameMethod          = "SEL"

    IsolatePopoverRow = isolateRow.row(align=True)
    popover = IsolatePopoverRow.popover(text="", panel="VIEW3D_PT_ntzsf_isolate_options", icon="DOWNARROW_HLT")

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
    op = frameAndIsolateOpRow.operator('view3d.ntzsf_frame_and_isolate', text=frameAndIsolateText)
    op.tooltip              = "Frame and Isolate an object, selection of objects, vertices, edges, or faces, simultaneously, or when all else fails: everything"
    op.frameSelection       = True
    op.isolateSelection     = True
    op.frameMethod          = "SEL"

    frameAndIsolateAndTemplateRow.separator()

    templateRow = frameAndIsolateAndTemplateRow.row(align=True)

    templateOpRow = templateRow.row(align=True)
    templateOpRow.alignment="EXPAND"
    templateOpRow.scale_x = 100

    op = templateOpRow.operator('view3d.ntzsf_toggle_template', text=templateText, icon="NONE")
    op.tooltip = "Converts an object to a wireframe with click-through (unselectable) capability for reference purposes"

    templatePopoverRow = templateRow.row(align=True)
    popover = templatePopoverRow.popover(text="", panel="VIEW3D_PT_ntzsf_tmpl_options", icon="DOWNARROW_HLT")

    layout.separator()


    #Viewport to Origin
    col = layout.column(align=True)
    op = col.operator('view3d.ntzsf_viewport_to_origin', text=viewOriginText)
    op.tooltip              = "Move the viewport to the origin"
    op.frameSelection       = True
    op.isolateSelection     = False
    op.frameMethod          = "ORIGIN"

def frameOptions_sectionInner(self, context, scene, addonPrefs, layout):

    layout.prop(addonPrefs, "bUseSmoothFraming", expand=True)

    layout.separator()

    layout.prop(addonPrefs, "expandSelectedObjsInOutliner", expand=True)

    
    layout.separator()

    layout.label(text="Experimental:")
    row = layout.row(align=True)
    row.enabled = addonPrefs.expandSelectedObjsInOutliner
    row.prop(addonPrefs, "collapseUnselectedObjsInOutliner", expand=True)
    

    layout.separator()

    label = layout.label(text="Calculate Zoom based on:")
    zoomDistanceMethodRow = layout.row(align=True)
    zoomDistanceMethodRow.prop(addonPrefs, "calcZoomDistanceMethod", expand=True)

    layout.separator()

    frameObjType_sectionInner(self, context, scene, addonPrefs, False, layout)

    layout.separator()

    layout.prop(addonPrefs, "useAllRegionsWhenFraming", expand=True)
    layout.prop(addonPrefs, "useAll3DAreasWhenFraming", expand=True)

    layout.separator()

    layout.label(text="Max Vert Limit for Zoom Adjust:")
    layout.prop(addonPrefs, "maxVertAllowanceForZoomAdjust", expand=True)
    layout.prop(addonPrefs, "maxVertSelectionAllowanceForZoomAdjust", expand=True)

        

def isolateOptions_sectionInner(self, context, scene, addonPrefs, layout):

    excludedObjsFromIsolate_sectionInner(self, context, scene, False, layout)

    layout.label(text="On Isolate, hide:")

    row = layout.row(align=True)

    row.prop(addonPrefs, "hideFloorOnIsolate", expand=True, text="Floor", toggle=True, icon="MESH_GRID")

    row.prop(addonPrefs, "hideAxesOnIsolate", expand=True, text="Axes", toggle=True, icon="EMPTY_AXIS")

    layout.separator()

    layout.prop(addonPrefs, "useExtremeHideOnIsolate", expand=True)






def frameObjType_sectionInner(self, context, scene, addonPrefs, bIndent, layout):

    if bIndent:
        row = layout.row(align=True)
        indent = row.column(align=True)
        indent.label(text="", icon="BLANK1")

        frameObjTypeCol = row.column(align=True)
    else:
        frameObjTypeCol = layout

    frameObjTypeCol.label(text="When nothing is selected, frame:")

    grid = frameObjTypeCol.grid_flow(row_major=True, columns=2, align=True)

    for frameObjType in addonPrefs.frameObjTypeList:
        grid.prop(addonPrefs, frameObjType, expand=True, toggle=True)

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

                op = row.operator('view3d.ntzsf_del_obj_from_excluded_isolate_objs', text="", icon="X")
                op.objectToUntemplate = item

                row.label(text=item)



    else: 
        row = boxCol.row(align=True)
        row.label(text="None")

    excludedObjectsSectionCol = excludedObjectsSection.column(align=True)

    op = excludedObjectsSectionCol.operator('view3d.ntzsf_add_obj_to_excluded_isolate_objs', text="", icon="ADD")
    op = excludedObjectsSectionCol.operator('view3d.ntzsf_del_obj_from_excluded_isolate_objs', text="", icon="REMOVE")
    op = excludedObjectsSectionCol.operator('view3d.ntzsf_refresh_excluded_isolate_objs', text="", icon="FILE_REFRESH")
    op = excludedObjectsSectionCol.operator('view3d.ntzsf_clear_all_excluded_isolate_objs', text="", icon="TRASH")


def templateOptions_section(self, context, scene, addonPrefs, bIndent, layout):

    layout.separator()

    if bIndent:
        row = layout.row(align=True)
        indent = row.column(align=True)
        indent.label(text="", icon="BLANK1")

        templatedObjsCol = row.column(align=True)
    else:
        templatedObjsCol = layout

    templatedObjsCol.label(text="Default Template Selectable State")
    prop = templatedObjsCol.prop(addonPrefs, 'defaultTemplateSelectableState', text="", toggle=True)

    templatedObjsCol.separator()

    templateSelectableCol = templatedObjsCol.column(align=True)
    templateSelectableCol.scale_y = 1.25
    templateSelectableCol.label(text="Make All Template Objects:")
    templateSelectableRow = templateSelectableCol.row(align=True)
    op = templateSelectableRow.operator('view3d.ntzsf_change_template_selection_state', text="Selectable", icon="NONE")
    op.makeSelectable = True

    op = templateSelectableRow.operator('view3d.ntzsf_change_template_selection_state', text="Un-selectable", icon="NONE")
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

                op = row.operator('view3d.ntzsf_untemplate_specific_obj', text="", icon="X")
                op.objectToUntemplate = item

                op = row.operator('view3d.ntzsf_sel_obj_by_name', text=item, icon="NONE", emboss=True)
                op.objToSelect = item

                selectState = bpy.data.objects[item]

                row.prop(bpy.data.objects[item], "hide_select", text="", emboss=False, invert_checkbox=True)



    else: 
        row = boxCol.row(align=True)
        row.label(text="None")

    templatedObjectsSectionCol = templatedObjectsSection.column(align=True)

    op = templatedObjectsSectionCol.operator('view3d.ntzsf_convert_obj_to_template', text="", icon="ADD")

    if addonPrefs.defaultTemplateSelectableState == "UNSELECTABLE":
        op.makeSelectable = False
    elif addonPrefs.defaultTemplateSelectableState == "SELECTABLE":
        op.makeSelectable = True

    removeOpRow = templatedObjectsSectionCol.row(align=True)
    activeObj = bpy.context.view_layer.objects.active


    if activeObj is None:
        removeOpRow.enabled = False
    op = removeOpRow.operator('view3d.ntzsf_untemplate_objs', text="", icon="REMOVE")

    op = templatedObjectsSectionCol.operator('view3d.ntzsf_refresh_template_objs', text="", icon="FILE_REFRESH")
    op = templatedObjectsSectionCol.operator('view3d.ntzsf_clear_all_template_objs', text="", icon="TRASH")