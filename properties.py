import bpy
from . import misc_functions

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)


class NTZSMFRM_ignitproperties(bpy.types.PropertyGroup):

    preventInfiniteRecursion : BoolProperty (
        name="Prevent Infinite Recursion",
        description="Reveals options.",
        default = False,
    )

    bShowOptions : BoolProperty (
        name="Show Options",
        description="Reveals options.",
        default = False,
    )

    bUseSmoothFraming : BoolProperty (
        name="Smoothly Frame",
        default = True,
    )

    bShowFrameObjTypes : BoolProperty (
        name="Show Frame Object Types",
        description="Show Frame Object Types.",
        default = True,
    )

    bShowExcludedObjFromIsolateTypes : BoolProperty (
        name="Show Excluded Object From Isolate Types",
        description="Show Excluded Object From Isolate Types.",
        default = True,
    )

    bShowTemplatedObjs : BoolProperty (
        name="Show Templated Objects",
        description="Show Templated Objects",
        default = True,
    )

    useAdvancedSettings : BoolProperty(
        name="Use Advanced Settings",
        description="Use advanced settings (Default: False)",
        default = False
    )

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

    optionsPopoverEnum : EnumProperty (
        items       = [("OPTIONS", "Options", "", "", 0)],
        name        = "Options Popover Enum",
        description = "Options Popover Enum",
        default     = "OPTIONS"
    )

    frameObjTypeList = ["frameMesh", "frameCurve", "frameSurface", "frameMeta", "frameText", "frameGreasePen", "frameArmature", "frameLattice", "frameEmpty", "frameLight", "frameLightProbe", "frameCamera", "frameSpeaker"]

    frameObjType : EnumProperty (
        items       = [("OBJTYPE", "Object Types", "", "", 0)],
        name        = "Frame Object Types",
        description = "Frame Object Types",
        default     = "OBJTYPE"
    )

    use_all_regions_when_framing : BoolProperty(
        name="Use all Regions when Framing",
        description="When framing an object, all regions will frame the object.  This is useful if you use Quad view. (Default: True)",
        default = True
    )

    use_all_3d_areas_when_framing : BoolProperty(
        name="Use all 3D Areas when Framing",
        description="When framing an object, all 3D Areas will frame the object.  This is useful if you use multiple 3D Views. (Default: True)",
        default = True
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

    showFrameList : BoolProperty(
        name="Show Frame List",
        description="Show Full list of object types that will be framed when nothing is selected (Default: False)",
        default = False
    )

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
        default = True
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

    currentlyBusyIsolating : BoolProperty(
        name="Currently Busy Isolating",
        description="Currently busy isolating (Default: False)",
        default = False
    )

    hideFullIsolateExclusionList : BoolProperty(
        name="Hide All",
        description="Hide the entire list of excluded objects from isolate",
        default = True
    )

    hideFullTemplateList : BoolProperty(
        name="Hide All",
        description="Hide the entire list of templated objects",
        default = True
    )


    floorWasPreviouslyVisible : BoolProperty(
        name="Previous Floor Visibility",
        description="Floor was visible before user entered isolate mode (Default: False)",
        default = False
    )

    hideFloorOnIsolate : BoolProperty(
        name="Hide Floor on Isolate",
        description="Hides the floor when you isolate an object. (Default: True)",
        default = True
    )

    axis_x_wasPreviouslyVisible : BoolProperty(
        name="Previous X Axis Visibility",
        description="X Axis was visible before user entered isolate mode (Default: False)",
        default = False
    )

    axis_y_wasPreviouslyVisible : BoolProperty(
        name="Previous Y Axis Visibility",
        description="Y Axis was visible before user entered isolate mode (Default: False)",
        default = False
    )

    axis_z_wasPreviouslyVisible : BoolProperty(
        name="Previous Z Axis Visibility",
        description="Z Axis was visible before user entered isolate mode (Default: False)",
        default = False
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

    hideErrorMessages : BoolProperty(
        name="Hide Error Messages",
        description="Hide Error Messages (Default: False)",
        default = False
    )



    excludedIsolateObjects = set()
    templatedObjects = set()