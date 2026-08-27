# -*- coding: utf-8 -*-
import bpy
import math
from mathutils import Euler, Quaternion, Vector

_is_updating_flag = False

SEMANTIC_TO_NODE_MAP = {
    'pelvis': 0,
    'left_thigh': 1,
    'right_thigh': 2,
    'spine': 3,
    'left_calf': 4,
    'right_calf': 5,
    'chest': 6,
    'left_foot': 7,
    'right_foot': 8,
    'up_chest': 9,
    'neck': 12,
    'left_clavicle': 13,
    'right_clavicle': 14,
    'head': 15,
    'left_upperarm': 16,
    'right_upperarm': 17,
    'left_lowerarm': 18,
    'right_lowerarm': 19,
    'left_hand': 20,
    'right_hand': 21,
}

NODE_TO_ATTR_MAP = {
    0: 'pelvis_offset',
    1: 'left_thigh_offset',
    2: 'right_thigh_offset',
    3: 'spine_offset',
    4: 'left_calf_offset',
    5: 'right_calf_offset',
    6: 'chest_offset',
    7: 'left_foot_offset',
    8: 'right_foot_offset',
    9: 'up_chest_offset',
    12: 'neck_offset',
    13: 'left_clavicle_offset',
    14: 'right_clavicle_offset',
    15: 'head_offset',
    16: 'left_upperarm_offset',
    17: 'right_upperarm_offset',
    18: 'left_lowerarm_offset',
    19: 'right_lowerarm_offset',
    20: 'left_hand_offset',
    21: 'right_hand_offset',
}

SEMANTIC_TO_ATTR_MAP = {
    'left_clavicle': 'left_clavicle_offset',
    'left_upperarm': 'left_upperarm_offset',
    'left_lowerarm': 'left_lowerarm_offset',
    'left_hand': 'left_hand_offset',
    'right_clavicle': 'right_clavicle_offset',
    'right_upperarm': 'right_upperarm_offset',
    'right_lowerarm': 'right_lowerarm_offset',
    'right_hand': 'right_hand_offset',
    'left_thigh': 'left_thigh_offset',
    'left_calf': 'left_calf_offset',
    'left_foot': 'left_foot_offset',
    'right_thigh': 'right_thigh_offset',
    'right_calf': 'right_calf_offset',
    'right_foot': 'right_foot_offset',
    'pelvis': 'pelvis_offset',
    'spine': 'spine_offset',
    'chest': 'chest_offset',
    'up_chest': 'up_chest_offset',
    'neck': 'neck_offset',
    'head': 'head_offset',
}

RIGHT_TO_LEFT_ATTR_MAP = {
    'right_clavicle_offset': 'left_clavicle_offset',
    'right_upperarm_offset': 'left_upperarm_offset',
    'right_lowerarm_offset': 'left_lowerarm_offset',
    'right_hand_offset': 'left_hand_offset',
    'right_thigh_offset': 'left_thigh_offset',
    'right_calf_offset': 'left_calf_offset',
    'right_foot_offset': 'left_foot_offset',
}


def force_viewport_redraw():
    try:
        wm = bpy.context.window_manager if hasattr(bpy.context, 'window_manager') else None
        if wm:
            for window in wm.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        area.tag_redraw()
    except Exception:
        pass


def get_bone_name_from_semantic(scene, semantic_key):
    if not scene:
        return ""
    bone_map = getattr(scene, 'rebocap_bone_map', None)
    if not bone_map:
        return ""
    node_idx = SEMANTIC_TO_NODE_MAP.get(semantic_key)
    if node_idx is None:
        return ""
    return getattr(bone_map, f"node_{node_idx}", "")


def get_a2t_quat_for_node_idx(scene, node_idx):
    if not scene:
        return Quaternion((1.0, 0.0, 0.0, 0.0))
    a2t = getattr(scene, 'rebocap_a2t', None)
    if not a2t or not a2t.enable_a2t or a2t.alpha <= 0.0001:
        return Quaternion((1.0, 0.0, 0.0, 0.0))

    attr_name = NODE_TO_ATTR_MAP.get(node_idx)
    if not attr_name:
        return Quaternion((1.0, 0.0, 0.0, 0.0))

    if a2t.mirror_edit and attr_name in RIGHT_TO_LEFT_ATTR_MAP:
        left_attr = RIGHT_TO_LEFT_ATTR_MAP[attr_name]
        left_rot = getattr(a2t, left_attr, (0.0, 0.0, 0.0))
        rot_deg = a2t.calculate_mirrored_rot(left_rot)
    else:
        rot_deg = getattr(a2t, attr_name, (0.0, 0.0, 0.0))

    if rot_deg[0] == 0.0 and rot_deg[1] == 0.0 and rot_deg[2] == 0.0:
        return Quaternion((1.0, 0.0, 0.0, 0.0))

    alpha = a2t.alpha
    eul = Euler((
        math.radians(rot_deg[0] * alpha),
        math.radians(rot_deg[1] * alpha),
        math.radians(rot_deg[2] * alpha)
    ), 'YXZ')
    return eul.to_quaternion()


