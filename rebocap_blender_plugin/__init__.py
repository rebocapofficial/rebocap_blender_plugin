import ctypes
import importlib
import sys
import time
import traceback

import bpy
import atexit
from . import core
from . import ops
from . import ui
from .ops import history
from .ui import history_panel
from .ui import puppet_canvas_hud
from .core import timer

bl_info = {
    "name": "REBOCAP BLENDER PLUGIN",
    "author": "Rebocap",
    "description": "",
    "blender": (3, 6, 0),
    "version": (11, 5, 0),
    "location": "",
    "warning": "",
    "doc_url": "https://doc.rebocap.com/zh_cn/plugins/blender.html",
    "tracker_url": "https://forum.rebocap.site/latest",
    "category": "Rebocap"
}

class_list = [
    ops.RebocapConnect,
    ops.RebocapDisconnect,
    ops.RebocapStartRecord,
    ops.RebocapStopRecord,
    ops.RebocapRestorePose,
    ops.AutoMapBone,
    ops.SaveBone,
    ops.REBOCAP_OT_select_foot_contact_point,
    ops.REBOCAP_OT_place_all_foot_contact_points,
    ops.puppet_mapper.REBOCAP_OT_puppet_mapper,
    ops.puppet_mapper.REBOCAP_OT_clear_all_bone_map,
    ops.ik_tracking.REBOCAP_OT_auto_detect_config,
    ops.ik_tracking.REBOCAP_OT_read_config_data,
    ops.a2t_ops.REBOCAP_OT_export_a2t_json,
    ops.a2t_ops.REBOCAP_OT_import_a2t_json,
    ops.a2t_ops.REBOCAP_OT_reset_a2t_offsets,
    ops.ik_tracking.REBOCAP_OT_create_tracking_nodes,
    ops.ik_tracking.REBOCAP_OT_import_character,
    core.RebocapBones,
    ui.REBOCAP_OT_change_scene_fps,
    ui.ConnectionPanel,
    history_panel.REBOCAP_UL_history_takes,
    history_panel.REBOCAP_PT_history_panel,
    ui.fk_panel.REBOCAP_PT_fk_panel,
    puppet_canvas_hud.REBOCAP_OT_toggle_puppet_hud,
    ui.a2t_panel.REBOCAP_PT_a2t_panel,
    ui.CreateSkeletonPanel,
    ui.ik_panel.REBOCAP_PT_ik_tracking_panel,
    ui.PickBoneOperator,
    ui.REBOCAP_OT_import_bone_map,
    ui.REBOCAP_OT_export_bone_map,
    ui.REBOCAP_OT_language_changed_msg,
    history.REBOCAP_OT_apply_take,
    history.REBOCAP_OT_delete_take,
    history.REBOCAP_OT_export_take,
    history.REBOCAP_OT_import_take,
]

joints = [
    "m_avg_Pelvis", "m_avg_L_Hip", "m_avg_R_Hip", "m_avg_Spine1", "m_avg_L_Knee", "m_avg_R_Knee",
    "m_avg_Spine2", "m_avg_L_Ankle", "m_avg_R_Ankle", "m_avg_Spine3", "m_avg_L_Foot", "m_avg_R_Foot",
    "m_avg_Neck", "m_avg_L_Collar", "m_avg_R_Collar", "m_avg_Head", "m_avg_L_Shoulder", "m_avg_R_Shoulder",
    "m_avg_L_Elbow", "m_avg_R_Elbow", "m_avg_L_Wrist", "m_avg_R_Wrist", "m_avg_L_Hand", "m_avg_R_Hand",
]

pyd_module = None
done_module_release = None
register_ts = time.time()


@bpy.app.handlers.persistent
def reset_property_values(_):
    try:
        from .ops.rebocap_connection import force_disconnect
        force_disconnect()
    except Exception as e:
        print("Rebocap auto disconnect error: " + str(e))
        
    try:
        bpy.context.scene.open = False
        bpy.context.scene.recording = False
    except:
        pass


def _cleanup_old_pycache():
    """Auto-clean stale __pycache__ and orphan files on overwrite installation."""
    try:
        import os
        import shutil
        current_dir = os.path.dirname(os.path.abspath(__file__))
        for root, dirs, files in os.walk(current_dir, topdown=False):
            for d in dirs:
                if d == '__pycache__':
                    pycache_path = os.path.join(root, d)
                    try:
                        shutil.rmtree(pycache_path, ignore_errors=True)
                    except Exception:
                        pass
    except Exception:
        pass


