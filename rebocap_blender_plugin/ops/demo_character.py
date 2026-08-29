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


def setup_demo_character_fk_translation(arm_obj):
    """
    100% 复刻上位机 3D 预览器（Rebocap3D.exe）底层渲染架构：
    1. FBX 静止基准（Edit Bones）保持 100% 原始不变（保证基准绑定矩阵纯净）。
    2. 全身骨骼缩放严格锁定为 (1.0, 1.0, 1.0)，绝不使用缩放，杜绝任何尖刺与形变。
    3. 不添加任何外部约束（Constraints），杜绝任何轴向强行扭曲。
    4. 纯粹在前向运动学（FK）骨骼树上，将每个子关节沿着父骨骼局部轴向平移身形差值（Delta L），
       实现与上位机 OpenGL 线性蒙皮着色器 1:1 像素级的自然肢体伸缩。
    """
    if not arm_obj or arm_obj.type != 'ARMATURE':
        return

    # 1. 彻底清除所有约束，重置缩放与位移
    for pb in arm_obj.pose.bones:
        pb.scale = (1.0, 1.0, 1.0)
        pb.location = Vector((0.0, 0.0, 0.0))
        for c in list(pb.constraints):
            pb.constraints.remove(c)

    def get_node_dist(n1, n2):
        o1 = bpy.data.objects.get(n1)
        o2 = bpy.data.objects.get(n2)
        if o1 and o2:
            return (o2.matrix_world.translation - o1.matrix_world.translation).length
        return None

    # 2. 骨盆（Hips）对齐 Pelvis 世界高度（实现双脚贴地）
    pelvis_node = bpy.data.objects.get('Rebocap_Pelvis')
    hip_pb = arm_obj.pose.bones.get('mixamorig:Hips')
    hip_db = arm_obj.data.bones.get('mixamorig:Hips')
    if pelvis_node and hip_pb and hip_db:
        z_diff = pelvis_node.matrix_world.translation.z - (arm_obj.matrix_world @ hip_db.head).z
        hip_pb.location = hip_db.matrix_local.to_3x3().inverted() @ Vector((0.0, 0.0, z_diff))

    # 3. 骨骼树前向运动学轴向平移映射表：(子骨骼, 父骨骼, 对应起点追踪点, 对应终点追踪点)
    fk_translations = [
        # 下半身腿部
        ('mixamorig:LeftLeg', 'mixamorig:LeftUpLeg', 'Rebocap_L_Upper_leg', 'Rebocap_L_Lower_leg'),
        ('mixamorig:RightLeg', 'mixamorig:RightUpLeg', 'Rebocap_R_Upper_leg', 'Rebocap_R_Lower_leg'),
        ('mixamorig:LeftFoot', 'mixamorig:LeftLeg', 'Rebocap_L_Lower_leg', 'Rebocap_L_Foot'),
        ('mixamorig:RightFoot', 'mixamorig:RightLeg', 'Rebocap_R_Lower_leg', 'Rebocap_R_Foot'),
        # 躯干与脊椎
        ('mixamorig:Spine', 'mixamorig:Hips', 'Rebocap_Pelvis', 'Rebocap_Spine1'),
        ('mixamorig:Spine1', 'mixamorig:Spine', 'Rebocap_Spine1', 'Rebocap_Spine2'),
        ('mixamorig:Spine2', 'mixamorig:Spine1', 'Rebocap_Spine2', 'Rebocap_Spine3'),
        ('mixamorig:Neck', 'mixamorig:Spine2', 'Rebocap_Spine3', 'Rebocap_Neck'),
        ('mixamorig:Head', 'mixamorig:Neck', 'Rebocap_Neck', 'Rebocap_Head'),
        # 上半身手臂
        ('mixamorig:LeftArm', 'mixamorig:LeftShoulder', 'Rebocap_L_Shoulder', 'Rebocap_L_Upper_arm'),
        ('mixamorig:RightArm', 'mixamorig:RightShoulder', 'Rebocap_R_Shoulder', 'Rebocap_R_Upper_arm'),
        ('mixamorig:LeftForeArm', 'mixamorig:LeftArm', 'Rebocap_L_Upper_arm', 'Rebocap_L_Lower_arm'),
        ('mixamorig:RightForeArm', 'mixamorig:RightArm', 'Rebocap_R_Upper_arm', 'Rebocap_R_Lower_arm'),
        ('mixamorig:LeftHand', 'mixamorig:LeftForeArm', 'Rebocap_L_Lower_arm', 'Rebocap_L_Hand'),
        ('mixamorig:RightHand', 'mixamorig:RightForeArm', 'Rebocap_R_Lower_arm', 'Rebocap_R_Hand'),
    ]

    for child_name, parent_name, n1, n2 in fk_translations:
        child_pb = arm_obj.pose.bones.get(child_name)
        child_db = arm_obj.data.bones.get(child_name)
        parent_db = arm_obj.data.bones.get(parent_name)
        target_len = get_node_dist(n1, n2)
        
        if child_pb and child_db and parent_db and target_len is not None:
            base_len = parent_db.length
            delta = target_len - base_len
            # 父骨骼在 Armature 空间中的主轴向向量
            parent_axis = (parent_db.tail_local - parent_db.head_local).normalized()
            # 在 Armature 空间中的平移矢量
            armature_delta = parent_axis * delta
            # 严格转换至子骨骼的局部坐标系
            child_local_delta = child_db.matrix_local.to_3x3().inverted() @ armature_delta
            child_pb.location = child_local_delta

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

            # 2. 100% 复刻上位机 3D 预览器架构（纯 FK 局部轴向平移自适应）
            setup_demo_character_fk_translation(armature_obj)

            self.report({'INFO'}, "示范角色已载入并完成上位机 1:1 纯 FK 架构自适应")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "未能在导入的模型中找到骨架")
            return {'FINISHED'}
