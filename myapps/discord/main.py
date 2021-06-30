from kivy.core import window
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.core.window import Window


class Discord(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "LightBlue"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.accent_palette = "Gray"
        self.theme_cls.accent_hue = "600"
        Window.size = (400, 640)

    def build(self):
        return Builder.load_file("./myapps/discord/main.kv")


if __name__ == "__main__":
    Discord().run()
