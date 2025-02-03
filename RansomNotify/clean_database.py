#!/usr/bin/env python3

import sqlite3
from datetime import datetime, timedelta

DB_FILE = "ransomware_alerts.db"

def clean_old_records(days_threshold=1):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    date_threshold = datetime.now() - timedelta(days=days_threshold)
    threshold_str = date_threshold.strftime("%Y-%m-%d %H:%M:%S")
        
    cursor.execute("DELETE FROM victims WHERE published < ?", (threshold_str,))
    conn.commit()
    conn.close()
    
    print(f"Records older than {days_threshold} days have been deleted.")

if __name__ == "__main__":
    clean_old_records()