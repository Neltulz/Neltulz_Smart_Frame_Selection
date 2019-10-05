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

    advancedSettings : BoolProperty(
        name="Checkbox Name",
        description="Use advanced settings (Default: False)",
        default = False
        #update=neltulzSubD_useAdvancedSettings_toggled
    )

    frameOnlyMesh : BoolProperty(
        name="Frame Only Mesh Objects",
        description="Frame only mesh objects when nothing in the scene is selected (Default: True)",
        default = True
    )

    frameMesh : BoolProperty(
        name="Frame Mesh",
        description="Frame Mesh (Default: True)",
        default = True
    )

    frameCurve : BoolProperty(
        name="Frame Curve",
        description="Frame Curve (Default: True)",
        default = True
    )

    frameSurface : BoolProperty(
        name="Frame Surface",
        description="Frame Surface (Default: True)",
        default = True
    )

    frameMeta : BoolProperty(
        name="Frame Meta",
        description="Frame Meta (Default: True)",
        default = True
    )

    frameText : BoolProperty(
        name="Frame Text",
        description="Frame Text (Default: True)",
        default = True
    )

    frameGreasePen : BoolProperty(
        name="Frame GreasePen",
        description="Frame GreasePen (Default: True)",
        default = True
    )

    frameArmature : BoolProperty(
        name="Frame Armature",
        description="Frame Armature (Default: True)",
        default = True
    )

    frameLattice : BoolProperty(
        name="Frame Lattice",
        description="Frame Lattice (Default: True)",
        default = True
    )

    frameEmpty : BoolProperty(
        name="Frame Empty",
        description="Frame Empty (Default: True)",
        default = True
    )

    frameLight : BoolProperty(
        name="Frame Light",
        description="Frame Light (Default: True)",
        default = True
    )

    frameLightProbe : BoolProperty(
        name="Frame LightProbe",
        description="Frame LightProbe (Default: True)",
        default = True
    )

    frameCamera : BoolProperty(
        name="Frame Camera",
        description="Frame Camera (Default: True)",
        default = True
    )

    frameSpeaker : BoolProperty(
        name="Frame Speaker",
        description="Frame Speaker (Default: True)",
        default = True
    )

    currentlyBusyIsolating : BoolProperty(
        name="Currently Busy Isolating",
        description="Currently busy isolating (Default: False)",
        default = False
    )

    excludedIsolateObjects = set()