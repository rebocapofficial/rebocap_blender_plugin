import bpy
import json
from bpy_extras.io_utils import ExportHelper, ImportHelper
from ..core.translation import T

class REBOCAP_OT_export_bone_map(bpy.types.Operator, ExportHelper):
    bl_idname = "rebocap.export_bone_map"
    bl_label = "导出 JSON (Export Config)"
    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'})

    def execute(self, context):
        bone_map = context.scene.rebocap_bone_map
        data = {}
        for i in range(24):
            data[f"node_{i}"] = getattr(bone_map, f"node_{i}", "")
        for i in range(12):
            data[f"foot_idx_{i}"] = getattr(bone_map, f"foot_idx_{i}", -1)

        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.report({'INFO'}, T("Bone map exported successfully"))
        return {'FINISHED'}

class REBOCAP_OT_import_bone_map(bpy.types.Operator, ImportHelper):
    bl_idname = "rebocap.import_bone_map"
    bl_label = "导入 JSON (Import Config)"
    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'})

    def execute(self, context):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            bone_map = context.scene.rebocap_bone_map
            for i in range(24):
                key = f"node_{i}"
                if key in data:
                    setattr(bone_map, key, data[key])
            for i in range(12):
                key = f"foot_idx_{i}"
                if key in data:
                    setattr(bone_map, key, data[key])
            self.report({'INFO'}, T("Bone map imported successfully"))
        except Exception as e:
            self.report({'ERROR'}, f"{T('Import failed')}: {e}")
        return {'FINISHED'}


def _get_scene_fps_str(scene):
    fps = getattr(scene.render, 'fps', 60)
    fps_base = getattr(scene.render, 'fps_base', 1.0)
    if abs(fps_base - 1.0) > 1e-4 and fps_base > 0:
        return f"{fps / fps_base:.2f} FPS"
    return f"{fps} FPS"

def _get_scene_unit_str(scene):
    units = getattr(scene, 'unit_settings', None)
    if not units:
        return "默认 (Default)"
    sys_name = getattr(units, 'system', 'METRIC')
    scale = getattr(units, 'scale_length', 1.0)
    if sys_name == 'NONE':
        return f"无 (None, 比例:{scale:g})"
    elif sys_name == 'IMPERIAL':
        unit_name = getattr(units, 'length_unit', 'FEET').capitalize()
        return f"英制: {unit_name} (比例:{scale:g})"
    else:  # METRIC
        len_unit = getattr(units, 'length_unit', 'METERS')
        unit_map = {
            'METERS': '米 (m)',
            'CENTIMETERS': '厘米 (cm)',
            'MILLIMETERS': '毫米 (mm)',
            'KILOMETERS': '千米 (km)',
            'ADAPTIVE': '自适应 (Adaptive)'
        }
        name = unit_map.get(len_unit, len_unit)
        if abs(scale - 1.0) > 1e-4:
            return f"公制: {name} (比例:{scale:g})"
        return f"公制: {name}"


class REBOCAP_OT_change_scene_fps(bpy.types.Operator):
    bl_idname = "rebocap.change_scene_fps"
    bl_label = "修改场景帧率 (Change Scene FPS)"
    bl_options = {'REGISTER', 'UNDO'}
    
    new_fps: bpy.props.IntProperty(
        name="FPS",
        description="设置新的场景帧率",
        default=60,
        min=1,
        max=240
    )
    
    def invoke(self, context, event):
        self.new_fps = round(context.scene.render.fps / context.scene.render.fps_base)
        return context.window_manager.invoke_props_dialog(self)
        
    def execute(self, context):
        context.scene.render.fps = self.new_fps
        context.scene.render.fps_base = 1.0
        return {'FINISHED'}

