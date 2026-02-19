"""
FILE: TheButler.py
VERSION: 0.24.1
LAST UPDATED: 2026-02-19
DESCRIPTION: The Graffiti Artist. Delivers the Kivy UI and voice-first interaction.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from _Configuration import cfg

# Theme Colors (High Contrast)
THEMES = {
    "DAY": {"bg": [1, 1, 1, 1], "text": [0, 0, 0, 1], "btn": [0.8, 0.8, 0.8, 1]},
    "NIGHT": {"bg": [0, 0, 0, 1], "text": [1, 0, 0, 1], "btn": [0.2, 0, 0, 1]}
}

class HomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        theme = THEMES.get(cfg.UI_THEME, THEMES["DAY"])
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # App Title
        layout.add_widget(Label(text="The Not Boring Company", font_size='30sp', color=theme["text"]))
        
        # Big Chunky Buttons
        btn_once = Button(text="ONCE", size_hint=(1, 0.3), background_color=theme["btn"])
        btn_once.bind(on_release=self.run_once)
        
        btn_exit = Button(text="EXIT", size_hint=(1, 0.3), background_color=theme["btn"])
        btn_exit.bind(on_release=lambda x: App.get_running_app().stop())
        
        layout.add_widget(btn_once)
        layout.add_widget(btn_exit)
        self.add_widget(layout)

    def run_once(self, instance):
        # This will trigger the main engine logic
        print("[BUTLER] Triggering Run Once...")
        self.manager.current = 'conversation'

class InConversationScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        theme = THEMES.get(cfg.UI_THEME, THEMES["DAY"])
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        self.location_label = Label(text="Locating...", font_size='20sp', color=theme["text"])
        self.layout.add_widget(self.location_label)
        
        # Interaction Buttons
        self.btn_more = Button(text="MORE", size_hint=(1, 0.2), background_color=theme["btn"])
        self.btn_repeat = Button(text="REPEAT", size_hint=(1, 0.2), background_color=theme["btn"])
        self.btn_stop = Button(text="STOP", size_hint=(1, 0.2), background_color=theme["btn"])
        
        self.layout.add_widget(self.btn_more)
        self.layout.add_widget(self.btn_repeat)
        self.layout.add_widget(self.btn_stop)
        self.add_widget(self.layout)

class TheButler(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(InConversationScreen(name='conversation'))
        return sm

    def speak(self, text):
        """Placeholder for Android TTS. Prints to console during development."""
        print(f"[VOICE RESPONSE]: {text}")
        # When compiled for Android, we will use: 
        # from plyer import tts; tts.speak(text)

# --- VERSION LOG ---
# 0.24.1: Initial UI skeleton with high-contrast themes and ScreenManager.