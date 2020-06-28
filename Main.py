# Kivy modules
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition

# Python & Self-defined modules
import threading
import multiprocessing
import Controller as c
from MainScreen import Main_Screen, show_tutorial
from ClassifyScreen import Classify_Screen, show_help
from CreateScreen import Create_Screen, show_createHelp
from SettingsScreen import Settings_Screen

# KV Files
kv_main = None
kv_classify = None
kv_create = None
kv_settings = None

def load_pages():
    global kv_main
    global kv_classify
    global kv_create
    global kv_settings
    kv_main = Builder.load_file('Main.kv')
    kv_classify = Builder.load_file('Classify.kv')
    kv_settings = Builder.load_file('Settings.kv')
    kv_create = Builder.load_file('Create.kv')

def cancel_pages():
    global kv_main
    global kv_classify
    global kv_create
    global kv_settings
    kv_main = None
    kv_classify = None
    kv_create = None
    kv_settings = None



class MainScreen(Main_Screen):
    def classify_press(self):
        if c.getShowHelp('Classify') == 'True':
            p = threading.Thread(target=show_help, args=[True])
            p.start()
        cicada_master.screen_manager.current = 'Classify'

    def settings_press(self):
        cicada_master.screen_manager.current = 'Settings'


class ClassifyScreen(Classify_Screen):
    def back_press(self):
        self.clear_values()
        cicada_master.screen_manager.current = 'Main'
        

class SettingsScreen(Settings_Screen):
    def back_press(self):
        cicada_master.screen_manager.current = 'Main'

    def create_press(self):
        if c.getShowHelp('Create') == 'True':
            p = threading.Thread(target=show_createHelp, args=[True])
            p.start()
        cicada_master.screen_manager.current = 'Create'


class CreateScreen(Create_Screen):
    def back_press(self):
        cicada_master.screen_manager.current = 'Settings'


class CicadaMaster(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = 'cicada_icon.png'
        self.screen_manager = ScreenManager(transition=NoTransition())

    def build(self):
        screen = Screen(name='Main')
        screen.add_widget(MainScreen())
        self.screen_manager.add_widget(screen)

        screen = Screen(name='Classify')
        screen.add_widget(ClassifyScreen())
        self.screen_manager.add_widget(screen)

        screen = Screen(name='Settings')
        screen.add_widget(SettingsScreen())
        self.screen_manager.add_widget(screen)

        screen = Screen(name='Create')
        screen.add_widget(CreateScreen())
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    multiprocessing.freeze_support()
    cicada_master = CicadaMaster()

    if c.getShowHelp('Tutorial') == 'True':
        p = threading.Thread(target=show_tutorial)
        p.start()

    load_pages()
    cicada_master.run()
    cancel_pages()
