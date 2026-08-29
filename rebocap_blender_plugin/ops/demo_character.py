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


def align_demo_character_bones_to_tracking_nodes(arm_obj):
    """
    第一阶段核心逻辑：
    1. 直接将 FBX 角色的受控骨骼（Edit Bones）头部和尾部精确挪动到对应的追踪点位置上。
    2. 对于无直接追踪点的末端/子骨骼（手指 HandIndex1~4、头顶 HeadTop_End、脚尖 Toe_End 等），
       严格以其父级骨骼（如小臂、脖子、小腿）的长度变化比例为基准，以 FBX 原始矢量为方向进行等比缩放和无缝跟随。
    """
    if not arm_obj or arm_obj.type != 'ARMATURE':
        return

    # 切换至编辑模式，记录原始 FBX 空间下的骨骼起点与终点矢量
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='EDIT')

    orig_heads = {b.name: b.head.copy() for b in arm_obj.data.edit_bones}
    orig_tails = {b.name: b.tail.copy() for b in arm_obj.data.edit_bones}

    bone_tracking_map = {
        'mixamorig:Hips': ('Rebocap_Pelvis', 'Rebocap_Spine1'),
        'mixamorig:Spine': ('Rebocap_Spine1', 'Rebocap_Spine2'),
        'mixamorig:Spine1': ('Rebocap_Spine2', 'Rebocap_Spine3'),
        'mixamorig:Spine2': ('Rebocap_Spine3', 'Rebocap_Neck'),
        'mixamorig:Neck': ('Rebocap_Neck', 'Rebocap_Head'),
        'mixamorig:LeftShoulder': ('Rebocap_L_Shoulder', 'Rebocap_L_Upper_arm'),
        'mixamorig:LeftArm': ('Rebocap_L_Upper_arm', 'Rebocap_L_Lower_arm'),
        'mixamorig:LeftForeArm': ('Rebocap_L_Lower_arm', 'Rebocap_L_Hand'),
        'mixamorig:LeftHand': ('Rebocap_L_Hand', 'Rebocap_L_Hand_end'),
        'mixamorig:RightShoulder': ('Rebocap_R_Shoulder', 'Rebocap_R_Upper_arm'),
        'mixamorig:RightArm': ('Rebocap_R_Upper_arm', 'Rebocap_R_Lower_arm'),
        'mixamorig:RightForeArm': ('Rebocap_R_Lower_arm', 'Rebocap_R_Hand'),
        'mixamorig:RightHand': ('Rebocap_R_Hand', 'Rebocap_R_Hand_end'),
        'mixamorig:LeftUpLeg': ('Rebocap_L_Upper_leg', 'Rebocap_L_Lower_leg'),
        'mixamorig:LeftLeg': ('Rebocap_L_Lower_leg', 'Rebocap_L_Foot'),
        'mixamorig:LeftFoot': ('Rebocap_L_Foot', 'Rebocap_L_Toe'),
        'mixamorig:RightUpLeg': ('Rebocap_R_Upper_leg', 'Rebocap_R_Lower_leg'),
        'mixamorig:RightLeg': ('Rebocap_R_Lower_leg', 'Rebocap_R_Foot'),
        'mixamorig:RightFoot': ('Rebocap_R_Foot', 'Rebocap_R_Toe'),
    }

    # 1. 挪动主干受控骨骼到对应追踪点
    for bname, (h_node_name, t_node_name) in bone_tracking_map.items():
        eb = arm_obj.data.edit_bones.get(bname)
        nh = bpy.data.objects.get(h_node_name)
        nt = bpy.data.objects.get(t_node_name)
        if eb and nh and nt:
            target_head = arm_obj.matrix_world.inverted() @ nh.matrix_world.translation
            target_tail = arm_obj.matrix_world.inverted() @ nt.matrix_world.translation

            eb.head = target_head
            if (target_tail - target_head).length > 0.001:
                eb.tail = target_tail
            else:
                eb.tail = target_head + Vector((0.0, 0.0, 0.05))

    # 2. 未映射子骨骼分组处理 (子骨骼列表, 挂载锚点骨骼, 参考基准父骨骼)
    unmapped_groups = [
        # 左手手指 -> 锚定在左手掌，基准参考左小臂长度
        (['mixamorig:LeftHandIndex1', 'mixamorig:LeftHandIndex2', 'mixamorig:LeftHandIndex3', 'mixamorig:LeftHandIndex4'], 'mixamorig:LeftHand', 'mixamorig:LeftForeArm'),
        # 右手手指 -> 锚定在右手掌，基准参考右小臂长度
        (['mixamorig:RightHandIndex1', 'mixamorig:RightHandIndex2', 'mixamorig:RightHandIndex3', 'mixamorig:RightHandIndex4'], 'mixamorig:RightHand', 'mixamorig:RightForeArm'),
        # 头部与头顶 -> 锚定在脖子末端，基准参考脊柱/脖子
        (['mixamorig:Head', 'mixamorig:HeadTop_End'], 'mixamorig:Neck', 'mixamorig:Spine2'),
        # 左脚趾 -> 锚定在左脚掌，基准参考左小腿长度
        (['mixamorig:LeftToeBase', 'mixamorig:LeftToe_End'], 'mixamorig:LeftFoot', 'mixamorig:LeftLeg'),
        # 右脚趾 -> 锚定在右脚掌，基准参考右小腿长度
        (['mixamorig:RightToeBase', 'mixamorig:RightToe_End'], 'mixamorig:RightFoot', 'mixamorig:RightLeg'),
    ]

    for child_names, anchor_name, ref_name in unmapped_groups:
        anchor_eb = arm_obj.data.edit_bones.get(anchor_name)
        ref_eb = arm_obj.data.edit_bones.get(ref_name)
        if not anchor_eb or not ref_eb or ref_name not in orig_heads:
            continue
        
        orig_ref_len = (orig_tails[ref_name] - orig_heads[ref_name]).length
        curr_ref_len = ref_eb.length
        scale = (curr_ref_len / orig_ref_len) if orig_ref_len > 1e-4 else 1.0
        
        orig_anchor_origin = orig_heads[anchor_name]
        new_anchor_origin = anchor_eb.head
        
        for cname in child_names:
            ceb = arm_obj.data.edit_bones.get(cname)
            if ceb and cname in orig_heads:
                rel_head = orig_heads[cname] - orig_anchor_origin
                rel_tail = orig_tails[cname] - orig_anchor_origin
                ceb.head = new_anchor_origin + rel_head * scale
                ceb.tail = new_anchor_origin + rel_tail * scale

    bpy.ops.object.mode_set(mode='OBJECT')
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

            # 2. 将各个骨骼挪到对应追踪点位置上（完全不进行缩放计算）
            align_demo_character_bones_to_tracking_nodes(armature_obj)

            self.report({'INFO'}, "示范角色已载入并对齐至追踪点")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "未能在导入的模型中找到骨架")
            return {'FINISHED'}
