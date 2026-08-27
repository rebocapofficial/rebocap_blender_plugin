import bpy
from ..core.translation import T, T_static


class REBOCAP_OT_puppet_mapper(bpy.types.Operator):
    bl_idname = "rebocap.open_puppet_mapper"
    bl_label = T_static("Rebocap 人偶骨骼映射器 (Puppet Bone Mapper)")
    bl_description = T_static("Rebocap 人偶骨骼映射器 (Puppet Bone Mapper)")
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=720)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rebocap_bone_map = getattr(scene, 'rebocap_bone_map', None)
        source = bpy.data.objects.get(scene.rebocap_source_armature)
        
        # 左右双分栏：左侧人偶画布拓扑，右侧映射清单与模板
        split = layout.split(factor=0.46, align=True)
        
        # ================= 左侧：人偶画布 (Rebocap Skeleton View) =================
        box_left = split.box()
        col_left = box_left.column(align=True)
        
        row_title = col_left.row(align=True)
        row_title.label(text=T("Rebocap 人偶画布 (Skeleton View)"), icon='USER')
        
        col_left.separator()
        
        # 1. 头部与颈部
        row_head = col_left.row(align=True)
        self._draw_slot_button(row_head, rebocap_bone_map, 15, "Head", "👤 Head")
        
        row_neck = col_left.row(align=True)
        self._draw_slot_button(row_neck, rebocap_bone_map, 12, "Neck", "👔 Neck")
        
        col_left.separator()
        # 2. 躯干与双臂
        row_clav = col_left.row(align=True)
        self._draw_slot_button(row_clav, rebocap_bone_map, 13, "L_Shoulder", "L_Clav")
        self._draw_slot_button(row_clav, rebocap_bone_map, 9, "UpChest", "🫁 UpChest")
        self._draw_slot_button(row_clav, rebocap_bone_map, 14, "R_Shoulder", "R_Clav")
        
        row_arm = col_left.row(align=True)
        self._draw_slot_button(row_arm, rebocap_bone_map, 16, "L_UpArm", "L_UpArm")
        self._draw_slot_button(row_arm, rebocap_bone_map, 6, "Chest", "🫀 Chest")
        self._draw_slot_button(row_arm, rebocap_bone_map, 17, "R_UpArm", "R_UpArm")
        
        row_elbow = col_left.row(align=True)
        self._draw_slot_button(row_elbow, rebocap_bone_map, 18, "L_DownArm", "L_Elbow")
        self._draw_slot_button(row_elbow, rebocap_bone_map, 3, "Spine", "🦴 Spine")
        self._draw_slot_button(row_elbow, rebocap_bone_map, 19, "R_DownArm", "R_Elbow")
        
        row_hand = col_left.row(align=True)
        self._draw_slot_button(row_hand, rebocap_bone_map, 20, "L_Palm", "L_Hand")
        self._draw_slot_button(row_hand, rebocap_bone_map, 0, "Pelvis", "👖 Pelvis")
        self._draw_slot_button(row_hand, rebocap_bone_map, 21, "R_Palm", "R_Hand")
        
        col_left.separator()
        # 3. 下半身双腿与脚踝
        row_upleg = col_left.row(align=True)
        self._draw_slot_button(row_upleg, rebocap_bone_map, 1, "L_UpLeg", "🦵 L_UpLeg")
        self._draw_slot_button(row_upleg, rebocap_bone_map, 2, "R_UpLeg", "🦵 R_UpLeg")
        
        row_knee = col_left.row(align=True)
        self._draw_slot_button(row_knee, rebocap_bone_map, 4, "L_DownLeg", "🦵 L_Knee")
        self._draw_slot_button(row_knee, rebocap_bone_map, 5, "R_DownLeg", "🦵 R_Knee")
        
        row_foot = col_left.row(align=True)
        self._draw_slot_button(row_foot, rebocap_bone_map, 7, "L_Foot", "🦶 L_Foot")
        self._draw_slot_button(row_foot, rebocap_bone_map, 8, "R_Foot", "🦶 R_Foot")
        
        row_toe = col_left.row(align=True)
        self._draw_slot_button(row_toe, rebocap_bone_map, 10, "L_Toe", "🦶 L_Toe")
        self._draw_slot_button(row_toe, rebocap_bone_map, 11, "R_Toe", "🦶 R_Toe")
        
        col_left.separator()
        col_tip = col_left.column(align=True)
        col_tip.enabled = False
        col_tip.label(text="💡 在3D视口选中骨骼后，", icon='INFO')
        col_tip.label(text="   点击人偶插槽一键映射绑定")
        
        # ================= 右侧：骨骼表单与模板 (FK Bone Definition) =================
        box_right = split.box()
        col_right = box_right.column(align=True)
        
        row_src = col_right.row(align=True)
        row_src.label(text=T("Source:"), icon='ARMATURE_DATA')
        row_src.prop_search(scene, 'rebocap_source_armature', scene, 'objects', text='')
        
        row_act = col_right.row(align=True)
        row_act.operator('rebocap.auto_map_bone', text=T('Auto Detect'), icon='BONE_DATA')
        row_act.operator('rebocap.clear_all_bone_map', text=T('清空全部'), icon='X')
        
        col_right.separator()
        col_right.label(text=T("FK 骨骼映射清单 (FK Definition):"), icon='ALIGN_JUSTIFY')
        
        # 中轴骨骼
        center_bones = [(0, "Pelvis"), (3, "Spine"), (6, "Chest"), (9, "UpChest"), (12, "Neck"), (15, "Head")]
        for node_i, b_label in center_bones:
            row_b = col_right.row(align=True)
            row_b.label(text=b_label)
            if source and source.type == 'ARMATURE':
                row_b.prop_search(rebocap_bone_map, f'node_{node_i}', source.pose, 'bones', text='')
            else:
                row_b.prop(rebocap_bone_map, f'node_{node_i}', text='')
            row_b.operator("object.pick_bone", text="", icon='RESTRICT_SELECT_OFF').bone_type = f'node_{node_i}'
            
        col_right.separator()
        # 四肢左右对照
        side_bones = [
            (1, 2, "UpLeg"), (4, 5, "DownLeg"), (7, 8, "Foot"), (10, 11, "Toe"),
            (13, 14, "Shoulder"), (16, 17, "UpArm"), (18, 19, "DownArm"), (20, 21, "Palm")
        ]
        row_lr_head = col_right.row(align=True)
        row_lr_head.label(text=T("四肢对称映射:"))
        row_lr_head.label(text=T("Left (左)"))
        row_lr_head.label(text=T("Right (右)"))
        for l_i, r_i, s_name in side_bones:
            row_s = col_right.row(align=True)
            row_s.label(text=s_name)
            # Left
            if source and source.type == 'ARMATURE':
                row_s.prop_search(rebocap_bone_map, f'node_{l_i}', source.pose, 'bones', text='')
            else:
                row_s.prop(rebocap_bone_map, f'node_{l_i}', text='')
            row_s.operator("object.pick_bone", text="", icon='RESTRICT_SELECT_OFF').bone_type = f'node_{l_i}'
            # Right
            if source and source.type == 'ARMATURE':
                row_s.prop_search(rebocap_bone_map, f'node_{r_i}', source.pose, 'bones', text='')
            else:
                row_s.prop(rebocap_bone_map, f'node_{r_i}', text='')
            row_s.operator("object.pick_bone", text="", icon='RESTRICT_SELECT_OFF').bone_type = f'node_{r_i}'

    def _draw_slot_button(self, layout, bone_map, node_idx, prop_name, display_label):
        val = getattr(bone_map, f"node_{node_idx}", "") if bone_map else ""
        is_mapped = bool(val and val.strip())
        
        icon_name = 'CHECKMARK' if is_mapped else 'RADIOBUT_OFF'
        short_val = val.split(':')[-1] if ':' in val else val
        btn_text = f"{display_label}: {short_val}" if is_mapped else f"{display_label}"
        
        row = layout.row(align=True)
        row.operator("object.pick_bone", text=btn_text, icon=icon_name, depress=is_mapped).bone_type = f"node_{node_idx}"

    def execute(self, context):
        self.report({'INFO'}, "FK 骨骼映射已保存")
        return {'FINISHED'}


class REBOCAP_OT_clear_all_bone_map(bpy.types.Operator):
    bl_idname = "rebocap.clear_all_bone_map"
    bl_label = T_static("清空全部骨骼映射")
    bl_description = T_static("清空全部骨骼映射")
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bone_map = getattr(context.scene, 'rebocap_bone_map', None)
        if bone_map:
            for i in range(24):
                if hasattr(bone_map, f"node_{i}"):
                    setattr(bone_map, f"node_{i}", "")
        self.report({'INFO'}, "已清空全部骨骼映射")
        return {'FINISHED'}
