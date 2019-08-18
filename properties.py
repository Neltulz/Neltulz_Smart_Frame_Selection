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
        description="Default: Off: Use advanced settings",
        default = False
        #update=neltulzSubD_useAdvancedSettings_toggled
    )