"""
FILE: Diagnostic.py
VERSION: 0.24.1
LAST UPDATED: 2026-02-19
DESCRIPTION: Quality Control. Manual utilities for testing system health.
"""

import os
from _Configuration import cfg
from Database import log_to_sheet, get_subjects_of_interest
from TheBrain import get_not_boring_fact

def run_system_check(password: str = "PASSWORD"):
    """
    Performs a comprehensive health check of the MVP components.
    """
    print("--- STARTING SYSTEM DIAGNOSTIC (v0.24.1) ---")
    
    # 1. Check for Service Account JSON
    if os.path.exists(cfg.SERVICE_ACCOUNT_FILE):
        print(f"[OK] Found credentials: {cfg.SERVICE_ACCOUNT_FILE}")
    else:
        print(f"[ERROR] Missing {cfg.SERVICE_ACCOUNT_FILE}! Did you upload it to Colab/the project folder?")
        return

    # 2. Test Google Sheets Connection
    print("[TEST] Attempting to write to Google Sheets...")
    log_to_sheet("Diagnostic: Manual system check initiated.", level=1, password=password)
    
    # 3. Test Subject Retrieval
    print("[TEST] Fetching Subjects of Interest...")
    subjects = get_subjects_of_interest()
    if subjects:
        print(f"[OK] Retrieved {len(subjects)} subjects from Google Sheet.")
    else:
        print("[ERROR] Could not retrieve subjects. Check Sheet ID and Permissions.")

    # 4. Test TheBrain (AI Connection)
    print("[TEST] Calling Rupert (TheBrain)...")
    # Using dummy coordinates (Helpston, Peterborough)
    test_fact = get_not_boring_fact(52.628, -0.347, ["History", "Archaeology"], password=password)
    
    if test_fact:
        print(f"[OK] Rupert Responded: {test_fact.location_name}")
        print(f"Fact: {test_fact.interesting_fact}")
    else:
        print("[ERROR] TheBrain failed to respond. Check AI_KEY and internet connection.")

    print("--- DIAGNOSTIC COMPLETE ---")

if __name__ == "__main__":
    # To run this, simply execute: python Diagnostic.py
    run_system_check("PASSWORD")

# --- VERSION LOG ---
# 0.24.1: Initial build. Tests Google Sheets, JSON presence, and AI responses.