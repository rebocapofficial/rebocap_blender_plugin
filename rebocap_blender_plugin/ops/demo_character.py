import os
import bpy
from mathutils import Vector, Quaternion, Euler
from ..core.translation import T, T_static
from .ik_tracking import parse_and_update_ik_config, find_rebocap_config_path


def get_demo_character_armature():
    for obj in bpy.data.objects:
        if obj.get("rebocap_demo_character") and obj.type == 'ARMATURE':
            return obj
    return None


def get_demo_character_meshes():
    return [obj for obj in bpy.data.objects if obj.get("rebocap_demo_character") and obj.type == 'MESH']


def is_demo_character_present():
    return any(obj.get("rebocap_demo_character") for obj in bpy.data.objects)


def remove_demo_character():
    to_remove = []
    for obj in list(bpy.data.objects):
        if obj.get("rebocap_demo_character"):
            to_remove.append(obj)
            
    for obj in to_remove:
        mesh_data = obj.data if obj.type == 'MESH' else None
        arm_data = obj.data if obj.type == 'ARMATURE' else None
        bpy.data.objects.remove(obj, do_unlink=True)
        if mesh_data and mesh_data.users == 0:
            bpy.data.meshes.remove(mesh_data, do_unlink=True)
        if arm_data and arm_data.users == 0:
            bpy.data.armatures.remove(arm_data, do_unlink=True)


