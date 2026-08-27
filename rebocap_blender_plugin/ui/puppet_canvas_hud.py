import os
import math
import bpy
import gpu
from gpu_extras.batch import batch_for_shader
import blf
from ..core.translation import T


# 22 Bone Slot Definitions matching Maya HumanIK Mannequin (Normalized Coordinates 389 x 865)
DEFAULT_SLOT_DEFS = [
    ( 0, "Pelvis",       [194.5, 394.7], 15.0, "Pelvis (骨盆)"),
    ( 1, "L_UpLeg",      [157.0, 520.0], 13.5, "L_UpLeg (左大腿)"),
    ( 2, "R_UpLeg",      [231.9, 520.0], 13.5, "R_UpLeg (右大腿)"),
    ( 3, "Spine",        [195.4, 340.8], 12.5, "Spine (脊椎)"),
    ( 4, "L_DownLeg",    [158.9, 695.5], 13.0, "L_DownLeg (左小腿)"),
    ( 5, "R_DownLeg",    [230.0, 695.5], 13.0, "R_DownLeg (右小腿)"),
    ( 6, "Chest",        [194.5, 265.1], 13.5, "Chest (胸部)"),
    ( 7, "L_Foot",       [166.3, 820.8], 12.5, "L_Foot (左脚踝)"),
    ( 8, "R_Foot",       [222.6, 820.8], 12.5, "R_Foot (右脚踝)"),
    ( 9, "UpChest",      [194.5, 195.8], 11.5, "UpChest (上胸)"),
    (10, "L_Toe",        [114.7, 835.8], 10.5, "L_Toe (左脚尖)"),
    (11, "R_Toe",        [274.3, 835.8], 10.5, "R_Toe (右脚尖)"),
    (12, "Neck",         [194.5, 143.5], 12.0, "Neck (颈部)"),
    (13, "L_Shoulder",   [141.6, 155.5], 12.0, "L_Shoulder (左锁骨)"),
    (14, "R_Shoulder",   [248.7, 155.5], 12.0, "R_Shoulder (右锁骨)"),
    (15, "Head",         [194.5,  50.2], 14.5, "Head (头部)"),
    (16, "L_UpArm",      [ 85.1, 269.5], 12.5, "L_UpArm (左大臂)"),
    (17, "R_UpArm",      [303.8, 269.5], 12.5, "R_UpArm (右大臂)"),
    (18, "L_DownArm",    [ 60.1, 394.7], 12.0, "L_DownArm (左前臂)"),
    (19, "R_DownArm",    [328.9, 394.7], 12.0, "R_DownArm (右前臂)"),
    (20, "L_Palm",       [ 47.7, 457.4], 12.5, "L_Palm (左手掌)"),
    (21, "R_Palm",       [341.2, 457.5], 12.5, "R_Palm (右手掌)"),
]

# Body wireframe bone link pairs (idx1, idx2)
BONE_LINKS = [
    (15, 12), (12, 9), (9, 6), (6, 3), (3, 0),       # Spine chain
    (9, 13), (13, 16), (16, 18), (18, 20),           # Left arm
    (9, 14), (14, 17), (17, 19), (19, 21),           # Right arm
    (0, 1), (1, 4), (4, 7), (7, 10),                 # Left leg
    (0, 2), (2, 5), (5, 8), (8, 11),                 # Right leg
]

IMG_REF_W = 389.0
IMG_REF_H = 865.0


def _get_shader_2d_uniform():
    try:
        return gpu.shader.from_builtin('UNIFORM_COLOR')
    except Exception:
        return gpu.shader.from_builtin('2D_UNIFORM_COLOR')

def _get_shader_2d_image():
    try:
        return gpu.shader.from_builtin('IMAGE_2D')
    except Exception:
        return gpu.shader.from_builtin('2D_IMAGE')


def draw_rect(x, y, w, h, color):
    try:
        shader = _get_shader_2d_uniform()
        vertices = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        indices = [(0, 1, 2), (2, 3, 0)]
        batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
        shader.bind()
        shader.uniform_float("color", color)
        batch.draw(shader)
    except Exception:
        pass


def draw_rect_border(x, y, w, h, color, line_width=1.0):
    try:
        shader = _get_shader_2d_uniform()
        vertices = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        indices = [(0, 1), (1, 2), (2, 3), (3, 0)]
        batch = batch_for_shader(shader, 'LINES', {"pos": vertices}, indices=indices)
        shader.bind()
        shader.uniform_float("color", color)
        gpu.state.line_width_set(line_width)
        batch.draw(shader)
        gpu.state.line_width_set(1.0)
    except Exception:
        pass


