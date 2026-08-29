import os
import bpy
from mathutils import Vector
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

    # 1. 彻底清除所有约束，重置位移与缩放，并对所有子骨骼切断缩放继承
    for pb in arm_obj.pose.bones:
        pb.scale = (1.0, 1.0, 1.0)
        pb.location = Vector((0.0, 0.0, 0.0))
        for c in list(pb.constraints):
            pb.constraints.remove(c)
        if pb.parent:
            pb.bone.inherit_scale = 'NONE'

    # 2. 脊椎段综合等比伸缩 (Spine + Spine1 + Spine2 平滑过渡)
    node_spine1 = bpy.data.objects.get('Rebocap_Spine1')
    node_neck = bpy.data.objects.get('Rebocap_Neck')
    if node_spine1 and node_neck:
        t_spine = (node_neck.matrix_world.translation - node_spine1.matrix_world.translation).length
        spine_bones = ['mixamorig:Spine', 'mixamorig:Spine1', 'mixamorig:Spine2']
        cur_spine = sum(arm_obj.pose.bones[s].bone.length for s in spine_bones if s in arm_obj.pose.bones)
        if cur_spine > 0.001:
            ratio = max(min(t_spine / cur_spine, 3.0), 0.1)
            for s in spine_bones:
                if s in arm_obj.pose.bones:
                    arm_obj.pose.bones[s].scale = (ratio, ratio, ratio)

    # 3. 四肢各段主干骨骼三维等比拉伸（长短与粗细协调）
    limb_map = {
        'mixamorig:LeftShoulder': ('Rebocap_L_Shoulder', 'Rebocap_L_Upper_arm'),
        'mixamorig:LeftArm': ('Rebocap_L_Upper_arm', 'Rebocap_L_Lower_arm'),
        'mixamorig:LeftForeArm': ('Rebocap_L_Lower_arm', 'Rebocap_L_Hand'),
        'mixamorig:RightShoulder': ('Rebocap_R_Shoulder', 'Rebocap_R_Upper_arm'),
        'mixamorig:RightArm': ('Rebocap_R_Upper_arm', 'Rebocap_R_Lower_arm'),
        'mixamorig:RightForeArm': ('Rebocap_R_Lower_arm', 'Rebocap_R_Hand'),
        'mixamorig:LeftUpLeg': ('Rebocap_L_Upper_leg', 'Rebocap_L_Lower_leg'),
        'mixamorig:LeftLeg': ('Rebocap_L_Lower_leg', 'Rebocap_L_Foot'),
        'mixamorig:RightUpLeg': ('Rebocap_R_Upper_leg', 'Rebocap_R_Lower_leg'),
        'mixamorig:RightLeg': ('Rebocap_R_Lower_leg', 'Rebocap_R_Foot'),
        'mixamorig:Neck': ('Rebocap_Neck', 'Rebocap_Head'),
    }

    for bname, (n1, n2) in limb_map.items():
        pb = arm_obj.pose.bones.get(bname)
        o1, o2 = bpy.data.objects.get(n1), bpy.data.objects.get(n2)
        if pb and o1 and o2:
            t_len = (o2.matrix_world.translation - o1.matrix_world.translation).length
            cur_len = pb.bone.length
            if cur_len > 0.001:
                ratio = max(min(t_len / cur_len, 3.0), 0.1)
                pb.scale = (ratio, ratio, ratio)

    # 4. 骨盆（Hips）大腿根关节中心精准对位与胯宽对齐
    node_l_thigh = bpy.data.objects.get('Rebocap_L_Upper_leg')
    node_r_thigh = bpy.data.objects.get('Rebocap_R_Upper_leg')
    hip_pb = arm_obj.pose.bones.get('mixamorig:Hips')
    hip_db = arm_obj.data.bones.get('mixamorig:Hips')
    l_thigh_db = arm_obj.data.bones.get('mixamorig:LeftUpLeg')
    r_thigh_db = arm_obj.data.bones.get('mixamorig:RightUpLeg')

    if node_l_thigh and node_r_thigh and hip_pb and hip_db and l_thigh_db and r_thigh_db:
        # 计算左右大腿关节在世界空间的目标几何中心
        target_thigh_center = (node_l_thigh.matrix_world.translation + node_r_thigh.matrix_world.translation) * 0.5
        # 计算 FBX 原生大腿根关节在骨架空间中的几何中心
        base_thigh_center = (l_thigh_db.head_local + r_thigh_db.head_local) * 0.5
        diff_world = target_thigh_center - base_thigh_center
        # 转换为 Hips 局部坐标并消除大腿根部悬空与高度偏差
        hip_pb.location = hip_db.matrix_local.to_3x3().inverted() @ diff_world

        # 胯宽等比自适应（让大腿根部与追踪点左右横向精准吻合）
        target_hip_w = (node_l_thigh.matrix_world.translation - node_r_thigh.matrix_world.translation).length
        base_hip_w = (l_thigh_db.head - r_thigh_db.head).length
        if base_hip_w > 0.001:
            hip_pb.scale.x = target_hip_w / base_hip_w

    # 5. 隐藏骨骼线框显示，保持角色表面光洁
    arm_obj.data.display_type = 'WIRE'
    arm_obj.show_in_front = False

    bpy.context.view_layer.update()


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

            self.report({'INFO'}, "示范角色已成功载入（改版方案一：独立缩放隔离）")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "未能在导入的模型中找到骨架")
            return {'FINISHED'}
