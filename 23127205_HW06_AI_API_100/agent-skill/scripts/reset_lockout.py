#!/usr/bin/env python3
"""
=============================================================================
Agent Skill Tool: SQLite Account Lockout Reset Utility
Author: Lam Huu Khanh (Student ID: 23127205)
Course: Software Testing (HCMUS) - HW06: API Testing

Description:
  Resets lockout state (login_attempts=0, locked_until=NULL) in the SUT SQLite
  database (database.sqlite) to prevent state pollution and flaky test runs.
=============================================================================
"""

import sys
import sqlite3
from pathlib import Path

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def find_database_file() -> Path:
    candidates = [
        Path("eshop-sut/backend/database.sqlite"),
        Path("HW06/eshop-sut/backend/database.sqlite"),
        Path("23127205_HW06_AI_API_100/eshop-sut/backend/database.sqlite"),
        Path("../eshop-sut/backend/database.sqlite"),
        Path("../../eshop-sut/backend/database.sqlite"),
        Path("../../../eshop-sut/backend/database.sqlite"),
    ]
    for c in candidates:
        if c.exists():
            return c.resolve()
    return None


def reset_lockouts():
    db_path = find_database_file()
    if not db_path:
        print("[WARN] database.sqlite not found. Initializing new database via seed...")
        return False

    print(f"[INFO] Connecting to SQLite database at: {db_path}")
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET login_attempts = 0, locked_until = NULL")
        affected = cursor.rowcount
        conn.commit()
        conn.close()

        print(f"✅ [SUCCESS] Reset login_attempts and locked_until for all {affected} users.")
        return True
    except Exception as e:
        print(f"❌ [ERROR] Failed to reset SQLite database: {e}")
        return False


if __name__ == "__main__":
    reset_lockouts()
