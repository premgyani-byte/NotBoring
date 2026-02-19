"""
FILE: TheBrain.py
VERSION: 0.24.2
LAST UPDATED: 2026-02-19
DESCRIPTION: Reverted to google-generativeai for Android compatibility. Fixed AI_KEY attribute error.
"""

import json
import google.generativeai as genai # We stick with the "Old" faithful
from pydantic import BaseModel, root_validator
from typing import List
from _Configuration import cfg, is_locked

# Initialize Gemini with the proper attribute call
genai.configure(api_key=cfg.AI_KEY)

# ... (RupertThought class stays the same)

def get_not_boring_fact(lat: float, lon: float, subjects: List[str], password: str = "PASSWORD"):
    if not is_locked(password):
        return None

    # Logic remains the same, just ensuring we use the correct genai calls
    model = genai.GenerativeModel(
        model_name=cfg.AI_MODEL_NAME,
        system_instruction="You are Rupert, a British, sarcastic AI..."
    )
    
    # ... (Rest of the function remains the same as v0.24.1)