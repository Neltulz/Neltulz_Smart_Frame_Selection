import bpy
from . properties import NeltulzSmartFrameSel_IgnitProperties
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

# -----------------------------------------------------------------------------
#   Panel
# ----------------------------------------------------------------------------- 

class OBJECT_PT_NeltulzSmartFrameSel(Panel):

    bl_idname = "object.neltulz_smart_frame_sel_panel"
    bl_label = "Smart Frame Selection v1.0.2"
    bl_category = "Neltulz - Smart Frame Selection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        #todo - make panel stuff later!
        pass