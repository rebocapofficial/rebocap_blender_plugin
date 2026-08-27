import bpy


def show_message_box(message="", title="Message Box", icon='INFO'):
    def draw(self, context):
        for line in str(message).split('\n'):
            if line:
                self.layout.label(text=line)
            else:
                self.layout.separator()

    try:
        wm = getattr(bpy.context, 'window_manager', None)
        if wm:
            wm.popup_menu(draw, title=title, icon=icon)
    except Exception:
        pass
