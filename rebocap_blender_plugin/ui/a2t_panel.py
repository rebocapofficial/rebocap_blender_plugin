# -*- coding: utf-8 -*-
import bpy
from ..core.translation import T

class REBOCAP_PT_a2t_panel(bpy.types.Panel):
    bl_idname = 'REBOCAP_PT_a2t_panel'
    bl_label = " "
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "REBOCAP CONNECTION"
    bl_order = 3

    def draw_header(self, context):
        a2t = getattr(context.scene, 'rebocap_a2t', None)
        is_enabled = a2t and a2t.enable_a2t
        status_icon = 'RADIOBUT_ON' if is_enabled else 'RADIOBUT_OFF'
        self.layout.label(text=T('A2T Pose Calibration (A-Pose to T-Pose)'), icon=status_icon)

    def draw(self, ctx):
        layout = self.layout
        scene = ctx.scene
        a2t = getattr(scene, 'rebocap_a2t', None)
        if not a2t:
            return

        col = layout.column()

        top_box = col.box()
        top_box.prop(a2t, 'enable_a2t', text=T('Enable A2T Calibration'), toggle=True, icon='CHECKMARK')

        if not a2t.enable_a2t:
            top_box.label(text=T("* A2T Disabled (Direct Mocap Mapping)"), icon='INFO')
            
        top_box.separator()
        row_preset = top_box.row(align=True)
        row_preset.label(text=T("Preset Template:"), icon='PRESET')
        row_preset.prop(a2t, 'preset_template', text="")

        row_json = top_box.row(align=True)
        row_json.operator('rebocap.export_a2t_json', text=T('Export JSON'), icon='EXPORT')
        row_json.operator('rebocap.import_a2t_json', text=T('Import JSON'), icon='IMPORT')

        top_box.separator()
        row_prev = top_box.row(align=True)
        row_prev.prop(a2t, 'preview_mode', text=T('Preview in Viewport'), toggle=True, icon='RESTRICT_VIEW_OFF' if not a2t.preview_mode else 'RESTRICT_VIEW_ON')
        row_prev.operator('rebocap.reset_a2t_offsets', text=T('Reset Offsets'), icon='LOOP_BACK')

        if not a2t.preview_mode:
            top_box.label(text="💡 点击 [实时视口预览] 即可在视口中看到骨骼实时转动", icon='INFO')
        else:
            top_box.label(text="🟢 实时视口预览中 (拖动下方滑块实时旋转骨骼)", icon='CHECKMARK')

        row_alpha = top_box.row(align=True)
        row_alpha.prop(a2t, 'alpha', slider=True)

        top_box.separator()
        box_mirror = top_box.box()
        box_mirror.prop(a2t, 'mirror_edit', text=T('Symmetrical Edit (Mirror Left -> Right)'), icon='MOD_MIRROR')
        if a2t.mirror_edit:
            row_inv = box_mirror.row(align=True)
            row_inv.prop(a2t, 'mirror_invert_roll', text="Invert X")
            row_inv.prop(a2t, 'mirror_invert_pitch', text="Invert Y")
            row_inv.prop(a2t, 'mirror_invert_yaw', text="Invert Z")

        # Limb Sub-sections
        def draw_rot_row(parent_layout, label, prop_name, enabled=True):
            sub_box = parent_layout.box()
            sub_col = sub_box.column()
            sub_col.enabled = enabled
            sub_col.label(text=label)
            r = sub_col.row(align=True)
            r.prop(a2t, prop_name, index=0, text="X")
            r.prop(a2t, prop_name, index=1, text="Y")
            r.prop(a2t, prop_name, index=2, text="Z")

        # 1. Left Arm
        box_l_arm = col.box()
        box_l_arm.label(text=T("1. Left Arm"), icon='TRIA_DOWN')
        draw_rot_row(box_l_arm, T("Left Clavicle (Collar)"), 'left_clavicle_offset')
        draw_rot_row(box_l_arm, T("Left UpperArm (Shoulder)"), 'left_upperarm_offset')
        draw_rot_row(box_l_arm, T("Left LowerArm (Elbow)"), 'left_lowerarm_offset')
        draw_rot_row(box_l_arm, T("Left Hand (Wrist)"), 'left_hand_offset')

        # 2. Right Arm
        box_r_arm = col.box()
        box_r_arm.label(text=T("2. Right Arm") + (" " + T("(Mirrored)") if a2t.mirror_edit else ""), icon='TRIA_DOWN')
        draw_rot_row(box_r_arm, T("Right Clavicle (Collar)"), 'right_clavicle_offset', enabled=not a2t.mirror_edit)
        draw_rot_row(box_r_arm, T("Right UpperArm (Shoulder)"), 'right_upperarm_offset', enabled=not a2t.mirror_edit)
        draw_rot_row(box_r_arm, T("Right LowerArm (Elbow)"), 'right_lowerarm_offset', enabled=not a2t.mirror_edit)
        draw_rot_row(box_r_arm, T("Right Hand (Wrist)"), 'right_hand_offset', enabled=not a2t.mirror_edit)

        # 3. Left Leg
        box_l_leg = col.box()
        box_l_leg.label(text=T("3. Left Leg"), icon='TRIA_DOWN')
        draw_rot_row(box_l_leg, T("Left Thigh (Hip)"), 'left_thigh_offset')
        draw_rot_row(box_l_leg, T("Left Calf (Knee)"), 'left_calf_offset')
        draw_rot_row(box_l_leg, T("Left Foot (Ankle)"), 'left_foot_offset')

        # 4. Right Leg
        box_r_leg = col.box()
        box_r_leg.label(text=T("4. Right Leg") + (" " + T("(Mirrored)") if a2t.mirror_edit else ""), icon='TRIA_DOWN')
        draw_rot_row(box_r_leg, T("Right Thigh (Hip)"), 'right_thigh_offset', enabled=not a2t.mirror_edit)
        draw_rot_row(box_r_leg, T("Right Calf (Knee)"), 'right_calf_offset', enabled=not a2t.mirror_edit)
        draw_rot_row(box_r_leg, T("Right Foot (Ankle)"), 'right_foot_offset', enabled=not a2t.mirror_edit)

        # 5. Root & Spine & Head
        box_torso = col.box()
        box_torso.label(text=T("5. Root & Spine & Head"), icon='TRIA_DOWN')
        draw_rot_row(box_torso, T("Pelvis (Hips)"), 'pelvis_offset')
        draw_rot_row(box_torso, T("Spine1 (Waist)"), 'spine_offset')
        draw_rot_row(box_torso, T("Spine2 (Chest)"), 'chest_offset')
        draw_rot_row(box_torso, T("Spine3 (Up Chest)"), 'up_chest_offset')
        draw_rot_row(box_torso, T("Neck"), 'neck_offset')
        draw_rot_row(box_torso, T("Head"), 'head_offset')