class ConnectionPanel(bpy.types.Panel):
    bl_idname = 'REBOCAP_PT_connection_panel'
    bl_label = " "
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "REBOCAP CONNECTION"
    bl_order = 0
    
    def draw_header(self, context):
        self.layout.label(text=T('Connection'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bones = [
            "Pelvis", "L_UpLeg", "R_UpLeg", "Spine", "L_DownLeg", "R_DownLeg",
            "Chest", "L_Foot", "R_Foot", "UpChest", "L_Toe", "R_Toe",
            "Neck", "L_Shoulder", "R_Shoulder", "Head", "L_UpArm", "R_UpArm",
            "L_DownArm", "R_DownArm", "L_Palm", "R_Palm", "L_Fingers", "R_Fingers",
        ]
        self.bones_map = ['' for _ in range(24)]
        self.center_bone = [0, 3, 6, 9, 12, 15]
        self.left_bone = [1, 4, 7, 10, 13, 16, 18, 20]
        self.right_bone = [2, 5, 8, 11, 14, 17, 19, 21]
        self.side_names = [self.bones[i][2:] for i in self.left_bone]

    def draw(self, ctx):
        layout = self.layout
        rebocap_bone_map = ctx.scene.rebocap_bone_map
        col = layout.column()
        row = col.row(align=True)
        row.label(text=T('Port'))
        row.prop(ctx.scene, 'port', text='')
        if ctx.scene.open is False:
            row = col.row(align=True)
            row.operator('rebocap.connect', text=T("Connect"), icon='URL')
            row = col.row(align=True)
            row.operator('rebocap.restore_pose', text=T("Restore T-Pose"), icon='FILE_REFRESH')
        else:
            row = col.row(align=True)
            row.operator('rebocap.disconnect', text=T("Connected"), icon='UNLINKED', depress=True)
            
            col.separator()
            row = col.row(align=True)
            row.prop(ctx.scene, 'rebocap_pause_control', text=T("Pause Control"), toggle=True, icon='PAUSE')
            row.operator('rebocap.restore_pose', text=T("Restore T-Pose"), icon='FILE_REFRESH')
            
            row = col.row(align=True)
            
            import time
            if not ctx.scene.recording:
                row.prop(ctx.scene, 'rebocap_auto_extend_end', text="", icon='TIME')
                time_since_stop = time.time() - ctx.scene.rebocap_last_record_stop_time
                if time_since_stop < 2.0:
                    row.enabled = False
                    row.operator('rebocap.start_record', text=f"{T('Wait')} {2.0 - time_since_stop:.1f}s", icon='REC')
                else:
                    row.operator('rebocap.start_record', text=T("Start Record"), icon='REC')
            else:
                row.alert = True
                row.operator('rebocap.stop_record', text=T("Stop Record"), icon='PAUSE', depress=True)
                row.alert = False
            
        self._draw_bottom_elements(ctx, layout)

    def _draw_bottom_elements(self, ctx, layout):
        layout.separator()
        row = layout.row()
        row.prop(ctx.scene, "rebocap_keep_character_position", text="")
        row.label(text=T("保持角色当前起点 (Keep Character Position)"))
        
        row = layout.row()
        row.prop(ctx.scene, "rebocap_sync_viewport_fps", text="")
        row.label(text=T("按场景帧率显示动捕 (Sync Viewport to Scene FPS)"))

        # 场景实时环境信息 (帧率与尺寸单位，无独立背景框，紧靠左侧显示)
        row_fps = layout.row(align=True)
        row_fps.alignment = 'LEFT'
        row_fps.label(text=f"{T('场景帧率:')} {_get_scene_fps_str(ctx.scene)}", icon='TIME')
        row_fps.operator("rebocap.change_scene_fps", text="", icon='GREASEPENCIL')
        
        row_unit = layout.row(align=True)
        row_unit.alignment = 'LEFT'
        row_unit.label(text=f"{T('尺寸单位:')} {_get_scene_unit_str(ctx.scene)}", icon='CON_SIZELIMIT')
        
        row = layout.row()
        row.label(text=T("Version: Beta 11.5"))
        
        row_lang = row.row(align=True)
        row_lang.alignment = 'RIGHT'
        row_lang.label(text="Language:")
        row_lang.prop(ctx.scene, "rebocap_language", text="", emboss=False)


class PickBoneOperator(bpy.types.Operator):
    bl_idname = "object.pick_bone"
    bl_label = "使用选中的骨骼 (Use Selected Bone)"
    bl_description = "分配当前在姿态模式或大纲中选中的骨骼 (Assign selected bone)"

    bone_type: bpy.props.StringProperty()

    def execute(self, context):
        armature = context.object
        if not armature or armature.type != 'ARMATURE':
            arm_name = getattr(context.scene, 'rebocap_source_armature', '')
            armature = bpy.data.objects.get(arm_name)

        if armature and armature.type == 'ARMATURE':
            bone_name = ""
            # Compatible with Blender 4.0 ~ 5.x bone selection APIs
            if getattr(context, 'active_pose_bone', None):
                bone_name = context.active_pose_bone.name
            elif getattr(context, 'selected_pose_bones', None):
                bone_name = context.selected_pose_bones[0].name
            elif getattr(context, 'selected_bones', None):
                bone_name = context.selected_bones[0].name
            elif getattr(armature.data.bones, 'active', None):
                bone_name = armature.data.bones.active.name

            if bone_name:
                setattr(context.scene.rebocap_bone_map, self.bone_type, bone_name)
                self.report({'INFO'}, f"{T('Selected bone')}: {bone_name}")
            else:
                self.report({'WARNING'}, T("No bone selected."))
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, T("Please select an armature object."))
            return {'CANCELLED'}
class CreateSkeletonPanel(bpy.types.Panel):
    bl_idname = 'REBOCAP_PT_create_skeleton_panel'
    bl_label = " "
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "REBOCAP CONNECTION"
    bl_order = 4
    
    def draw_header(self, context):
        self.layout.label(text=T('Character Skeleton'))

    def draw(self, ctx):
        layout = self.layout
        rebocap_bone_map = ctx.scene.rebocap_bone_map
        col = layout.column()

        check_attr = ['node_0', 'node_1', 'node_2', 'node_4', 'node_5', 'node_7', 'node_8']
        all_bind = True
        for attr in check_attr:
            if getattr(rebocap_bone_map, attr, '') == '':
                all_bind = False

        row = col.row()
        row.enabled = all_bind
        row.operator('rebocap.save_bone', text=T('Export Skeleton File'), icon='EXPORT')
        if not all_bind:
            col.label(text=T("* Please bind Pelvis and Legs first"), icon="ERROR")
            
        col.separator()

        box = col.box()
        
        box.prop(rebocap_bone_map, "use_legacy_foot_contact")
        if not rebocap_bone_map.use_legacy_foot_contact:
            box.prop(rebocap_bone_map, "show_visual_foot_points", icon='HIDE_OFF' if rebocap_bone_map.show_visual_foot_points else 'HIDE_ON')
            
        box.separator()
        
        box.label(text=T("Foot Contact Positions"), icon="ARMATURE_DATA")
        
        if rebocap_bone_map.use_legacy_foot_contact:
            row = box.row(align=True).split(factor=0.15, align=True)
            column0 = row.column(align=True)
            column1 = row.column(align=True)
            column2 = row.column(align=True)
            column0.label(text='')
            column1.label(text=T('Left'))
            column2.label(text=T('Right'))

            label_names = ['1- toe Right', '2- toe Center', '3- toe Left', '4- heel Right', '5- heel Center', '6- heel Left']
            for i in range(6):
                column0.label(text=label_names[i])
                column1.prop(rebocap_bone_map, f'foot_idx_{i}', text='')
                column2.prop(rebocap_bone_map, f'foot_idx_{i + 6}', text='')
                if i == 2:
                    column0.separator()
                    column1.separator()
                    column2.separator()
        else:
            box.operator("rebocap.place_all_foot_contact_points", text=T("Place All 6 Contact Points"), icon='SNAP_VOLUME')
            row = box.row(align=True).split(factor=0.25, align=True)
            column0 = row.column(align=True)
            column1 = row.column(align=True)
            column2 = row.column(align=True)
            column0.label(text='')
            column1.label(text=T('Right (Control)'))
            column2.label(text=T('Left (Mirrored)'))
            
            label_names = ['1- toe Right', '2- toe Center', '3- toe Left', '4- heel Right', '5- heel Center', '6- heel Left']
            for i in range(6):
                column0.label(text=label_names[i])
                
                op = column1.operator("rebocap.select_foot_contact_point", text=T("Set Point"), icon='CON_TRACKTO')
                op.point_name = label_names[i]
                
                # Left foot (Auto Mirrored)
                column2.label(text=T("Auto Mirrored"), icon='MOD_MIRROR')
                
                if i == 2:
                    column0.separator()
                    column1.separator()
                    column2.separator()
