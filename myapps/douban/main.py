# -*- coding: utf-8 -*-
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (
    IRightBody,
    MDList,
    ILeftBody,
    OneLineIconListItem,
)
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivymd.uix.list import TwoLineAvatarIconListItem
from movie_data import Movies
from kivy.uix.image import AsyncImage
from MOVIE_TYPES import MOVIE_TYPES


class douban(MDApp):
    def __init__(self, **kwargs) -> None:
        self.type_id = 3
        self.theme_cls.primary_palette = "LightBlue"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.accent_palette = "Gray"
        self.theme_cls.accent_hue = "600"

        # Need to replace the default font to show Chinese characters
        # use MSYH font
        LabelBase.register(name="MSYH", fn_regular="./myapps/douban/fonts/msyh.ttc")
        theme_font_styles.append("MSYH")
        # This version of kivyMD has a bug that it doesn't allow you to use the custom font styles
        # Even you have added them to the theme class
        # As a workaround, changed the 2 presets of font styles: Body2 and H6 to use new fonts
        self.theme_cls.font_styles["Body2"] = [
            "MSYH",
            16,
            False,
            0.15,
        ]
        self.theme_cls.font_styles["H6"] = [
            "MSYH",
            20,
            False,
            0.15,
        ]
        Window.size = (400, 640)
        super().__init__(**kwargs)

    def build(self):
        self.title = "Top Movies"
        Builder.load_file("./myapps/douban/main.kv")
        return Root()


class Root(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(ListScreen(name="list"))
        self.add_widget(CardScreen(name="card"))
        self.current = "list"


class ListScreen(Screen):
    pass


class CardScreen(Screen):
    movie = ObjectProperty(None)

    def go_back(self):
        self.parent.current = "list"


class MovieList(MDList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.refresh_widgets()

    def get_movies(self, type_id):
        self.movies = Movies(type_id).get_movies()

    def refresh_widgets(self):
        self.clear_widgets()
        self.get_movies(MDApp.get_running_app().type_id)
        for movie in self.movies:
            movie["cover_url"] = movie["cover_url"].replace("\\", "/")
            self.add_widget(MovieItem(movie))


class MovieItem(TwoLineAvatarIconListItem):
    def __init__(self, movie_info, **kwargs):
        super().__init__(**kwargs)
        self.movie_info = movie_info
        title = movie_info["title"]
        score = movie_info["score"]
        self.text = f"{title}"
        self.secondary_text = movie_info["release_date"]
        self.font_style = "Body2"

        # Don't know if there are better ways to assess the child widgets
        self.children[1].children[0].source = movie_info["cover_url"]
        self.children[0].children[0].text = score

    def on_press(self):
        card_screen = MDApp.get_running_app().root.get_screen("card")
        card_screen.ids.card_toolbar.title = self.movie_info["title"]
        card_screen.ids.card_post.source = self.movie_info["cover_url"]
        card_screen.ids.card_region.text = " ".join(self.movie_info["regions"])
        card_screen.ids.card_actors.text = " ".join(self.movie_info["actors"])
        MDApp.get_running_app().root.current = "card"

        return super().on_press()


# custom class to use the AsyncImage instead of Image for the widget
class AsyncImageLeftWidget(ILeftBody, AsyncImage):
    pass


# custom class to use the MDLabel instead of Image/Icon for the widget
class LabelLeftWidget(IRightBody, MDLabel):
    pass


# Navigation Draw
class TypeList(MDList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for movie_type in MOVIE_TYPES:
            self.add_widget(MovieTypeItem(movie_type))


class MovieTypeItem(OneLineIconListItem):
    def __init__(self, movie_type, **kwargs):
        super().__init__(**kwargs)
        self.text = movie_type["title"]
        self.children[0].children[0].icon = movie_type["icon"]
        self.type_id = movie_type["type"]

    def on_press(self):
        MDApp.get_running_app().type_id = self.type_id
        main_screen = MDApp.get_running_app().root.get_screen("list")
        main_screen.ids.list_toolbar.title = self.text
        main_screen.ids.nav_drawer.set_state("close")
        main_screen.ids.movie_list.refresh_widgets()
        return super().on_press()


if __name__ == "__main__":
    douban().run()
