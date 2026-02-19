"""
FILE: TheBrain.py
VERSION: 0.24.1
LAST UPDATED: 2026-02-19
DESCRIPTION: The Researcher. Handles interaction with Gemini AI using Pydantic v1.
"""

import json
from pydantic import BaseModel, Field, root_validator
from typing import List, Optional
import google.generativeai as genai
from _Configuration import cfg, is_locked

# Initialize Gemini
genai.configure(api_key=cfg.AI_KEY)

class RupertThought(BaseModel):
    """
    Structured response from Gemini.
    Using Pydantic v1 root_validator for Android compatibility.
    """
    subject_found: bool
    location_name: str
    interesting_fact: str
    distance_expanded: float
    is_test_mode: bool = cfg.TEST_MODE

    @root_validator(pre=False)
    def validate_thought(cls, values):
        # Ensure we are maintaining our metric-only sanity
        if values.get("distance_expanded") is None:
            values["distance_expanded"] = 0.0
        return values

def get_not_boring_fact(lat: float, lon: float, subjects: List[str], password: str = "PASSWORD"):
    """
    The main research function. Finds something interesting about a coordinate.
    """
    # 1. Check Security Lock
    if not is_locked(password):
        return "Access Denied: Incorrect Password for TheBrain logic."

    # 2. Construct the Rupert Persona Prompt
    persona = (
        "You are Rupert, a British, highly intelligent, and bitingly sarcastic AI. "
        "You hate boredom. You are a world traveler and history expert. "
        "Your goal: Provide an interesting fact about the user's current location. "
        "Be witty, irreverent, and detailed unless TEST_MODE is active."
    )
    
    if cfg.TEST_MODE:
        persona += " CRITICAL: TEST_MODE is ON. Limit your response to one short, sharp sentence."

    # 3. Handle subjects of interest from the Google Sheet
    subject_list = ", ".join(subjects)
    
    prompt = f"""
    Location: Latitude {lat}, Longitude {lon}
    Possible Areas of Interest: {subject_list}
    
    Search for something fascinating near these coordinates. 
    If nothing is within the immediate area, expand your search by {cfg.EXPAND_DISTANCE} km.
    
    Return your answer strictly in JSON format:
    {{
        "subject_found": true/false,
        "location_name": "Name of the area",
        "interesting_fact": "Your sarcastic and brilliant discovery",
        "distance_expanded": numeric_value_in_km
    }}
    """

    # 4. Call Gemini (The Flash variant for pennies)
    model = genai.GenerativeModel(
        model_name=cfg.AI_MODEL_NAME,
        system_instruction=persona
    )

    try:
        response = model.generate_content(prompt)
        # Extract JSON from response (handling potential markdown formatting)
        raw_text = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(raw_text)
        
        # Validate with Pydantic v1
        thought = RupertThought(**data)
        
        # Log Level 3: Full Diagnostic
        if cfg.DEBUG_LEVEL >= 3:
            print(f"[DEBUG LEVEL 3] AI Response: {thought.json()}")
            
        return thought

    except Exception as e:
        # Log Level 1: Error reporting
        error_msg = f"TheBrain Error: {str(e)}"
        if cfg.DEBUG_LEVEL >= 1:
            print(error_msg)
        return None

# --- VERSION LOG ---
# 0.24.1: Initial build with Pydantic v1 root_validator. 
#         Implemented Rupert's persona and Test Mode constraints.
#         Added expansion distance logic and metric checks.