"""Empty window example."""

import math
import os

import moderngl_window as mglw


class Example(mglw.WindowConfig):
    """ModernGL Example."""

    aspect_ratio = 16 / 9
    gl_version = (3, 3)
    resizable = True
    resource_dir = os.path.normpath(os.path.join(__file__, "../data"))
    title = "ModernGL Example"
    window_size = (1280, 720)

    def render(self, time: float, frame_time: float):
        pass


class EmptyWindow(Example):
    """Empty Window class."""

    title = "Empty Window"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, time: float, frame_time: float):
        """Render the scene."""
        self.ctx.clear(
            (math.sin(time) + 1.0) / 2,
            (math.sin(time + 2) + 1.0) / 2,
            (math.sin(time + 3) + 1.0) / 2,
        )

    def resize(self, width: int, height: int):
        """Pick window resizes in case we need yo update internal states when this
        happens."""
        print("Window resized to", width, height)

    def iconify(self, iconified: bool):
        """Window hide/minimize and restore."""
        print("Window was iconified:", iconified)

    def key_event(self, key, action, modifiers):
        """Handle keyboard events."""
        keys = self.wnd.keys

        # Ignore key presses without action
        if action != keys.ACTION_PRESS:
            return

        # Move window around with WASD
        if key == keys.A:
            self.wnd.position = self.wnd.position[0] - 20, self.wnd.position[1]
        if key == keys.D:
            self.wnd.position = self.wnd.position[0] + 20, self.wnd.position[1]
        if key == keys.W:
            self.wnd.position = self.wnd.position[0], self.wnd.position[1] - 20
        if key == keys.S:
            self.wnd.position = self.wnd.position[0], self.wnd.position[1] + 20


if __name__ == "__main__":
    EmptyWindow.run()
