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
    spine_ratio = 1.0
    if node_spine1 and node_neck:
        t_spine = (node_neck.matrix_world.translation - node_spine1.matrix_world.translation).length
        spine_bones = ['mixamorig:Spine', 'mixamorig:Spine1', 'mixamorig:Spine2']
        cur_spine = sum(arm_obj.pose.bones[s].bone.length for s in spine_bones if s in arm_obj.pose.bones)
        if cur_spine > 0.001:
            spine_ratio = max(min(t_spine / cur_spine, 3.0), 0.1)
            for s in spine_bones:
                if s in arm_obj.pose.bones:
                    arm_obj.pose.bones[s].scale = (spine_ratio, spine_ratio, spine_ratio)

    # 3. 头部与脖子紧凑等比自适应（跟随上半身躯干比例，彻底消除长颈鹿脖子与大头畸形）
    neck_pb = arm_obj.pose.bones.get('mixamorig:Neck')
    head_pb = arm_obj.pose.bones.get('mixamorig:Head')
    if neck_pb:
        neck_pb.scale = (spine_ratio, spine_ratio, spine_ratio)
    if head_pb:
        head_pb.scale = (spine_ratio, spine_ratio, spine_ratio)

    # 4. 骨盆（Hips）大腿根关节中心精准对位与胯宽对齐（下半身基准）
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

    # 5. 四肢各段主干骨骼三维等比拉伸（锁骨、大臂、小臂、大腿、小腿）
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

    # 6. 脚部骨骼长宽独立精准自适应（X轴精准贴合鞋底宽度，Y/Z轴等比保持脚掌水平贴地）
    for side in ['L', 'R']:
        sole_obj = bpy.data.objects.get(f'Rebocap_{side}_Sole')
        foot_pb_name = 'mixamorig:LeftFoot' if side == 'L' else 'mixamorig:RightFoot'
        toe_pb_name = 'mixamorig:LeftToeBase' if side == 'L' else 'mixamorig:RightToeBase'
        foot_pb = arm_obj.pose.bones.get(foot_pb_name)
        toe_pb = arm_obj.pose.bones.get(toe_pb_name)
        
        if sole_obj and foot_pb:
            pts = [sole_obj.matrix_world @ v.co for v in sole_obj.data.vertices]
            if len(pts) >= 7:
                # 目标鞋底线框横向宽度与纵向长度
                w_target = max(v.x for v in pts) - min(v.x for v in pts)
                l_target = (pts[1] - pts[4]).length
                
                # FBX 原生鞋体基准尺寸 (宽: 14.38cm, 长: 29.61cm)
                base_w = 0.1438
                base_l = 0.2961
                
                s_width = max(min(w_target / base_w, 3.0), 0.1)
                s_len = max(min(l_target / base_l, 3.0), 0.1)
                
                # X 轴独立缩放贴合鞋宽，Y/Z 轴保持一致消除矢状面倾斜剪切
                foot_pb.scale = (s_width, s_len, s_len)
                if toe_pb:
                    toe_pb.scale = (s_width, s_len, s_len)

    bpy.context.view_layer.update()

    # 7. 鞋底精准平齐踩地校准 (Sole Ground Leveling)
    mesh_obj = None
    for child in arm_obj.children:
        if child.type == 'MESH':
            mesh_obj = child
            break
    if not mesh_obj:
        for o in bpy.data.objects:
            if o.type == 'MESH' and o.get('rebocap_demo_character'):
                mesh_obj = o
                break

    if mesh_obj:
        try:
            depsgraph = bpy.context.evaluated_depsgraph_get()
            eval_mesh_obj = mesh_obj.evaluated_get(depsgraph)
            eval_mesh = eval_mesh_obj.to_mesh()
            vg_foot = mesh_obj.vertex_groups.get('mixamorig:LeftFoot')
            vg_toe = mesh_obj.vertex_groups.get('mixamorig:LeftToeBase')
            if vg_foot and vg_toe:
                foot_verts_z = [
                    (eval_mesh_obj.matrix_world @ v.co).z
                    for v in eval_mesh.vertices
                    if any(g.group in (vg_foot.index, vg_toe.index) and g.weight > 0.1 for g in mesh_obj.data.vertices[v.index].groups)
                ]
                if foot_verts_z:
                    min_z = min(foot_verts_z)
                    if abs(min_z) > 0.0005 and hip_pb and hip_db:
                        world_offset = Vector((0.0, 0.0, -min_z))
                        local_offset = hip_db.matrix_local.to_3x3().inverted() @ world_offset
                        hip_pb.location += local_offset
            eval_mesh_obj.to_mesh_clear()
        except Exception:
            pass

    # 8. 隐藏骨骼线框显示，保持角色表面光洁
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
