import bpy
from ..core.translation import T, T_static
from ..ops.demo_character import is_demo_character_present, get_demo_character_armature


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

            # Horizontal Offset Buttons
            box = layout.box()
            box.label(text=T("水平偏开位置:"), icon='SNAP_NORMAL')
            
            row_fixed = box.row(align=True)
            op = row_fixed.operator("rebocap.offset_demo_character", text=T("左 2m"))
            op.mode = 'SET'
            op.offset_x = -2.0

            op = row_fixed.operator("rebocap.offset_demo_character", text=T("居中"))
            op.mode = 'SET'
            op.offset_x = 0.0

            op = row_fixed.operator("rebocap.offset_demo_character", text=T("右 2m"))
            op.mode = 'SET'
            op.offset_x = 2.0

            row_step = box.row(align=True)
            op = row_step.operator("rebocap.offset_demo_character", text=T("-1m 步进"))
            op.mode = 'ADD'
            op.offset_x = -1.0

            op = row_step.operator("rebocap.offset_demo_character", text=T("+1m 步进"))
            op.mode = 'ADD'
            op.offset_x = 1.0
        else:
            row_btn = layout.row(align=True)
            row_btn.operator("rebocap.toggle_demo_character", text=T("导入示范角色"), icon='IMPORT')

        # Medium-gray entertainment note at the bottom
        col_note = layout.column(align=True)
        col_note.enabled = False
        col_note.label(text=T("注：示范角色为娱乐预览功能，非实机绑定。"), icon='INFO')

