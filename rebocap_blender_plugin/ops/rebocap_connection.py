from ..core.a2t_types import get_a2t_quat_for_node_idx
import os
import time
from threading import Thread

import atexit
import bpy
import random
from mathutils import Vector, Matrix, Quaternion, Euler
from ..rebocap_api import *
from typing import Optional
from .utils import show_message_box
from ..rebocap_api.rebocap_ws_sdk import REBOCAP_JOINT_NAMES

# ================= 强制上下文操作器 =================
def force_stop_animation(ctx):
    """强制且安全地停止时间轴，忽略 UI 上下文错误"""
    if getattr(ctx.screen, 'is_animation_playing', False):
        try:
            bpy.ops.screen.animation_cancel(restore_frame=False)
        except Exception:
            # 强行覆写到 3D 视图上下文执行
            for window in ctx.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        with ctx.temp_override(window=window, area=area):
                            bpy.ops.screen.animation_cancel(restore_frame=False)
                        return

def force_start_animation(ctx):
    """强制开始播放，忽略 UI 上下文错误"""
    try:
        bpy.ops.screen.animation_play()
    except Exception:
        for window in ctx.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    with ctx.temp_override(window=window, area=area):
                        bpy.ops.screen.animation_play()
                    return
# =================================================

def _is_legacy_action(action):
    # 精准判断：Blender 4.4/4.5 以后引入了 slots，不再单纯依赖 fcurves 的存在与否
    return hasattr(action, 'fcurves') and not hasattr(action, 'slots')

def _get_fcurves_coll(owner, attrs):
    """Probe *owner* for a collection-like attribute from *attrs* that has ``.new()``."""
    for attr in attrs:
        coll = getattr(owner, attr, None)
        if coll is not None and hasattr(coll, 'new'):
            return coll
    avail = [a for a in dir(owner) if not a.startswith('_')]
    raise AttributeError(
        f"{type(owner).__name__} has no recognised FCurve collection. "
        f"Tried: {attrs}. Available: {avail}"
    )


def _action_setup_slot(action, obj):
    """Ensure the action has a slot for *obj* (Blender 5.x slotted actions).

    Call this right **before** ``obj.animation_data.action = action`` so that
    the assignment can bind the pre-created slot to the object.
    """
    if _is_legacy_action(action):
        return  # Blender 3.x-4.3: nothing to do

    if not hasattr(action, 'slots'):
        return

    # Create a slot for this object if none exists yet
    if len(action.slots) == 0:
        action.slots.new('OBJECT', name=obj.name if obj else 'Slot')

    # Ensure the layer → strip → channelbag chain exists
    if len(action.layers) == 0:
        action.layers.new('Layer')
    layer = action.layers[0]
    if len(layer.strips) == 0:
        layer.strips.new()
    strip = layer.strips[0]

    if hasattr(strip, 'channelbags') and len(strip.channelbags) == 0:
        slot = action.slots[0]
        strip.channelbags.new(slot=slot)


def _action_fcurve_new(action, data_path, index):
    """Create a new FCurve on an Action, compatible across Blender 3.x-5.x.

    Call ``_action_setup_slot(action, obj)`` **before** using this on Blender 5.x.
    """
    if _is_legacy_action(action) or not hasattr(action, 'slots'):
        return action.fcurves.new(data_path=data_path, index=index)

    # Blender 4.4+: hierarchy must already exist (set up by _action_setup_slot)
    strip = action.layers[0].strips[0]
    if hasattr(strip, 'channelbags') and len(strip.channelbags) > 0:
        bag = strip.channelbags[0]
    elif hasattr(strip, 'channelbag'):
        bag = strip.channelbag
    else:
        raise AttributeError(
            f"Strip has no channelbag. Call _action_setup_slot() first. "
            f"Available: {[a for a in dir(strip) if not a.startswith('_')]}"
        )

    coll = _get_fcurves_coll(bag, ('fcurves', 'channels'))
    return coll.new(data_path=data_path, index=index)


def _action_iter_fcurves(action):
    """Iterate over all FCurves in an Action, compatible across Blender versions."""
    if _is_legacy_action(action) or not hasattr(action, 'slots'):
        yield from action.fcurves
        return

    # Blender 4.4+: layers → strips → channelbags → fcurves
    for layer in action.layers:
        for strip in layer.strips:
            bags = (getattr(strip, 'channelbags', None)
                    or getattr(strip, 'channelbag', None))
            if bags is None:
                continue
            # Normalise to iterable
            if not hasattr(bags, '__iter__'):
                bags = [bags]
            for bag in bags:
                coll = getattr(bag, 'fcurves', None) or getattr(bag, 'channels', None)
                if coll is not None:
                    yield from coll


class RebocapWsSdkV1(RebocapWsSdk):

    def __init__(self, coordinate_type: CoordinateType = CoordinateType.DefaultCoordinate, use_global_rotation=False):
        super().__init__(coordinate_type, use_global_rotation)
        super().set_pose_msg_callback(self.pose_msg_callback_own)
        self.last_msg = None
        self.record_list = None

    def pose_msg_callback_own(self, parent: RebocapWsSdk, trans: list, pose24: list, static_index: int, tp: float):
        self.last_msg = (trans, pose24, static_index, tp)
        if self.record_list is not None:
            self.record_list.append(self.last_msg)

    def get_last_msg(self):
        return self.last_msg

    def start_record(self):
        self.record_list = []

    def stop_record(self):
        record_list = self.record_list
        self.record_list = None
        return record_list


