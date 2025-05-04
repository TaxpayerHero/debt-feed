
import time
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import random

RSS_FILE = "debt_feed.xml"
DEBT_CLOCK_URL = "https://www.debtclock.nz"

# Values copied from the website
DEBT_START = 175_464_000_000
START_TIME = 1719748800  # Monday, 1 July 2024 00:00:00 NZST in UNIX timestamp
PER_SECOND_INCREASE = 550.038051750381
HOUSEHOLDS = 2_034_500  # Corrected from JS variable populationSize

def calculate_debt_as_of(target_time):
    now_utc = target_time.timestamp()
    progress = now_utc - START_TIME
    debt = DEBT_START + progress * PER_SECOND_INCREASE
    return round(debt)

def get_midday_stat(current_debt, household_count, local_time):
    stats = []

    stats.append(f"📈 Since the 2023 election, government debt has grown by $14.5 billion.")
    stats.append(f"📈 Debt up $14.5 billion since the 2023 election.")
    stats.append(f"📈 That’s $7,127 more debt per household since the election.")
    stats.append(f"⏱️ Debt is increasing by $550.04 every second, $33,002 every minute, and $47,523,456 every day.")
    stats.append(f"💸 We're spending $28 million every day — just on interest.")
    stats.append(f"🧨 Government debt is now at its highest level in New Zealand’s history.")

    return random.choice(stats) if local_time.hour == 12 else ""

def generate_rss(debt, household_count, pub_time):
    per_household = debt / household_count
    stat_line = get_midday_stat(debt, household_count, pub_time)

    debt_title = (
        f"🇳🇿 NZ Government Debt: ${debt:,.0f}\n"
        f"👉 Your household’s share: ${per_household:,.2f}\n"
        f"{stat_line}"
    )

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "NZ Debt Updates"
    ET.SubElement(channel, "link").text = DEBT_CLOCK_URL
    ET.SubElement(channel, "description").text = "Hourly updates on NZ's national debt."

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = debt_title.strip()
    ET.SubElement(item, "link").text = DEBT_CLOCK_URL
    ET.SubElement(item, "pubDate").text = pub_time.strftime('%a, %d %b %Y %H:%M:%S +1200')
    ET.SubElement(item, "guid").text = f"debt-{pub_time.timestamp()}"

    tree = ET.ElementTree(rss)
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    # Use the top of the next hour as the publication time (NZST offset)
    now = datetime.utcnow()
    next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    
    current_debt = calculate_debt_as_of(next_hour)
    generate_rss(current_debt, HOUSEHOLDS, next_hour)

    print(f"RSS updated: total=${current_debt:,.0f}, per household=${current_debt / HOUSEHOLDS:,.2f}")
