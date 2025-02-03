#!/usr/bin/env python3

# ========================================
# Author: Alejandro Baño
# ========================================

import requests 
import sqlite3
import json
from datetime import datetime

# Telegram Chat & Bot Configuration

CHAT_ID = ""
TOKEN = ""
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
DB_FILE = "ransomware_alerts.db"

COUNTRIES = {
    "AF": "Afghanistan 🇦🇫", "AL": "Albania 🇦🇱", "DZ": "Algeria 🇩🇿", "AD": "Andorra 🇦🇩", "AO": "Angola 🇦🇴",
    "AR": "Argentina 🇦🇷", "AM": "Armenia 🇦🇲", "AU": "Australia 🇦🇺", "AT": "Austria 🇦🇹", "AZ": "Azerbaijan 🇦🇿",
    "BH": "Bahrain 🇧🇭", "BD": "Bangladesh 🇧🇩", "BY": "Belarus 🇧🇾", "BE": "Belgium 🇧🇪", "BZ": "Belize 🇧🇿",
    "BJ": "Benin 🇧🇯", "BO": "Bolivia 🇧🇴", "BA": "Bosnia 🇧🇦", "BW": "Botswana 🇧🇼", "BR": "Brazil 🇧🇷",
    "BG": "Bulgaria 🇧🇬", "BF": "Burkina Faso 🇧🇫", "BI": "Burundi 🇧🇮", "KH": "Cambodia 🇰🇭", "CM": "Cameroon 🇨🇲",
    "CA": "Canada 🇨🇦", "CL": "Chile 🇨🇱", "CN": "China 🇨🇳", "CO": "Colombia 🇨🇴", "CR": "Costa Rica 🇨🇷",
    "HR": "Croatia 🇭🇷", "CU": "Cuba 🇨🇺", "CY": "Cyprus 🇨🇾", "CZ": "Czech Republic 🇨🇿", "DK": "Denmark 🇩🇰",
    "DO": "Dominican Republic 🇩🇴", "EC": "Ecuador 🇪🇨", "EG": "Egypt 🇪🇬", "SV": "El Salvador 🇸🇻",
    "EE": "Estonia 🇪🇪", "FI": "Finland 🇫🇮", "FR": "France 🇫🇷", "GA": "Gabon 🇬🇦", "DE": "Germany 🇩🇪",
    "GH": "Ghana 🇬🇭", "GR": "Greece 🇬🇷", "GT": "Guatemala 🇬🇹", "HN": "Honduras 🇭🇳", "HU": "Hungary 🇭🇺",
    "IS": "Iceland 🇮🇸", "IN": "India 🇮🇳", "ID": "Indonesia 🇮🇩", "IR": "Iran 🇮🇷", "IQ": "Iraq 🇮🇶",
    "IE": "Ireland 🇮🇪", "IL": "Israel 🇮🇱", "IT": "Italy 🇮🇹", "JM": "Jamaica 🇯🇲", "JP": "Japan 🇯🇵",
    "JO": "Jordan 🇯🇴", "KZ": "Kazakhstan 🇰🇿", "KE": "Kenya 🇰🇪", "KW": "Kuwait 🇰🇼", "KG": "Kyrgyzstan 🇰🇬",
    "LA": "Laos 🇱🇦", "LV": "Latvia 🇱🇻", "LB": "Lebanon 🇱🇧", "LY": "Libya 🇱🇾", "LT": "Lithuania 🇱🇹",
    "LU": "Luxembourg 🇱🇺", "MY": "Malaysia 🇲🇾", "MX": "Mexico 🇲🇽", "MD": "Moldova 🇲🇩", "MC": "Monaco 🇲🇨",
    "MN": "Mongolia 🇲🇳", "ME": "Montenegro 🇲🇪", "MA": "Morocco 🇲🇦", "MZ": "Mozambique 🇲🇿", "NP": "Nepal 🇳🇵",
    "NL": "Netherlands 🇳🇱", "NZ": "New Zealand 🇳🇿", "NI": "Nicaragua 🇳🇮", "NG": "Nigeria 🇳🇬", "NO": "Norway 🇳🇴",
    "OM": "Oman 🇴🇲", "PK": "Pakistan 🇵🇰", "PA": "Panama 🇵🇦", "PY": "Paraguay 🇵🇾", "PE": "Peru 🇵🇪",
    "PH": "Philippines 🇵🇭", "PL": "Poland 🇵🇱", "PT": "Portugal 🇵🇹", "QA": "Qatar 🇶🇦", "RO": "Romania 🇷🇴",
    "RU": "Russia 🇷🇺", "SA": "Saudi Arabia 🇸🇦", "RS": "Serbia 🇷🇸", "SG": "Singapore 🇸🇬", "SK": "Slovakia 🇸🇰",
    "SI": "Slovenia 🇸🇮", "ZA": "South Africa 🇿🇦", "KR": "South Korea 🇰🇷", "ES": "Spain 🇪🇸",
    "SE": "Sweden 🇸🇪", "CH": "Switzerland 🇨🇭", "TH": "Thailand 🇹🇭", "TR": "Turkey 🇹🇷", "UA": "Ukraine 🇺🇦",
    "AE": "United Arab Emirates 🇦🇪", "GB": "United Kingdom 🇬🇧", "US": "United States 🇺🇸",
    "UY": "Uruguay 🇺🇾", "VE": "Venezuela 🇻🇪", "VN": "Vietnam 🇻🇳", "YE": "Yemen 🇾🇪"
}

def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS victims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT,
            country TEXT,
            post_title TEXT,
            post_url TEXT,
            website TEXT,
            published TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def get_latest_victims():
    headers = {"accept": "application/json"}
    url = "https://api.ransomware.live/recentvictims"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return sorted(response.json(), key=lambda x: x['published'], reverse=True)[:10]
    return []

def get_last_10_published():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT published FROM victims ORDER BY published DESC LIMIT 10")
    last_10 = [row[0] for row in cursor.fetchall()]
    conn.close()
    return last_10

def save_victim(victim):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO victims (group_name, country, post_title, post_url, website, published)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (victim["group_name"], victim["country"], victim["post_title"],
               victim["post_url"], victim["website"], victim["published"]))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f" [!] Victim already exists in the database: {victim['post_title']}")
    finally:
        conn.close()

def send_telegram_notification(victim):

    published_date = victim.get('published', 'Fecha no disponible')
    group_name = victim.get('group_name', 'Grupo no disponible')
    country_code = victim.get('country', 'Unknown')
    country_name = COUNTRIES.get(country_code, country_code)
    post_title = victim.get('post_title', 'Título no disponible')
    website = victim.get('website', 'No disponible')
    post_url = victim.get('post_url', 'No disponible')

    message = (
        f"🆕 New ransomware victim detected:\n\n"
        f"📅 Date: {published_date}\n"
        f"🔴 Group: {group_name}\n"
        f"🌍 Country: {country_name}\n"
        f"📌 Victim: {post_title}\n"
        f"🌐 Website: {website}\n"
        f"🧅 Onion Link: {post_url}"
    )

    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(TELEGRAM_URL, data=data)

def is_victim_in_database(published_date):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM victims WHERE published = ?", (published_date,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def main():
    setup_database()
    victims = get_latest_victims()
    last_10_published = get_last_10_published()

    for victim in victims:
        if victim["published"] not in last_10_published:
            if not is_victim_in_database(victim["published"]):
                send_telegram_notification(victim)
                save_victim(victim)
            else:
                print(f"[!] Victim already exists in the database: {victim['post_title']}")

if __name__ == "__main__":
    main()