def apply_a2t_preview_to_armature(scene, arm_obj=None, force_apply=False):
    if not scene:
        return
    if not arm_obj:
        arm_name = getattr(scene, 'rebocap_source_armature', '')
        if not arm_name:
            return
        arm_obj = bpy.data.objects.get(arm_name)
    if not arm_obj or arm_obj.type != 'ARMATURE' or not arm_obj.pose:
        return

    a2t = getattr(scene, 'rebocap_a2t', None)
    if not a2t:
        return

    if (not force_apply and not a2t.preview_mode) or not a2t.enable_a2t or a2t.alpha <= 0.0001:
        for pb in arm_obj.pose.bones:
            pb.rotation_quaternion = Quaternion((1.0, 0.0, 0.0, 0.0))
            pb.rotation_euler = Euler((0.0, 0.0, 0.0))
        force_viewport_redraw()
        return

    if a2t.mirror_edit:
        a2t.sync_mirror_offsets()

    alpha = a2t.alpha
    for sem_key, attr_name in SEMANTIC_TO_ATTR_MAP.items():
        bone_name = get_bone_name_from_semantic(scene, sem_key)
        if not bone_name:
            continue
        pb = arm_obj.pose.bones.get(bone_name)
        if not pb:
            continue

        if a2t.mirror_edit and attr_name in RIGHT_TO_LEFT_ATTR_MAP:
            left_attr = RIGHT_TO_LEFT_ATTR_MAP[attr_name]
            left_rot = getattr(a2t, left_attr, (0.0, 0.0, 0.0))
            rot_deg = a2t.calculate_mirrored_rot(left_rot)
        else:
            rot_deg = getattr(a2t, attr_name, (0.0, 0.0, 0.0))

        eul = Euler((
            math.radians(rot_deg[0] * alpha),
            math.radians(rot_deg[1] * alpha),
            math.radians(rot_deg[2] * alpha)
        ), 'YXZ')

        pb.rotation_mode = 'QUATERNION'
        pb.rotation_quaternion = eul.to_quaternion()

    force_viewport_redraw()


def on_a2t_property_updated(self, context):
    global _is_updating_flag
    if _is_updating_flag:
        return

    _is_updating_flag = True
    try:
        scene = getattr(context, 'scene', None)
        if not scene:
            return
        a2t = getattr(scene, 'rebocap_a2t', None)
        if not a2t:
            return

        if a2t.mirror_edit:
            a2t.sync_mirror_offsets()

        if a2t.preview_mode:
            apply_a2t_preview_to_armature(scene)
    finally:
        _is_updating_flag = False


def on_preview_mode_toggle(self, context):
    scene = getattr(context, 'scene', None)
    if not scene:
        return
    a2t = getattr(scene, 'rebocap_a2t', None)
    if a2t and a2t.mirror_edit:
        a2t.sync_mirror_offsets()
    apply_a2t_preview_to_armature(scene)


