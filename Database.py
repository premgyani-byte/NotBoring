"""
FILE: Database.py
VERSION: 0.24.2
LAST UPDATED: 2026-02-19
DESCRIPTION: Production Control. Handles Google Sheets logging and Subject retrieval.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from _Configuration import cfg, is_locked

# Setup the scope for Google Sheets and Drive
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

def get_sheet_client():
    """Authenticates and returns the Gspread client."""
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(cfg.SERVICE_ACCOUNT_FILE, SCOPE)
        return gspread.authorize(creds)
    except Exception as e:
        print(f"Auth Error: {e}")
        return None

def log_to_sheet(message: str, level: int = 1, password: str = "PASSWORD"):
    """
    Main logging function. Maintains a rolling log of 1000 rows.
    Level 1: Basic | Level 2: Detailed | Level 3: AI Raw Data
    """
    if not is_locked(password):
        return
        
    if level > cfg.DEBUG_LEVEL:
        return

    client = get_sheet_client()
    if not client: return

    try:
        sheet = client.open_by_key(cfg.SS_ID).worksheet("LOG")
        
        # --- Rolling Log Logic ---
        # Check current row count
        all_records = sheet.get_all_values()
        row_count = len(all_records)
        
        if row_count >= cfg.LOG_MAX_ROWS:
            # Delete rows 2 through 251 (preserving header at Row 1)
            sheet.delete_rows(2, cfg.LOG_DELETE_COUNT + 1)
            
        # --- Prepare the entry ---
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Columns: Timestamp, Level, Message
        row = [timestamp, f"Level {level}", message]
        sheet.append_row(row)

    except Exception as e:
        print(f"Logging Failed: {e}")

def get_subjects_of_interest():
    """Retrieves the list of subjects from the SUBJECT_OF_INTEREST sheet."""
    client = get_sheet_client()
    if not client: return []

    try:
        sheet = client.open_by_key(cfg.SS_ID).worksheet("SUBJECT_OF_INTEREST")
        # Assuming Column B (Index 1) holds the Subject names
        records = sheet.get_all_records()
        subjects = [r['Subject'] for r in records if r.get('Subject')]
        return subjects
    except Exception as e:
        log_to_sheet(f"Failed to fetch subjects: {e}", level=1)
        return []

# --- VERSION LOG ---
# 0.24.1: Initial creation. Basic gspread connection.
# 0.24.2: Added rolling log logic (1000 row cap). 
#         Implemented debug level filtering based on _Configuration.