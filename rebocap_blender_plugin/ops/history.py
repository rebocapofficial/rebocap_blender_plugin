import bpy
import json
import os
from bpy_extras.io_utils import ExportHelper, ImportHelper
from ..core.translation import T
from .rebocap_connection import _is_legacy_action, _action_iter_fcurves, _action_fcurve_new
def _get_effective_target_fps(scene):
    mode = getattr(scene, 'rebocap_fps_mode', 'SCENE')
    if mode == 'SCENE':
        fps_base = getattr(scene.render, 'fps_base', 1.0)
        return scene.render.fps / fps_base if abs(fps_base - 1.0) > 1e-4 and fps_base > 0 else float(scene.render.fps)
    elif mode == 'FPS_24':
        return 24.0
    elif mode == 'FPS_30':
        return 30.0
    elif mode == 'FPS_60':
        return 60.0
    elif mode == 'CUSTOM':
        return float(getattr(scene, 'rebocap_target_fps', 60))
    return float(scene.render.fps)


class REBOCAP_OT_apply_take(bpy.types.Operator):
    bl_idname = "rebocap.apply_take"
    bl_label = "挂载到时间轴 (Apply Take)"
    bl_description = "将选中的历史记录应用到当前时间轴"
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.rebocap_takes) > 0
        
    def execute(self, context):
        scene = context.scene
        idx = scene.rebocap_active_take_index
        take = scene.rebocap_takes[idx]
        
        # Clear new take notification badge
        if hasattr(scene, 'rebocap_has_new_take'):
            scene.rebocap_has_new_take = False
        
        # 1. If currently connected, auto-enable pause control to prevent live stream from conflicting with timeline
        if getattr(scene, 'open', False):
            scene.rebocap_pause_control = True
        
        target_fps = _get_effective_target_fps(scene)
        mode = getattr(scene, 'rebocap_fps_mode', 'SCENE')
        if mode != 'SCENE':
            scene.render.fps = int(round(target_fps))
            scene.render.fps_base = 1.0
                
        recorded_fps = take.recorded_fps if hasattr(take, 'recorded_fps') and take.recorded_fps > 0 else 60.0
        scale_factor = target_fps / recorded_fps
            
        def scale_action(action):
            if abs(scale_factor - 1.0) < 0.001:
                return action
            new_action = action.copy()
            for fcurve in _action_iter_fcurves(new_action):
                for kp in fcurve.keyframe_points:
                    kp.co[0] = (kp.co[0] - 1.0) * scale_factor + 1.0
                    kp.handle_left[0] = (kp.handle_left[0] - 1.0) * scale_factor + 1.0
                    kp.handle_right[0] = (kp.handle_right[0] - 1.0) * scale_factor + 1.0
            return new_action
        
        if take.take_type == 'FK':
            source_obj = bpy.data.objects.get(scene.rebocap_source_armature)
            if source_obj and take.action_fk:
                source_obj.animation_data_create()
                action = scale_action(take.action_fk)
                source_obj.animation_data.action = action
                if hasattr(source_obj.animation_data, 'action_slot') and hasattr(action, 'slots') and len(action.slots) > 0:
                    source_obj.animation_data.action_slot = action.slots[0]
                self.report({'INFO'}, f"FK Take {take.name} applied to {source_obj.name} at {target_fps:g} FPS (Live stream paused)")
        elif take.take_type == 'IK':
            joints = [
                "Pelvis", "L_Upper_leg", "R_Upper_leg", "Spine1", "L_Lower_leg", "R_Lower_leg",
                "Spine2", "L_Foot", "R_Foot", "Spine3", "L_Toe", "R_Toe",
                "Neck", "L_Shoulder", "R_Shoulder", "Head", "L_Upper_arm", "R_Upper_arm",
                "L_Lower_arm", "R_Lower_arm", "L_Hand", "R_Hand", "L_Hand_end", "R_Hand_end",
            ]
            applied = 0
            for j_name in joints:
                node = bpy.data.objects.get(f"Rebocap_{j_name}")
                if not node:
                    continue
                prefix = f"rebocap_{j_name}_"
                matching_act = None
                for a in bpy.data.actions:
                    if a.name.startswith(prefix) and a.name.endswith(f"_{take.ik_uuid}"):
                        matching_act = a
                        break
                if matching_act:
                    node.animation_data_create()
                    new_act = scale_action(matching_act)
                    node.animation_data.action = new_act
                    if hasattr(node.animation_data, 'action_slot') and hasattr(new_act, 'slots') and len(new_act.slots) > 0:
                        node.animation_data.action_slot = new_act.slots[0]
                    applied += 1
            self.report({'INFO'}, f"IK Take {take.name} applied to {applied} nodes at {target_fps:g} FPS (Live stream paused)")
            
        # 2. Reset timeline to frame 1 and safely update view layer
        try:
            scene.frame_set(1)
            context.view_layer.update()
        except Exception:
            pass
            
        return {'FINISHED'}

