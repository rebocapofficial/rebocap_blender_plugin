# -*- coding: utf-8 -*-
import bpy
import json
from bpy_extras.io_utils import ExportHelper, ImportHelper
from ..core.translation import T
from ..core.a2t_types import apply_a2t_preview_to_armature

class REBOCAP_OT_export_a2t_json(bpy.types.Operator, ExportHelper):
    bl_idname = 'rebocap.export_a2t_json'
    bl_label = 'Export A2T JSON'
    bl_description = 'Export A2T Pose Calibration configuration to JSON file (Compatible with UE plugin)'
    filename_ext = '.json'
    filter_glob: bpy.props.StringProperty(default='*.json', options={'HIDDEN'})

    def execute(self, context):
        scene = context.scene
        a2t = getattr(scene, 'rebocap_a2t', None)
        if not a2t:
            self.report({'ERROR'}, 'A2T Settings not found in scene')
            return {'CANCELLED'}

        data = {
            "version": "2.0",
            "type": "rebocap_a2t_calibration",
            "preset_template": 0,
            "mirror_settings": {
                "mirror_edit": a2t.mirror_edit,
                "invert_roll": a2t.mirror_invert_roll,
                "invert_pitch": a2t.mirror_invert_pitch,
                "invert_yaw": a2t.mirror_invert_yaw
            },
            "alpha": a2t.alpha,
            "bone_rotations": {
                "left_clavicle": list(a2t.left_clavicle_offset),
                "left_upperarm": list(a2t.left_upperarm_offset),
                "left_lowerarm": list(a2t.left_lowerarm_offset),
                "left_hand": list(a2t.left_hand_offset),
                "right_clavicle": list(a2t.right_clavicle_offset),
                "right_upperarm": list(a2t.right_upperarm_offset),
                "right_lowerarm": list(a2t.right_lowerarm_offset),
                "right_hand": list(a2t.right_hand_offset),
                "left_thigh": list(a2t.left_thigh_offset),
                "left_calf": list(a2t.left_calf_offset),
                "left_foot": list(a2t.left_foot_offset),
                "right_thigh": list(a2t.right_thigh_offset),
                "right_calf": list(a2t.right_calf_offset),
                "right_foot": list(a2t.right_foot_offset),
                "pelvis": list(a2t.pelvis_offset),
                "spine": list(a2t.spine_offset),
                "chest": list(a2t.chest_offset),
                "up_chest": list(a2t.up_chest_offset),
                "neck": list(a2t.neck_offset),
                "head": list(a2t.head_offset)
            }
        }

        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            self.report({'INFO'}, f"Exported A2T config to: {self.filepath}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export A2T JSON: {str(e)}")
            return {'CANCELLED'}


class REBOCAP_OT_import_a2t_json(bpy.types.Operator, ImportHelper):
    bl_idname = 'rebocap.import_a2t_json'
    bl_label = 'Import A2T JSON'
    bl_description = 'Import A2T Pose Calibration configuration from JSON file'
    filename_ext = '.json'
    filter_glob: bpy.props.StringProperty(default='*.json', options={'HIDDEN'})

    def execute(self, context):
        scene = context.scene
        a2t = getattr(scene, 'rebocap_a2t', None)
        if not a2t:
            self.report({'ERROR'}, 'A2T Settings not found in scene')
            return {'CANCELLED'}

        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "mirror_settings" in data:
                ms = data["mirror_settings"]
                a2t.mirror_edit = ms.get("mirror_edit", True)
                a2t.mirror_invert_roll = ms.get("invert_roll", False)
                a2t.mirror_invert_pitch = ms.get("invert_pitch", True)
                a2t.mirror_invert_yaw = ms.get("invert_yaw", True)

            if "alpha" in data:
                a2t.alpha = float(data["alpha"])

            if "bone_rotations" in data:
                br = data["bone_rotations"]
                for key, val in br.items():
                    attr = f"{key}_offset"
                    if hasattr(a2t, attr) and isinstance(val, (list, tuple)) and len(val) >= 3:
                        setattr(a2t, attr, (float(val[0]), float(val[1]), float(val[2])))

            a2t.preset_template = 'Custom'
            if a2t.preview_mode:
                apply_a2t_preview_to_armature(scene)

            self.report({'INFO'}, f"Successfully imported A2T config from: {self.filepath}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Failed to import A2T JSON: {str(e)}")
            return {'CANCELLED'}


class REBOCAP_OT_reset_a2t_offsets(bpy.types.Operator):
    bl_idname = 'rebocap.reset_a2t_offsets'
    bl_label = 'Reset Offsets'
    bl_description = 'Reset all A2T limb rotation offsets to zero'

    def execute(self, context):
        a2t = getattr(context.scene, 'rebocap_a2t', None)
        if not a2t:
            return {'CANCELLED'}

        all_attrs = [
            'left_clavicle_offset', 'left_upperarm_offset', 'left_lowerarm_offset', 'left_hand_offset',
            'right_clavicle_offset', 'right_upperarm_offset', 'right_lowerarm_offset', 'right_hand_offset',
            'left_thigh_offset', 'left_calf_offset', 'left_foot_offset',
            'right_thigh_offset', 'right_calf_offset', 'right_foot_offset',
            'pelvis_offset', 'spine_offset', 'chest_offset', 'up_chest_offset', 'neck_offset', 'head_offset'
        ]
        for attr in all_attrs:
            setattr(a2t, attr, (0.0, 0.0, 0.0))

        a2t.preset_template = 'Custom'
        if a2t.preview_mode:
            apply_a2t_preview_to_armature(context.scene)

        self.report({'INFO'}, "All A2T offsets reset to 0.")
        return {'FINISHED'}
