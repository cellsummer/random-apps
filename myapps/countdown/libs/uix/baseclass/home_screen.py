from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextFieldRect
from kivy.uix.popup import Popup
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from numpy import spacing


class HomeScreen(MDScreen):

    username = "Guest"
    leaderboard = {}

    def __init__(self, **kw):
        super().__init__(**kw)

    def refresh(self):
        try:
            board = self.children[0].children[0].children[1].children[0].children[0]
            board.generate()
        except:
            pass

    def reset(self):
        try:
            board = self.children[0].children[0].children[1].children[0].children[0]
            board.reset()
        except:
            pass

    def login(self):
        box = BoxLayout(
            orientation="vertical",
            padding=("10dp", "10dp", "10dp", "10dp"),
            spacing="10dp",
        )
        box.add_widget(
            MDTextFieldRect(size_hint=(1, None), height="40dp", multiline=False)
        )
        popup = Popup(
            title="Login",
            # title_size=(14),
            title_align="left",
            content=box,
            size_hint=(None, None),
            size=("500dp", "175dp"),
            auto_dismiss=True,
        )

        def signed_in(instance):
            self.username = box.children[1].text
            MDApp.get_running_app().username = self.username
            print(self.username)
            popup.dismiss(force=True)

        box.add_widget(MDRaisedButton(text="Log in", on_press=signed_in))

        # box.add_widget(Button(text="NO TO GO BACK", on_press=self.hypochlorinator_1))
        popup.open()

    """
    Example Screen.
    """