rebocap_app: Optional[RebocapWsSdkV1] = None

rebocap_timer = None
rebocap_connected = False
drive_direct_when_connect = True
cached_initial_pose = {}


class FrameData:
    def __init__(self, trans, pose24, static_index, ts) -> None:
        self.trans = trans
        self.pose24 = pose24
        self.static_index = static_index
        self.ts = ts


joints = [
    "mixamorig:Hips",
    "mixamorig:LeftUpLeg",
    "mixamorig:RightUpLeg",
    "mixamorig:Spine",
    "mixamorig:LeftLeg",
    "mixamorig:RightLeg",
    "mixamorig:Spine1",
    "mixamorig:LeftFoot",
    "mixamorig:RightFoot",
    "mixamorig:Spine2",
    "mixamorig:LeftToeBase",
    "mixamorig:RightToeBase",
    "mixamorig:Neck",
    "mixamorig:LeftShoulder",
    "mixamorig:RightShoulder",
    "mixamorig:Head",
    "mixamorig:LeftArm",
    "mixamorig:RightArm",
    "mixamorig:LeftForeArm",
    "mixamorig:RightForeArm",
    "mixamorig:LeftHand",
    "mixamorig:RightHand",
    "mixamorig:LeftHandIndex1",
    "mixamorig:RightHandIndex1"
]

idx_vec = [name.lower() for name in REBOCAP_JOINT_NAMES]
joints_lower = [name.lower() for name in joints]

stop_debug_thread = False

class BoneInfo:
    def __init__(self) -> None:
        self.rest_matrix_to_world = None
        self.rest_matrix_from_world = None
    
    def is_rest_init(self):
        if self.rest_matrix_to_world is None or self.rest_matrix_from_world is None:
            return False
        return True

    def rest_init(self, rest_matrix_to_world, rest_matrix_from_world):
        self.rest_matrix_to_world = rest_matrix_to_world
        self.rest_matrix_from_world = rest_matrix_from_world

    def get_rest_init(self):
        return (self.rest_matrix_to_world, self.rest_matrix_from_world)

class ObjInfo:
    def __init__(self) -> None:
        self.bone_map = {}
        self.root_bone = None
        self.matrix_global_hip = None
        self.matrix_global_2_root_inverse = None
        self.matrix_root_2_hip_inverse = None

    def get_bone(self, name):
        if name in self.bone_map:
            return self.bone_map[name]
        return None

    def insert_bone(self, name):
        bone = BoneInfo()
        self.bone_map[name] = bone
        return bone

    def get_or_insert_bone(self, name):
        bone = self.get_bone(name)
        if bone is None:
            bone = self.insert_bone(name)
        return bone

    def set_root_info(self, root_bone, matrix_global_hip, matrix_global_2_root_inverse, matrix_root_2_hip_inverse):
        self.root_bone = root_bone
        self.matrix_global_hip = matrix_global_hip
        self.matrix_global_2_root_inverse = matrix_global_2_root_inverse
        self.matrix_root_2_hip_inverse = matrix_root_2_hip_inverse


class ObjInfoHelper:
    def __init__(self) -> None:
        self.obj_map = {}

    def get_obj(self, name):
        if name in self.obj_map:
            return self.obj_map[name]
        return None

    def insert_obj(self, name):
        obj = ObjInfo()
        self.obj_map[name] = obj
        return obj

    def get_or_insert_obj(self, name):
        obj = self.get_obj(name)
        if obj is None:
            obj = self.insert_obj(name)
        return obj


obj_info_helper = ObjInfoHelper()


def t_run():
    global stop_debug_thread
    print(f'started!!!!!!!')
    while True:
        time.sleep(1.0)
        continue


# 注册退出函数
if sys.gettrace() is not None:
    t = Thread(target=t_run)
    t.start()


def init_rebocap_api():
    global rebocap_app
    print(f'first init rebocap api')
    rebocap_app = RebocapWsSdkV1(coordinate_type=CoordinateType.BlenderCoordinate)
    print(f'finish init rebocap api')


def uninit_rebocap_api():
    global rebocap_app
    if rebocap_app is not None:
        rebocap_app.close()
    rebocap_app = None


def show_error_message(self, ctx):
    self.layout.label(text=ctx.scene.error_msg)


def get_pose_idx(bone: bpy.types.PoseBone):
    if bone.rebocap_init:
        return bone.rebocap_pose_idx
    name_l = bone.name.lower()
    for idx, name in enumerate(idx_vec):
        if name.lower() == name_l:
            bone.rebocap_pose_idx = idx
            bone.rebocap_init = True
            return bone.rebocap_pose_idx
    for idx, name in enumerate(joints_lower):
        if name == name_l:
            bone.rebocap_pose_idx = idx
            bone.rebocap_init = True
            return bone.rebocap_pose_idx
    bone.rebocap_init = True
    return bone.rebocap_pose_idx


def show_error(msg, ctx):
    ctx.scene.error_msg = msg
    bpy.context.window_manager.popup_menu(
        show_error_message, title="Error", icon='ERROR')