def register():
    global done_module_release, pyd_module, register_ts
    print("start register rebocap Beta 11.5!")

    # 1. Clean stale pycache
    _cleanup_old_pycache()

    # 2. Check SDK loading status
    from .rebocap_api.rebocap_ws_sdk import REBOCAP_JOINT_NAMES, my_pyd_module, pyd_load_error

    if pyd_load_error:
        print("[REBOCAP WARNING] SDK load issue: " + str(pyd_load_error))
        def show_overwrite_warning():
            from .ops.utils import show_message_box
            msg = (
                "【Rebocap 插件提醒】\n"
                "检测到可能存在覆盖安装或动态库占用。\n"
                "为了确保所有新功能正常运行，请直接【重启 Blender】！"
            )
            show_message_box(msg, title="Rebocap Notice", icon='ERROR')
        bpy.app.timers.register(show_overwrite_warning, first_interval=1.0)

    pyd_module = my_pyd_module
    if reset_property_values not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(reset_property_values)
        
    try:
        ops.init_rebocap_api()
    except Exception as e:
        print(f"init_rebocap_api notice: {e}")

    for item in class_list:
        try:
            bpy.utils.register_class(item)
        except ValueError:
            # Already registered in memory, unregister and re-register
            try:
                bpy.utils.unregister_class(item)
                bpy.utils.register_class(item)
            except Exception:
                pass
        except Exception as e:
            print(f"Error registering class {item}: {e}")

    core.register_types()
    timer.register()
    
    # Auto-detect config.data on startup and on file load
    def auto_detect_config_on_start(_=None):
        try:
            import os
            scene = bpy.context.scene
            if hasattr(scene, 'rebocap_bone_map'):
                rebocap = scene.rebocap_bone_map
                if not rebocap.ik_config_path or not os.path.exists(rebocap.ik_config_path):
                    from .ops.ik_tracking import find_rebocap_config_path, parse_and_update_ik_config
                    cfg_path = find_rebocap_config_path()
                    if cfg_path and os.path.exists(cfg_path):
                        rebocap.ik_config_path = cfg_path
                        parse_and_update_ik_config(cfg_path, rebocap)
        except Exception:
            pass
        return None
        
    if auto_detect_config_on_start not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(auto_detect_config_on_start)
    bpy.app.timers.register(auto_detect_config_on_start, first_interval=0.5)

    done_module_release = None
    register_ts = time.time()


def cleanup():
    global done_module_release
    if pyd_module is None:
        return

    ops.uninit_rebocap_api()
    return
    target_modules = []
    for e in sys.modules:
        if 'rebocap_ws_sdk_ext' in e:
            target_modules.append(e)

    for target_module in target_modules:
        module = sys.modules.get(target_module)
        if not module:
            print(f"Module '{target_module}' not found in sys.modules", flush=True)
            return

        # 获取模块的文件路径
        module_path = getattr(module, '__file__', None)
        if not module_path:
            print(f"Module '{target_module}' has no __file__ attribute", flush=True)
            return

        # 将文件路径转换为宽字符字符串（Windows API 需要）
        module_path_wide = ctypes.c_wchar_p(module_path)

        # 获取模块句柄
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        get_module_handle = kernel32.GetModuleHandleW
        get_module_handle.argtypes = [ctypes.c_wchar_p]
        get_module_handle.restype = ctypes.c_void_p

        handle = get_module_handle(module_path_wide)
        if not handle:
            print(f"Failed to get handle for module '{target_module}'", flush=True)
            return

        # 卸载模块
        free_library = kernel32.FreeLibrary
        free_library.argtypes = [ctypes.c_void_p]
        free_library.restype = ctypes.c_int

        if free_library(handle):
            print(f"Successfully unloaded module for rebocap '{target_module}'", flush=True)
            # del sys.modules[target_module]  # 从 sys.modules 中移除
            done_module_release = module
        else:
            print(f"Failed to unload module '{target_module}'", flush=True)


def unregister():
    print("unregister rebocap!", flush=True)
    if reset_property_values in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(reset_property_values)

    if time.time() - register_ts > 2.0:
        cleanup()

    for item in class_list:
        bpy.utils.unregister_class(item)
        
    try:
        del bpy.types.Scene.rebocap_active_take_index
        del bpy.types.Scene.rebocap_takes
        del bpy.types.Scene.rebocap_a2t
        bpy.utils.unregister_class(core.a2t_types.RebocapA2TSettings)
        bpy.utils.unregister_class(core.types.RebocapTake)
    except Exception:
        pass