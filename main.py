import time

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import sp, dp
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.clock import Clock
import os

Window.size = (450, 900)

Builder.load_file('clicker.kv')

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    # Перехід до екрана гри
    def go_game(self, *args):
        app.LEVEL = 0
        self.manager.current = "game"
        self.manager.transition.direction = "left"

    # Перехід до екрана налаштувань
    def go_settings(self, *args):
        self.manager.current = "settings"
        self.manager.transition.direction = "up"

    # Вихід з програми
    def exit_app(self, *args):
        App.get_running_app().stop()


class GameScreen(Screen):
    score = NumericProperty(0)

    def on_pre_enter(self, *args):
        self.score = 0
        app = App.get_running_app()

        self.ids.game_complete.opacity = 0
        self.ids.game_complete.text = ""
        self.ids.game_complete.font_size = "40sp"

        self.ids.level_complete.opacity = 0
        self.ids.level_complete.text = ""
        self.ids.level_complete.font_size = "40sp"

        self.ids.fish.fish_index = 0
        self.ids.click_label.text = f"Clicks: {self.score}"
        return super().on_pre_enter(*args)

    def on_enter(self, *args):
        self.start_game()
        return super().on_enter(*args)

    def start_game(self):
        self.ids.fish.new_fish()

    def game_complete(self, *args):

        self.ids.game_complete.text = "YOU WIN!"
        self.ids.game_complete.color = "green"
        self.ids.game_complete.font_name = app.fonty
        self.ids.game_complete.opacity = 1

    def level_complete(self, *args):
        self.ids.level_complete.text = "Level complete!"
        self.ids.level_complete.color = "cyan"
        self.ids.level_complete.font_name = app.fonty
        self.ids.level_complete.opacity = 1
        Clock.schedule_once(self.next_level_text, 3)
        Clock.schedule_once(self.hide_text, 6)


    def next_level_text(self, dt):
        self.ids.level_complete.opacity = 0
        self.ids.level_complete.text = "Next level!"
        self.ids.level_complete.opacity = 1

    def hide_text(self, dt):
        self.ids.level_complete.opacity = 0

    def go_menu(self):
        self.manager.current = "menu"
        self.manager.transition.direction = "right"


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def go_menu(self, *args):
        self.manager.current = "menu"
        self.manager.transition.direction = "down"



class Fish(Image):
    fish_current = None
    fish_index = 0
    hp_current = None


    def on_touch_down(self, touch):

        game_screen = self.parent.parent.parent
        app = App.get_running_app()


        if self.collide_point(*touch.pos) and self.opacity:
            self.hp_current -= 1


            game_screen.score += 1
            game_screen.ids.click_label.text = f"Clicks: {game_screen.score}"


            if self.hp_current <= 0:
                self.defeated()


                if len(app.LEVELS[app.LEVEL]) > self.fish_index + 1:
                    self.fish_index += 1
                    Clock.schedule_once(self.new_fish, 1.2)
                else:
                    self.fish_index = 0
                    app.LEVEL += 1
                    Clock.schedule_once(game_screen.level_complete, 1.2)
                    if app.LEVEL < len(app.LEVELS):
                        Clock.schedule_once(self.new_fish, 7.2)
                    else:
                        Clock.schedule_once(game_screen.game_complete, 1.2)


            return True

        return super().on_touch_down(touch)

    def new_fish(self, *args):
        app = App.get_running_app()
        self.fish_current = app.LEVELS[app.LEVEL][self.fish_index]
        self.source = app.FISHES[self.fish_current]['source']
        self.hp_current = app.FISHES[self.fish_current]['hp']
        self.opacity = 1


    def defeated(self):
        self.opacity = 0



class ClickerApp(App):
    LEVEL = 0
    fonty = "assets/fonts/Lemon-Regular.ttf"
    imagy_main = "assets/images/cool cat.jpg"
    imagy_car1 = "assets/images/cat1.jpg"
    imagy_car2 = "assets/images/cat2.jpg"
    imagy_car3 = "assets/images/cat3.jpg"

    FISHES = {
        'cat1':
            {'source': imagy_car1, 'hp': 10},
        'cat2':
            {'source': imagy_car2, 'hp': 20},
        'cat3':
            {'source': imagy_car3, 'hp' : 25}
    }

    LEVELS = [
        ['cat1', 'cat1', 'cat2'],
        ['cat1', 'cat2', 'cat3'],
        ['cat2', 'cat3', 'cat3']
    ]

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm


app = ClickerApp()
app.run()