def draw_line(x1, y1, x2, y2, color, line_width=1.5):
    try:
        shader = _get_shader_2d_uniform()
        vertices = [(x1, y1), (x2, y2)]
        indices = [(0, 1)]
        batch = batch_for_shader(shader, 'LINES', {"pos": vertices}, indices=indices)
        shader.bind()
        shader.uniform_float("color", color)
        gpu.state.line_width_set(line_width)
        batch.draw(shader)
        gpu.state.line_width_set(1.0)
    except Exception:
        pass


def draw_circle(cx, cy, r, color, segments=24):
    try:
        shader = _get_shader_2d_uniform()
        vertices = [(cx, cy)]
        indices = []
        for i in range(1, segments + 1):
            angle = 2.0 * math.pi * (i - 1) / segments
            vertices.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        for i in range(1, segments):
            indices.append((0, i, i + 1))
        indices.append((0, segments, 1))
        batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
        shader.bind()
        shader.uniform_float("color", color)
        batch.draw(shader)
    except Exception:
        pass


def draw_ring(cx, cy, r, color, line_width=2.0, segments=24):
    try:
        shader = _get_shader_2d_uniform()
        vertices = []
        indices = []
        for i in range(segments):
            angle = 2.0 * math.pi * i / segments
            vertices.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
            indices.append((i, (i + 1) % segments))
        batch = batch_for_shader(shader, 'LINES', {"pos": vertices}, indices=indices)
        shader.bind()
        shader.uniform_float("color", color)
        gpu.state.line_width_set(line_width)
        batch.draw(shader)
        gpu.state.line_width_set(1.0)
    except Exception:
        pass


def draw_image(image_texture, x, y, w, h, color=(1.0, 1.0, 1.0, 1.0)):
    if not image_texture:
        return
    try:
        shader = _get_shader_2d_image()
        vertices = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        tex_coords = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        indices = [(0, 1, 2), (2, 3, 0)]
        batch = batch_for_shader(shader, 'TRIS', {"pos": vertices, "texCoord": tex_coords}, indices=indices)
        shader.bind()
        try:
            shader.uniform_sampler("image", image_texture)
        except Exception:
            shader.uniform_float("image", image_texture)
        batch.draw(shader)
    except Exception:
        pass


def draw_text(text, x, y, size=11, color=(1.0, 1.0, 1.0, 1.0)):
    try:
        font_id = 0
        blf.position(font_id, x, y, 0)
        blf.size(font_id, size)
        blf.color(font_id, *color)
        blf.draw(font_id, text)
    except Exception:
        pass


# ================== Viewport HUD State & Manager ==================
class PuppetCanvasState:
    is_active = False
    draw_handle = None
    
    # Position & Size (Floating on 3D Viewport)
    x = 40.0
    y = 80.0
    w = 220.0
    h = 480.0
    
    is_dragging = False
    drag_offset_x = 0.0
    drag_offset_y = 0.0
    
    hovered_slot = -1
    image_texture = None
    bpy_image = None


def ensure_texture_loaded():
    if PuppetCanvasState.image_texture:
        return PuppetCanvasState.image_texture
        
    res_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
    img_path = os.path.join(res_dir, "mannequin_outline.png")
    if not os.path.exists(img_path):
        return None
        
    img_name = ".rebocap_mannequin_outline"
    bpy_img = bpy.data.images.get(img_name)
    if not bpy_img:
        try:
            bpy_img = bpy.data.images.load(img_path, check_existing=True)
            bpy_img.name = img_name
            bpy_img.use_fake_user = True
        except Exception:
            return None
            
    PuppetCanvasState.bpy_image = bpy_img
    try:
        PuppetCanvasState.image_texture = gpu.texture.from_image(bpy_img)
    except Exception:
        pass
    return PuppetCanvasState.image_texture


