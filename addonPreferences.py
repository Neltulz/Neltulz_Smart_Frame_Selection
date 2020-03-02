# Update "Tab Category Name" inspired by "Meta-Androcto's" "Edit Mesh Tools" Add-on
# recommended by "cytoo"

import bpy
from . panels  import VIEW3D_PT_ntzsf_sb_panel
from .         import miscLay

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# Define Panel classes for updating
panels = (
        VIEW3D_PT_ntzsf_sb_panel,
        )

        

def update_panel(self, context):

    sidebarPanelSize_PropVal        = context.preferences.addons[__package__].preferences.sidebarPanelSize
    category_PropVal                = context.preferences.addons[__package__].preferences.category
    popupAndPiePanelSize_PropVal    = context.preferences.addons[__package__].preferences.popupAndPiePanelSize

    message = "Neltulz - Smart Frame: Updating Panel locations has failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        #Whatever the user typed into the text box in the add-ons settings, set that as the addon's tab category name
        for panel in panels:
            
            if sidebarPanelSize_PropVal == "HIDE":
                panel.bl_category = ""
                panel.bl_region_type = "WINDOW"

            else:
                if self.sidebarPanelSize == "DEFAULT":
                    panel.bUseCompactSidebarPanel = False
                else:
                    panel.bUseCompactSidebarPanel = True

                panel.bl_category = category_PropVal
                panel.bl_region_type = "UI"

            if self.popupAndPiePanelSize == "DEFAULT":
                panel.bUseCompactPopupAndPiePanel = False
            else:
                panel.bUseCompactPopupAndPiePanel = True

            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__package__, message, e))
        pass