def compute_hierarchical_t_pose(source_obj, scene, is_retarget=False):
    t_pose_matrices = {}
    bone_name_to_idx = {}
    
    if is_retarget:
        rebocap_bone_map = scene.rebocap_bone_map
        for i in range(22):
            bname = getattr(rebocap_bone_map, f'node_{i}')
            if bname:
                bone_name_to_idx[bname] = i
    else:
        for pb in source_obj.pose.bones:
            idx = get_pose_idx(pb)
            if idx != -1:
                bone_name_to_idx[pb.name] = idx
                
    def get_matrix(bone):
        if bone.name in t_pose_matrices:
            return t_pose_matrices[bone.name]
            
        parent = bone.parent
        if parent:
            parent_t_pose = get_matrix(parent)
            rest_local = parent.matrix_local.inverted() @ bone.matrix_local
        else:
            parent_t_pose = Matrix.Identity(4)
            rest_local = bone.matrix_local
            
        a2t_quat = Quaternion()
        if bone.name in bone_name_to_idx:
            idx = bone_name_to_idx[bone.name]
            if idx not in (10, 11, 22, 23):
                a2t_quat = get_a2t_quat_for_node_idx(scene, idx)
                
        t_pose = parent_t_pose @ rest_local @ a2t_quat.to_matrix().to_4x4()
        t_pose_matrices[bone.name] = t_pose
        return t_pose

    for bone in source_obj.data.bones:
        get_matrix(bone)
        
    return t_pose_matrices


class CustomObj:
    def __init__(self, obj: bpy.types.Object) -> None:
        self.obj = None
        self.vec = []
        self.update_obj(obj)

    def update(self, obj: bpy.types.Object):
        if self.obj == obj:
            return
        self.update_obj(obj)

    def update_obj(self, obj: bpy.types.Object):
        self.vec = [None for _ in range(24)]
        for bone in obj.pose.bones:
            name = bone.name.lower()
            for idx, item in enumerate(idx_vec):
                if item.lower() in name or joints_lower[idx] in name:
                    self.vec[idx] = (bone, obj.data.bones.get(bone.name))
                    break
        self.obj = obj


