#!/bin/bash

SCRIPT_PATH="$PWD/ransom_notify.py"
SCRIPT_CLEANDB="$PWD/clean_database.py"

NOTIFY="*/10 * * * * /usr/bin/python3 $SCRIPT_PATH >/dev/null 2>&1" # Run every 10 minutes
CLEAN_DATABASE="0 2 * * * /usr/bin/python3 $SCRIPT_CLEANDB >/dev/null 2>&1" # Run at 2 PM

CURRENT_CRON=$(crontab -l 2>/dev/null)

if [[ ! -f "$SCRIPT_PATH" || ! -f "$SCRIPT_CLEANDB" ]]; then
    echo "[!] Error: $SCRIPT_PATH or $SCRIPT_CLEANDB does not exist"
    exit 1
fi

NEW_CRON="$CURRENT_CRON"$'\n'"$NOTIFY"$'\n'"$CLEAN_DATABASE"

if ! echo "$CURRENT_CRON" | grep -Fxq "$NOTIFY"; then
    CURRENT_CRON="$CURRENT_CRON"$'\n'"$NOTIFY"
    echo "[+] Cronjob for notifications successfully added"
else
    echo "[+] Cronjob for notifications already running"
fi

if ! echo "$CURRENT_CRON" | grep -Fxq "$CLEAN_DATABASE"; then
    CURRENT_CRON="$CURRENT_CRON"$'\n'"$CLEAN_DATABASE"
    echo "[+] Cronjob for database cleaning successfully added"
else
    echo "[+] Cronjob for database cleaning already running"
fi

echo "$CURRENT_CRON" | crontab -

echo -e "[*] Current Cronjobs:\n"
crontab -l | tail -n 2