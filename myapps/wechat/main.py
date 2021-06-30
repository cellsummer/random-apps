from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.bottomnavigation import MDBottomNavigationItem


class MainApp(MDApp):
    def __init__(self, **kwargs):
        # theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "400"
        self.theme_cls.accent_palette = "Gray"
        self.theme_cls.accent_hue = "900"
        self.theme_cls.theme_style = "Dark"
        super().__init__(**kwargs)

    def on_start(self):
        Window.size = (320, 600)
        return super().on_start()


class BottomNavChat(MDBottomNavigationItem):
    def on_enter(self, *args):
        self.icon = "chat"
        return super().on_enter(*args)

    def on_leave(self, *args):
        self.icon = "chat-outline"
        return super().on_leave(*args)


if __name__ == "__main__":
    MainApp().run()
