import json

import bpy
from mathutils import Vector, Quaternion

from _ctypes import PyObj_FromPtr
import json
import re

from .utils import show_message_box


class NoIndent(object):
    """ Value wrapper. """

    def __init__(self, value):
        self.value = value


class MyEncoder(json.JSONEncoder):
    FORMAT_SPEC = '@@{}@@'
    regex = re.compile(FORMAT_SPEC.format(r'(\d+)'))

    def __init__(self, **kwargs):
        # Save copy of any keyword argument values needed for use here.
        self.__sort_keys = kwargs.get('sort_keys', None)
        super(MyEncoder, self).__init__(**kwargs)

    def default(self, obj):
        return (self.FORMAT_SPEC.format(id(obj)) if isinstance(obj, NoIndent)
                else super(MyEncoder, self).default(obj))

    def encode(self, obj):
        format_spec = self.FORMAT_SPEC  # Local var to expedite access.
        json_repr = super(MyEncoder, self).encode(obj)  # Default JSON.

        # Replace any marked-up object ids in the JSON repr with the
        # value returned from the json.dumps() of the corresponding
        # wrapped Python object.
        for match in self.regex.finditer(json_repr):
            # see https://stackoverflow.com/a/15012814/355230
            id = int(match.group(1))
            no_indent = PyObj_FromPtr(id)
            json_obj_repr = json.dumps(no_indent.value, sort_keys=self.__sort_keys)

            # Replace the matched id string with json formatted representation
            # of the corresponding Python object.
            json_repr = json_repr.replace(
                '"{}"'.format(format_spec.format(id)), json_obj_repr)

        return json_repr


def find_all_child_bones(avatar, bone_name):
    if avatar.type != 'ARMATURE':
        raise ValueError("提供的avatar不是骨架对象")
    armature = avatar.data
    if bone_name not in armature.bones:
        return []
    all_children = []
    traversal_queue = [(armature.bones[bone_name], 0)]  # (bone, level)
    while traversal_queue:
        current_bone, level = traversal_queue.pop(0)
        if level == 0 and current_bone.name == bone_name:
            pass
        else:
            all_children.append(current_bone.name)
        for child in current_bone.children:
            traversal_queue.append((child, level + 1))
    return all_children


