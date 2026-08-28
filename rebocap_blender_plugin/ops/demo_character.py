import os
import bpy
from mathutils import Vector, Quaternion
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


def apply_demo_character_body_shape(armature_obj, scene):
    """
    根据上位机 config.data 中的 12 项骨骼长度，
    自动调整示范角色各骨骼的 PoseBone.scale 矩阵，使其精准匹配穿戴者身材。
    """
    if not armature_obj or armature_obj.type != 'ARMATURE':
        return
        
    rebocap = getattr(scene, 'rebocap_bone_map', None)
    if not rebocap:
        return
        
    # 读取穿戴者身材参数 (若未连接则采用标准人体默认值)
    user_ua = rebocap.sk_upper_arm if rebocap.sk_upper_arm > 0 else 28.0
    user_la = rebocap.sk_lower_arm if rebocap.sk_lower_arm > 0 else 28.0
    user_ul = rebocap.sk_upper_leg if rebocap.sk_upper_leg > 0 else 45.0
    user_ll = rebocap.sk_lower_leg if rebocap.sk_lower_leg > 0 else 45.0
    user_spine = (rebocap.sk_spine + rebocap.sk_chest) if (rebocap.sk_spine + rebocap.sk_chest) > 0 else 41.5
    user_nh = rebocap.sk_neck_head if rebocap.sk_neck_head > 0 else 17.0
    user_foot = rebocap.sk_foot if rebocap.sk_foot > 0 else 27.0
    user_shoulder = (rebocap.sk_shoulder_width / 2.0) if rebocap.sk_shoulder_width > 0 else 14.0
    
    # 计算各肢体相对出厂基准尺寸的伸缩比率
    scale_ua = user_ua / 24.24
    scale_la = user_la / 20.42
    scale_ul = user_ul / 46.75
    scale_ll = user_ll / 44.31
    scale_spine = (user_spine / 3.0) / 11.45
    scale_nh = user_nh / 17.0
    scale_foot = user_foot / 25.43
    scale_shoulder = user_shoulder / 13.48
    
    # 1. 大臂 (Y 轴为骨骼主轴长度)
    for bname in ('mixamorig:LeftArm', 'mixamorig:RightArm'):
        pb = armature_obj.pose.bones.get(bname)
        if pb: pb.scale = Vector((1.0, scale_ua, 1.0))
        
    # 2. 小臂
    for bname in ('mixamorig:LeftForeArm', 'mixamorig:RightForeArm'):
        pb = armature_obj.pose.bones.get(bname)
        if pb: pb.scale = Vector((1.0, scale_la, 1.0))
        
    # 3. 大腿
    for bname in ('mixamorig:LeftUpLeg', 'mixamorig:RightUpLeg'):
        pb = armature_obj.pose.bones.get(bname)
        if pb: pb.scale = Vector((1.0, scale_ul, 1.0))
        
    # 4. 小腿
    for bname in ('mixamorig:LeftLeg', 'mixamorig:RightLeg'):
        pb = armature_obj.pose.bones.get(bname)
        if pb: pb.scale = Vector((1.0, scale_ll, 1.0))
        
    # 5. 脊柱各段
    for bname in ('mixamorig:Spine', 'mixamorig:Spine1', 'mixamorig:Spine2'):
        pb = armature_obj.pose.bones.get(bname)
        if pb: pb.scale = Vector((1.0, scale_spine, 1.0))
        
    # 6. 肩部宽窄
    for bname in ('mixamorig:LeftShoulder', 'mixamorig:RightShoulder'):
        pb = armature_obj.pose.bones.get(bname)
        if pb: pb.scale = Vector((1.0, scale_shoulder, 1.0))
        
    # 7. 头颈 (3 轴等比缩放)
    for bname in ('mixamorig:Neck', 'mixamorig:Head'):
        pb = armature_obj.pose.bones.get(bname)
        if pb: pb.scale = Vector((scale_nh, scale_nh, scale_nh))
        
    # 8. 脚部
    for bname in ('mixamorig:LeftFoot', 'mixamorig:RightFoot'):
        pb = armature_obj.pose.bones.get(bname)
        if pb: pb.scale = Vector((scale_foot, scale_foot, scale_foot))


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

        # Deselect all
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
            # 1. 统一应用旋转与缩放变换，保证站立在世界空间
            bpy.ops.object.select_all(action='DESELECT')
            armature_obj.select_set(True)
            for m in mesh_objs:
                m.select_set(True)
            context.view_layer.objects.active = armature_obj
            
            try:
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            except Exception as e:
                print(f"[Rebocap] transform_apply notice: {e}")

            # 2. 设置骨骼独立缩放继承 (防止肢体拉伸相互干涉)
            bpy.ops.object.mode_set(mode='EDIT')
            for ebone in armature_obj.data.edit_bones:
                if hasattr(ebone, 'inherit_scale'):
                    ebone.inherit_scale = 'NONE'
                else:
                    ebone.use_inherit_scale = False
            bpy.ops.object.mode_set(mode='OBJECT')

            # 3. 自动适配当前上位机身材骨骼长度
            apply_demo_character_body_shape(armature_obj, context.scene)

            # 4. 应用站位预设
            preset = getattr(context.scene, 'rebocap_demo_preset', 'SIDE_R')
            if preset == 'SIDE_R':
                armature_obj.location = Vector((1.2, 0.0, 0.0))
            elif preset == 'SIDE_L':
                armature_obj.location = Vector((-1.2, 0.0, 0.0))
            else:
                armature_obj.location = Vector((0.0, 0.0, 0.0))
            
            self.report({'INFO'}, "示范角色已成功载入并完成体型适配")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "未能在导入的模型中找到骨架")
            return {'FINISHED'}