class RebocapConnect(bpy.types.Operator):
    bl_idname = 'rebocap.connect'
    bl_label = 'Connect'
    pelvis_offset = [0.0, 0.0, 0.0]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reinit_data()
        self.root_bone_matrix_inverse = None

    def reinit_data(self):
        self.obj_map = {}
        self.root_bone = None
        global obj_info_helper
        obj_info_helper = ObjInfoHelper()
        self.root_relative_position = Vector((0.0, 0.0, 0.0))
        self.root_bone_matrix_inverse = None
        self.initial_mocap_trans = None
        self.initial_root_location = None
        self.cached_t_pose_matrices = None

    def execute(self, ctx):
        global rebocap_app, rebocap_connected, drive_direct_when_connect

        source_obj = bpy.data.objects.get(ctx.scene.rebocap_source_armature)

        rebocap_bone_map = ctx.scene.rebocap_bone_map
        
        # Always auto-detect and freshly read IK config & bone lengths on Connect
        try:
            from .ik_tracking import get_rebocap_config_path, parse_and_update_ik_config
            if not rebocap_bone_map.ik_config_path or not os.path.exists(rebocap_bone_map.ik_config_path):
                auto_path = get_rebocap_config_path()
                if auto_path:
                    rebocap_bone_map.ik_config_path = auto_path
            
            if rebocap_bone_map.ik_config_path and os.path.exists(rebocap_bone_map.ik_config_path):
                parse_and_update_ik_config(rebocap_bone_map.ik_config_path, rebocap_bone_map, None)
        except Exception as e:
            print(f"Error auto-refreshing IK config on connect: {e}")
                
        if source_obj is not None:
            
            avatar = source_obj
            down_body = [
                0, 1, 4, 7, 2, 5, 8  # root, left legs,  right legs
            ]

            bones = [avatar.pose.bones.get(getattr(rebocap_bone_map, f'node_{e}', '')) for e in down_body]
            if '' in bones:
                show_message_box(message='down body not all bind, please set target bone for Legs and Pelvis')
                return {'CANCELLED'}

        res = rebocap_app.open(ctx.scene.port, uid=random.randint(1, 100000))
        if res != 0:
            show_error(f"Connect Fail. ret={res}", ctx)
            return {'CANCELLED'}

        # Cache the initial pose for restoring later
        global cached_initial_pose
        cached_initial_pose.clear()
        source_obj = bpy.data.objects.get(ctx.scene.rebocap_source_armature)
        if source_obj and source_obj.type == 'ARMATURE':
            for pb in source_obj.pose.bones:
                cached_initial_pose[pb.name] = (pb.location.copy(), pb.rotation_quaternion.copy(), pb.rotation_euler.copy())
                
        # Also cache tracking nodes
        for obj in bpy.context.scene.objects:
            if obj.name.startswith("Rebocap_") and obj.type == 'EMPTY':
                cached_initial_pose[obj.name] = (obj.location.copy(), obj.rotation_quaternion.copy(), obj.rotation_euler.copy())

        self.reinit_data()
        ctx.window_manager.modal_handler_add(self)
        global rebocap_timer
        rebocap_timer = ctx.window_manager.event_timer_add(1 / 60, window=ctx.window)
        ctx.scene.open = True
        rebocap_connected = True
        return {'RUNNING_MODAL'}

    def drive_demo_character(self, trans, pose24):
        demo_robot = None
        for obj in bpy.data.objects:
            if obj.get("rebocap_demo_character") and obj.type == 'ARMATURE':
                demo_robot = obj
                break
                
        if not demo_robot:
            return
            
        hip_pbone = demo_robot.pose.bones.get('mixamorig:Hips')
        if hip_pbone:
            hip_pbone.location = Vector((trans[0], trans[1], trans[2]))
            
        bone_mapping_list = [
            'mixamorig:Hips', 'mixamorig:LeftUpLeg', 'mixamorig:RightUpLeg', 'mixamorig:Spine',
            'mixamorig:LeftLeg', 'mixamorig:RightLeg', 'mixamorig:Spine1', 'mixamorig:LeftFoot',
            'mixamorig:RightFoot', 'mixamorig:Spine2', 'mixamorig:LeftToeBase', 'mixamorig:RightToeBase',
            'mixamorig:Neck', 'mixamorig:LeftShoulder', 'mixamorig:RightShoulder', 'mixamorig:Head',
            'mixamorig:LeftArm', 'mixamorig:RightArm', 'mixamorig:LeftForeArm', 'mixamorig:RightForeArm',
            'mixamorig:LeftHand', 'mixamorig:RightHand'
        ]
        all_pose = [Quaternion([pose[3], pose[0], pose[1], pose[2]]) for pose in pose24]
        
        for idx, bone_name in enumerate(bone_mapping_list):
            if idx in (10, 11, 22, 23):
                continue
            pbone = demo_robot.pose.bones.get(bone_name)
            data_bone = demo_robot.data.bones.get(bone_name)
            if pbone and data_bone:
                pbone.rotation_mode = 'QUATERNION'
                rest_to_world = demo_robot.matrix_world.to_quaternion() @ data_bone.matrix_local.to_quaternion()
                rest_from_world = rest_to_world.inverted()
                pbone.rotation_quaternion = rest_from_world @ all_pose[idx] @ rest_to_world

    def drive_ik_tracking(self, trans, pose24):
        root_name = "Rebocap_Root"
        if root_name not in bpy.data.objects:
            return
            
        joints = [
            "Pelvis", "L_Upper_leg", "R_Upper_leg", "Spine1", "L_Lower_leg", "R_Lower_leg",
            "Spine2", "L_Foot", "R_Foot", "Spine3", "L_Toe", "R_Toe",
            "Neck", "L_Shoulder", "R_Shoulder", "Head", "L_Upper_arm", "R_Upper_arm",
            "L_Lower_arm", "R_Lower_arm", "L_Hand", "R_Hand", "L_Hand_end", "R_Hand_end",
        ]
        
        pelvis_node = bpy.data.objects.get("Rebocap_Pelvis")
        if pelvis_node:
            pelvis_node.location = Vector((trans[0], trans[1], trans[2]))
            
        for i, name in enumerate(joints):
            node = bpy.data.objects.get(f"Rebocap_{name}")
            if node:
                pose = pose24[i]
                node.rotation_quaternion = Quaternion([pose[3], pose[0], pose[1], pose[2]])
        return


    def drive_retarget(self, trans, pose24, static_index, ts):
        source_obj = bpy.data.objects.get(bpy.context.scene.rebocap_source_armature)
        if source_obj is None or source_obj.type != 'ARMATURE':
            return
            
        rebocap_bone_map = bpy.context.scene.rebocap_bone_map
        map_bones_names = [
            getattr(rebocap_bone_map, f'node_{i}') for i in range(22)
        ]
        map_bones = [
            source_obj.pose.bones.get(map_bones_names[i]) if map_bones_names[i] != '' else None for i in range(22)
        ]

        global obj_info_helper
        obj_info = obj_info_helper.get_or_insert_obj(source_obj.name)

        # handle merge pose for spine and chest
        hip_bone = map_bones[0]
        spine_bone = map_bones[3]
        chest_bone = map_bones[6]
        up_chest_bone = map_bones[9]
        left_shoulder_bone = map_bones[13]
        right_shoulder_bone = map_bones[14]
        left_arm_bone = map_bones[16]
        right_arm_bone = map_bones[17]
        all_pose = []
        for pose in pose24:
            all_pose.append(Quaternion([pose[3], pose[0], pose[1], pose[2]]))

        if spine_bone is not None or chest_bone is not None or up_chest_bone is not None:
            if spine_bone is None:
                all_pose[6] = all_pose[3] @ all_pose[6]
            if chest_bone is None and up_chest_bone is None:
                all_pose[3] = all_pose[3] @ all_pose[6] @ all_pose[9]
            elif chest_bone is None:
                all_pose[9] = all_pose[6] @ all_pose[9]
            elif up_chest_bone is None:
                all_pose[6] = all_pose[6] @ all_pose[9]
        if left_shoulder_bone is None and left_arm_bone is not None:
            all_pose[16] = all_pose[13] @ all_pose[16]
        if right_shoulder_bone is None and right_arm_bone is not None:
            all_pose[17] = all_pose[14] @ all_pose[17]

        # Use cached T-pose matrices or compute once
        if not hasattr(self, 'cached_t_pose_matrices') or self.cached_t_pose_matrices is None:
            self.cached_t_pose_matrices = compute_hierarchical_t_pose(source_obj, bpy.context.scene, is_retarget=True)
        t_pose_matrices = self.cached_t_pose_matrices

        for idx, bone in enumerate(map_bones):
            if bone is None or idx == -1 or idx in (10, 11, 22, 23):
                if idx == 0:  # hip must bind!!!
                    break
                continue
            bone_name = bone.name
            bone_info = obj_info.get_or_insert_bone(bone_name)
            data_bone = source_obj.data.bones.get(map_bones_names[idx])
            bone.rotation_mode = 'QUATERNION'

            a2t_quat = get_a2t_quat_for_node_idx(bpy.context.scene, idx)
            t_mat = t_pose_matrices.get(bone_name)
            if t_mat:
                virtual_rest_to_world = source_obj.matrix_world.to_quaternion() @ t_mat.to_quaternion()
                virtual_rest_from_world = virtual_rest_to_world.inverted()
            else:
                virtual_rest_to_world = source_obj.matrix_world.to_quaternion()
                virtual_rest_from_world = virtual_rest_to_world.inverted()

            if idx == 0:
                if obj_info.root_bone is None:
                    current_hip_bone = bone
                    root_bone = bone
                    visited = set()
                    while root_bone.parent is not None and root_bone not in visited:
                        visited.add(root_bone)
                        root_bone = root_bone.parent

                    matrix_root_2_hip = source_obj.data.bones[root_bone.name].matrix_local.inverted() @ source_obj.data.bones[current_hip_bone.name].matrix_local
                    matrix_global_2_root = source_obj.matrix_world @ source_obj.data.bones.get(root_bone.name).matrix_local
                    matrix_global_hip = source_obj.matrix_world @ source_obj.data.bones[current_hip_bone.name].matrix_local
                    obj_info.set_root_info(root_bone, matrix_global_hip, matrix_global_2_root.inverted(), matrix_root_2_hip.inverted())

                origin_hip_trans = Vector((trans[0], trans[1], trans[2]))
                keep_pos = getattr(bpy.context.scene, 'rebocap_keep_character_position', False)
                if keep_pos:
                    if self.initial_mocap_trans is None:
                        self.initial_mocap_trans = origin_hip_trans.copy()
                        self.initial_root_location = obj_info.root_bone.location.copy()
                    
                    delta_trans = origin_hip_trans - self.initial_mocap_trans
                    root_bone_data = source_obj.data.bones.get(obj_info.root_bone.name)
                    world_to_root_rot = (source_obj.matrix_world.to_quaternion() @ root_bone_data.matrix_local.to_quaternion()).inverted()
                    local_delta = world_to_root_rot @ delta_trans
                    obj_info.root_bone.location = self.initial_root_location + local_delta
                else:
                    new_global_hip: Matrix = obj_info.matrix_global_hip.copy()
                    new_global_hip.translation = origin_hip_trans
                    new_local_matrix = obj_info.matrix_global_2_root_inverse @ new_global_hip @ obj_info.matrix_root_2_hip_inverse
                    obj_info.root_bone.location = new_local_matrix.translation

            pose = all_pose[idx]
            mocap_delta_T = virtual_rest_from_world @ pose @ virtual_rest_to_world
            bone.rotation_quaternion = a2t_quat @ mocap_delta_T

    def modal(self, ctx, evt):
        global rebocap_app, rebocap_connected, drive_direct_when_connect
        if not rebocap_connected or rebocap_app is None:
            return {'PASS_THROUGH'}
            
        # ONLY process animation & mocap drive on TIMER ticks (prevents mousemove spam)
        if evt.type == 'TIMER':
            if getattr(ctx.scene, 'rebocap_pause_control', False):
                return {'PASS_THROUGH'}

            if getattr(ctx.scene, 'recording', False) and getattr(ctx.scene, 'rebocap_auto_extend_end', True):
                if ctx.scene.frame_current >= ctx.scene.frame_end - 2:
                    ctx.scene.frame_end += 60

            try:
                last_data = rebocap_app.get_last_msg()
                if last_data is not None:
                    # Only force redraw if we actually received real-time data
                    # Check if user wants to throttle redraws to Scene FPS
                    sync_fps = getattr(ctx.scene, 'rebocap_sync_viewport_fps', True)
                    
                    if not sync_fps:
                        # Full speed redraw (60Hz default)
                        trans, pose24, static_index, ts = last_data
                        self.drive_retarget(trans, pose24, static_index, ts)
                        self.drive_demo_character(trans, pose24)
                        self.drive_ik_tracking(trans, pose24)
                        for window in ctx.window_manager.windows:
                            for area in window.screen.areas:
                                if area.type in ('VIEW_3D', 'PROPERTIES'):
                                    area.tag_redraw()
                    else:
                        import time
                        current_time = time.time()
                        if not hasattr(self, "_last_redraw_time"):
                            self._last_redraw_time = 0
                            
                        scene_fps = ctx.scene.render.fps / ctx.scene.render.fps_base
                        scene_fps = max(10.0, min(120.0, scene_fps)) # clamp sensible range
                        redraw_interval = 1.0 / scene_fps
                        
                        if current_time - self._last_redraw_time >= redraw_interval:
                            self._last_redraw_time = current_time
                            
                            # Move math inside throttle! Mutating RNA forces Blender depsgraph redraw.
                            trans, pose24, static_index, ts = last_data
                            self.drive_retarget(trans, pose24, static_index, ts)
                            self.drive_demo_character(trans, pose24)
                            self.drive_ik_tracking(trans, pose24)
                            
                            for window in ctx.window_manager.windows:
                                for area in window.screen.areas:
                                    if area.type in ('VIEW_3D', 'PROPERTIES'):
                                        area.tag_redraw()
            except Exception as e:
                # Safe disconnect if connection broke down
                print(f"[Rebocap] Driver error: {e}")
                
        return {'PASS_THROUGH'}