class SaveBone(bpy.types.Operator):
    bl_idname = 'rebocap.save_bone'
    bl_label = 'Save Bone'

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_data = ''

    def execute(self, ctx):
        if self.file_data == '':
            return {'CANCELLED'}
        with open(self.filepath, "w") as f:
            f.write(self.file_data)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.file_data = self.save_file(context)
        if self.file_data == '':
            return {'CANCELLED'}

        self.filepath = "rebo_export.rebo_skeleton"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def save_file(self, ctx) -> str:
        # Try to use the source armature first, fallback to active object
        source_name = getattr(ctx.scene, 'rebocap_source_armature', '')
        avatar = bpy.data.objects.get(source_name)
        if not avatar or avatar.type != 'ARMATURE':
            avatar = ctx.active_object

        if avatar is None or avatar.type != 'ARMATURE':
            show_message_box(message="Please select the character Armature in the viewport first!", icon='ERROR')
            return ''
            
        rebocap_bone_map = ctx.scene.rebocap_bone_map
        origin_mode = avatar.mode
        glb_mat = avatar.matrix_world
        
        # Check if A2T calibration is enabled
        a2t = getattr(ctx.scene, 'rebocap_a2t', None)
        use_a2t = a2t and getattr(a2t, 'enable_a2t', False)
        
        if use_a2t:
            # Apply A2T calibrated pose to armature
            from ..core.a2t_types import apply_a2t_preview_to_armature
            apply_a2t_preview_to_armature(ctx.scene, avatar, force_apply=True)
            bpy.context.view_layer.update()
            if avatar.mode == 'EDIT':
                bpy.ops.object.mode_set(mode='OBJECT')
        else:
            # Reset to default rest pose
            for bone in avatar.pose.bones:
                bone.location = Vector()
                bone.rotation_quaternion = Quaternion((1.0, 0, 0, 0))

            bpy.context.view_layer.update()
            bpy.context.view_layer.objects.active = avatar
            bpy.ops.object.mode_set(mode='EDIT')

        down_body = [
            0, 1, 4, 7, 2, 5, 8  # root, left legs,  right legs
        ]

        bones = [avatar.pose.bones.get(getattr(rebocap_bone_map, f'node_{e}', '')) for e in down_body]
        if None in bones:
            show_message_box(message='down body not all bind, please set target bone for Legs and Pelvis')
            return ''

        root_position = glb_mat @ bones[0].head
        left_leg_positions = [glb_mat @ bones[1].head, glb_mat @ bones[2].head, glb_mat @ bones[3].head]
        right_leg_positions = [glb_mat @ bones[4].head, glb_mat @ bones[5].head, glb_mat @ bones[6].head]
        fix_min_v = Vector((1e-8, 1e-8, 1e-8))
        
        # In Unity / Rebocap Upper Computer export convention:
        # key 'left_legs' holds Character's Right Leg (+X in Unity), key 'right_legs' holds Left Leg (-X in Unity).
        output_data = {'root': root_position, 'left_legs': right_leg_positions, 'right_legs': left_leg_positions}

        spine = avatar.pose.bones.get(getattr(rebocap_bone_map, f'node_{3}', ''))
        chest = avatar.pose.bones.get(getattr(rebocap_bone_map, f'node_{6}', ''))
        up_chest = avatar.pose.bones.get(getattr(rebocap_bone_map, f'node_{9}', ''))
        if chest is None and up_chest is None:
            show_message_box(message='chest not bind, you should at least bind one of [chest, up_chest]!!!')
            return ''

        if chest is not None and up_chest is not None:
            output_data['chest'] = [glb_mat @ chest.head, glb_mat @ up_chest.head]
        else:
            real_chest = chest if chest is not None else up_chest
            up_chest = real_chest
            output_data['chest'] = [glb_mat @ real_chest.head, glb_mat @ real_chest.head + fix_min_v]

        if spine is None:
            output_data['spine'] = output_data['chest'][0] - fix_min_v
        else:
            output_data['spine'] = glb_mat @ spine.head

        neck = avatar.pose.bones.get(getattr(rebocap_bone_map, f'node_{12}', ''))
        head = avatar.pose.bones.get(getattr(rebocap_bone_map, f'node_{15}', ''))
        if neck is None:
            output_data['neck'] = glb_mat @ up_chest.tail
        else:
            output_data['neck'] = glb_mat @ neck.head
        if head is None:
            output_data['head'] = glb_mat @ neck.tail if neck is not None else output_data['neck'] + fix_min_v
        else:
            output_data['head'] = glb_mat @ head.head

        left_arm_ids = [13, 16, 18, 20]
        right_arm_ids = [14, 17, 19, 21]
        last_pos = [output_data['chest'][1], output_data['chest'][1]]
        left_arms = []
        right_arms = []
        for i in range(len(left_arm_ids)):
            lbone = avatar.pose.bones.get(getattr(rebocap_bone_map, f'node_{left_arm_ids[i]}', ''))
            rbone = avatar.pose.bones.get(getattr(rebocap_bone_map, f'node_{right_arm_ids[i]}', ''))
            lvert = last_pos[0] + fix_min_v if lbone is None else glb_mat @ lbone.head
            rvert = last_pos[1] + fix_min_v if rbone is None else glb_mat @ rbone.head
            last_pos = [lvert, rvert]
            left_arms.append(lvert)
            right_arms.append(rvert)

        # In Unity export convention: key 'left_arms' holds Right arm, key 'right_arms' holds Left arm
        output_data['left_arms'] = right_arms
        output_data['right_arms'] = left_arms

        if getattr(rebocap_bone_map, 'use_legacy_foot_contact', False):
            foot_vert_ids = [getattr(rebocap_bone_map, f'foot_idx_{i}', -1) for i in range(12)]
            foot_vert_pos = [None for _ in range(12)]
            if -1 in foot_vert_ids:
                show_message_box(message='foot vert id not set, export data will not contains foot vertex!')
            else:
                # find foot vert
                foot_names = [rebocap_bone_map.node_7, rebocap_bone_map.node_10, rebocap_bone_map.node_8,
                              rebocap_bone_map.node_11]
                foot_names = list(set(foot_names + find_all_child_bones(avatar, rebocap_bone_map.node_7) + find_all_child_bones(avatar, rebocap_bone_map.node_8)))
                for obj in bpy.context.scene.objects:
                    if obj.type != 'MESH':
                        continue
                    foot_groups = set()
                    for e in obj.vertex_groups:
                        if e.name in foot_names:
                            foot_groups.add(e.index)
                    for i in range(12):
                        if foot_vert_ids[i] < len(obj.data.vertices):
                            vert = obj.data.vertices[foot_vert_ids[i]]
                            if len(set([g.group for g in vert.groups]).intersection(foot_groups)) > 0:
                                foot_vert_pos[i] = glb_mat @ vert.co

                not_valid_vert = [foot_vert_ids[i] for i in range(12) if foot_vert_pos[i] is None]
                if len(not_valid_vert) > 0:
                    show_message_box(message=f'vert index id for:{not_valid_vert} not found correctly, please check!!!')
                else:
                    output_data['foot_vertex_left'] = foot_vert_pos[6:]
                    output_data['foot_vertex_right'] = foot_vert_pos[:6]
        else:
            # Visual Empties setup
            label_names = ['1- toe Right', '2- toe Center', '3- toe Left', '4- heel Right', '5- heel Center', '6- heel Left']
            alias_map = {
                '1- toe Right': ['1- toe Right', 'toeRight', 'toeLeft'],
                '2- toe Center': ['2- toe Center', 'toeCenter'],
                '3- toe Left': ['3- toe Left', 'toeLeft', 'toeRight'],
                '4- heel Right': ['4- heel Right', 'heelRight', 'heelLeft'],
                '5- heel Center': ['5- heel Center', 'heelCenter'],
                '6- heel Left': ['6- heel Left', 'heelLeft', 'heelRight'],
            }
            right_pos = []
            left_pos = []
            valid = True
            
            # Sync visible objects to JSON first
            if getattr(rebocap_bone_map, 'show_visual_foot_points', True):
                import json
                data = {}
                if rebocap_bone_map.foot_contact_data_json:
                    try: data = json.loads(rebocap_bone_map.foot_contact_data_json)
                    except: pass
                for obj in bpy.data.objects:
                    if 'rebocap_foot_point' in obj:
                        pos = obj.matrix_world.translation
                        data[obj['rebocap_foot_point']] = [pos.x, pos.y, pos.z]
                    else:
                        for target_name in label_names:
                            for alias in alias_map[target_name]:
                                if obj.name == alias or obj.name == f"REBOCAP_FOOT_{alias}":
                                    pos = obj.matrix_world.translation
                                    data[target_name] = [pos.x, pos.y, pos.z]
                                    break
                rebocap_bone_map.foot_contact_data_json = json.dumps(data)
                
            # Read from JSON
            import json
            data = {}
            if rebocap_bone_map.foot_contact_data_json:
                try: data = json.loads(rebocap_bone_map.foot_contact_data_json)
                except: pass

            for name in label_names:
                coords = None
                for alias in alias_map[name]:
                    if alias in data:
                        coords = data[alias]
                        break
                if coords is None:
                    show_message_box(message=f'Visual foot contact point "{name}" not found! Please make sure all 6 points are generated.', icon='ERROR')
                    return ''
                
                # World position of the right foot
                w_pos = Vector((coords[0], coords[1], coords[2]))
                right_pos.append(w_pos)
                
                # Mirror to left foot: convert to armature local, mirror X, back to world
                local_pos = glb_mat.inverted() @ w_pos
                local_pos.x *= -1
                left_w_pos = glb_mat @ local_pos
                left_pos.append(left_w_pos)
                
            if valid and len(right_pos) == 6:
                # Key 'foot_vertex_left' holds Character's Right Foot points [1, 2, 3, 4, 5, 6] (which become +X in Unity)
                # Key 'foot_vertex_right' holds Character's Left Foot points [Mirrored 3, 2, 1, 6, 5, 4] (which become -X in Unity)
                output_data['foot_vertex_left'] = right_pos
                output_data['foot_vertex_right'] = [left_pos[2], left_pos[1], left_pos[0], left_pos[5], left_pos[4], left_pos[3]]
            elif valid:
                output_data['foot_vertex_left'] = right_pos
                output_data['foot_vertex_right'] = left_pos

        try:
            if avatar and avatar.mode != origin_mode:
                bpy.ops.object.mode_set(mode=origin_mode)
        except Exception:
            pass

        # Transform Blender (x: right=-x, y: front=-y, z: up=+z) to Unity / SMPL (x: right=+x, y: up=+y, z: front=+z)
        # Formula: Unity_X = -Blender_X, Unity_Y = Blender_Z, Unity_Z = -Blender_Y
        for k in output_data.keys():
            v = output_data[k]
            if isinstance(v, list):
                for i in range(len(v)):
                    v0 = v[i]
                    if isinstance(v0, list):
                        for ii in range(len(v0)):
                            co = v0[ii]
                            v0[ii] = NoIndent([-co[0], co[2], -co[1]])
                    else:
                        co = v0
                        v[i] = NoIndent([-co[0], co[2], -co[1]])
            elif isinstance(v, Vector):
                output_data[k] = NoIndent([-v[0], v[2], -v[1]])
        return json.dumps(output_data, cls=MyEncoder, indent=2)
