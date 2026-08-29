import bpy
from ..core.translation import T, T_static
from ..ops.demo_character import is_demo_character_present


class REBOCAP_PT_demo_character_panel(bpy.types.Panel):
    bl_idname = "REBOCAP_PT_demo_character_panel"
    bl_label = " "
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "REBOCAP CONNECTION"
    bl_order = 7

    def draw_header(self, context):
        self.layout.label(text=T("示范角色 (Demo Character)"))

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        has_char = is_demo_character_present()

        # Action button
        if has_char:
            row_btn = layout.row(align=True)
            row_btn.alert = True
            row_btn.operator("rebocap.toggle_demo_character", text=T("移除示范角色"), icon='TRASH')
            row_btn.alert = False
        else:
            row_btn = layout.row(align=True)
            row_btn.operator("rebocap.toggle_demo_character", text=T("导入示范角色"), icon='IMPORT')
