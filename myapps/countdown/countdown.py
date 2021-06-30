import os
import platform

from kivy.core.window import Window
from kivymd.app import MDApp

from libs.uix.baseclass.root import Root

# This is needed for supporting Windows 10 with OpenGL < v2.0
if platform.system() == "Windows":
    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"


class countdown(MDApp):  # NOQA: N801

    username = "Guest"

    def __init__(self, **kwargs):
        super(countdown, self).__init__(**kwargs)
        Window.soft_input_mode = "below_target"
        Window.size = (600, 650)
        self.title = "Countdown 321"

        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.primary_hue = "400"

        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.accent_hue = "400"

        self.theme_cls.theme_style = "Light"

    def build(self):
        return Root()
