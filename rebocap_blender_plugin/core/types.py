from .translation import T
from .a2t_types import RebocapA2TSettings
import bpy


class RebocapBones(bpy.types.PropertyGroup):
    node_0: bpy.props.StringProperty()
    node_1: bpy.props.StringProperty()
    node_2: bpy.props.StringProperty()
    node_3: bpy.props.StringProperty()
    node_4: bpy.props.StringProperty()
    node_5: bpy.props.StringProperty()
    node_6: bpy.props.StringProperty()
    node_7: bpy.props.StringProperty()
    node_8: bpy.props.StringProperty()
    node_9: bpy.props.StringProperty()
    node_10: bpy.props.StringProperty()
    node_11: bpy.props.StringProperty()
    node_12: bpy.props.StringProperty()
    node_13: bpy.props.StringProperty()
    node_14: bpy.props.StringProperty()
    node_15: bpy.props.StringProperty()
    node_16: bpy.props.StringProperty()
    node_17: bpy.props.StringProperty()
    node_18: bpy.props.StringProperty()
    node_19: bpy.props.StringProperty()
    node_20: bpy.props.StringProperty()
    node_21: bpy.props.StringProperty()
    node_22: bpy.props.StringProperty()
    node_23: bpy.props.StringProperty()

    foot_idx_0: bpy.props.IntProperty(name='indices id', default=-1, min=-1)
    foot_idx_1: bpy.props.IntProperty(name='indices id', default=-1, min=-1)
    foot_idx_2: bpy.props.IntProperty(name='indices id', default=-1, min=-1)
    foot_idx_3: bpy.props.IntProperty(name='indices id', default=-1, min=-1)
    foot_idx_4: bpy.props.IntProperty(name='indices id', default=-1, min=-1)
    foot_idx_5: bpy.props.IntProperty(name='indices id', default=-1, min=-1)
    foot_idx_6: bpy.props.IntProperty(name='indices id', default=-1, min=-1)
    foot_idx_7: bpy.props.IntProperty(name='indices id', default=-1, min=-1)
    foot_idx_8: bpy.props.IntProperty(name='indices id', default=-1, min=-1)
    foot_idx_9: bpy.props.IntProperty(name='indices id', default=-1, min=-1)
    foot_idx_10: bpy.props.IntProperty(name='indices id', default=-1, min=-1)
    foot_idx_11: bpy.props.IntProperty(name='indices id', default=-1, min=-1)

    use_legacy_foot_contact: bpy.props.BoolProperty(
        name="Use Legacy Foot Setup",
        default=False,
        description="Use the old 12 vertex index method for foot contact points"
    )

    def update_foot_points_visibility(self, context):
        import json
        show = self.show_visual_foot_points
        if not show:
            # Save positions to JSON before deleting
            data = {}
            if self.foot_contact_data_json:
                try:
                    data = json.loads(self.foot_contact_data_json)
                except:
                    pass
            for obj in bpy.data.objects:
                if 'rebocap_foot_point' in obj:
                    name = obj['rebocap_foot_point']
                    pos = obj.matrix_world.translation
                    data[name] = [pos.x, pos.y, pos.z]
                    bpy.data.objects.remove(obj, do_unlink=True)
            self.foot_contact_data_json = json.dumps(data)
        else:
            # Recreate objects from JSON
            data = {}
            if self.foot_contact_data_json:
                try:
                    data = json.loads(self.foot_contact_data_json)
                except:
                    pass
            
            # Calculate dynamic radius once for recreation
            source_name = getattr(context.scene, 'rebocap_source_armature', '')
            avatar = bpy.data.objects.get(source_name)
            if not avatar or avatar.type != 'ARMATURE':
                avatar = context.active_object
            neck_height = 1.7
            if avatar and avatar.type == 'ARMATURE':
                neck_bone_name = getattr(self, 'node_12', '')
                neck_bone = avatar.pose.bones.get(neck_bone_name)
                if neck_bone:
                    neck_world_pos = avatar.matrix_world @ neck_bone.head
                    neck_height = abs(neck_world_pos.z)
                else:
                    neck_height = avatar.dimensions.z
            neck_height = max(neck_height, 0.01)
            dynamic_radius = neck_height / 340.0

            for name, coords in data.items():
                if name not in bpy.data.objects:
                    empty_obj = bpy.data.objects.new(name, None)
                    empty_obj['rebocap_foot_point'] = name
                    context.collection.objects.link(empty_obj)
                else:
                    empty_obj = bpy.data.objects[name]
                
                from mathutils import Vector
                empty_obj.location = Vector((coords[0], coords[1], coords[2]))
                empty_obj.empty_display_type = 'SPHERE'
                empty_obj.empty_display_size = dynamic_radius
                empty_obj.show_in_front = True
                empty_obj.show_name = True

    show_visual_foot_points: bpy.props.BoolProperty(
        name="Show Foot Points",
        default=True,
        description="Toggle visibility of the visual foot contact points",
        update=update_foot_points_visibility
    )
    
    foot_contact_data_json: bpy.props.StringProperty(
        default="{}"
    )

    def update_tracking_nodes(self, context):
        if "Rebocap_Root" not in bpy.data.objects:
            return
            
        rebocap = self
        ratio = rebocap.sk_skeleton_ratio if rebocap.sk_skeleton_ratio > 0.01 else 1.0
        s = 0.01 * ratio
        hw = (rebocap.sk_hip_width / 2.0) * s
        hh = rebocap.sk_hip_height * s
        ul = rebocap.sk_upper_leg * s
        ll = rebocap.sk_lower_leg * s
        ah = (rebocap.sk_ankle if rebocap.sk_ankle > 0 else 9.0) * s
        fl = (rebocap.sk_foot if rebocap.sk_foot > 0 else 27.0) * s
        sp = (rebocap.sk_spine / 3.0) * s
        ch = rebocap.sk_chest * s
        nh = rebocap.sk_neck_head * s
        sw = (rebocap.sk_shoulder_width / 2.0) * s
        ua = rebocap.sk_upper_arm * s
        la = rebocap.sk_lower_arm * s
        
        # 骨盆静态 T-Pose 绝对高度：包含 ah
        pelvis_z = hh + ul + ll + ah
        toe_forward = fl * 0.75
        
        offsets = {
            0: (0, 0, pelvis_z), # Root (world) -> Pelvis
            1: (hw, 0, -hh), 2: (-hw, 0, -hh), 3: (0, 0, sp),
            4: (0, 0, -ul), 5: (0, 0, -ul), 6: (0, 0, sp),
            7: (0, 0, -ll), 8: (0, 0, -ll), 9: (0, 0, sp),  # L_Foot / R_Foot (脚踝) 此时世界 Z 为 +fh
            10: (0, -toe_forward, -fh), 11: (0, -toe_forward, -fh), 12: (0, 0, ch), # L_Toe (脚尖) 偏移 -fh，世界 Z 完美归 0.0
            13: (sw*0.2, 0, ch), 14: (-sw*0.2, 0, ch), 15: (0, 0, nh),
            16: (sw*0.8, 0, 0), 17: (-sw*0.8, 0, 0), 18: (ua, 0, 0),
            19: (-ua, 0, 0), 20: (la, 0, 0), 21: (-la, 0, 0),
            22: (0.1, 0, 0), 23: (-0.1, 0, 0)
        }

        joints = [
            "Pelvis", "L_Upper_leg", "R_Upper_leg", "Spine1", "L_Lower_leg", "R_Lower_leg",
            "Spine2", "L_Foot", "R_Foot", "Spine3", "L_Toe", "R_Toe",
            "Neck", "L_Shoulder", "R_Shoulder", "Head", "L_Upper_arm", "R_Upper_arm",
            "L_Lower_arm", "R_Lower_arm", "L_Hand", "R_Hand", "L_Hand_end", "R_Hand_end",
        ]

        for i, name in enumerate(joints):
            node = bpy.data.objects.get(f"Rebocap_{name}")
            if node and i in offsets:
                node.location = offsets[i]
                
        # Dynamically update wireframe foot soles if they exist
        try:
            from ..ops.ik_tracking import update_or_create_sole_mesh
            node_l = bpy.data.objects.get("Rebocap_L_Foot")
            node_r = bpy.data.objects.get("Rebocap_R_Foot")
            if node_l:
                update_or_create_sole_mesh('L', node_l)
            if node_r:
                update_or_create_sole_mesh('R', node_r)
        except Exception:
            pass
                

                
        # Handle Neck and Foot scaling safely
        neck_scale_factor = rebocap.sk_neck_head / 15.0
        foot_scale_factor = rebocap.sk_foot / 30.0
        
        for obj in bpy.data.objects:
            if obj.get("rebocap_robot_character") and obj.type == 'ARMATURE':
                neck_bone = obj.pose.bones.get('mixamorig:Neck')
                if neck_bone:
                    neck_bone.scale = (neck_scale_factor, neck_scale_factor, neck_scale_factor)
                    
                left_foot = obj.pose.bones.get('mixamorig:LeftFoot')
                right_foot = obj.pose.bones.get('mixamorig:RightFoot')
                if left_foot: left_foot.scale = (foot_scale_factor, foot_scale_factor, foot_scale_factor)
                if right_foot: right_foot.scale = (foot_scale_factor, foot_scale_factor, foot_scale_factor)
                break
                
        if getattr(context.scene, 'rebocap_debug_log', False):
            print(f"[Rebocap LiveSync] Bone property changed. Safely updated tracking node locations.")
            print(f"[Rebocap LiveSync] Neck uniform scale applied: {neck_scale_factor:.3f} (base 15.0)")
            print(f"[Rebocap LiveSync] Foot uniform scale applied: {foot_scale_factor:.3f} (base 30.0)")

    # IK Tracking Properties
    ik_config_path: bpy.props.StringProperty(
        name="Rebocap Config Path",
        subtype='FILE_PATH',
        default="",
        description="Path to the config.data file"
    )
    
    ik_auto_refresh: bpy.props.BoolProperty(
        name="Auto Refresh",
        default=True,
        description="Automatically refresh skeleton lengths when the config file changes"
    )
    
    sk_upper_arm: bpy.props.FloatProperty(name="Upper Arm", default=0.0)
    sk_lower_arm: bpy.props.FloatProperty(name="Lower Arm", default=0.0)
    sk_upper_leg: bpy.props.FloatProperty(name="Upper Leg", default=0.0)
    sk_lower_leg: bpy.props.FloatProperty(name="Lower Leg", default=0.0)
    sk_spine: bpy.props.FloatProperty(name="Spine", default=0.0)
    sk_chest: bpy.props.FloatProperty(name="Chest", default=0.0)
    sk_shoulder_width: bpy.props.FloatProperty(name="Shoulder Width", default=0.0)
    sk_hip_width: bpy.props.FloatProperty(name="Hip Width", default=0.0)
    sk_hip_height: bpy.props.FloatProperty(name="Hip Height", default=0.0)
    sk_neck_head: bpy.props.FloatProperty(name="Neck & Head", default=0.0)
    sk_foot: bpy.props.FloatProperty(name="Foot", default=0.0)
    sk_ankle: bpy.props.FloatProperty(name="Ankle Height", default=9.0)
    sk_final_height: bpy.props.FloatProperty(name="Final Height", default=180.0)
    sk_skeleton_ratio: bpy.props.FloatProperty(name="Skeleton Ratio", default=1.0)
    sk_use_imported: bpy.props.BoolProperty(name="Use Imported Skeleton", default=False)

