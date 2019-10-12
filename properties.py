import bpy
from . import misc_functions

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

class NeltulzSmartFrameSel_IgnitProperties(bpy.types.PropertyGroup):

    useAdvancedSettings : BoolProperty(
        name="Use Advanced Settings",
        description="Use advanced settings (Default: False)",
        default = False
        #update=neltulzSubD_useAdvancedSettings_toggled
    )

    use_all_regions_when_framing : BoolProperty(
        name="Use all Regions when Framing",
        description="When framing an object, all regions will frame the object.  This is useful if you use Quad view. (Default: True)",
        default = True
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

    hideErrorMessages : BoolProperty(
        name="Hide Error Messages",
        description="Hide Error Messages (Default: False)",
        default = False
    )



    excludedIsolateObjects = set()
    templatedObjects = set()