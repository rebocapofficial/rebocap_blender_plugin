import bpy
from ..core.translation import T

class REBOCAP_PT_fk_panel(bpy.types.Panel):
    bl_idname = 'REBOCAP_PT_fk_panel'
    bl_label = " "
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "REBOCAP CONNECTION"
    bl_order = 2
    
    def draw_header(self, context):
        self.layout.label(text=T('FK Animation Mode'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bones = [
            "Pelvis", "L_UpLeg", "R_UpLeg", "Spine", "L_DownLeg", "R_DownLeg",
            "Chest", "L_Foot", "R_Foot", "UpChest", "L_Toe", "R_Toe",
            "Neck", "L_Shoulder", "R_Shoulder", "Head", "L_UpArm", "R_UpArm",
            "L_DownArm", "R_DownArm", "L_Palm", "R_Palm", "L_Fingers", "R_Fingers",
        ]
        self.center_bone = [0, 3, 6, 9, 12, 15]
        self.left_bone = [1, 4, 7, 10, 13, 16, 18, 20]
        self.right_bone = [2, 5, 8, 11, 14, 17, 19, 21]
        self.side_names = [self.bones[i][2:] for i in self.left_bone]

    def draw(self, ctx):
        layout = self.layout
        rebocap_bone_map = ctx.scene.rebocap_bone_map
        col = layout.column()
        
        # 1. 3D 视口人偶画布 HUD 入口
        from .puppet_canvas_hud import PuppetCanvasState
        row_puppet = col.row(align=True)
        row_puppet.scale_y = 1.3
        is_active = PuppetCanvasState.is_active
        btn_text = T("👤 隐藏人偶骨骼HUD") if is_active else T("👤 显示人偶骨骼HUD")
        row_puppet.operator('rebocap.toggle_puppet_hud', text=btn_text, icon='USER', depress=is_active)
        col.separator()
        
        row = col.row(align=True)
        source = bpy.data.objects.get(ctx.scene.rebocap_source_armature)
        
        label_col = row.column(align=True)
        if source is None or source.type != 'ARMATURE':
            label_col.alert = True
            label_col.label(text=T('Source'), icon='ERROR')
        else:
            label_col.label(text=T('Source'))
            
        search_col = row.column(align=True)
        search_col.prop_search(ctx.scene, 'rebocap_source_armature', ctx.scene, 'objects', text='')
        
        if True:
            row = col.row()
            row.operator('rebocap.auto_map_bone', text=T('Auto Detect'), icon='BONE_DATA')
            row = col.row()
            if getattr(ctx.scene, 'rebocap_show_auto_detect_help', False):
                row.prop(ctx.scene, 'rebocap_show_auto_detect_help', text=T("Hide Supported Formats"), icon='TRIA_DOWN', toggle=True)
                box_help = col.box()
                box_help.label(text=T("✅ Unreal Engine (UE4/UE5/MetaHuman)"))
                box_help.label(text=T("✅ Rebocap Standard"))
                box_help.label(text=T("✅ Mixamo (with/without prefix)"))
                box_help.label(text=T("✅ VRM Humanoid"))
            else:
                row.prop(ctx.scene, 'rebocap_show_auto_detect_help', text=T("View Supported Formats"), icon='TRIA_RIGHT', toggle=True)
            col = layout.column()
            
            box = layout.box()
            box.label(text=T("Setup Character Bones"), icon="ARMATURE_DATA")
            
            # JSON 导入导出按键
            row = box.row(align=True)
            row.operator("rebocap.import_bone_map", text=T("Import Bone Map JSON"), icon='IMPORT')
            row.operator("rebocap.export_bone_map", text=T("Export Bone Map JSON"), icon='EXPORT')
            box.separator()

            row = box.row(align=True).split(factor=0.15, align=True)
            column0 = row.column(align=True)
            column1 = row.column(align=True)
            for i in range(len(self.center_bone)):
                name = self.bones[self.center_bone[i]]
                column0.label(text=name)
                new_row = column1.split(factor=0.93, align=True)
                if source and source.type == 'ARMATURE':
                    new_row.prop_search(rebocap_bone_map, f'node_{self.center_bone[i]}', source.pose, 'bones', text='')
                else:
                    new_row.prop(rebocap_bone_map, f'node_{self.center_bone[i]}', text='')
                new_row.operator("object.pick_bone", text="", icon='RESTRICT_SELECT_OFF').bone_type = f'node_{self.center_bone[i]}'

            row = box.row(align=True).split(factor=0.15, align=True)
            column0 = row.column(align=True)
            column1 = row.column(align=True)
            column2 = row.column(align=True)
            column0.label(text='')
            column1.label(text=T('Left'))
            column2.label(text=T('Right'))
            for i in range(len(self.side_names)):
                column0.label(text=self.side_names[i])
                new_row1 = column1.split(factor=0.93, align=True)
                if source and source.type == 'ARMATURE':
                    new_row1.prop_search(rebocap_bone_map,  f'node_{self.left_bone[i]}', source.pose, 'bones', text='')
                else:
                    new_row1.prop(rebocap_bone_map,  f'node_{self.left_bone[i]}', text='')
                new_row1.operator("object.pick_bone", text="", icon='RESTRICT_SELECT_OFF').bone_type = f'node_{self.left_bone[i]}'

                new_row2 = column2.split(factor=0.93, align=True)
                if source and source.type == 'ARMATURE':
                    new_row2.prop_search(rebocap_bone_map,  f'node_{self.right_bone[i]}', source.pose, 'bones', text='')
                else:
                    new_row2.prop(rebocap_bone_map,  f'node_{self.right_bone[i]}', text='')
                new_row2.operator("object.pick_bone", text="", icon='RESTRICT_SELECT_OFF').bone_type = f'node_{self.right_bone[i]}'
                if i == 3:
                    column0.separator()
                    column1.separator()
                    column2.separator()



