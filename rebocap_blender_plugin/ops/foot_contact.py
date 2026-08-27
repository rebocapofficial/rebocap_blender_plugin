import bpy
from mathutils import Vector

class REBOCAP_OT_select_foot_contact_point(bpy.types.Operator):
    bl_idname = "rebocap.select_foot_contact_point"
    bl_label = "Select Foot Contact Point"
    bl_description = "Create or select the foot contact point gizmo"

    point_name: bpy.props.StringProperty()

    def execute(self, context):
        obj_name = self.point_name
        
        # Ensure visibility is on globally when user clicks this button
        # This will trigger the update callback and recreate any deleted points from JSON
        context.scene.rebocap_bone_map.show_visual_foot_points = True
        
        # Calculate dynamic size based on neck height
        # Try to get the neck bone from the source armature
        rebocap_bone_map = context.scene.rebocap_bone_map
        source_name = getattr(context.scene, 'rebocap_source_armature', '')
        avatar = bpy.data.objects.get(source_name)
        if not avatar or avatar.type != 'ARMATURE':
            avatar = context.active_object
            
        neck_height = 1.7 # fallback default height
        if avatar and avatar.type == 'ARMATURE':
            neck_bone_name = getattr(rebocap_bone_map, 'node_12', '')
            neck_bone = avatar.pose.bones.get(neck_bone_name)
            if neck_bone:
                # Get world coordinate of the neck head
                neck_world_pos = avatar.matrix_world @ neck_bone.head
                neck_height = abs(neck_world_pos.z)
            else:
                # Fallback to armature dimension Z
                neck_height = avatar.dimensions.z

        # Avoid division by zero or negative size
        neck_height = max(neck_height, 0.01)
        
        # If height is 170(cm), diameter is 1(cm) or 10(mm). 
        # Ratio: diameter = height / 170. Radius = height / 340.
        dynamic_radius = neck_height / 340.0
        
        # Check if the object already exists
        empty_obj = None
        for obj in bpy.data.objects:
            if obj.get('rebocap_foot_point') == self.point_name:
                empty_obj = obj
                break
                
        if empty_obj is None:
            # Create a new empty object
            empty_obj = bpy.data.objects.new(obj_name, None)
            empty_obj['rebocap_foot_point'] = self.point_name
            
            # Link to the current collection
            context.collection.objects.link(empty_obj)
            
            # Determine base position and orientation for the pattern
            from mathutils import Vector
            base_pos = context.scene.cursor.location.copy()
            forward_dir = Vector((0, -1, 0)) # Default facing -Y
            right_dir = Vector((-1, 0, 0))   # Default right
            
            if avatar and avatar.type == 'ARMATURE':
                r_foot_bone_name = getattr(rebocap_bone_map, 'node_8', '')
                r_foot_bone = avatar.pose.bones.get(r_foot_bone_name)
                r_toe_bone_name = getattr(rebocap_bone_map, 'node_11', '')
                r_toe_bone = avatar.pose.bones.get(r_toe_bone_name)
                
                if r_foot_bone:
                    base_pos = avatar.matrix_world @ r_foot_bone.head
                    base_pos.z = 0.0 # Snap to floor
                    
                    # Calculate forward direction from ankle to toe
                    if r_toe_bone:
                        toe_pos = avatar.matrix_world @ r_toe_bone.head
                        fwd = toe_pos - base_pos
                        fwd.z = 0
                        if fwd.length > 0.001:
                            forward_dir = fwd.normalized()
                            right_dir = forward_dir.cross(Vector((0, 0, 1))).normalized()

            scale = neck_height / 1.7
            
            # Define pattern offsets (Right, Forward, Up)
            # Right foot: "Left" means inner side (negative Right), "Right" means outer side (positive Right)
            offsets = {
                '1- toe Right':   Vector(( 0.035,  0.12, 0)),
                '2- toe Center':  Vector(( 0.000,  0.15, 0)),
                '3- toe Left':    Vector((-0.035,  0.12, 0)),
                '4- heel Right':  Vector(( 0.025, -0.05, 0)),
                '5- heel Center': Vector(( 0.000, -0.07, 0)),
                '6- heel Left':   Vector((-0.025, -0.05, 0)),
                
                # Backwards compatibility
                'toeRight':   Vector(( 0.035,  0.12, 0)),
                'toeCenter':  Vector(( 0.000,  0.15, 0)),
                'toeLeft':    Vector((-0.035,  0.12, 0)),
                'heelRight':  Vector(( 0.025, -0.05, 0)),
                'heelCenter': Vector(( 0.000, -0.07, 0)),
                'heelLeft':   Vector((-0.025, -0.05, 0)),
            }
            
            local_offset = offsets.get(self.point_name, Vector((0,0,0))) * scale
            
            # Apply offset: base_pos + right_dir * local.x + forward_dir * local.y
            final_pos = base_pos + right_dir * local_offset.x + forward_dir * local_offset.y
            empty_obj.location = final_pos

        empty_obj.empty_display_type = 'SPHERE'
        empty_obj.empty_display_size = dynamic_radius
        empty_obj.show_in_front = True
        empty_obj.show_name = True

        # Make it the active object and select it safely without context dependence
        for obj in list(context.selected_objects):
            obj.select_set(False)
        
        # Ensure it's selectable and visible
        empty_obj.hide_select = False
        empty_obj.hide_viewport = False
        
        context.view_layer.objects.active = empty_obj
        empty_obj.select_set(True)
        
        # Switch to Move tool safely
        try:
            bpy.ops.wm.tool_set_by_id(name="builtin.move")
        except Exception:
            pass

        return {'FINISHED'}


class REBOCAP_OT_place_all_foot_contact_points(bpy.types.Operator):
    bl_idname = "rebocap.place_all_foot_contact_points"
    bl_label = "Place All Foot Contact Points"
    bl_description = "Automatically generate and place all 6 visual foot contact points aligned to the right foot"

    def execute(self, context):
        point_names = ['1- toe Right', '2- toe Center', '3- toe Left', '4- heel Right', '5- heel Center', '6- heel Left']
        for name in point_names:
            bpy.ops.rebocap.select_foot_contact_point(point_name=name)
        return {'FINISHED'}
