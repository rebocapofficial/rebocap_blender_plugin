import bpy
import os
from ..ops.ik_tracking import parse_and_update_ik_config

last_mtime = 0.0

def config_watchdog():
    global last_mtime
    
    # Safely get context property
    if not hasattr(bpy.context, 'scene') or not bpy.context.scene:
        return 1.0
        
    try:
        rebocap = getattr(bpy.context.scene, 'rebocap_bone_map', None)
        if not rebocap or not getattr(rebocap, 'ik_auto_refresh', False):
            return 1.0
            
        path = rebocap.ik_config_path
        if not path or not os.path.exists(path):
            from ..ops.ik_tracking import find_rebocap_config_path
            auto_path = find_rebocap_config_path()
            if auto_path and os.path.exists(auto_path):
                rebocap.ik_config_path = auto_path
                path = auto_path

        if path and os.path.exists(path):
            current_mtime = os.path.getmtime(path)
            # Auto refresh on initial start, or when file mtime changes, or if values are 0
            if last_mtime == 0.0 or current_mtime != last_mtime or getattr(rebocap, 'sk_spine', 0.0) == 0.0:
                last_mtime = current_mtime
                parse_and_update_ik_config(path, rebocap, None)
                
                # Auto refresh tracking nodes in viewport if they exist
                if "Rebocap_Root" in bpy.data.objects:
                    try:
                        bpy.ops.rebocap.create_tracking_nodes()
                    except Exception:
                        pass
    except Exception as e:
        # Ignore errors during timer to prevent crashing blender UI
        pass
        
    return 1.0

def register():
    if not bpy.app.timers.is_registered(config_watchdog):
        bpy.app.timers.register(config_watchdog, persistent=True)

def unregister():
    if bpy.app.timers.is_registered(config_watchdog):
        bpy.app.timers.unregister(config_watchdog)
