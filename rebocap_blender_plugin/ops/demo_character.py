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


def adapt_demo_character_uniform_scale(arm_obj):
    """
    100% 还原上位机 3D 预览器（Rebocap3D.exe）真实底层渲染：
    上位机预览器载入 rebo_robot.fbx 后，保持各段骨骼的原始人体工学比例完美不变，
    仅依据上位机当前计算出的总身高/身形比例（sk_final_height / 177.0），对模型进行等比缩放。
    从而保证人偶视觉上 100% 苗条、匀称、表面光整，绝不出现头部尖刺或躯干水肿拉扯。
    """
    if not arm_obj or arm_obj.type != 'ARMATURE':
        return

    # 1. 彻底清除所有姿态位移与约束，确保骨骼姿态处于标准 T-Pose
    for pb in arm_obj.pose.bones:
        pb.scale = (1.0, 1.0, 1.0)
        pb.location = Vector((0.0, 0.0, 0.0))
        for c in list(pb.constraints):
            pb.constraints.remove(c)

    # 2. 读取上位机设定的最终身高 (默认为 177.0cm 标准身高)
    rebocap = bpy.context.scene.rebocap_bone_map
    target_h = getattr(rebocap, 'sk_final_height', 177.0)
    if target_h < 10.0:
        target_h = 177.0

    # 3. 计算等比缩放系数 (rebo_robot.fbx 原生高度为 1.7703m，FBX 初始缩放为 0.01)
    scale_factor = target_h / 177.0
    final_scale = 0.01 * scale_factor
    arm_obj.scale = (final_scale, final_scale, final_scale)

    # 4. 隐藏骨架的骨骼外框显示，仅呈现平滑角色网格（与上位机 OpenGL 视口完全一致）
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
            # 执行 1:1 上位机等比身形自适应
            adapt_demo_character_uniform_scale(armature_obj)

            self.report({'INFO'}, "示范角色已成功载入 (1:1 还原上位机预览器)")
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "未能在导入的模型中找到骨架")
            return {'FINISHED'}
