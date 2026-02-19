"""
FILE: TheButlersVoice.py
VERSION: 0.25.0
LAST UPDATED: 2026-02-19
DESCRIPTION: Ultra-HD Vocalist. Uses Google Cloud Studio TTS for natural British speech.
"""

import os
from google.cloud import texttospeech
from _Configuration import cfg

# Use the same credentials we use for the Database
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cfg.SERVICE_ACCOUNT_FILE

def speak(text: str):
    """
    Sends text to Google Cloud TTS and plays back high-fidelity British audio.
    """
    if not text:
        return

    print(f"[RUPERT THINKING]: Preparing voice response...")

    try:
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request
        # 'en-GB-Studio-B' is the gold standard for natural British male speech
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-GB",
            name="en-GB-Studio-B" 
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            pitch=0.0,
            speaking_rate=1.0
        )

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Save the temporary audio file
        audio_file = "rupert_speech.mp3"
        with open(audio_file, "wb") as out:
            out.write(response.audio_content)

        # PLAYBACK LOGIC
        # On Windows (for testing):
        if os.name == 'nt':
            os.system(f"start {audio_file}")
        # On Android (in the APK):
        else:
            # We will use Kivy's SoundLoader to play the MP3
            from kivy.core.audio import SoundLoader
            sound = SoundLoader.load(audio_file)
            if sound:
                sound.play()

    except Exception as e:
        print(f"[VOICE ERROR] Google Cloud TTS failed: {e}")
        # Fallback to console print so we don't lose the fact
        print(f"[FALLBACK]: {text}")

# --- VERSION LOG ---
# 0.25.0: Switched from System TTS to Google Cloud Studio TTS for "Gemini-App" quality.