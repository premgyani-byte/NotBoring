"""
FILE: TheBrain.py
VERSION: 0.24.2
LAST UPDATED: 2026-02-19
DESCRIPTION: The Researcher. Uses google-generativeai (Legacy) to avoid Rust/Pydantic v2 issues on Android.
"""

import json
import google.generativeai as genai
from pydantic import BaseModel, root_validator
from typing import List, Optional
from _Configuration import cfg, is_locked

# Initialize Gemini with the fixed config attribute
genai.configure(api_key=cfg.AI_KEY)

class RupertThought(BaseModel):
    """
    Structured response from Gemini.
    Using Pydantic v1 root_validator for Android/Buildozer compatibility.
    """
    subject_found: bool
    location_name: str
    interesting_fact: str
    distance_expanded: float
    is_test_mode: bool = cfg.TEST_MODE

    @root_validator(pre=False)
    def validate_thought(cls, values):
        """Ensures logic holds even if AI gets creative with JSON."""
        if values.get("distance_expanded") is None:
            values["distance_expanded"] = 0.0
        return values

def get_not_boring_fact(lat: float, lon: float, subjects: List[str], password: str = "PASSWORD"):
    """
    The main research function. Finds something fascinating about a coordinate.
    """
    # 1. Security Check
    if not is_locked(password):
        print("[SECURITY] Invalid password attempt on TheBrain.")
        return None

    # 2. Build the Rupert Persona
    persona = (
        "You are Rupert, a British, highly intelligent, and bitingly sarcastic AI. "
        "You are an expert in history, archaeology, and anthropology. "
        "Your tone is irreverent and witty. You are a master of the 'pub quiz' fact. "
        "You strictly communicate in metric units (kilometers, meters)."
    )
    
    if cfg.TEST_MODE:
        persona += " CRITICAL: TEST_MODE is active. Limit your response to exactly one short, sharp sentence."

    # 3. Construct the Prompt
    subject_list = ", ".join(subjects)
    prompt = f"""
    Current Latitude: {lat}
    Current Longitude: {lon}
    Subjects of Interest: {subject_list}
    
    Find something truly interesting at or very near these coordinates. 
    If nothing interesting is found, assume we have expanded the search by {cfg.EXPAND_DISTANCE} km.
    
    Return your response ONLY as a JSON object:
    {{
        "subject_found": true,
        "location_name": "Specific Name of the spot",
        "interesting_fact": "Your sarcastic and brilliant discovery here",
        "distance_expanded": {cfg.EXPAND_DISTANCE if not cfg.TEST_MODE else 0.0}
    }}
    """

    # 4. Execute the Research (Using Flash for cost efficiency)
    model = genai.GenerativeModel(
        model_name=cfg.AI_MODEL_NAME,
        system_instruction=persona
    )

    try:
        response = model.generate_content(prompt)
        
        # Clean the response in case Gemini wraps it in markdown code blocks
        clean_json = response.text.strip().replace('```json', '').replace('```', '').strip()
        data = json.loads(clean_json)
        
        # Validate against our Pydantic v1 model
        thought = RupertThought(**data)
        
        # Level 3 Diagnostic Logging
        if cfg.DEBUG_LEVEL >= 3:
            print(f"[DEBUG 3] Rupert's Raw Thought: {thought.json()}")
            
        return thought

    except Exception as e:
        # Level 1 Error Logging
        if cfg.DEBUG_LEVEL >= 1:
            print(f"[DEBUG 1] TheBrain Failure: {str(e)}")
        return None

# --- VERSION LOG ---
# 0.24.1: Initial creation.
# 0.24.2: Fixed cfg.AI_KEY attribute error and reverted to legacy SDK to ensure
#         Android compatibility without Rust requirements.