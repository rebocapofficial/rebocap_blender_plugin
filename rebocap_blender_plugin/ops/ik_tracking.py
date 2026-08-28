import bpy
import os
import pickle
import subprocess
from mathutils import Vector
from .utils import show_message_box

def find_rebocap_config_path():
    """Tries multiple methods to find rebocap config.data path automatically."""
    # 1. Try finding running rebocap.exe via wmic
    try:
        cmd = 'wmic process where "name=\'rebocap.exe\'" get ExecutablePath'
        output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        if len(lines) > 1:
            exe_path = lines[1]
            if exe_path and os.path.exists(exe_path):
                root_dir = os.path.dirname(exe_path)
                p = os.path.join(root_dir, "data", "config.data")
                if os.path.exists(p):
                    return p
    except Exception:
        pass

    # 2. Try PowerShell Get-Process
    try:
        ps_cmd = 'powershell -NoProfile -Command "(Get-Process -Name rebocap -ErrorAction SilentlyContinue).Path"'
        output = subprocess.check_output(ps_cmd, shell=True, text=True, stderr=subprocess.DEVNULL).strip()
        if output and os.path.exists(output):
            p = os.path.join(os.path.dirname(output), "data", "config.data")
            if os.path.exists(p):
                return p
    except Exception:
        pass

    # 3. Check common standard installation / AppData paths
    candidates = [
        os.path.join(os.environ.get('APPDATA', ''), '..', 'LocalLow', 'RebornTechnology', 'Rebocap', 'config.data'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Rebocap', 'data', 'config.data'),
        os.path.join(os.environ.get('PROGRAMFILES', ''), 'Rebocap', 'data', 'config.data'),
        os.path.join(os.environ.get('ProgramFiles(x86)', ''), 'Rebocap', 'data', 'config.data'),
        r"D:\Rebocap\data\config.data",
        r"C:\Rebocap\data\config.data",
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return os.path.abspath(c)

    return ""

get_rebocap_config_path = find_rebocap_config_path

class REBOCAP_OT_auto_detect_config(bpy.types.Operator):
    bl_idname = "rebocap.auto_detect_config"
    bl_label = "Auto Detect Config Path"
    bl_description = "Automatically detect rebocap configuration path and load skeleton data"

    def execute(self, context):
        config_path = find_rebocap_config_path()
        if config_path and os.path.exists(config_path):
            context.scene.rebocap_bone_map.ik_config_path = config_path
            parse_and_update_ik_config(config_path, context.scene.rebocap_bone_map, self)
            self.report({'INFO'}, f"Auto-detected and loaded config: {config_path}")
            return {'FINISHED'}
        else:
            show_message_box("Could not automatically locate rebocap config.data. Please select manually.", icon='ERROR')
            return {'CANCELLED'}


# Global cache for imported skeleton positions
cached_imported_positions = None
cached_imported_foot_vertices = None

class REBOCAP_OT_read_config_data(bpy.types.Operator):
    bl_idname = "rebocap.read_config_data"
    bl_label = "Read Bone Lengths"
    bl_description = "Read IK skeleton scale settings from config.data"
    
    def execute(self, context):
        rebocap = context.scene.rebocap_bone_map
        path = rebocap.ik_config_path
        if not path or not os.path.exists(path):
            path = find_rebocap_config_path()
            if path and os.path.exists(path):
                rebocap.ik_config_path = path
                
        if parse_and_update_ik_config(path, rebocap, self):
            if "Rebocap_Root" in bpy.data.objects:
                try:
                    bpy.ops.rebocap.create_tracking_nodes()
                except Exception:
                    pass
            return {'FINISHED'}
        return {'CANCELLED'}

def parse_and_update_ik_config(path, rebocap_props, operator=None):
    global cached_imported_positions, cached_imported_foot_vertices
    if not path or not os.path.exists(path):
        if operator:
            show_message_box("Config path is invalid or file does not exist!", icon='ERROR')
        return False
        
    try:
        with open(path, 'rb') as f:
            data = f.read()
            
        import struct
        sk = {}
        
        # 1. Check if switch_use_skeleton_data is True
        use_imported = False
        idx_switch = data.find(b'switch_use_skeleton_data')
        if idx_switch != -1:
            switch_bytes = data[idx_switch+24:idx_switch+30]
            # \x88 is True, K\x01 is int 1, \x89 is False, K\x00 is int 0
            if b'\x88' in switch_bytes or b'K\x01' in switch_bytes:
                use_imported = True
                
        rebocap_props.sk_use_imported = use_imported
        
        if use_imported:
            import base64
            import pickle
            import sys
            import types
            import math
            
            # Mock the SkeletonData class
            if 'common' not in sys.modules:
                class MockSkeletonData: pass
                m = types.ModuleType('common')
                m.config = types.ModuleType('config')
                m.config.SkeletonData = MockSkeletonData
                sys.modules['common'] = m
                sys.modules['common.config'] = m.config
                
            idx_import = data.find(b'import_skeleton_data')
            if idx_import != -1:
                s = data[idx_import+20:]
                x = s.find(b'X')
                if x != -1:
                    length = struct.unpack('<I', s[x+1:x+5])[0]
                    b64_str = s[x+5:x+5+length]
                    dec = base64.b64decode(b64_str)
                    obj = pickle.loads(dec)
                    positions = getattr(obj, 'skeleton_positions', None)
                    cached_imported_positions = positions
                    cached_imported_foot_vertices = getattr(obj, 'foot_vertex_positions', None)
                    
                    if positions and len(positions) >= 24:
                        def dist(i, j):
                            p1, p2 = positions[i], positions[j]
                            return math.sqrt(sum((a-b)**2 for a,b in zip(p1, p2))) * 100
                            
                        sk[b'skeleton_upper_arm'] = dist(16, 18)
                        sk[b'skeleton_lower_arm'] = dist(18, 20)
                        sk[b'skeleton_upper_leg_len'] = dist(1, 4)
                        sk[b'skeleton_lower_leg_len'] = dist(4, 7)
                        sk[b'skeleton_spine_len'] = dist(0, 9)
                        sk[b'skeleton_chest_len'] = dist(9, 12)
                        sk[b'skeleton_shoulder_width'] = dist(16, 17)
                        sk[b'skeleton_hip_width'] = dist(1, 2)
                        sk[b'skeleton_hip_height'] = dist(0, 1)
                        sk[b'skeleton_neck_and_head_len'] = dist(12, 15)
                        sk[b'skeleton_foot_len'] = dist(7, 10)
                        sk[b'skeleton_ankle_len'] = positions[7][1] * 100 if len(positions) > 7 else 9.0
        else:
            # Manual Mode: Strictly clear imported cache and read 12 manual parameters
            cached_imported_positions = None
            cached_imported_foot_vertices = None
            cached_imported_foot_left = None
            cached_imported_foot_right = None
            keys = [
                b'skeleton_upper_arm', b'skeleton_lower_arm', b'skeleton_upper_leg_len',
                b'skeleton_lower_leg_len', b'skeleton_spine_len', b'skeleton_chest_len',
                b'skeleton_shoulder_width', b'skeleton_hip_width', b'skeleton_hip_height',
                b'skeleton_neck_and_head_len', b'skeleton_foot_len', b'skeleton_ankle_len'
            ]
            for k in keys:
                idx = data.find(k)
                if idx != -1:
                    s = data[idx+len(k):idx+len(k)+15]
                    g = s.find(b'G')
                    if g != -1:
                        val = struct.unpack('>d', data[idx+len(k)+g+1 : idx+len(k)+g+9])[0]
                        sk[k] = val

        if not sk:
            if operator:
                show_message_box("No skeleton data found in the config file!", icon='ERROR')
                operator.report({'ERROR'}, "No skeleton data found in the config file!")
            return False
            
        # Read final_height and skeleton_ratio
        for k in [b'final_height', b'skeleton_ratio']:
            idx = data.find(k)
            if idx != -1:
                s = data[idx+len(k):idx+len(k)+15]
                g = s.find(b'G')
                if g != -1:
                    sk[k] = struct.unpack('>d', data[idx+len(k)+g+1 : idx+len(k)+g+9])[0]

        rebocap_props.sk_upper_arm = float(sk.get(b'skeleton_upper_arm', 28.0))
        rebocap_props.sk_lower_arm = float(sk.get(b'skeleton_lower_arm', 28.0))
        rebocap_props.sk_upper_leg = float(sk.get(b'skeleton_upper_leg_len', 45.0))
        rebocap_props.sk_lower_leg = float(sk.get(b'skeleton_lower_leg_len', 45.0))
        rebocap_props.sk_spine = float(sk.get(b'skeleton_spine_len', 22.5))
        rebocap_props.sk_chest = float(sk.get(b'skeleton_chest_len', 19.0))
        rebocap_props.sk_shoulder_width = float(sk.get(b'skeleton_shoulder_width', 28.0))
        rebocap_props.sk_hip_width = float(sk.get(b'skeleton_hip_width', 20.0))
        rebocap_props.sk_hip_height = float(sk.get(b'skeleton_hip_height', 11.0))
        rebocap_props.sk_neck_head = float(sk.get(b'skeleton_neck_and_head_len', 17.0))
        rebocap_props.sk_foot = float(sk.get(b'skeleton_foot_len', 27.0))
        rebocap_props.sk_ankle = float(sk.get(b'skeleton_ankle_len', 9.0))
        rebocap_props.sk_final_height = float(sk.get(b'final_height', 180.0))
        rebocap_props.sk_skeleton_ratio = float(sk.get(b'skeleton_ratio', 1.0))
        
        if operator:
            operator.report({'INFO'}, f"Config updated from Rebocap")
            
        return True
    except Exception as e:
        if operator:
            show_message_box(f"Failed to parse config: {str(e)}", icon='ERROR')
            operator.report({'ERROR'}, f"Failed to parse config: {str(e)}")
        return False

class REBOCAP_OT_create_tracking_nodes(bpy.types.Operator):
    bl_idname = "rebocap.create_tracking_nodes"
    bl_label = "Generate Tracking Nodes"
    bl_description = "Generate the 24 tracking IK preview nodes from config data"

    def execute(self, context):
        rebocap = context.scene.rebocap_bone_map
        root_name = "Rebocap_Root"
        
        # 1. Clean existing tracking nodes
        for obj in list(bpy.data.objects):
            if obj.name == root_name or (obj.name.startswith("Rebocap_") and not obj.get("rebocap_demo_character") and obj.type == 'EMPTY'):
                bpy.data.objects.remove(obj, do_unlink=True)
                
        for mesh in list(bpy.data.meshes):
            if mesh.name.startswith("Rebocap_") and mesh.users == 0:
                bpy.data.meshes.remove(mesh, do_unlink=True)

        joints = [
            "Pelvis", "L_Upper_leg", "R_Upper_leg", "Spine1", "L_Lower_leg", "R_Lower_leg",
            "Spine2", "L_Foot", "R_Foot", "Spine3", "L_Toe", "R_Toe",
            "Neck", "L_Shoulder", "R_Shoulder", "Head", "L_Upper_arm", "R_Upper_arm",
            "L_Lower_arm", "R_Lower_arm", "L_Hand", "R_Hand", "L_Hand_end", "R_Hand_end",
        ]
        
        parents = {
            1: 0, 2: 0, 3: 0,
            4: 1, 5: 2, 6: 3,
            7: 4, 8: 5, 9: 6,
            10: 7, 11: 8, 12: 9,
            13: 9, 14: 9, 15: 12,
            16: 13, 17: 14, 18: 16,
            19: 17, 20: 18, 21: 19,
            22: 20, 23: 21
        }
        
        raw_joints_world = {}
        
        if rebocap.sk_use_imported and cached_imported_positions is not None and len(cached_imported_positions) >= 24:
            # 1. Applied Skeleton: Use exact 3D coordinates from imported skeleton
            for i in range(24):
                p = cached_imported_positions[i]
                # Convert Unity/SMPL [X, Y(up), Z] to Blender [X, -Z, Y(up)]
                raw_joints_world[i] = (p[0], -p[2], p[1])
                
            # Toe logic: Exactly matches '2- toe Center' contact point from config.data
            if cached_imported_foot_vertices and len(cached_imported_foot_vertices) >= 12:
                p_lt = cached_imported_foot_vertices[1]
                p_rt = cached_imported_foot_vertices[7]
                raw_joints_world[10] = (p_lt[0], -p_lt[2], p_lt[1])
                raw_joints_world[11] = (p_rt[0], -p_rt[2], p_rt[1])
            else:
                fl = (rebocap.sk_foot if rebocap.sk_foot > 0 else 27.0) * 0.01
                raw_joints_world[10] = (raw_joints_world[7][0], raw_joints_world[7][1] - fl * 0.75, 0.0)
                raw_joints_world[11] = (raw_joints_world[8][0], raw_joints_world[8][1] - fl * 0.75, 0.0)
            
            # Same Hand End logic: Extends 10cm along forearm direction
            # Left Hand End (22)
            dx_l = raw_joints_world[20][0] - raw_joints_world[18][0]
            dy_l = raw_joints_world[20][1] - raw_joints_world[18][1]
            dz_l = raw_joints_world[20][2] - raw_joints_world[18][2]
            d_len_l = (dx_l*dx_l + dy_l*dy_l + dz_l*dz_l)**0.5
            if d_len_l > 1e-4:
                raw_joints_world[22] = (
                    raw_joints_world[20][0] + (dx_l / d_len_l) * 0.10,
                    raw_joints_world[20][1] + (dy_l / d_len_l) * 0.10,
                    raw_joints_world[20][2] + (dz_l / d_len_l) * 0.10
                )
            else:
                raw_joints_world[22] = (raw_joints_world[20][0] + 0.10, raw_joints_world[20][1], raw_joints_world[20][2])
                
            # Right Hand End (23)
            dx_r = raw_joints_world[21][0] - raw_joints_world[19][0]
            dy_r = raw_joints_world[21][1] - raw_joints_world[19][1]
            dz_r = raw_joints_world[21][2] - raw_joints_world[19][2]
            d_len_r = (dx_r*dx_r + dy_r*dy_r + dz_r*dz_r)**0.5
            if d_len_r > 1e-4:
                raw_joints_world[23] = (
                    raw_joints_world[21][0] + (dx_r / d_len_r) * 0.10,
                    raw_joints_world[21][1] + (dy_r / d_len_r) * 0.10,
                    raw_joints_world[21][2] + (dz_r / d_len_r) * 0.10
                )
            else:
                raw_joints_world[23] = (raw_joints_world[21][0] - 0.10, raw_joints_world[21][1], raw_joints_world[21][2])
        else:
            # 2. Manual Skeleton: Build accurate T-pose strictly from 12 manual parameters scaled by skeleton_ratio (final_height)
            ratio = rebocap.sk_skeleton_ratio if rebocap.sk_skeleton_ratio > 0.01 else 1.0
            scale = 0.01 * ratio
            hw = (rebocap.sk_hip_width / 2.0) * scale
            hh = rebocap.sk_hip_height * scale
            ul = rebocap.sk_upper_leg * scale
            ll = rebocap.sk_lower_leg * scale
            ah = (rebocap.sk_ankle if rebocap.sk_ankle > 0 else 9.0) * scale
            fl = (rebocap.sk_foot if rebocap.sk_foot > 0 else 27.0) * scale
            sp = (rebocap.sk_spine / 3.0) * scale
            ch = rebocap.sk_chest * scale
            nh = rebocap.sk_neck_head * scale
            sw = (rebocap.sk_shoulder_width / 2.0) * scale
            ua = rebocap.sk_upper_arm * scale
            la = rebocap.sk_lower_arm * scale
            
            pelvis_z = hh + ul + ll + ah
            spine_top_z = pelvis_z + sp * 3.0
            
            raw_joints_world = {
                0:  (0.0, 0.0, pelvis_z),
                1:  (hw, 0.0, pelvis_z - hh),
                2:  (-hw, 0.0, pelvis_z - hh),
                3:  (0.0, 0.0, pelvis_z + sp),
                4:  (hw, 0.0, pelvis_z - hh - ul),
                5:  (-hw, 0.0, pelvis_z - hh - ul),
                6:  (0.0, 0.0, pelvis_z + sp * 2.0),
                7:  (hw, 0.0, ah),
                8:  (-hw, 0.0, ah),
                9:  (0.0, 0.0, spine_top_z),
                10: (hw, -fl * 0.75, 0.0),
                11: (-hw, -fl * 0.75, 0.0),
                12: (0.0, 0.0, spine_top_z + ch),
                13: (sw * 0.2, 0.0, spine_top_z + ch),
                14: (-sw * 0.2, 0.0, spine_top_z + ch),
                15: (0.0, 0.0, spine_top_z + ch + nh),
                16: (sw, 0.0, spine_top_z + ch),
                17: (-sw, 0.0, spine_top_z + ch),
                18: (sw + ua, 0.0, spine_top_z + ch),
                19: (-sw - ua, 0.0, spine_top_z + ch),
                20: (sw + ua + la, 0.0, spine_top_z + ch),
                21: (-sw - ua - la, 0.0, spine_top_z + ch),
                22: (sw + ua + la + 0.1, 0.0, spine_top_z + ch),
                23: (-sw - ua - la - 0.1, 0.0, spine_top_z + ch),
            }
        
        # Calculate local offsets relative to parent directly from absolute 3D world positions
        offsets = {}
        for i in range(24):
            if i == 0:
                offsets[0] = raw_joints_world[0]
            else:
                p_idx = parents[i]
                w_cur = raw_joints_world[i]
                w_par = raw_joints_world[p_idx]
                offsets[i] = (w_cur[0] - w_par[0], w_cur[1] - w_par[1], w_cur[2] - w_par[2])
        
        collection = context.collection
        
        node_size_m = context.scene.rebocap_tracking_node_size / 1000.0
        
        root_empty = bpy.data.objects.new(root_name, None)
        root_empty.empty_display_type = 'PLAIN_AXES'
        root_empty.empty_display_size = node_size_m * 2.0  # Root is twice as large
        collection.objects.link(root_empty)
        
        objects = {}
        for i, name in enumerate(joints):
            empty = bpy.data.objects.new(f"Rebocap_{name}", None)
            empty.empty_display_type = 'PLAIN_AXES'
            empty.empty_display_size = node_size_m
            empty.rotation_mode = 'QUATERNION'
            collection.objects.link(empty)
            objects[i] = empty
            
            if i == 0:
                empty.parent = root_empty
                empty.location = offsets[0]
            else:
                parent = objects[parents[i]]
                empty.parent = parent
                empty.location = offsets[i]
                
        # Generate wireframe foot soles
        ankle_h = raw_joints_world[7][2] if 7 in raw_joints_world else ((rebocap.sk_ankle if rebocap.sk_ankle > 0 else 9.0) * (scale if not rebocap.sk_use_imported else 0.01))
        foot_l = (rebocap.sk_foot if rebocap.sk_foot > 0 else 27.0) * (scale if not rebocap.sk_use_imported else 0.01)
        if 7 in objects:
            update_or_create_sole_mesh('L', objects[7], raw_joints_world.get(7), ankle_h, foot_l, collection)
        if 8 in objects:
            update_or_create_sole_mesh('R', objects[8], raw_joints_world.get(8), ankle_h, foot_l, collection)
                
        self.report({'INFO'}, "Generated Tracking Nodes successfully")
        return {'FINISHED'}

def update_or_create_sole_mesh(side, foot_obj, ankle_world_pos=None, ankle_h=0.09, foot_l=0.27, collection=None):
    # side: 'L' or 'R'
    mesh_name = f"Rebocap_{side}_Sole_Mesh"
    obj_name = f"Rebocap_{side}_Sole"
    
    global cached_imported_foot_vertices
    
    # 1. If imported skeleton in config.data has 12 contact vertex positions (6 for each foot)
    if cached_imported_foot_vertices and len(cached_imported_foot_vertices) >= 12 and ankle_world_pos:
        # Points 0..5 are Right Foot in Unity (+X) -> Left Foot (Joint 7) in Blender
        # Points 6..11 are Left Foot in Unity (-X) -> Right Foot (Joint 8) in Blender
        pts = cached_imported_foot_vertices[0:6] if side == 'L' else cached_imported_foot_vertices[6:12]
        
        # Local offset relative to this foot ankle joint in Blender
        # Unity: [X, Y(up), Z] -> Blender: [X, -Z, Y(up)]
        def to_local(p):
            return (p[0] - ankle_world_pos[0], -p[2] - ankle_world_pos[1], p[1] - ankle_world_pos[2])
            
        v0 = to_local(pts[0]) # toe Right
        v1 = to_local(pts[1]) # toe Center
        v2 = to_local(pts[2]) # toe Left
        v3 = to_local(pts[5]) # heel Left
        v4 = to_local(pts[4]) # heel Center
        v5 = to_local(pts[3]) # heel Right
        v6 = (0.0, 0.0, 0.0)  # Ankle
        
        verts = [ v0, v1, v2, v3, v4, v5, v6 ]
        edges = [
            # Closed outer perimeter following exact vector contact points from config.data
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),
            # Center longitudinal line
            (1, 4),
            # Forefoot width crossbar
            (0, 2),
            # Heel width crossbar
            (5, 3),
            # Ankle struts
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5)
        ]
    else:
        # 2. Manual Mode: 6 standard vector contact points scaled strictly to foot_l and ankle_h from config.data
        sign = 1.0 if side == 'L' else -1.0
        ground_z = -ankle_h # Sole is at ground plane (Z = -ankle_height relative to ankle)
        
        v0 = (sign * foot_l * 0.16, -foot_l * 0.65, ground_z) # 1- toe Right
        v1 = (0.0, -foot_l * 0.75, ground_z)                  # 2- toe Center
        v2 = (-sign * foot_l * 0.14, -foot_l * 0.65, ground_z)# 3- toe Left
        v3 = (-sign * foot_l * 0.12, foot_l * 0.18, ground_z) # 6- heel Left
        v4 = (0.0, foot_l * 0.22, ground_z)                   # 5- heel Center
        v5 = (sign * foot_l * 0.15, foot_l * 0.18, ground_z)  # 4- heel Right
        v6 = (0.0, 0.0, 0.0)                                  # Ankle
        
        verts = [ v0, v1, v2, v3, v4, v5, v6 ]
        edges = [
            # Closed outer perimeter matching 6-point vector topology
            (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),
            # Center longitudinal line (Toe tip to Heel back)
            (1, 4),
            # Forefoot width crossbar (Toe Right to Toe Left)
            (0, 2),
            # Heel width crossbar (Heel Right to Heel Left)
            (5, 3),
            # Ankle connection struts
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5)
        ]
        
    faces = []
    
    obj = bpy.data.objects.get(obj_name)
    if not obj:
        mesh = bpy.data.meshes.new(mesh_name)
        mesh.from_pydata(verts, edges, faces)
        mesh.update()
        obj = bpy.data.objects.new(obj_name, mesh)
        obj.display_type = 'WIRE'
        obj.show_in_front = True
        target_col = collection if collection else bpy.context.collection
        if target_col and obj.name not in target_col.objects:
            target_col.objects.link(obj)
    else:
        mesh = obj.data
        if len(mesh.vertices) == len(verts):
            for idx, v_co in enumerate(verts):
                mesh.vertices[idx].co = v_co
            mesh.update()
        else:
            mesh.clear_geometry()
            mesh.from_pydata(verts, edges, faces)
            mesh.update()
            
    obj.parent = foot_obj
    obj.location = (0, 0, 0)
    obj.rotation_quaternion = (1, 0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    return obj