def stop_record_ik_tracking(ctx, record_list, begin_t, take_id, take_name):
    joints = [
        "Pelvis", "L_Upper_leg", "R_Upper_leg", "Spine1", "L_Lower_leg", "R_Lower_leg",
        "Spine2", "L_Foot", "R_Foot", "Spine3", "L_Toe", "R_Toe",
        "Neck", "L_Shoulder", "R_Shoulder", "Head", "L_Upper_arm", "R_Upper_arm",
        "L_Lower_arm", "R_Lower_arm", "L_Hand", "R_Hand", "L_Hand_end", "R_Hand_end",
    ]
    
    # Process pose data to match logic in drive_retarget
    all_pose_list = []
    for frame in record_list:
        pose24 = frame[1]
        all_pose = []
        for pose in pose24:
            all_pose.append(Quaternion([pose[3], pose[0], pose[1], pose[2]]))
        all_pose_list.append(all_pose)
            
    dt = 1.0 / 60.0
    
    actions = []
    
    for i, name in enumerate(joints):
        node = bpy.data.objects.get(f"Rebocap_{name}")
        if not node: continue
        
        node.animation_data_create()
        # IK Action names format: rebocap_{name}_{take_id}
        action = bpy.data.actions.new(name=f'rebocap_{name}_{take_name}_{take_id}')
        _action_setup_slot(action, node)
        actions.append(action)
        
        rotation_quaternion = []
        t = []
        for fn, frame in enumerate(record_list):
            t.append((frame[3] - begin_t) / dt + 1)
            pose = all_pose_list[fn][i]
            rotation_quaternion.append(pose)
            
        data_path = 'rotation_quaternion'
        for axis_i in range(4):
            curve = _action_fcurve_new(action, data_path, index=axis_i)
            keyframe_points = curve.keyframe_points
            keyframe_points.add(len(rotation_quaternion))
            for fn, rot in enumerate(rotation_quaternion):
                keyframe_points[fn].co = (t[fn], rot[axis_i])
                
        if i == 0:
            data_path = 'location'
            locations = []
            for frame in record_list:
                trans = frame[0]
                locations.append(Vector((trans[0], trans[1], trans[2])))
            for axis_i in range(3):
                curve = _action_fcurve_new(action, data_path, index=axis_i)
                keyframe_points = curve.keyframe_points
                keyframe_points.add(len(locations))
                for fn, loc in enumerate(locations):
                    keyframe_points[fn].co = (t[fn], loc[axis_i])
                    
        for cu in _action_iter_fcurves(action):
            for bez in cu.keyframe_points:
                bez.interpolation = 'LINEAR'
                
        node.animation_data.action = action
        if hasattr(node.animation_data, 'action_slot') and hasattr(action, 'slots') and len(action.slots) > 0:
            node.animation_data.action_slot = action.slots[0]

    return actions



