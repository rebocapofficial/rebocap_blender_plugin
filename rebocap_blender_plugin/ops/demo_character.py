import os
import bpy
from mathutils import Vector, Matrix, Quaternion
from ..core.translation import T, T_static


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


def update_demo_character_offset(self, context):
    arm = get_demo_character_armature()
    if not arm:
        return
    preset = getattr(context.scene, 'rebocap_demo_preset', 'SIDE_R')
    if preset == 'SIDE_R':
        arm.location = Vector((1.2, 0.0, 0.0))
    elif preset == 'SIDE_L':
        arm.location = Vector((-1.2, 0.0, 0.0))
    elif preset == 'CENTER':
        arm.location = Vector((0.0, 0.0, 0.0))


def adapt_demo_character_bone_lengths(arm_obj):
    """
    基于上位机 Rebocap3D (PoseDriver) 原理：
    在 Pose Mode 中通过 Y 轴局部比例缩放（Pose Bone Scale）自适应骨骼长短，
    使示范角色四肢关节与骨架追踪点 1:1 物理重合，
    同时保持 Edit Bones 完整不被破坏，确保骨骼轴向与旋转绝对正确。
    """
    if not arm_obj or arm_obj.type != 'ARMATURE':
        return
        
    bone_node_map = {
        'mixamorig:Hips': ('Rebocap_Pelvis', 'Rebocap_Spine1'),
        'mixamorig:LeftUpLeg': ('Rebocap_L_Upper_leg', 'Rebocap_L_Lower_leg'),
        'mixamorig:RightUpLeg': ('Rebocap_R_Upper_leg', 'Rebocap_R_Lower_leg'),
        'mixamorig:LeftLeg': ('Rebocap_L_Lower_leg', 'Rebocap_L_Foot'),
        'mixamorig:RightLeg': ('Rebocap_R_Lower_leg', 'Rebocap_R_Foot'),
        'mixamorig:Spine': ('Rebocap_Spine1', 'Rebocap_Spine2'),
        'mixamorig:Spine1': ('Rebocap_Spine2', 'Rebocap_Spine3'),
        'mixamorig:Spine2': ('Rebocap_Spine3', 'Rebocap_Neck'),
        'mixamorig:Neck': ('Rebocap_Neck', 'Rebocap_Head'),
        'mixamorig:LeftShoulder': ('Rebocap_L_Shoulder', 'Rebocap_L_Upper_arm'),
        'mixamorig:RightShoulder': ('Rebocap_R_Shoulder', 'Rebocap_R_Upper_arm'),
        'mixamorig:LeftArm': ('Rebocap_L_Upper_arm', 'Rebocap_L_Lower_arm'),
        'mixamorig:RightArm': ('Rebocap_R_Upper_arm', 'Rebocap_R_Lower_arm'),
        'mixamorig:LeftForeArm': ('Rebocap_L_Lower_arm', 'Rebocap_L_Hand'),
        'mixamorig:RightForeArm': ('Rebocap_R_Lower_arm', 'Rebocap_R_Hand'),
    }
    
    if not bpy.data.objects.get('Rebocap_Pelvis'):
        return
        
    # 计算需要的目标长度
    target_lengths = {}
    for bname, (h_name, t_name) in bone_node_map.items():
        nh = bpy.data.objects.get(h_name)
        nt = bpy.data.objects.get(t_name)
        if nh and nt:
            target_lengths[bname] = (nt.matrix_world.translation - nh.matrix_world.translation).length

    # 1. 设置所有子骨骼为 ALIGNED 继承缩放，确保缩放只沿局部 Y 轴传递
    for pb in arm_obj.pose.bones:
        if pb.parent:
            pb.bone.inherit_scale = 'ALIGNED'
            
    arm_world_scale_y = arm_obj.matrix_world.to_scale().y
    if arm_world_scale_y < 0.0001:
        arm_world_scale_y = 1.0
            
    # 2. 递归地计算并应用累积的 Y 轴抗缩放系数
    def apply_scale(pb, cumulative_scale_y):
        if cumulative_scale_y < 0.001:
            cumulative_scale_y = 0.001
            
        if pb.name in target_lengths:
            target_len = target_lengths[pb.name]
            base_len_world = pb.bone.length * arm_world_scale_y
            
            desired_scale_y = target_len / base_len_world if base_len_world > 0.001 else 1.0
            if desired_scale_y < 0.001:
                desired_scale_y = 0.001
                
            local_scale_y = desired_scale_y / cumulative_scale_y
            pb.scale = (1.0, local_scale_y, 1.0)
            
            for child in pb.children:
                apply_scale(child, desired_scale_y)
        else:
            local_scale_y = 1.0 / cumulative_scale_y
            pb.scale = (1.0, local_scale_y, 1.0)
            
            for child in pb.children:
                apply_scale(child, 1.0)
                
    root_bones = [pb for pb in arm_obj.pose.bones if not pb.parent]
    for pb in root_bones:
        apply_scale(pb, 1.0)
        
    bpy.context.view_layer.update()


class REBOCAP_OT_toggle_demo_character(bpy.types.Operator):
    bl_idname = "rebocap.toggle_demo_character"
    bl_label = T_static("导入示范角色")
    bl_description = T_static("一键导入/移除示范角色，实时伴随动捕，不影响生产录制管线")
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
            
            # 使用针对 Blender 5.2+ 兼容的 temp_override 调用
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

            # 2. 如果场景中已有追踪节点，直接自适应骨骼长短；如果还没有，自动生成追踪点并完成对齐
            if bpy.data.objects.get('Rebocap_Pelvis'):
                adapt_demo_character_bone_lengths(armature_obj)
            else:
                try:
                    bpy.ops.rebocap.create_tracking_nodes()
                    bpy.context.view_layer.update()
                    adapt_demo_character_bone_lengths(armature_obj)
                except Exception:
                    pass

            # 3. 应用站位预设
            preset = getattr(context.scene, 'rebocap_demo_preset', 'SIDE_R')
            if preset == 'SIDE_R':
                armature_obj.location = Vector((1.2, 0.0, 0.0))
            elif preset == 'SIDE_L':
                armature_obj.location = Vector((-1.2, 0.0, 0.0))
            else:
                armature_obj.location = Vector((0.0, 0.0, 0.0))
            
            self.report({'INFO'}, "示范角色已成功载入并完成上位机骨骼身形自适应")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "未能在导入的模型中找到骨架")
            return {'FINISHED'}
