import re
import time
import pytz
import random
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os  # For checking the event type

# Constants
RSS_FILE = "debt_feed.xml"
DEBT_CLOCK_URL = "https://www.debtclock.nz"

# Hardcoded parameters from the live site
DEBT_START = 175_464_000_000
START_TIMESTAMP = 1719748800  # 1 July 2024 00:00:00 NZT
PER_SECOND_INCREASE = 550.038051750381
HOUSEHOLDS = 2_034_500

# Election reference point
ELECTION_DEBT = 175_600_000_000  # Based on October 31 estimate
ELECTION_DATE = datetime(2023, 10, 31, 0, 0, 0, tzinfo=pytz.timezone("Pacific/Auckland"))


def calculate_debt_at(timestamp):
    seconds_elapsed = timestamp - START_TIMESTAMP
    return DEBT_START + seconds_elapsed * PER_SECOND_INCREASE


def get_midday_stat(current_debt, household_count, now):
    stats = []
    election_increase = current_debt - ELECTION_DEBT
    per_household_increase = election_increase / household_count

    # Format 1: plain
    stats.append(f"📈 Since the 2023 election, government debt has grown by ${election_increase/1e9:.1f} billion.")

    # Format 2: punchy
    stats.append(f"📈 Debt up ${election_increase/1e9:.1f} billion since the 2023 election.")

    # Format 3: targeted-household
    stats.append(f"📈 That’s ${per_household_increase:,.0f} more debt per household since the election.")

    # Format 4: debt growth rate
    stats.append("⏱️ Debt is increasing by $550.04 every second, $33,002 every minute, and $47,523,456 every day.")

    # Format 9: interest cost
    stats.append("💸 We're spending $28 million every day — just on interest.")

    # Format 10: historic high
    stats.append("💨 Government debt is now at its highest level in New Zealand’s history.")

    return random.choice(stats) if now.hour == 12 else ""


def generate_rss():
    tz = pytz.timezone("Pacific/Auckland")
    now = datetime.now(tz)
    future_time = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    pub_timestamp = int(future_time.timestamp())

    # Calculate future debt (on the hour) for sync with website
    debt = calculate_debt_at(pub_timestamp)
    per_household = debt / HOUSEHOLDS
    stat_line = get_midday_stat(debt, HOUSEHOLDS, future_time)

    # Compose title
    debt_title = (
        f"🇳🇿 NZ Government Debt: ${debt:,.0f}\n"
        f"👉 Your household’s share: ${per_household:,.2f}\n"
        f"{stat_line}"
    )

    # Format pubDate in RSS format
    pubdate = future_time.strftime('%a, %d %b %Y %H:%M:%S %z')

    # Build RSS
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "NZ Debt Updates"
    ET.SubElement(channel, "link").text = DEBT_CLOCK_URL
    ET.SubElement(channel, "description").text = "Hourly updates on NZ's national debt."

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = debt_title.strip()
    ET.SubElement(item, "link").text = DEBT_CLOCK_URL
    ET.SubElement(item, "pubDate").text = pubdate
    ET.SubElement(item, "guid").text = f"debt-{pub_timestamp}"

    tree = ET.ElementTree(rss)
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)

    # Determine trigger type
    trigger_type = os.getenv('GITHUB_EVENT_NAME', 'manual')
    print(f"RSS updated at {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')} — Triggered by: {trigger_type}")
    print(f"Debt total=${debt:,.0f}, per household=${per_household:,.2f}")


if __name__ == "__main__":
    generate_rss()