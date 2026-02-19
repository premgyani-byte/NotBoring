"""
FILE: TheButlersVoice.py
VERSION: 0.26.0
LAST UPDATED: 2026-02-19
DESCRIPTION: The 'Posh' Vocalist. Uses Gemini 3.1 Pro Native TTS for app-quality voice.
"""

import google.generativeai as genai
from _Configuration import cfg
import os

# Initialize the Native TTS Model
# This is the 'Paid Tier' model you just confirmed in your audit
VOICE_MODEL_NAME = "models/gemini-3.1-pro-preview-tts"

def speak(text: str):
    """
    Generates ultra-natural audio using Gemini's native voice engine.
    """
    if not text:
        return

    print(f"[RUPERT]: \"I'm currently warming up my vocal cords...\"")

    try:
        # 1. Setup the specific Voice model
        model = genai.GenerativeModel(VOICE_MODEL_NAME)
        
        # 2. Generate the Audio Content
        # We ask it to say the text with a specific persona cue
        prompt = f"Speak this exactly as Rupert (British, sarcastic, intelligent): {text}"
        response = model.generate_content(prompt)

        # 3. Extract and Save the Audio
        # Gemini 3.1 TTS returns the audio bytes in the 'parts' of the response
        audio_file = "rupert_natural.mp3"
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                with open(audio_file, "wb") as f:
                    f.write(part.inline_data.data)
        
        # 4. Playback Logic
        if os.name == 'nt':
            os.system(f"start {audio_file}")
        else:
            from kivy.core.audio import SoundLoader
            sound = SoundLoader.load(audio_file)
            if sound: sound.play()

    except Exception as e:
        print(f"[VOICE FAIL]: {e}")
        print(f"Fallback Text: {text}")

# --- VERSION LOG ---
# 0.26.0: Upgraded to Gemini 3.1 Pro Preview TTS for native 'Gemini App' voice quality.