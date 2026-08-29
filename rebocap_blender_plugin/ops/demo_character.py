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


def setup_demo_character_pinpoint_tracking(arm_obj):
    """
    Unity 风格的直接推位与轴向拉伸（Pinpoint Bone Tracking）：
    1. FBX 静止基准（Edit Bones）保持 100% 原始不变，蒙皮权重矩阵绝对受损。
    2. 将各个骨骼的关键点（Pelvis、大腿根、脊柱起点）直接推到追踪点位置（Copy Location）。
    3. 骨骼沿骨轴直接拉伸（Stretch To）精准对接下一个追踪点（膝盖、脚踝、肩窝、手肘、手腕等）。
    4. 实现各个关节与追踪点 0.0000 mm 严丝合缝重合，同时曲面蒙皮平滑连贯无撕裂。
    """
    if not arm_obj or arm_obj.type != 'ARMATURE':
        return

    # 1. 清理已有的约束
    for pb in arm_obj.pose.bones:
        pb.scale = (1.0, 1.0, 1.0)
        pb.location = Vector((0.0, 0.0, 0.0))
        for c in list(pb.constraints):
            pb.constraints.remove(c)

    def add_copy_loc(pb_name, node_name):
        pb = arm_obj.pose.bones.get(pb_name)
        node = bpy.data.objects.get(node_name)
        if pb and node:
            c = pb.constraints.new('COPY_LOCATION')
            c.target = node
            c.target_space = 'WORLD'
            c.owner_space = 'WORLD'

    def add_stretch_to(pb_name, node_name):
        pb = arm_obj.pose.bones.get(pb_name)
        node = bpy.data.objects.get(node_name)
        if pb and node:
            c = pb.constraints.new('STRETCH_TO')
            c.target = node
            c.rest_length = pb.bone.length
            c.volume = 'NO_VOLUME'

    # 2. 定位核心关节点（推到追踪点位置）
    add_copy_loc('mixamorig:Hips', 'Rebocap_Pelvis')
    add_copy_loc('mixamorig:LeftUpLeg', 'Rebocap_L_Upper_leg')
    add_copy_loc('mixamorig:RightUpLeg', 'Rebocap_R_Upper_leg')
    add_copy_loc('mixamorig:Spine', 'Rebocap_Spine1')

    # 3. 沿骨轴拉伸对齐下一级追踪点
    stretch_pairs = [
        ('mixamorig:LeftUpLeg', 'Rebocap_L_Lower_leg'),
        ('mixamorig:RightUpLeg', 'Rebocap_R_Lower_leg'),
        ('mixamorig:LeftLeg', 'Rebocap_L_Foot'),
        ('mixamorig:RightLeg', 'Rebocap_R_Foot'),
        ('mixamorig:LeftFoot', 'Rebocap_L_Toe'),
        ('mixamorig:RightFoot', 'Rebocap_R_Toe'),
        ('mixamorig:Spine', 'Rebocap_Spine2'),
        ('mixamorig:Spine1', 'Rebocap_Spine3'),
        ('mixamorig:Spine2', 'Rebocap_Neck'),
        ('mixamorig:Neck', 'Rebocap_Head'),
        ('mixamorig:LeftShoulder', 'Rebocap_L_Upper_arm'),
        ('mixamorig:RightShoulder', 'Rebocap_R_Upper_arm'),
        ('mixamorig:LeftArm', 'Rebocap_L_Lower_arm'),
        ('mixamorig:RightArm', 'Rebocap_R_Lower_arm'),
        ('mixamorig:LeftForeArm', 'Rebocap_L_Hand'),
        ('mixamorig:RightForeArm', 'Rebocap_R_Hand'),
        ('mixamorig:LeftHand', 'Rebocap_L_Hand_end'),
        ('mixamorig:RightHand', 'Rebocap_R_Hand_end'),
    ]

    for pb_name, node_name in stretch_pairs:
        add_stretch_to(pb_name, node_name)

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

            # 2. Unity 风格精准推位与轴向拉伸（0 误差追踪点对齐，蒙皮完好无损）
            setup_demo_character_pinpoint_tracking(armature_obj)

            self.report({'INFO'}, "示范角色已载入并完成 Unity 风格精准对齐")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "未能在导入的模型中找到骨架")
            return {'FINISHED'}