def stop_record_retarget(ctx, record_list, obj, take_id, take_name):
    begin_t = record_list[0][3]
    rebocap_bone_map = bpy.context.scene.rebocap_bone_map
    map_bones_names = [
        getattr(rebocap_bone_map, f'node_{i}') for i in range(22)
    ]
    map_bones = [
        obj.pose.bones.get(map_bones_names[i]) if map_bones_names[i] != '' else None for i in range(22)
    ]
    if obj is None:
        return
    all_pose_list = []
    for record in record_list:
        all_pose_list.append([Quaternion([pose[3], pose[0], pose[1], pose[2]]) for pose in record[1]])
    hip_bone = map_bones[0]
    spine_bone = map_bones[3]
    chest_bone = map_bones[6]
    up_chest_bone = map_bones[9]
    left_shoulder_bone = map_bones[13]
    right_shoulder_bone = map_bones[14]
    left_arm_bone = map_bones[16]
    right_arm_bone = map_bones[17]
    if spine_bone is not None or chest_bone is not None or up_chest_bone is not None:
        if spine_bone is None:
            for all_pose in all_pose_list:
                all_pose[6] = all_pose[3] @ all_pose[6]
        if chest_bone is None and up_chest_bone is None:
            for all_pose in all_pose_list:
                all_pose[3] = all_pose[3] @ all_pose[6] @ all_pose[9]
        elif chest_bone is None:
            for all_pose in all_pose_list:
                all_pose[9] = all_pose[6] @ all_pose[9]
        elif up_chest_bone is None:
            for all_pose in all_pose_list:
                all_pose[6] = all_pose[6] @ all_pose[9]
    if left_shoulder_bone is None and left_arm_bone is not None:
        for all_pose in all_pose_list:
            all_pose[16] = all_pose[13] @ all_pose[16]
    if right_shoulder_bone is None and right_arm_bone is not None:
        for all_pose in all_pose_list:
            all_pose[17] = all_pose[14] @ all_pose[17]
    obj.animation_data_create()
    action = bpy.data.actions.new(name=f'rebocap_{take_name}_{take_id}')
    _action_setup_slot(action, obj)
    
    dt = 1.0 / 60.0
    
    global obj_info_helper
    obj_info = obj_info_helper.get_or_insert_obj(obj.name)
    t_pose_matrices = compute_hierarchical_t_pose(obj, ctx.scene, is_retarget=True)
    for idx, bone in enumerate(map_bones):
        if bone is None or idx == -1 or idx in (10, 11, 22, 23):
            if idx == 0:  # hip must bind!!!
                break
            continue
        bone_name = bone.name
        bone_info = obj_info.get_or_insert_bone(bone_name)
        data_bone = obj.data.bones.get(map_bones_names[idx])
        a2t_quat = get_a2t_quat_for_node_idx(ctx.scene, idx)
        virtual_rest_to_world = obj.matrix_world.to_quaternion() @ t_pose_matrices[bone_name].to_quaternion()
        virtual_rest_from_world = virtual_rest_to_world.inverted()

        rotation_quaternion = []
        t = []
        for fn, frame in enumerate(record_list):
            t.append((frame[3] - begin_t) / dt + 1)
            pose = all_pose_list[fn][idx]
            mocap_delta_T = virtual_rest_from_world @ pose @ virtual_rest_to_world
            rotation_quaternion.append(a2t_quat @ mocap_delta_T)
        data_path = 'pose.bones["%s"].rotation_quaternion' % bone.name
        for axis_i in range(4):
            curve = _action_fcurve_new(action, data_path, index=axis_i)
            keyframe_points = curve.keyframe_points
            frame_count = len(rotation_quaternion)
            keyframe_points.add(frame_count)
            for i, rotation_quaternion_item in enumerate(rotation_quaternion):
                keyframe_points[i].co = (
                    t[i],
                    rotation_quaternion_item[axis_i]
                )
        if idx == 0 and obj_info.root_bone is not None:
            bone = obj_info.root_bone
            data_path = 'pose.bones["%s"].location' % bone.name
            all_trans_new = []
            keep_pos = getattr(ctx.scene, 'rebocap_keep_character_position', False)
            if keep_pos and len(record_list) > 0:
                first_trans = record_list[0][0]
                init_mocap_trans = Vector((first_trans[0], first_trans[1], first_trans[2]))
                init_root_loc = cached_initial_pose.get(bone.name, (Vector((0.0, 0.0, 0.0)), None, None))[0] if cached_initial_pose else Vector((0.0, 0.0, 0.0))
                root_bone_data = obj.data.bones.get(bone.name)
                world_to_root_rot = (obj.matrix_world.to_quaternion() @ root_bone_data.matrix_local.to_quaternion()).inverted()
                for i, frame in enumerate(record_list):
                    trans = frame[0]
                    delta_trans = Vector((trans[0], trans[1], trans[2])) - init_mocap_trans
                    local_delta = world_to_root_rot @ delta_trans
                    all_trans_new.append(init_root_loc + local_delta)
            else:
                for i, frame in enumerate(record_list):
                    trans = frame[0]
                    origin_global_hip_trans = Vector((trans[0], trans[1], trans[2]))
                    new_global_hip: Matrix = obj_info.matrix_global_hip.copy()
                    new_global_hip.translation = origin_global_hip_trans
                    new_local_matrix = obj_info.matrix_global_2_root_inverse @ new_global_hip @ obj_info.matrix_root_2_hip_inverse
                    all_trans_new.append(new_local_matrix.translation)
            for axis_i in range(3):
                curve = _action_fcurve_new(action, data_path, index=axis_i)
                keyframe_points = curve.keyframe_points
                frame_count = len(record_list)
                keyframe_points.add(frame_count)
                for i, frame in enumerate(record_list):
                    keyframe_points[i].co = (
                        t[i],
                        all_trans_new[i][axis_i]
                    )
    for cu in _action_iter_fcurves(action):
        for bez in cu.keyframe_points:
            bez.interpolation = 'LINEAR'
            
    obj.animation_data.action = action
    if hasattr(obj.animation_data, 'action_slot') and hasattr(action, 'slots') and len(action.slots) > 0:
        obj.animation_data.action_slot = action.slots[0]
        
    return action