def adapt_demo_character_scale_isolated(arm_obj):
    """
    改版方案一：独立等比缩放隔离法（Proportional 3D Limb Scaling with Scale Isolation）
    1. 在姿态模式下，强制全身所有骨骼的 inherit_scale = 'NONE'，彻底切断父级缩放的级联传递；
    2. 肢体粗细与长短同步等比收放（scale = (ratio, ratio, ratio)），彻底消除单向压扁带来的水肿矮胖感；
    3. 手指（HandIndex1~4）、头顶（HeadTop_End）、脚尖等末端骨骼严格锁定为 (1.0, 1.0, 1.0)，0 避雷针尖刺、0 畸变；
    4. 骨盆（Hips）高度下沉对齐 Pelvis 追踪点，实现双脚踩实地面；
    5. 全程非破坏性纯姿态层计算，FBX 原始网格与绑定骨架 100% 纯净无损。
    """
    if not arm_obj or arm_obj.type != 'ARMATURE':
        return

    # 1. 彻底清除所有约束，重置位移、旋转与缩放，并对所有子骨骼切断缩放继承
    for pb in arm_obj.pose.bones:
        pb.scale = (1.0, 1.0, 1.0)
        pb.location = Vector((0.0, 0.0, 0.0))
        pb.rotation_quaternion = Quaternion((1.0, 0.0, 0.0, 0.0))
        pb.rotation_euler = (0.0, 0.0, 0.0)
        for c in list(pb.constraints):
            pb.constraints.remove(c)
        if pb.parent:
            pb.bone.inherit_scale = 'NONE'

    # 2. 脚部骨骼长宽独立精准自适应（X轴横向加宽15%增强饱满度与包裹感，Y/Z轴等比保持脚掌水平贴地）
    sole_obj = bpy.data.objects.get('Rebocap_L_Sole')
    s_len = 1.0
    s_width = 1.0
    if sole_obj:
        pts = [sole_obj.matrix_world @ v.co for v in sole_obj.data.vertices]
        if len(pts) >= 7:
            w_target = max(v.x for v in pts) - min(v.x for v in pts)
            l_target = (pts[1] - pts[4]).length
            s_width = max(min((w_target / 0.1438) * 1.15, 3.0), 0.1)
            s_len = max(min(l_target / 0.2961, 3.0), 0.1)
            
    for side in ['Left', 'Right']:
        foot_pb = arm_obj.pose.bones.get(f'mixamorig:{side}Foot')
        toe_pb = arm_obj.pose.bones.get(f'mixamorig:{side}ToeBase')
        if foot_pb:
            foot_pb.scale = (s_width, s_len, s_len)
        if toe_pb:
            toe_pb.scale = (s_width, s_len, s_len)

    # 3. 大腿与小腿三维等比适配（消除脚底悬空与膝盖错位）
    node_knee = bpy.data.objects.get('Rebocap_L_Lower_leg')
    node_thigh = bpy.data.objects.get('Rebocap_L_Upper_leg')
    if node_knee and node_thigh:
        current_ankle_h = 0.0928 * s_len
        target_calf_len = max(0.05, (node_knee.matrix_world.translation - Vector((node_knee.matrix_world.translation.x, node_knee.matrix_world.translation.y, current_ankle_h))).length)
        target_thigh_len = (node_knee.matrix_world.translation - node_thigh.matrix_world.translation).length
        
        for side in ['Left', 'Right']:
            up_leg_pb = arm_obj.pose.bones.get(f'mixamorig:{side}UpLeg')
            leg_pb = arm_obj.pose.bones.get(f'mixamorig:{side}Leg')
            if up_leg_pb and up_leg_pb.bone.length > 0.001:
                ratio_thigh = target_thigh_len / up_leg_pb.bone.length
                up_leg_pb.scale = (ratio_thigh, ratio_thigh, ratio_thigh)
            if leg_pb and leg_pb.bone.length > 0.001:
                ratio_calf = target_calf_len / leg_pb.bone.length
                leg_pb.scale = (ratio_calf, ratio_calf, ratio_calf)

    # 4. 骨盆（Hips）大腿根关节中心精准对位与胯宽对齐
    node_l_thigh = bpy.data.objects.get('Rebocap_L_Upper_leg')
    node_r_thigh = bpy.data.objects.get('Rebocap_R_Upper_leg')
    hip_pb = arm_obj.pose.bones.get('mixamorig:Hips')
    hip_db = arm_obj.data.bones.get('mixamorig:Hips')
    l_thigh_db = arm_obj.data.bones.get('mixamorig:LeftUpLeg')
    r_thigh_db = arm_obj.data.bones.get('mixamorig:RightUpLeg')

    if node_l_thigh and node_r_thigh and hip_pb and hip_db and l_thigh_db and r_thigh_db:
        target_thigh_center = (node_l_thigh.matrix_world.translation + node_r_thigh.matrix_world.translation) * 0.5
        base_thigh_center = (l_thigh_db.head_local + r_thigh_db.head_local) * 0.5
        diff_world = target_thigh_center - base_thigh_center
        hip_pb.location = hip_db.matrix_local.to_3x3().inverted() @ diff_world

        target_hip_w = (node_l_thigh.matrix_world.translation - node_r_thigh.matrix_world.translation).length
        base_hip_w = (l_thigh_db.head - r_thigh_db.head).length
        if base_hip_w > 0.001:
            hip_pb.scale.x = target_hip_w / base_hip_w

    # 5. 脊椎段与肩膀高度精准对齐（消除手臂下垂偏矮问题）
    node_shoulder = bpy.data.objects.get('Rebocap_L_Upper_arm')
    if node_shoulder and node_l_thigh and node_r_thigh:
        target_thigh_center = (node_l_thigh.matrix_world.translation + node_r_thigh.matrix_world.translation) * 0.5
        t_torso_h = node_shoulder.matrix_world.translation.z - target_thigh_center.z
        spine_ratio = max(min(t_torso_h / 0.4215, 3.0), 0.1)
        
        spine_bones = ['mixamorig:Spine', 'mixamorig:Spine1', 'mixamorig:Spine2']
        for s in spine_bones:
            pb = arm_obj.pose.bones.get(s)
            if pb:
                pb.scale = (spine_ratio, spine_ratio, spine_ratio)
        neck_pb = arm_obj.pose.bones.get('mixamorig:Neck')
        head_pb = arm_obj.pose.bones.get('mixamorig:Head')
        if neck_pb:
            neck_pb.scale = (spine_ratio, spine_ratio, spine_ratio)
        if head_pb:
            head_pb.scale = (spine_ratio, spine_ratio, spine_ratio)

    # 6. 上肢各段骨骼等比拉伸（锁骨、大臂、小臂）
    for sh_name, arm_name, fa_name, side in [
        ('mixamorig:LeftShoulder', 'mixamorig:LeftArm', 'mixamorig:LeftForeArm', 'L'),
        ('mixamorig:RightShoulder', 'mixamorig:RightArm', 'mixamorig:RightForeArm', 'R')]:
        sh_pb = arm_obj.pose.bones.get(sh_name)
        arm_pb = arm_obj.pose.bones.get(arm_name)
        fa_pb = arm_obj.pose.bones.get(fa_name)
        node_sh = bpy.data.objects.get(f'Rebocap_{side}_Shoulder')
        node_ua = bpy.data.objects.get(f'Rebocap_{side}_Upper_arm')
        node_la = bpy.data.objects.get(f'Rebocap_{side}_Lower_arm')
        node_hd = bpy.data.objects.get(f'Rebocap_{side}_Hand')
        
        if sh_pb and node_sh and node_ua and sh_pb.bone.length > 0.001:
            sh_len = (node_ua.matrix_world.translation - node_sh.matrix_world.translation).length
            sh_pb.scale = (sh_len / sh_pb.bone.length, sh_len / sh_pb.bone.length, sh_len / sh_pb.bone.length)
        if arm_pb and node_ua and node_la and arm_pb.bone.length > 0.001:
            ua_len = (node_la.matrix_world.translation - node_ua.matrix_world.translation).length
            arm_pb.scale = (ua_len / arm_pb.bone.length, ua_len / arm_pb.bone.length, ua_len / arm_pb.bone.length)
        if fa_pb and node_la and node_hd and fa_pb.bone.length > 0.001:
            la_len = (node_hd.matrix_world.translation - node_la.matrix_world.translation).length
            fa_pb.scale = (la_len / fa_pb.bone.length, la_len / fa_pb.bone.length, la_len / fa_pb.bone.length)

    # 7. 隐藏骨骼线框显示，保持角色表面光洁，并记录基准贴地坐标与静止骨盆高供实时驱动增量使用
    arm_obj.data.display_type = 'WIRE'
    arm_obj.show_in_front = False
    if hip_pb:
        arm_obj['rebocap_adapted_hip_location'] = list(hip_pb.location)
    node_pelvis = bpy.data.objects.get('Rebocap_Pelvis')
    if node_pelvis:
        arm_obj['rebocap_rest_pelvis_z'] = float(node_pelvis.matrix_world.translation.z)

    bpy.context.view_layer.update()


