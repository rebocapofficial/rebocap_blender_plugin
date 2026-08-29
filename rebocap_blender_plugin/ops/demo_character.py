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


def adapt_demo_character_bone_stretch(arm_obj):
    """
    姿态模式下的平滑骨骼轴向伸缩（Pose Mode Stretch / Scale）：
    1. FBX 静止基准（Edit Bones）保持 100% 完整无修改，确保蒙皮权重和几何曲面永远不碎裂、不拉扯。
    2. 在姿态模式下，使各段受控骨骼（大腿、小腿、手臂、脊椎）仅沿局部 Y 轴平滑伸缩至目标长度。
    3. 子骨骼继承缩放设为 'NONE'，彻底杜绝父级缩放传递到手指和末端造成尖刺变形。
    4. 臀部（Hips）初始基准高度对齐 Pelvis 追踪点，实现双脚踩实地面。
    """
    if not arm_obj or arm_obj.type != 'ARMATURE':
        return

    # 1. 重置所有姿态骨骼，继承缩放设为 NONE，防止缩放层层叠加
    for pb in arm_obj.pose.bones:
        pb.scale = (1.0, 1.0, 1.0)
        if pb.parent:
            pb.bone.inherit_scale = 'NONE'

    # 2. 脊椎段综合伸缩 (Spine + Spine1 + Spine2 作为一个整体平滑过渡)
    node_spine1 = bpy.data.objects.get('Rebocap_Spine1')
    node_neck = bpy.data.objects.get('Rebocap_Neck')
    if node_spine1 and node_neck:
        target_spine_len = (node_neck.matrix_world.translation - node_spine1.matrix_world.translation).length
        spine_bones = ['mixamorig:Spine', 'mixamorig:Spine1', 'mixamorig:Spine2']
        base_spine_len = sum(arm_obj.pose.bones[s].bone.length for s in spine_bones if s in arm_obj.pose.bones)
        if base_spine_len > 0.001:
            spine_ratio = max(target_spine_len / base_spine_len, 0.1)
            for sname in spine_bones:
                if sname in arm_obj.pose.bones:
                    arm_obj.pose.bones[sname].scale.y = spine_ratio

    # 3. 四肢各段骨骼的独立 Y 轴自适应伸缩
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

    for bname, (h_node, t_node) in limb_map.items():
        pb = arm_obj.pose.bones.get(bname)
        nh = bpy.data.objects.get(h_node)
        nt = bpy.data.objects.get(t_node)
        if pb and nh and nt:
            target_len = (nt.matrix_world.translation - nh.matrix_world.translation).length
            base_len = pb.bone.length
            if base_len > 0.001:
                pb.scale.y = max(target_len / base_len, 0.1)

    # 4. 将 Hips 初始静止高度对齐到 Rebocap_Pelvis，消除悬空
    node_pelvis = bpy.data.objects.get('Rebocap_Pelvis')
    hip_pb = arm_obj.pose.bones.get('mixamorig:Hips')
    hip_db = arm_obj.data.bones.get('mixamorig:Hips')
    if node_pelvis and hip_pb and hip_db:
        z_offset = node_pelvis.matrix_world.translation.z - (arm_obj.matrix_world @ hip_db.head).z
        world_offset = Vector((0.0, 0.0, z_offset))
        local_offset = hip_db.matrix_local.to_3x3().inverted() @ (arm_obj.matrix_world.to_3x3().inverted() @ world_offset)
        hip_pb.location = local_offset

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

            # 2. 姿态模式下的平滑骨骼轴向伸缩自适应（确保蒙皮完整光滑）
            adapt_demo_character_bone_stretch(armature_obj)

            self.report({'INFO'}, "示范角色已载入并完成骨骼平滑伸缩对齐")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "未能在导入的模型中找到骨架")
            return {'FINISHED'}