def stop_record(ctx):
    if ctx.scene.recording is False:
        return
    ctx.scene.recording = False
    global rebocap_app
    record_list = rebocap_app.stop_record()
    if not record_list or len(record_list) == 0:
        return
        
    import uuid
    take_id = str(uuid.uuid4())[:8]
    begin_t = record_list[0][3]
    
    ctx.scene.rebocap_record_counter += 1
    counter = ctx.scene.rebocap_record_counter
    
    source_obj = bpy.data.objects.get(ctx.scene.rebocap_source_armature)
    has_fk = source_obj is not None and source_obj.type == 'ARMATURE'
    has_ik = bpy.data.objects.get("Rebocap_Pelvis") is not None
    
    if not has_fk and not has_ik:
        has_ik = True
        
    frame_count = len(record_list)
        
    if has_fk:
        take_name = f"Take_FK_{counter}"
        action_fk = stop_record_retarget(ctx, record_list, source_obj, take_id, take_name)
        
        take = ctx.scene.rebocap_takes.add()
        take.name = take_name
        take.take_type = 'FK'
        take.action_fk = action_fk
        take.fk_uuid = take_id
        take.frame_count = len(record_list)
        take.recorded_fps = 60.0
        ctx.scene.rebocap_active_take_index = len(ctx.scene.rebocap_takes) - 1

    if has_ik and not has_fk:
        take_name = f"Take_IK_{counter}"
        stop_record_ik_tracking(ctx, record_list, begin_t, take_id, take_name)
        
        take = ctx.scene.rebocap_takes.add()
        take.name = take_name
        take.take_type = 'IK'
        take.ik_uuid = take_id
        take.frame_count = len(record_list)
        take.recorded_fps = 60.0
        ctx.scene.rebocap_active_take_index = len(ctx.scene.rebocap_takes) - 1

    if has_fk or has_ik:
        ctx.scene.rebocap_has_new_take = True

    source_obj = bpy.data.objects.get(ctx.scene.rebocap_source_armature)
    if source_obj is None or source_obj.type != 'ARMATURE':
        return