def draw_puppet_hud_callback():
    if not PuppetCanvasState.is_active:
        return
        
    context = bpy.context
    scene = context.scene
    bone_map = getattr(scene, 'rebocap_bone_map', None)
    
    gpu.state.blend_set('ALPHA')
    
    px = PuppetCanvasState.x
    py = PuppetCanvasState.y
    pw = PuppetCanvasState.w
    ph = PuppetCanvasState.h
    header_h = 28.0
    
    # 1. 绘制主体卡片背景 (半透明黑灰色) + 细边框
    draw_rect(px, py, pw, ph, (0.11, 0.12, 0.14, 0.94))
    draw_rect_border(px, py, pw, ph, (0.28, 0.30, 0.35, 0.95), line_width=1.5)
    
    # 2. 标题栏
    draw_rect(px, py + ph - header_h, pw, header_h, (0.15, 0.17, 0.20, 0.98))
    draw_rect_border(px, py + ph - header_h, pw, header_h, (0.32, 0.35, 0.40, 0.8), line_width=1.0)
    draw_text("👤 Rebocap Skeleton View", px + 8.0, py + ph - 19.0, size=11, color=(0.95, 0.95, 0.98, 1.0))
    
    # 关闭按钮 [X]
    btn_close_x = px + pw - 20.0
    btn_close_y = py + ph - 20.0
    draw_text("✕", btn_close_x, btn_close_y, size=12, color=(0.8, 0.8, 0.85, 1.0))
    
    # 3. 计算 22 个插槽在视口屏幕上的绝对坐标
    body_pad_x = 12.0
    body_pad_bottom = 28.0
    body_w = pw - body_pad_x * 2.0
    body_h = ph - header_h - body_pad_bottom
    body_x = px + body_pad_x
    body_y = py + body_pad_bottom
    scale_x = body_w / IMG_REF_W
    scale_y = body_h / IMG_REF_H
    
    # 绘制人体线稿图片底图 (mannequin_outline.png)
    tex = ensure_texture_loaded()
    if tex:
        draw_image(tex, body_x, body_y, body_w, body_h, color=(1.0, 1.0, 1.0, 0.85))
        
    slot_screen_coords = {}
    for idx, b_name, ref_pos, radius, label in DEFAULT_SLOT_DEFS:
        cx = body_x + ref_pos[0] * scale_x
        cy = body_y + (IMG_REF_H - ref_pos[1]) * scale_y
        slot_screen_coords[idx] = (cx, cy, radius * 0.52)
        
    # 4. 绘制人偶骨骼拓扑骨架连线 (Vector Skeleton Bone Links)
    for idx1, idx2 in BONE_LINKS:
        if idx1 in slot_screen_coords and idx2 in slot_screen_coords:
            p1 = slot_screen_coords[idx1]
            p2 = slot_screen_coords[idx2]
            draw_line(p1[0], p1[1], p2[0], p2[1], (0.38, 0.44, 0.54, 0.55), line_width=1.5)
            
    # 5. 绘制 22 个发光同心圆插槽 (原点)
    for idx, b_name, ref_pos, radius, label in DEFAULT_SLOT_DEFS:
        cx, cy, r = slot_screen_coords[idx]
        
        # 判断映射状态
        mapped_bone = getattr(bone_map, f"node_{idx}", "") if bone_map else ""
        is_mapped = bool(mapped_bone and mapped_bone.strip())
        is_hovered = (PuppetCanvasState.hovered_slot == idx)
        
        # 5.1 光晕与外圈
        if is_hovered:
            draw_ring(cx, cy, r + 3.0, (0.95, 0.61, 0.07, 0.65), line_width=3.5) # 橙黄发光
            draw_ring(cx, cy, r, (1.0, 1.0, 1.0, 1.0), line_width=2.0)
            draw_circle(cx, cy, r * 0.45, (1.0, 1.0, 1.0, 1.0))
        elif is_mapped:
            draw_ring(cx, cy, r, (0.18, 0.80, 0.44, 1.0), line_width=2.2)      # 绿色已映射
            draw_circle(cx, cy, r * 0.42, (1.0, 1.0, 1.0, 0.95))
        else:
            draw_ring(cx, cy, r, (0.50, 0.53, 0.60, 0.85), line_width=1.5)     # 灰色未映射
            draw_circle(cx, cy, r * 0.38, (0.28, 0.30, 0.35, 0.85))
            
    # 6. 底部状态提示条
    if PuppetCanvasState.hovered_slot >= 0:
        h_idx = PuppetCanvasState.hovered_slot
        h_item = DEFAULT_SLOT_DEFS[h_idx]
        b_val = getattr(bone_map, f"node_{h_idx}", "") if bone_map else ""
        disp_txt = f"{h_item[1]}: {b_val}" if b_val else f"{h_item[1]}: (点击绑定)"
        draw_rect(px + 4.0, py + 4.0, pw - 8.0, 18.0, (0.0, 0.5, 0.8, 0.9))
        draw_text(disp_txt, px + 8.0, py + 8.0, size=10, color=(1.0, 1.0, 1.0, 1.0))
    else:
        draw_text("💡 点击插槽绑定当前选中骨骼", px + 8.0, py + 8.0, size=10, color=(0.6, 0.65, 0.7, 0.8))
        
    gpu.state.blend_set('NONE')