class RebocapTake(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Take Name", default="New Take")
    take_type: bpy.props.EnumProperty(
        items=[('FK', 'FK', 'FK Animation'), ('IK', 'IK', 'Tracking Nodes')],
        name="Type"
    )
    action_fk: bpy.props.PointerProperty(type=bpy.types.Action)
    ik_uuid: bpy.props.StringProperty()
    fk_uuid: bpy.props.StringProperty()
    frame_count: bpy.props.IntProperty(default=0)
    recorded_fps: bpy.props.FloatProperty(default=60.0)

def on_active_take_changed(self, context):
    if hasattr(self, 'rebocap_has_new_take'):
        self.rebocap_has_new_take = False

def get_fps_mode_items(self, context):
    return [
        ('SCENE', T('自动匹配场景 (Auto Scene)'), T('自动根据当前 Blender 场景帧率重采样动作关键帧')),
        ('FPS_24', T('24 FPS (电影/标准动画 Film)'), T('匹配 24 FPS 标准电影与影视动画帧率')),
        ('FPS_30', T('30 FPS (电视/短视频 TV/Video)'), T('匹配 30 FPS 电视与视频帧率')),
        ('FPS_60', T('60 FPS (原生动捕/流畅游戏 60Hz)'), T('匹配 60 FPS 原生动捕高帧率')),
        ('CUSTOM', T('自定义帧率 (Custom...)'), T('手动指定任意目标帧率数值'))
    ]

def on_language_changed(self, context):
    from .translation import set_saved_language
    set_saved_language(self.rebocap_language)
    try:
        bpy.ops.rebocap.language_changed_msg('INVOKE_DEFAULT')
    except:
        pass

def register_types():
    bpy.utils.register_class(RebocapTake)
    bpy.types.Scene.rebocap_takes = bpy.props.CollectionProperty(type=RebocapTake)
    bpy.types.Scene.rebocap_active_take_index = bpy.props.IntProperty(
        name="Active Take Index",
        default=0,
        update=on_active_take_changed
    )
    bpy.types.Scene.rebocap_has_new_take = bpy.props.BoolProperty(
        name="Has New Take Notification",
        default=False
    )
    bpy.types.Scene.rebocap_show_auto_detect_help = bpy.props.BoolProperty(
        name="Show Auto Detect Help",
        default=False
    )
    
    from .translation import get_saved_language
    bpy.types.Scene.rebocap_language = bpy.props.EnumProperty(
        name="Language",
        items=[
            ('AUTO', 'Auto', '自动跟随 Blender 语言 (Auto follows Blender)'),
            ('EN', 'English', '强制使用英语 (Force English)'),
            ('ZH', '中文', '强制使用简体中文 (Force Simplified Chinese)'),
            ('JA', '日本語', '强制使用日语 (Force Japanese)')
        ],
        default=get_saved_language(),
        update=on_language_changed
    )
    
    bpy.types.Scene.port = bpy.props.IntProperty(
        name='Port',
        default=7690,
        max=65535,
        min=0
    )
    bpy.types.Scene.open = bpy.props.BoolProperty(
        name='Open',
        default=False,
    )
    bpy.types.Scene.error_msg = bpy.props.StringProperty(
        name='error_msg',
    )
    bpy.types.Scene.recording = bpy.props.BoolProperty(
        name='Recording',
        default=False,
    )
    bpy.types.Scene.rebocap_source_armature = bpy.props.StringProperty(
        name='Armature Source'
    )
    
    from .translation import T_static
    
    bpy.types.Scene.rebocap_keep_character_position = bpy.props.BoolProperty(
        name=T_static("保持角色当前起点 (Keep Character Position)"),
        description=T_static("勾选后以角色当前物体位置为参考系动捕，不会强制吸回世界原点"),
        default=False
    )
    
    bpy.types.Scene.rebocap_sync_viewport_fps = bpy.props.BoolProperty(
        name=T_static("按场景帧率显示动捕 (Sync Viewport to Scene FPS)"),
        description=T_static("勾选后视口刷新率将降至与当前场景FPS一致以节省GPU性能；取消勾选则保持默认的最高实时刷新率"),
        default=False
    )
    
    bpy.types.Scene.rebocap_record_counter = bpy.props.IntProperty(name="Record Counter", default=0)
    
    bpy.types.Scene.rebocap_fps_mode = bpy.props.EnumProperty(
        items=get_fps_mode_items,
        name="FPS Mode"
    )
    
    bpy.types.Scene.rebocap_target_fps = bpy.props.IntProperty(name="Target FPS", default=60, min=1, max=240)
    
    bpy.types.Scene.rebocap_pause_control = bpy.props.BoolProperty(
        name="Pause Control",
        description="Pause motion capture input and allow manual pose editing",
        default=False
    )
    
    bpy.types.Scene.rebocap_auto_extend_end = bpy.props.BoolProperty(
        name="Auto Extend Timeline",
        description="Automatically extend the timeline end frame while recording",
        default=True
    )
    
    bpy.types.Scene.rebocap_last_record_stop_time = bpy.props.FloatProperty(
        name="Last Record Stop Time",
        default=0.0
    )
    bpy.types.Bone.rebocap_source_bone = bpy.props.StringProperty(
        name='Bone Source'
    )
    bpy.types.PoseBone.rebocap_init = bpy.props.BoolProperty(
        name="PoseBone Init",
        default=False,
    )
    bpy.types.PoseBone.rebocap_pose_idx = bpy.props.IntProperty(
        name="Pose Idx",
        default=-1,
    )
    
    # Debug UI Flag
    bpy.types.Scene.rebocap_debug_log = bpy.props.BoolProperty(
        name="Debug Log",
        default=False,
        description="开启后在Blender系统控制台中输出插件详细运行日志"
    )
    
    bpy.types.Scene.rebocap_tracking_node_size = bpy.props.IntProperty(
        name="Tracking Node Size (mm)",
        description="追踪点十字轴的显示大小 (毫米)",
        default=100,
        min=1,
        max=2000
    )

    bpy.types.Scene.rebocap_bone_map = bpy.props.PointerProperty(type=RebocapBones)
    bpy.utils.register_class(RebocapA2TSettings)
    bpy.types.Scene.rebocap_a2t = bpy.props.PointerProperty(type=RebocapA2TSettings)
    
    bpy.types.Scene.rebocap_use_calibration = bpy.props.BoolProperty(
        name="启用智能A-Pose自动补偿",
        description="启用后，自动在后台建立完美的T-Pose数学模型，无损解决手臂插模、腿外八字问题",
        default=True
    )
    
    bpy.types.Scene.rebocap_preview_calibration = bpy.props.BoolProperty(
        name="Preview Calibration",
        description="Currently in T-Pose preview/calibration mode",
        default=False
    )