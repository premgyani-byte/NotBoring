"""
FILE: _Configuration.py
VERSION: 0.24.1
LAST UPDATED: 2026-02-19
DESCRIPTION: Central configuration and variable management for The Not Boring Company MVP.
STRATEGY: Pydantic v1.10.15 (Android/Buildozer Compatibility)
"""

from pydantic import BaseModel, Field, root_validator
from typing import Optional

    # =================================================================
    # !!! SENSITIVE DATA - DO NOT COPY/PASTE FOR ANALYSIS !!!
    # =================================================================
class AppConfig(BaseModel):
    # =================================================================
    # !!! SENSITIVE DATA - NOW WITH TYPE HINTS !!!
    # =================================================================
    AI_KEY: str = "AIzaSyATQLT_eYrQyd5i_YF0nQs-HQT39rW7vTM" # Added : str
    SS_ID: str = "17qAoBsYn11CkZohNR6aSpu0Rb_JvrETRrIusgHt3AGU" # Added : str
    PREM_EMAIL: str = "premgyani@gmail.com" # Added : str
    LOCK_PASSWORD: str = "PASSWORD" # Added : str
    # =================================================================
    # =================================================================
    # --- Version Control & Security ---
    version: str = "0.24.1"
    password_lock: str = LOCK_PASSWORD
    
    # --- Logging & Debugging ---
    # Level 1: Basic | Level 2: Detailed | Level 3: Full Diagnostics (AI calls)
    DEBUG_LEVEL: int = 1 
    LOG_MAX_ROWS: int = 1000
    LOG_DELETE_COUNT: int = 250
    
    # --- Environment Toggles ---
    # MUST be turned off for MVP, set to True for PILOT
    FOREGROUND_SERVICE_ENABLED: bool = False
    # Test mode: Limits TheBrain to single short sentences
    TEST_MODE: bool = True
    
    # --- AI & Persona (Rupert) ---
    AI_MODEL_NAME: str = "gemini-2.5-flash-lite"
    MAX_TALK_TIME: int = 180  # seconds
    MIN_TALK_TIME: int = 30   # seconds
    DELIVER_NUMBER_SEGMENTS: int = 1
    ANSWER_RESPONSE_TIMEOUT: int = 10 # seconds
    
    # --- Navigation & Search ---
    EXPAND_DISTANCE: float = 2.0  # Kilometers (Metric Only)
    GAMEIFY: bool = False
    
    # --- UI (TheButler) ---
    # Options: "DAY" or "NIGHT"
    UI_THEME: str = "DAY"
    
    # --- Paths & Files ---
    SERVICE_ACCOUNT_FILE: str = "service_account.json"
    GOOGLE_DRIVE_APK_PATH: str = "/content/drive/MyDrive/Private/Scripts/APK/"

    @root_validator(pre=False)
    def validate_config(cls, values):
        """
        Pydantic v1 validator to ensure logical consistency.
        Matches the versioning logic required for the Android build.
        """
        # Ensure we don't have silly talk times
        if values.get("MIN_TALK_TIME") > values.get("MAX_TALK_TIME"):
            values["MIN_TALK_TIME"] = values["MAX_TALK_TIME"]
            
        return values

# Global instance of configuration to be imported by other modules
cfg = AppConfig()

def is_locked(input_password: str) -> bool:
    """
    Facility to LOCK code with a password.
    Returns True if the password matches, allowing execution.
    """
    return input_password == cfg.password_lock

# --- VERSION LOG ---
# 0.24.1: Initial creation of the Pydantic v1 configuration strategy.
#         Added placeholders for API keys and global toggle for Foreground Service.
#         Implemented the required 3-level debug variable.