# ================== Modal Operator for Interactive Viewport Control ==================
class REBOCAP_OT_toggle_puppet_hud(bpy.types.Operator):
    bl_idname = "rebocap.toggle_puppet_hud"
    bl_label = "开启人偶骨骼映射视口 (Puppet HUD)"
    bl_description = "在 3D 视口中开启/关闭交互式人偶骨骼映射画布"

    def modal(self, context, event):
        if not PuppetCanvasState.is_active:
            self.stop_hud(context)
            return {'FINISHED'}

        mx = event.mouse_region_x
        my = event.mouse_region_y
        px = PuppetCanvasState.x
        py = PuppetCanvasState.y
        pw = PuppetCanvasState.w
        ph = PuppetCanvasState.h
        header_h = 28.0

        # 1. 拖拽标题栏移动窗口
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                # 检查关闭按钮
                if (px + pw - 25 <= mx <= px + pw) and (py + ph - header_h <= my <= py + ph):
                    self.stop_hud(context)
                    return {'FINISHED'}
                # 检查标题栏拖拽
                if (px <= mx <= px + pw) and (py + ph - header_h <= my <= py + ph):
                    PuppetCanvasState.is_dragging = True
                    PuppetCanvasState.drag_offset_x = mx - px
                    PuppetCanvasState.drag_offset_y = my - py
                    return {'RUNNING_MODAL'}
                # 检查点击插槽绑定
                if (px <= mx <= px + pw) and (py <= my <= py + ph - header_h):
                    clicked_slot = self._hit_test_slot(mx, my)
                    if clicked_slot >= 0:
                        self._assign_selected_bone_to_slot(context, clicked_slot)
                        context.area.tag_redraw()
                        return {'RUNNING_MODAL'}
            elif event.value == 'RELEASE':
                PuppetCanvasState.is_dragging = False

        elif event.type == 'MOUSEMOVE':
            if PuppetCanvasState.is_dragging:
                PuppetCanvasState.x = mx - PuppetCanvasState.drag_offset_x
                PuppetCanvasState.y = my - PuppetCanvasState.drag_offset_y
                context.area.tag_redraw()
                return {'RUNNING_MODAL'}
            else:
                # 鼠标悬停检测
                prev_h = PuppetCanvasState.hovered_slot
                PuppetCanvasState.hovered_slot = self._hit_test_slot(mx, my)
                if PuppetCanvasState.hovered_slot != prev_h:
                    context.area.tag_redraw()

        elif event.type in {'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            self.stop_hud(context)
            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def _hit_test_slot(self, mx, my):
        px = PuppetCanvasState.x
        py = PuppetCanvasState.y
        pw = PuppetCanvasState.w
        ph = PuppetCanvasState.h
        header_h = 28.0
        body_pad_x = 12.0
        body_pad_bottom = 28.0
        body_w = pw - body_pad_x * 2.0
        body_h = ph - header_h - body_pad_bottom
        body_x = px + body_pad_x
        body_y = py + body_pad_bottom
        scale_x = body_w / IMG_REF_W
        scale_y = body_h / IMG_REF_H

        for idx, b_name, ref_pos, radius, label in DEFAULT_SLOT_DEFS:
            cx = body_x + ref_pos[0] * scale_x
            cy = body_y + (IMG_REF_H - ref_pos[1]) * scale_y
            r = radius * 0.55
            dist = math.hypot(mx - cx, my - cy)
            if dist <= r + 4.0:
                return idx
        return -1

    def _assign_selected_bone_to_slot(self, context, slot_idx):
        bone_map = getattr(context.scene, 'rebocap_bone_map', None)
        if not bone_map:
            return
        armature = context.object
        if not armature or armature.type != 'ARMATURE':
            src_name = context.scene.rebocap_source_armature
            armature = bpy.data.objects.get(src_name)
            
        if not armature or armature.type != 'ARMATURE':
            self.report({'WARNING'}, T("Please select an armature object."))
            return

        selected_bones = [b.name for b in armature.data.bones if b.select]
        if not selected_bones:
            self.report({'WARNING'}, T("No bone selected."))
            return

        bone_name = selected_bones[0]
        setattr(bone_map, f"node_{slot_idx}", bone_name)
        slot_info = DEFAULT_SLOT_DEFS[slot_idx]
        self.report({'INFO'}, f"✅ {slot_info[1]} ➔ {bone_name}")

    def invoke(self, context, event):
        if PuppetCanvasState.is_active:
            self.stop_hud(context)
            return {'FINISHED'}
            
        PuppetCanvasState.is_active = True
        PuppetCanvasState.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            draw_puppet_hud_callback, (), 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def stop_hud(self, context):
        PuppetCanvasState.is_active = False
        if PuppetCanvasState.draw_handle:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(PuppetCanvasState.draw_handle, 'WINDOW')
            except Exception:
                pass
            PuppetCanvasState.draw_handle = None
        if context and context.area:
            context.area.tag_redraw()
