import bpy
from ..core.translation import T
from ..ops.history import _get_effective_target_fps

class REBOCAP_UL_history_takes(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        take = item
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.prop(take, "name", text="", emboss=False, icon='ACTION')
            row.label(text=f"[{take.take_type}]", icon='ARMATURE_DATA' if take.take_type == 'FK' else 'EMPTY_DATA')
            
            target_fps = _get_effective_target_fps(context.scene)
            recorded_fps = take.recorded_fps if hasattr(take, 'recorded_fps') and take.recorded_fps > 0 else 60.0
            converted_frames = int(round(take.frame_count * target_fps / recorded_fps))
            
            if take.frame_count == converted_frames and abs(recorded_fps - target_fps) < 0.1:
                row.label(text=f"{take.frame_count} F")
            else:
                row.label(text=f"{take.frame_count} F ➔ {converted_frames} F")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='ACTION')

class REBOCAP_PT_history_panel(bpy.types.Panel):
    bl_idname = "REBOCAP_PT_history_panel"
    bl_label = " "
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "REBOCAP CONNECTION"
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 1
    
    def draw_header(self, context):
        scene = context.scene
        count = len(scene.rebocap_takes)
        has_new = getattr(scene, 'rebocap_has_new_take', False) and count > 0
        if count == 0:
            self.layout.label(text=T("History & Takes"), icon='FILE_FOLDER')
        else:
            badge = f"[{count}] 🔴" if has_new else f"[{count}]"
            icon_name = 'REC' if has_new else 'ACTION'
            self.layout.label(text=f"{T('History & Takes')}  {badge}", icon=icon_name)

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row(align=True)
        row.operator("rebocap.apply_take", icon='PLAY', text=T("Apply Take"))
        
        # 表头 (Table Header)
        target_fps = _get_effective_target_fps(scene)
        tgt_str = f"{target_fps:g}fps" if abs(target_fps - round(target_fps)) < 1e-3 else f"{target_fps:.2f}fps"
        
        row_hdr = layout.row(align=True)
        row_hdr.label(text=T("片段名称"))
        row_hdr.label(text=T("类型"))
        if abs(target_fps - 60.0) < 0.1:
            row_hdr.label(text=f"{T('总帧数')} (60fps)")
        else:
            row_hdr.label(text=f"60fps ➔ {tgt_str}")
        
        row = layout.row()
        row.template_list(
            "REBOCAP_UL_history_takes",
            "",
            scene,
            "rebocap_takes",
            scene,
            "rebocap_active_take_index"
        )
        
        col = layout.column(align=True)
        col.operator("rebocap.delete_take", icon='X', text=T("Delete Take"))
        
        layout.separator()
        
        box = layout.box()
        col = box.column(align=True)
        col.label(text=T("挂载与导出帧率设置 (FPS Mode):"), icon='TIME')
        col.prop(scene, "rebocap_fps_mode", text="")
        if getattr(scene, 'rebocap_fps_mode', 'SCENE') == 'CUSTOM':
            col.prop(scene, "rebocap_target_fps", text=T("自定义帧率 (Target FPS)"))
            
        col.separator()
        col_note = col.column(align=True)
        col_note.enabled = False
        col_note.label(text=T("插件录制时按60fps记录母带保存，"), icon='INFO')
        col_note.label(text=f"   {T('通过该选项转换帧率挂载到blender时间轴上。')}")
            
        layout.separator()
        
        row = layout.row(align=True)
        row.operator("rebocap.export_take", icon='EXPORT', text=T("导出片段json"))
        row.operator("rebocap.import_take", icon='IMPORT', text=T("导入片段json"))

classes = [
    REBOCAP_UL_history_takes,
    REBOCAP_PT_history_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
