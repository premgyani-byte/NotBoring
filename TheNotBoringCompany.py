"""
FILE: TheNotBoringCompany.py
VERSION: 0.24.1
LAST UPDATED: 2026-02-19
DESCRIPTION: The Master Engine. Connects the UI, Database, and AI Researcher.
"""

from _Configuration import cfg
from Database import log_to_sheet, get_subjects_of_interest
from TheBrain import get_not_boring_fact
from TheButler import TheButler
import threading

class NotBoringEngine:
    """Coordinates the background logic so the UI doesn't freeze."""
    
    @staticmethod
    def run_research_cycle(app_instance):
        """The core logic for finding a 'Not Boring' fact."""
        try:
            log_to_sheet("Engine: Starting Research Cycle...", level=1)
            
            # 1. Get interests from your Google Sheet
            subjects = get_subjects_of_interest()
            
            # 2. Get current coordinates (Using Helpston as default for MVP testing)
            # In the final APK, these will come from the Android GPS
            lat, lon = 52.628, -0.347 
            
            # 3. Call Rupert
            thought = get_not_boring_fact(lat, lon, subjects, password=cfg.LOCK_PASSWORD)
            
            if thought and thought.subject_found:
                # Update the UI and speak the fact
                app_instance.root.get_screen('conversation').location_label.text = thought.location_name
                app_instance.speak(thought.interesting_fact)
                log_to_sheet(f"Rupert found: {thought.location_name}", level=2)
            else:
                msg = "Rupert found nothing but sheep and boredom here."
                app_instance.speak(msg)
                log_to_sheet(msg, level=1)
                
        except Exception as e:
            error_msg = f"Engine Error: {str(e)}"
            log_to_sheet(error_msg, level=1)
            print(error_msg)

def on_once_pressed(instance):
    """Bridge between the Button and the AI logic."""
    app = TheButler.get_running_app()
    # Run in a separate thread so the UI stays responsive while the AI 'thinks'
    threading.Thread(target=NotBoringEngine.run_research_cycle, args=(app,)).start()

if __name__ == "__main__":
    # Initialize the UI
    app = TheButler()
    
    # Bind the 'ONCE' button logic manually to the engine
    # (Doing this here keeps TheButler.py strictly focused on graphics)
    def setup_bindings(dt):
        home_screen = app.root.get_screen('home')
        # Find the button we created in TheButler and give it life
        for child in home_screen.children[0].children:
            if hasattr(child, 'text') and child.text == "ONCE":
                child.bind(on_release=on_once_pressed)

    from kivy.clock import Clock
    Clock.schedule_once(setup_bindings, 1)
    
    # Launch the App
    app.run()

# --- VERSION LOG ---
# 0.24.1: Initial integration of UI, Brain, and Database using threading.