class REBOCAP_OT_offset_demo_character(bpy.types.Operator):
    bl_idname = "rebocap.offset_demo_character"
    bl_label = T_static("偏移示范角色")
    bl_description = T_static("左右移动示范角色水平位置")
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.StringProperty(default='SET')
    offset_x: bpy.props.FloatProperty(default=0.0)

    def execute(self, context):
        arm = get_demo_character_armature()
        if not arm:
            self.report({'WARNING'}, "未找到示范角色")
            return {'CANCELLED'}
        if self.mode == 'SET':
            arm.location.x = self.offset_x
        elif self.mode == 'ADD':
            arm.location.x += self.offset_x
        context.view_layer.update()
        return {'FINISHED'}


class REBOCAP_OT_toggle_demo_character(bpy.types.Operator):
    bl_idname = "rebocap.toggle_demo_character"
    bl_label = T_static("导入示范角色")
    bl_description = T_static("一键导入/移除示范角色")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if is_demo_character_present():
            remove_demo_character()
            self.report({'INFO'}, "已移除示范角色")
            return {'FINISHED'}

        addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fbx_path = os.path.join(addon_dir, 'assets', 'rebo_robot.fbx')
        
        if not os.path.exists(fbx_path):
            self.report({'ERROR'}, f"未找到示范角色模型文件: {fbx_path}")
            return {'CANCELLED'}

        # 确保场景中已有追踪节点数据
        if not bpy.data.objects.get('Rebocap_Pelvis'):
            try:
                rebocap = context.scene.rebocap_bone_map
                if rebocap.sk_upper_leg <= 0.001:
                    cfg_path = rebocap.ik_config_path or find_rebocap_config_path()
                    if cfg_path and os.path.exists(cfg_path):
                        parse_and_update_ik_config(cfg_path, rebocap, None)
                bpy.ops.rebocap.create_tracking_nodes()
                bpy.context.view_layer.update()
            except Exception as e:
                print(f"[Rebocap] auto generate tracking nodes notice: {e}")

        # 确保处于物体模式，防止在姿态/编辑模式下导入报错
        if context.object and context.object.mode != 'OBJECT':
            try:
                bpy.ops.object.mode_set(mode='OBJECT')
            except Exception:
                pass

        # 取消选择场景已有物体
        for obj in list(context.selected_objects):
            obj.select_set(False)

        try:
            bpy.ops.import_scene.fbx(filepath=fbx_path)
        except Exception as e:
            self.report({'ERROR'}, f"导入示范角色失败: {e}")
            return {'CANCELLED'}

        imported_objs = list(context.selected_objects)
        armature_obj = None
        mesh_objs = []

        for obj in imported_objs:
            obj["rebocap_demo_character"] = True
            if obj.type == 'ARMATURE':
                armature_obj = obj
                obj.name = "Rebo_Official_Demo_Character"
            elif obj.type == 'MESH':
                mesh_objs.append(obj)
                obj.name = "Rebo_Official_Demo_Mesh"

        if armature_obj:
            # 1. 统一应用旋转与缩放变换，保证模型以标准 1.0 比例直立在世界空间
            bpy.ops.object.select_all(action='DESELECT')
            armature_obj.select_set(True)
            for m in mesh_objs:
                m.select_set(True)
            context.view_layer.objects.active = armature_obj
            
            try:
                area = None
                window = None
                for w in context.window_manager.windows:
                    for a in w.screen.areas:
                        if a.type == 'VIEW_3D':
                            area = a
                            window = w
                            break
                    if area: break
                    
                if hasattr(context, "temp_override") and area:
                    with context.temp_override(window=window, area=area):
                        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                else:
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            except Exception as e:
                print(f"[Rebocap] transform_apply notice: {e}")
                
            bpy.context.view_layer.update()

            # 2. 执行改版方案一（独立缩放隔离法自适应）
            adapt_demo_character_scale_isolated(armature_obj)

            # 3. 默认偏开右侧 2m，避免遮挡中心的主模型或追踪节点
            armature_obj.location.x = 2.0
            bpy.context.view_layer.update()

            self.report({'INFO'}, "示范角色已成功载入（默认偏开右侧 2m）")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "未能在导入的模型中找到骨架")
            return {'FINISHED'}