class VIEW3D_OT_ntzsf_addon_prefs(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    navTabs_List = [
        ("UILAY",      "UI Layout",  "", "", 0),
        ("FRAME",      "Frame",      "", "", 1),
        ("ISO",        "Isolate",    "", "", 2),
        ("TMPL",       "Template",   "", "", 3),
    ]

    navTabs : EnumProperty (
        items       = navTabs_List,
        name        = "Navigation Tabs",
        default     = "FRAME"
    )

    category: StringProperty(
        name="Tab Category",
        description="Choose a name for the category of the panel",
        default="Neltulz",
        update=update_panel,
    )
        
    sidebarpanelSize_List = [
        ("DEFAULT", "Default", "", "", 0),
        ("COMPACT", "Compact", "", "", 1),
        ("HIDE",    "Hide",    "", "", 2),
    ]

    popupAndPiePanelSize_List = [
        ("DEFAULT", "Default", "", "", 0),
        ("COMPACT", "Compact", "", "", 1),
    ]

    sidebarPanelSize : EnumProperty (
        items       = sidebarpanelSize_List,
        name        = "Sidebar Panel Size",
        description = "Sidebar Panel Size",
        default     = "DEFAULT",
        update=update_panel,
    )

    popupAndPiePanelSize : EnumProperty (
        items       = popupAndPiePanelSize_List,
        name        = "Popup & Pie Panel Size",
        description = "Popup & Pie Panel Size",
        default     = "COMPACT",
        update=update_panel,
    )

    # -----------------------------------------------------------------------------
    #    Frame
    # -----------------------------------------------------------------------------

    bUseSmoothFraming : BoolProperty (
        name="Smoothly Frame",
        default = True,
    )

    calcZoomDistanceMethod_List = [
        ("MIN", "Min", "Get the minimum length of the bounding box axes (or in the case of single vertice selection, only the closest vertice(s) will be framed)",                                                                 "", 0),
        ("AVG", "Avg", "Get the average length of the bounding box axes (or in the case of single vertice selection, framing will be based on the average distance of all adjacent vertices.  Some vertices may not be framed)",   "", 1),
        ("MAX", "Max", "Get the maximum length of the bounding box axes (or in the case of single vertice selection: All adjacent vertices will be framed)",                                                                       "", 2),
    ]


    calcZoomDistanceMethod : EnumProperty (
        items       = calcZoomDistanceMethod_List,
        name        = "Zoom Distance Calculation Method",
        default     = "AVG"
    )

    frameObjTypeList = ["frameMesh", "frameCurve", "frameSurface", "frameMeta", "frameText", "frameGreasePen", "frameArmature", "frameLattice", "frameEmpty", "frameLight", "frameLightProbe", "frameCamera", "frameSpeaker"]

    frameObjTypeList2 = {
        'MESH':         'frameMesh',
        'CURVE':        'frameCurve',
        'SURFACE':      'frameSurface',
        'META':         'frameMeta',
        'FONT':         'frameText',
        'GPENCIL':      'frameGreasePen',
        'ARMATURE':     'frameArmature',
        'LATTICE':      'frameLattice',
        'EMPTY':        'frameEmpty',
        'LIGHT':        'frameLight',
        'LIGHTPROBE':   'frameLightProbe',
        'CAMERA':       'frameCamera',
        'SPEAKER':      'frameSpeaker',
    }

    frameMesh : BoolProperty(
        name="Mesh",
        description="Frame Mesh (Default: True)",
        default = True
    )

    frameCurve : BoolProperty(
        name="Curve",
        description="Frame Curve (Default: True)",
        default = True
    )

    frameSurface : BoolProperty(
        name="Surface",
        description="Frame Surface (Default: True)",
        default = True
    )

    frameMeta : BoolProperty(
        name="Meta",
        description="Frame Meta (Default: True)",
        default = True
    )

    frameText : BoolProperty(
        name="Text",
        description="Frame Text (Default: True)",
        default = True
    )

    frameGreasePen : BoolProperty(
        name="GreasePen",
        description="Frame GreasePen (Default: True)",
        default = True
    )

    frameArmature : BoolProperty(
        name="Armature",
        description="Frame Armature (Default: True)",
        default = True
    )

    frameLattice : BoolProperty(
        name="Lattice",
        description="Frame Lattice (Default: True)",
        default = True
    )

    frameEmpty : BoolProperty(
        name="Empty",
        description="Frame Empty (Default: True)",
        default = True
    )

    frameLight : BoolProperty(
        name="Light",
        description="Frame Light (Default: True)",
        default = False
    )

    frameLightProbe : BoolProperty(
        name="LightProbe",
        description="Frame LightProbe (Default: True)",
        default = True
    )

    frameCamera : BoolProperty(
        name="Camera",
        description="Frame Camera (Default: True)",
        default = True
    )

    frameSpeaker : BoolProperty(
        name="Speaker",
        description="Frame Speaker (Default: True)",
        default = True
    )

    useAllRegionsWhenFraming : BoolProperty(
        name="Use all Regions when Framing",
        description="When framing an object, all regions will frame the object.  This is useful if you use Quad view. (Default: True)",
        default = True
    )

    useAll3DAreasWhenFraming : BoolProperty(
        name="Use all 3D Areas when Framing",
        description="When framing an object, all 3D Areas will frame the object.  This is useful if you use multiple 3D Views. (Default: True)",
        default = True
    )

    #Updated by "Frame", "Isolate" and, "Frame & Isolate" operators at end of execute, and fetched by the operator on invoke
    use_zoomAdjust : BoolProperty (default=True)
    zoomAdjust : FloatProperty(default=0)


    maxVertAllowanceForZoomAdjust : IntProperty (
        name="Total",
        description="Maximum number of vertices a mesh can have in order to to use Zoom Adjust.  This is a performance setting.  Setting this number too high can result in program slowness and instability.  Recommended: 1 million or less",
        default = 1000000
    )

    maxVertSelectionAllowanceForZoomAdjust : IntProperty (
        name="Selected",
        description='Maximum number of vertices a mesh can have "Selected" in order to to use Zoom Adjust.  This is a performance setting.  Setting this number too high can result in program slowness and instability.  Recommended: 10,000 or less',
        default = 10000
    )

    # -----------------------------------------------------------------------------
    #    Isolate
    # -----------------------------------------------------------------------------

    hideFloorOnIsolate : BoolProperty(
        name="Hide Floor on Isolate",
        description="Hides the floor when you isolate an object. (Default: True)",
        default = True
    )

    hideAxesOnIsolate : BoolProperty(
        name="Hide Axes on Isolate",
        description="Hides the axes when you isolate an object. (Default: True)",
        default = True
    )

    useExtremeHideOnIsolate : BoolProperty(
        name="Use Extreme Isolate (Use Caution)",
        description='Sets "Show in Viewports" to "False" to grant a super performance increase.  Useful for adding objects to the scene and adjusting operator properties with minimal performance lag. (Default: False)',
        default = False
    )

    # -----------------------------------------------------------------------------
    #    Template   
    # -----------------------------------------------------------------------------

    defaultTemplateSelectableState_List = [
        ("UNSET",        "Unset (Use Last Known)",         "", "",                    0),
        ("UNSELECTABLE", "Un-selectable",                  "", "RESTRICT_SELECT_ON",  1),
        ("SELECTABLE",   "Selectable",                     "", "RESTRICT_SELECT_OFF", 2),
    ]

    defaultTemplateSelectableState : EnumProperty (
        items       = defaultTemplateSelectableState_List,
        name        = "Default Template Selectable State",
        description = "Default Selectable Method for new Template Objects",
        default     = "UNSELECTABLE"
    )

    def draw(self, context):

        lay = self.layout.column(align=True)



        if self.sidebarPanelSize == "HIDE":
            bTabCatEnabled = False
        else:
            bTabCatEnabled = True

        navRow = lay.row(align=True)
        navRow.scale_y = 1.25
        navRow.prop(self, 'navTabs', expand=True)


        box = lay.box()

        labelJustify = "RIGHT"
        
        propJustify = "LEFT"

        if self.navTabs == "UILAY":
            propHeight = 1
            labelWidth = 7
            propWidth = 15

            miscLay.createProp(self, context, None, True,           "Sidebar Panel",                      self, "sidebarPanelSize",      propHeight, labelWidth, propWidth, labelJustify, propJustify, None,  True, False, box)
            miscLay.createProp(self, context, None, bTabCatEnabled, "Tab Category",                       self, "category",              propHeight, labelWidth, propWidth, labelJustify, propJustify, "",    True, False, box)
            miscLay.createProp(self, context, None, True,           "Popup & Pie Panel",                  self, "popupAndPiePanelSize",  propHeight, labelWidth, propWidth, labelJustify, propJustify, None,  True, False, box)

        elif self.navTabs == "FRAME":
            propHeight = 1
            labelWidth = 7
            propWidth = 15
            
            miscLay.createProp(self, context, None, True,           "",                                   self, "bUseSmoothFraming",     propHeight, labelWidth, propWidth, labelJustify, propJustify, None,  True, False, box)
            

            
            # calcZoomDistanceMethod prop
            #-----------------------------------------------------------------------------------------------------------
            row = box.row(align=True)

            col1MasterContainer = row.row(align=True)
            col1MasterContainer.alignment="EXPAND"
            col1MasterContainer.ui_units_x = labelWidth

            col1Container = col1MasterContainer.column(align=True)
            col1Container.alignment=labelJustify
            col1Container.scale_x = 1
            col1Container.scale_y = 0.75

            col1Container.separator(factor=0.75)
            col1Container.label(text='Calculate Zoom')

            col2MasterContainer = row.row(align=True)
            col2MasterContainer.alignment=propJustify

            col2Container = col2MasterContainer.column(align=True)
            col2Container.alignment=propJustify
            col2Container.ui_units_x = propWidth
            col2Container.scale_x = 100

            propRow = col2Container.row(align=True)
            propRow.prop(self, "calcZoomDistanceMethod", expand=True)

            # When nothing is selected, frame:
            #-----------------------------------------------------------------------------------------------------------
            row = box.row(align=True)

            col1MasterContainer = row.row(align=True)
            col1MasterContainer.alignment="EXPAND"
            col1MasterContainer.ui_units_x = labelWidth

            col1Container = col1MasterContainer.column(align=True)
            col1Container.alignment=labelJustify
            col1Container.scale_x = 1
            col1Container.scale_y = 0.75

            col1Container.separator(factor=0.75)
            col1Container.label(text='When nothing is')
            col1Container.label(text='selected, frame:')

            col2MasterContainer = row.row(align=True)
            col2MasterContainer.alignment=propJustify

            col2Container = col2MasterContainer.column(align=True)
            col2Container.alignment=propJustify
            col2Container.ui_units_x = propWidth
            col2Container.scale_x = 100

            propGrid = col2Container.grid_flow(row_major=True, columns=2, align=True)

            for frameObjType in self.frameObjTypeList:
                propGrid.prop(self, frameObjType, expand=True, toggle=True)

            # When framing, use all:
            #-----------------------------------------------------------------------------------------------------------
            row = box.row(align=True)

            col1MasterContainer = row.row(align=True)
            col1MasterContainer.alignment="EXPAND"
            col1MasterContainer.ui_units_x = labelWidth

            col1Container = col1MasterContainer.column(align=True)
            col1Container.alignment=labelJustify
            col1Container.scale_x = 1
            col1Container.scale_y = 0.75

            col1Container.separator(factor=0.75)
            col1Container.label(text='When framing,')
            col1Container.label(text='use all:')

            col2MasterContainer = row.row(align=True)
            col2MasterContainer.alignment=propJustify

            col2Container = col2MasterContainer.column(align=True)
            col2Container.alignment=propJustify
            col2Container.ui_units_x = propWidth
            col2Container.scale_x = 100

            col2Container.separator(factor=1)

            propRow = col2Container.row(align=True)
            
            propRow.prop(self, "useAllRegionsWhenFraming", toggle=True, text="Regions")          
            propRow.prop(self, "useAll3DAreasWhenFraming", toggle=True, text="3D Areas")

            # Max Allowable Total Verts:
            #-----------------------------------------------------------------------------------------------------------
            row = box.row(align=True)

            col1MasterContainer = row.row(align=True)
            col1MasterContainer.alignment="EXPAND"
            col1MasterContainer.ui_units_x = labelWidth

            col1Container = col1MasterContainer.column(align=True)
            col1Container.alignment=labelJustify
            col1Container.scale_x = 1
            col1Container.scale_y = 0.75

            col1Container.separator(factor=2.5)
            col1Container.label(text='Max Vert Limit')
            col1Container.label(text='for Zoom Adjust:')

            col2MasterContainer = row.row(align=True)
            col2MasterContainer.alignment=propJustify

            col2Container = col2MasterContainer.column(align=True)
            col2Container.alignment=propJustify
            col2Container.ui_units_x = propWidth
            col2Container.scale_x = 100

            col2Container.separator(factor=1)

            propRow = col2Container.column(align=True)
            
            propRow.prop(self, "maxVertAllowanceForZoomAdjust")
            propRow.prop(self, "maxVertSelectionAllowanceForZoomAdjust")





        elif self.navTabs == "ISO":
            propHeight = 1
            labelWidth = 7
            propWidth = 15

            floorAxesRow = box.row(align=True)

            labelRow = floorAxesRow.row(align=True)
            labelRow.scale_y = propHeight
            labelRow.alignment="EXPAND"
            labelRow.ui_units_x = labelWidth

            labelRow2 = labelRow.row(align=True)
            labelRow2.alignment=labelJustify
            labelRow2.scale_x = 1
            
            labelRow2.label(text='On Isolate, hide:')

            propRow = floorAxesRow.row(align=True)
            propRow.scale_x = 150
            propRow.ui_units_x = propWidth
            propRow.alignment = propJustify

            propRow.scale_y = propHeight

            propRow.prop(self, 'hideFloorOnIsolate', text="Floor", toggle=False, icon="MESH_GRID")

            propRow.prop(self, 'hideAxesOnIsolate',  text="Axes", toggle=False, icon="EMPTY_AXIS")


            miscLay.createProp(self, context, None, True,           "",                                    self, "useExtremeHideOnIsolate",  propHeight, labelWidth, propWidth, labelJustify, propJustify, None,  True, False, box)

        elif self.navTabs == "TMPL":
            propHeight = 1
            labelWidth = 7
            propWidth = 15
            
            # calcZoomDistanceMethod prop
            #-----------------------------------------------------------------------------------------------------------
            row = box.row(align=True)

            col1MasterContainer = row.row(align=True)
            col1MasterContainer.alignment="EXPAND"
            col1MasterContainer.ui_units_x = labelWidth

            col1Container = col1MasterContainer.column(align=True)
            col1Container.alignment=labelJustify
            col1Container.scale_x = 1
            col1Container.scale_y = 0.75

            col1Container.separator(factor=0.75)
            col1Container.label(text='Default Template')
            col1Container.label(text='Selectable State:')

            col2MasterContainer = row.row(align=True)
            col2MasterContainer.alignment=propJustify


            col2Container = col2MasterContainer.column(align=True)
            
            col2Container.separator(factor=1)

            col2Container.alignment=propJustify
            col2Container.ui_units_x = propWidth
            col2Container.scale_x = 100

            propRow = col2Container.row(align=True)
            
            propRow.prop(self, "defaultTemplateSelectableState", expand=False, text="")