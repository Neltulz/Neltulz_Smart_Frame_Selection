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

    optionsPopoverEnum : EnumProperty (
        items       = [("OPTIONS", "Options", "", "", 0)],
        name        = "Options Popover Enum",
        description = "Options Popover Enum",
        default     = "OPTIONS"
    )

    frameObjType : EnumProperty (
        items       = [("OBJTYPE", "Object Types", "", "", 0)],
        name        = "Frame Object Types",
        description = "Frame Object Types",
        default     = "OBJTYPE"
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

    hideErrorMessages : BoolProperty(
        name="Hide Error Messages",
        description="Hide Error Messages (Default: False)",
        default = False
    )



    excludedIsolateObjects = set()
    templatedObjects = set()