def force_disconnect():
    global rebocap_app, rebocap_connected, rebocap_timer, obj_info_helper
    if rebocap_app:
        try:
            rebocap_app.close()
        except:
            pass
    if rebocap_timer:
        try:
            bpy.context.window_manager.event_timer_remove(rebocap_timer)
        except:
            pass
    rebocap_timer = None
    rebocap_connected = False
    obj_info_helper = ObjInfoHelper()

class RebocapDisconnect(bpy.types.Operator):
    bl_idname = 'rebocap.disconnect'
    bl_label = 'Disconnect'

    def execute(self, ctx):
        # 【多国语言防卡死拦截】：如果处于录像中，直接拦截阻止断开
        if getattr(ctx.scene, 'recording', False):
            lang = bpy.context.preferences.view.language
            if lang == 'zh_CN':
                msg = "您正在录制！请先点击【Stop Record】完成烘焙，然后再断开连接。"
            elif lang == 'zh_TW':
                msg = "您正在錄製！請先點擊【Stop Record】完成烘焙，然後再斷開連接。"
            elif lang == 'ja_JP':
                msg = "録画中です！先に[Stop Record]をクリックしてベイクを完了させてから切断してください。"
            elif lang == 'ko_KR':
                msg = "녹화 중입니다! 먼저 [Stop Record]를 클릭하여 베이크를 완료한 후 연결을 해제하세요."
            else:
                msg = "Recording! Please click [Stop Record] to finish baking before disconnecting."

            self.report({'WARNING'}, msg)
            show_message_box(message=msg, icon='ERROR')
            return {'CANCELLED'}
            
        ctx.scene.open = False
        force_disconnect()
        return {'FINISHED'}


class RebocapStartRecord(bpy.types.Operator):
    bl_idname = 'rebocap.start_record'
    bl_label = 'Start Record'

    def execute(self, ctx):
        global rebocap_app
        rebocap_app.start_record()
        ctx.scene.recording = True
        
        for obj in bpy.context.scene.objects:
            is_target = obj.type == 'ARMATURE'
            if obj.name.startswith("Rebocap_"):
                is_target = True
                
            if is_target and obj.animation_data:
                obj.animation_data.action = None
                if hasattr(obj.animation_data, 'action_slot'):
                    try:
                        obj.animation_data.action_slot = None
                    except:
                        pass
                        
        ctx.scene.frame_set(1)
        force_start_animation(ctx)
            
        return {'FINISHED'}


class RebocapStopRecord(bpy.types.Operator):
    bl_idname = 'rebocap.stop_record'
    bl_label = 'Stop Record'

    def execute(self, ctx):
        # 强制安全停止联动时间轴
        force_stop_animation(ctx)
            
        stop_record(ctx)
        
        return {'FINISHED'}


class RebocapRestorePose(bpy.types.Operator):
    bl_idname = 'rebocap.restore_pose'
    bl_label = 'Restore Pose'
    bl_description = 'Restore the character to the temporary pose it had before connection'

    def execute(self, ctx):
        from mathutils import Vector, Quaternion, Euler
        
        # Clear active actions so the restored pose isn't overridden
        for obj in bpy.context.scene.objects:
            is_target = obj.type == 'ARMATURE' or obj.name.startswith("Rebocap_")
            if is_target and obj.animation_data:
                obj.animation_data.action = None
                if hasattr(obj.animation_data, 'action_slot'):
                    try:
                        obj.animation_data.action_slot = None
                    except:
                        pass

        # 1. Restore FK source armature to clean T-Pose / Rest Pose
        source_obj = bpy.data.objects.get(ctx.scene.rebocap_source_armature)
        if source_obj and source_obj.type == 'ARMATURE':
            for pb in source_obj.pose.bones:
                pb.location = Vector((0.0, 0.0, 0.0))
                pb.rotation_quaternion = Quaternion((1.0, 0.0, 0.0, 0.0))
                pb.rotation_euler = Euler((0.0, 0.0, 0.0))
                pb.scale = Vector((1.0, 1.0, 1.0))
            
            # If A2T calibration is enabled, apply calibrated T-Pose offsets
            a2t = getattr(ctx.scene, 'rebocap_a2t', None)
            if a2t and a2t.enable_a2t:
                try:
                    from ..core.a2t_types import apply_a2t_preview_to_armature
                    apply_a2t_preview_to_armature(ctx.scene)
                except Exception as e:
                    print(f"A2T restore error: {e}")
                    
        # 2. Restore IK Tracking nodes (Rebocap_*)
        for obj in bpy.context.scene.objects:
            if obj.name.startswith("Rebocap_") and obj.type == 'EMPTY':
                obj.rotation_quaternion = Quaternion((1.0, 0.0, 0.0, 0.0))
                obj.rotation_euler = Euler((0.0, 0.0, 0.0))
                if obj.name == "Rebocap_Pelvis":
                    obj.location.x = 0.0
                    obj.location.y = 0.0

        # 3. Force viewport update
        try:
            ctx.view_layer.update()
            wm = getattr(ctx, 'window_manager', None) or bpy.context.window_manager
            if wm:
                for window in wm.windows:
                    for area in window.screen.areas:
                        if area.type == 'VIEW_3D':
                            area.tag_redraw()
        except Exception:
            pass

        return {'FINISHED'}