class RebocapA2TSettings(bpy.types.PropertyGroup):
    enable_a2t: bpy.props.BoolProperty(
        name="Enable A2T Calibration",
        default=False,
        description="Enable A-Pose to T-Pose calibration layer in runtime retargeting",
        update=on_a2t_property_updated
    )



    def on_preset_changed(self, context):
        global _is_updating_flag
        if _is_updating_flag:
            return
        _is_updating_flag = True
        try:
            self.apply_preset(self.preset_template)
            scene = getattr(context, 'scene', None)
            if scene and self.preview_mode:
                apply_a2t_preview_to_armature(scene)
        finally:
            _is_updating_flag = False

    preset_template: bpy.props.EnumProperty(
        name="Preset Template",
        items=[
            ('UE5_Manny_Quinn', 'UE5 (Manny / Quinn / MetaHuman)', 'Standard UE5 A-Pose preset'),
            ('Mixamo_APose', 'Mixamo A-Pose (~40°)', 'Standard Mixamo A-Pose preset'),
            ('VRoid_VRM', 'VRoid / VRM (~35°)', 'Standard VRoid / VRM A-Pose preset'),
            ('MMD_Standard', 'MMD Standard (~35°)', 'Standard MMD A-Pose preset'),
            ('Custom', 'Custom', 'User-defined custom offsets'),
        ],
        default='UE5_Manny_Quinn',
        description="Quick presets for common character A-Poses",
        update=on_preset_changed
    )

    mirror_edit: bpy.props.BoolProperty(
        name="Symmetrical Edit",
        default=True,
        description="Automatically mirror left limb modifications to right limb",
        update=on_a2t_property_updated
    )

    mirror_invert_roll: bpy.props.BoolProperty(
        name="Invert Roll (X)",
        default=False,
        description="Invert Roll (X axis) when mirroring",
        update=on_a2t_property_updated
    )

    mirror_invert_pitch: bpy.props.BoolProperty(
        name="Invert Pitch (Y)",
        default=True,
        description="Invert Pitch (Y axis) when mirroring",
        update=on_a2t_property_updated
    )

    mirror_invert_yaw: bpy.props.BoolProperty(
        name="Invert Yaw (Z)",
        default=True,
        description="Invert Yaw (Z axis) when mirroring",
        update=on_a2t_property_updated
    )

    alpha: bpy.props.FloatProperty(
        name="Alpha",
        default=1.0,
        min=0.0,
        max=1.0,
        description="A2T Calibration Strength Weight",
        update=on_a2t_property_updated
    )

    preview_mode: bpy.props.BoolProperty(
        name="Preview in Viewport",
        default=True,
        description="Preview A2T calibration pose directly on the character in 3D viewport",
        update=on_preview_mode_toggle
    )

    # 1. Left Arm (Default UE5 Manny/Quinn)
    left_clavicle_offset: bpy.props.FloatVectorProperty(name="Left Clavicle", size=3, default=(-15.0, 0.0, 0.0), update=on_a2t_property_updated)
    left_upperarm_offset: bpy.props.FloatVectorProperty(name="Left UpperArm", size=3, default=(-40.0, 0.0, 0.0), update=on_a2t_property_updated)
    left_lowerarm_offset: bpy.props.FloatVectorProperty(name="Left LowerArm", size=3, default=(0.0, 0.0, -40.0), update=on_a2t_property_updated)
    left_hand_offset: bpy.props.FloatVectorProperty(name="Left Hand", size=3, default=(0.0, 0.0, 0.0), update=on_a2t_property_updated)

    # 2. Right Arm (Mirrored defaults)
    right_clavicle_offset: bpy.props.FloatVectorProperty(name="Right Clavicle", size=3, default=(-15.0, 0.0, 0.0), update=on_a2t_property_updated)
    right_upperarm_offset: bpy.props.FloatVectorProperty(name="Right UpperArm", size=3, default=(-40.0, 0.0, 0.0), update=on_a2t_property_updated)
    right_lowerarm_offset: bpy.props.FloatVectorProperty(name="Right LowerArm", size=3, default=(0.0, 0.0, 40.0), update=on_a2t_property_updated)
    right_hand_offset: bpy.props.FloatVectorProperty(name="Right Hand", size=3, default=(0.0, 0.0, 0.0), update=on_a2t_property_updated)

    # 3. Left Leg
    left_thigh_offset: bpy.props.FloatVectorProperty(name="Left Thigh", size=3, default=(3.0, 5.0, 0.0), update=on_a2t_property_updated)
    left_calf_offset: bpy.props.FloatVectorProperty(name="Left Calf", size=3, default=(0.0, 0.0, 0.0), update=on_a2t_property_updated)
    left_foot_offset: bpy.props.FloatVectorProperty(name="Left Foot", size=3, default=(0.0, 0.0, 0.0), update=on_a2t_property_updated)

    # 4. Right Leg (Mirrored defaults: Y inverted to -5.0)
    right_thigh_offset: bpy.props.FloatVectorProperty(name="Right Thigh", size=3, default=(3.0, -5.0, 0.0), update=on_a2t_property_updated)
    right_calf_offset: bpy.props.FloatVectorProperty(name="Right Calf", size=3, default=(0.0, 0.0, 0.0), update=on_a2t_property_updated)
    right_foot_offset: bpy.props.FloatVectorProperty(name="Right Foot", size=3, default=(0.0, 0.0, 0.0), update=on_a2t_property_updated)

    # 5. Root & Spine & Head
    pelvis_offset: bpy.props.FloatVectorProperty(name="Pelvis", size=3, default=(0.0, 0.0, 0.0), update=on_a2t_property_updated)
    spine_offset: bpy.props.FloatVectorProperty(name="Spine", size=3, default=(0.0, 0.0, 0.0), update=on_a2t_property_updated)
    chest_offset: bpy.props.FloatVectorProperty(name="Chest", size=3, default=(0.0, 0.0, 0.0), update=on_a2t_property_updated)
    up_chest_offset: bpy.props.FloatVectorProperty(name="Up Chest", size=3, default=(0.0, 0.0, 0.0), update=on_a2t_property_updated)
    neck_offset: bpy.props.FloatVectorProperty(name="Neck", size=3, default=(0.0, 0.0, 0.0), update=on_a2t_property_updated)
    head_offset: bpy.props.FloatVectorProperty(name="Head", size=3, default=(0.0, 0.0, 0.0), update=on_a2t_property_updated)

    def calculate_mirrored_rot(self, in_rot):
        x = -in_rot[0] if self.mirror_invert_roll else in_rot[0]
        y = -in_rot[1] if self.mirror_invert_pitch else in_rot[1]
        z = -in_rot[2] if self.mirror_invert_yaw else in_rot[2]
        return (x, y, z)

    def sync_mirror_offsets(self):
        if not self.mirror_edit:
            return
        self.right_clavicle_offset = self.calculate_mirrored_rot(self.left_clavicle_offset)
        self.right_upperarm_offset = self.calculate_mirrored_rot(self.left_upperarm_offset)
        self.right_lowerarm_offset = self.calculate_mirrored_rot(self.left_lowerarm_offset)
        self.right_hand_offset = self.calculate_mirrored_rot(self.left_hand_offset)

        self.right_thigh_offset = self.calculate_mirrored_rot(self.left_thigh_offset)
        self.right_calf_offset = self.calculate_mirrored_rot(self.left_calf_offset)
        self.right_foot_offset = self.calculate_mirrored_rot(self.left_foot_offset)

    def apply_preset(self, preset_name):
        if preset_name == 'UE5_Manny_Quinn':
            self.mirror_invert_roll = False
            self.mirror_invert_pitch = True
            self.mirror_invert_yaw = True

            self.left_clavicle_offset = (-15.0, 0.0, 0.0)
            self.left_upperarm_offset = (-40.0, 0.0, 0.0)
            self.left_lowerarm_offset = (0.0, 0.0, -40.0)
            self.left_hand_offset = (0.0, 0.0, 0.0)

            self.left_thigh_offset = (3.0, 5.0, 0.0)
            self.left_calf_offset = (0.0, 0.0, 0.0)
            self.left_foot_offset = (0.0, 0.0, 0.0)

            self.pelvis_offset = (0.0, 0.0, 0.0)
            self.spine_offset = (0.0, 0.0, 0.0)
            self.chest_offset = (0.0, 0.0, 0.0)
            self.up_chest_offset = (0.0, 0.0, 0.0)
            self.neck_offset = (0.0, 0.0, 0.0)
            self.head_offset = (0.0, 0.0, 0.0)
            self.sync_mirror_offsets()

        elif preset_name in ('MMD_Standard', 'VRoid_VRM'):
            self.mirror_invert_roll = False
            self.mirror_invert_pitch = True
            self.mirror_invert_yaw = True

            self.left_clavicle_offset = (0.0, 0.0, 0.0)
            self.left_upperarm_offset = (0.0, 0.0, 35.0)
            self.left_lowerarm_offset = (0.0, 0.0, 0.0)
            self.left_hand_offset = (0.0, 0.0, 0.0)

            self.left_thigh_offset = (0.0, 0.0, 0.0)
            self.left_calf_offset = (0.0, 0.0, 0.0)
            self.left_foot_offset = (0.0, 0.0, 0.0)

            self.pelvis_offset = (0.0, 0.0, 0.0)
            self.spine_offset = (0.0, 0.0, 0.0)
            self.chest_offset = (0.0, 0.0, 0.0)
            self.up_chest_offset = (0.0, 0.0, 0.0)
            self.neck_offset = (0.0, 0.0, 0.0)
            self.head_offset = (0.0, 0.0, 0.0)
            self.sync_mirror_offsets()

        elif preset_name == 'Mixamo_APose':
            self.mirror_invert_roll = False
            self.mirror_invert_pitch = True
            self.mirror_invert_yaw = True

            self.left_clavicle_offset = (0.0, 0.0, 0.0)
            self.left_upperarm_offset = (0.0, 0.0, 40.0)
            self.left_lowerarm_offset = (0.0, 0.0, 0.0)
            self.left_hand_offset = (0.0, 0.0, 0.0)

            self.left_thigh_offset = (0.0, 0.0, 0.0)
            self.left_calf_offset = (0.0, 0.0, 0.0)
            self.left_foot_offset = (0.0, 0.0, 0.0)

            self.pelvis_offset = (0.0, 0.0, 0.0)
            self.spine_offset = (0.0, 0.0, 0.0)
            self.chest_offset = (0.0, 0.0, 0.0)
            self.up_chest_offset = (0.0, 0.0, 0.0)
            self.neck_offset = (0.0, 0.0, 0.0)
            self.head_offset = (0.0, 0.0, 0.0)
            self.sync_mirror_offsets()