class REBOCAP_OT_delete_take(bpy.types.Operator):
    bl_idname = "rebocap.delete_take"
    bl_label = "删除记录 (Delete Take)"
    bl_description = "删除当前选中的历史记录及其实际的动作数据"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.rebocap_takes) > 0
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=280)
        
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        if len(scene.rebocap_takes) > 0 and 0 <= scene.rebocap_active_take_index < len(scene.rebocap_takes):
            take = scene.rebocap_takes[scene.rebocap_active_take_index]
            layout.label(text=T("确定要删除此动捕记录吗？"), icon='QUESTION')
            box = layout.box()
            row = box.row(align=True)
            row.label(text=f"Take: {take.name} [{take.take_type}]", icon='ACTION')
            layout.label(text=T("此操作将永久删除相关动作数据。"), icon='INFO')
        
    def execute(self, context):
        scene = context.scene
        if len(scene.rebocap_takes) == 0 or scene.rebocap_active_take_index >= len(scene.rebocap_takes):
            return {'CANCELLED'}
        idx = scene.rebocap_active_take_index
        take = scene.rebocap_takes[idx]
        take_name = take.name
        
        # Remove the actions from Blender data to free memory
        if take.take_type == 'FK' and take.action_fk:
            bpy.data.actions.remove(take.action_fk)
        elif take.take_type == 'IK' and take.ik_uuid:
            actions_to_remove = [a for a in bpy.data.actions if a.name.endswith(f"_{take.ik_uuid}")]
            for a in actions_to_remove:
                bpy.data.actions.remove(a)
                
        scene.rebocap_takes.remove(idx)
        if idx > 0:
            scene.rebocap_active_take_index = idx - 1
        elif len(scene.rebocap_takes) == 0:
            scene.rebocap_active_take_index = 0
            
        self.report({'INFO'}, f"{T('动捕记录已删除')}: {take_name}")
        return {'FINISHED'}

class REBOCAP_OT_export_take(bpy.types.Operator, ExportHelper):
    bl_idname = "rebocap.export_take"
    bl_label = "导出片段json (Export JSON)"
    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'})
    
    @classmethod
    def poll(cls, context):
        return len(context.scene.rebocap_takes) > 0
        
    def invoke(self, context, event):
        scene = context.scene
        if len(scene.rebocap_takes) > 0 and 0 <= scene.rebocap_active_take_index < len(scene.rebocap_takes):
            take = scene.rebocap_takes[scene.rebocap_active_take_index]
            safe_name = "".join(c for c in take.name if c.isalnum() or c in ('_', '-'))
            self.filepath = f"{safe_name}_{take.frame_count}F.json"
        return super().invoke(context, event)
        
    def execute(self, context):
        scene = context.scene
        idx = scene.rebocap_active_take_index
        take = scene.rebocap_takes[idx]
        
        target_fps = _get_effective_target_fps(scene)
        recorded_fps = take.recorded_fps if hasattr(take, 'recorded_fps') and take.recorded_fps > 0 else 60.0
        scale_factor = target_fps / recorded_fps
        
        export_data = {
            "name": take.name,
            "type": take.take_type,
            "frame_count": int(round(take.frame_count * target_fps / recorded_fps)),
            "target_fps": target_fps,
            "actions": {}
        }
        
        def serialize_action(action):
            action_data = {}
            for fcurve in _action_iter_fcurves(action):
                if fcurve.data_path not in action_data:
                    action_data[fcurve.data_path] = {}
                points = []
                for kp in fcurve.keyframe_points:
                    points.append(((kp.co[0] - 1.0) * scale_factor + 1.0, kp.co[1]))
                action_data[fcurve.data_path][str(fcurve.array_index)] = points
            return action_data

        if take.take_type == 'FK' and take.action_fk:
            export_data["actions"]["FK_ACTION"] = serialize_action(take.action_fk)
        elif take.take_type == 'IK' and take.ik_uuid:
            actions = [a for a in bpy.data.actions if a.name.endswith(f"_{take.ik_uuid}")]
            for a in actions:
                # Store by the node name extracted from action name
                node_name = a.name.replace("rebocap_", "").replace(f"_{take.ik_uuid}", "")
                export_data["actions"][node_name] = serialize_action(a)
                
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            self.report({'INFO'}, f"Take exported successfully to {self.filepath}")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export: {str(e)}")
            
        return {'FINISHED'}

class REBOCAP_OT_import_take(bpy.types.Operator, ImportHelper):
    bl_idname = "rebocap.import_take"
    bl_label = "导入片段json (Import JSON)"
    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'})
    
    def execute(self, context):
        scene = context.scene
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                import_data = json.loads(f.read())
                
            import uuid
            take_id = str(uuid.uuid4())[:8]
            
            take = scene.rebocap_takes.add()
            take.name = import_data.get("name", "Imported Take")
            take.take_type = import_data.get("type", "FK")
            take.frame_count = import_data.get("frame_count", 0)
            
            def deserialize_action(action, action_data):
                for data_path, indices in action_data.items():
                    for index_str, points in indices.items():
                        fcurve = _action_fcurve_new(action, data_path, int(index_str))
                        fcurve.keyframe_points.add(len(points))
                        for i, pt in enumerate(points):
                            fcurve.keyframe_points[i].co = pt
                        for kp in fcurve.keyframe_points:
                            kp.interpolation = 'LINEAR'
                            
            if take.take_type == 'FK':
                take.fk_uuid = take_id
                action_data = import_data["actions"].get("FK_ACTION")
                if action_data:
                    action = bpy.data.actions.new(name=f'rebocap_{take.name}_{take_id}')
                    deserialize_action(action, action_data)
                    take.action_fk = action
            elif take.take_type == 'IK':
                take.ik_uuid = take_id
                for node_name, action_data in import_data["actions"].items():
                    action = bpy.data.actions.new(name=f"rebocap_{node_name}_{take_id}")
                    deserialize_action(action, action_data)
                    
            scene.rebocap_active_take_index = len(scene.rebocap_takes) - 1
            self.report({'INFO'}, f"Take {take.name} imported successfully")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to import: {str(e)}")
            
        return {'FINISHED'}

classes = [
    REBOCAP_OT_apply_take,
    REBOCAP_OT_delete_take,
    REBOCAP_OT_export_take,
    REBOCAP_OT_import_take,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
