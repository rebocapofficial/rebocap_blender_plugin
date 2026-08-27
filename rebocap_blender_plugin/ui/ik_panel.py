import bpy
from ..core.translation import T
class REBOCAP_PT_ik_tracking_panel(bpy.types.Panel):
    bl_idname = "REBOCAP_PT_ik_tracking_panel"
    bl_label = " "
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "REBOCAP CONNECTION"
    bl_order = 5
    
    def draw_header(self, context):
        self.layout.label(text=T("Tracking Point Mode"))
    
    def draw(self, context):
        layout = self.layout
        rebocap = context.scene.rebocap_bone_map
        # Main Actions
        action_box = layout.box()
        
        row1 = action_box.row()
        row1.operator("rebocap.create_tracking_nodes", text=T("Generate Nodes"), icon='OUTLINER_OB_EMPTY')
        
        row_size = action_box.row()
        row_size.prop(context.scene, "rebocap_tracking_node_size", text=T("Node Size (mm)"))
        
        has_character = any(obj.get("rebocap_robot_character") for obj in bpy.data.objects)
        row4 = action_box.row()
        if has_character:
            row4.operator("rebocap.import_character", text=T("Cancel Usage"), icon='CANCEL')
        else:
            row4.operator("rebocap.import_character", text=T("Use Rebocap Character"), icon='USER')
            
        # Config Path and Auto Detect
        box = layout.box()
        box.label(text=T("Config Path"))
        
        row = box.row()
        row.prop(rebocap, "ik_config_path", text="")
        row.operator("rebocap.auto_detect_config", text="", icon="VIEWZOOM")
        
        row2 = box.row()
        row2.operator("rebocap.read_config_data", text=T("Read Data"), icon='FILE_REFRESH')
        row2.prop(rebocap, "ik_auto_refresh", text=T("Auto Refresh"))
        
        # Display Bone Lengths (Read-only to view data from upper computer)
        data_box = layout.box()
        mode_text = T("Mode: Applied Skeleton") if rebocap.sk_use_imported else T("Mode: Manual Skeleton")
        data_box.label(text=f"{T('Current Bone Lengths')} ({mode_text})")
        col = data_box.column(align=True)
        col.enabled = False # Read-only display
        
        col.prop(rebocap, "sk_neck_head", text=T("Neck & Head"))
        col.prop(rebocap, "sk_chest", text=T("Chest"))
        col.prop(rebocap, "sk_spine", text=T("Spine"))
        col.prop(rebocap, "sk_shoulder_width", text=T("Shoulder Width"))
        col.prop(rebocap, "sk_upper_arm", text=T("Upper Arm"))
        col.prop(rebocap, "sk_lower_arm", text=T("Lower Arm"))
        col.prop(rebocap, "sk_hip_width", text=T("Hip Width"))
        col.prop(rebocap, "sk_hip_height", text=T("Hip Height"))
        col.prop(rebocap, "sk_upper_leg", text=T("Upper Leg"))
        col.prop(rebocap, "sk_lower_leg", text=T("Lower Leg"))
        col.prop(rebocap, "sk_ankle", text=T("Ankle Height"))
        col.prop(rebocap, "sk_foot", text=T("Foot"))
