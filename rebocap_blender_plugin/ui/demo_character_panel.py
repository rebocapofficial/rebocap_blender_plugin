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
        self.layout.label(text=T("官方示范角色 (Official Demo Character)"), icon='COMMUNITY')

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        has_char = is_demo_character_present()

        box = layout.box()

        # Status row
        if has_char:
            row_stat = box.row(align=True)
            row_stat.label(text="● 示范角色已载入 (在场中)", icon='CHECKMARK')
            
            # Action button: Remove
            row_btn = box.row(align=True)
            row_btn.alert = True
            row_btn.operator("rebocap.toggle_demo_character", text=T("移除官方示范角色"), icon='TRASH')
            row_btn.alert = False
        else:
            row_stat = box.row(align=True)
            row_stat.label(text="开箱即用的官方标准伴随角色", icon='INFO')
            
            # Action button: Import
            row_btn = box.row(align=True)
            row_btn.operator("rebocap.toggle_demo_character", text=T("导入官方示范角色"), icon='IMPORT')

        # Offset settings
        box_pos = layout.box()
        box_pos.label(text=T("站位设置 (Position Preset):"))
        row_pos = box_pos.row(align=True)
        row_pos.prop(scene, "rebocap_demo_preset", expand=True)

        col_desc = layout.column(align=True)
        col_desc.label(text="💡 提示: 示范角色仅用于视口实时伴随，", icon='LIGHT')
        col_desc.label(text="   录制时不会向历史列表生成多余切片。")
