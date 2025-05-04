import re
import time
import requests
from datetime import datetime
import xml.etree.ElementTree as ET
import pytz

RSS_FILE = "debt_feed.xml"
DEBT_CLOCK_URL = "https://www.debtclock.nz"

# Fallback values (interpreted as NZ time)
FALLBACK_PARAMS = {
    "initial_debt": 175_464_000_000,
    "target_debt": 192_810_000_000,
    "start_time": int(datetime(2024, 7, 1, 0, 1, tzinfo=pytz.timezone("Pacific/Auckland")).timestamp()),
    "end_time": int(datetime(2025, 6, 30, 23, 59, tzinfo=pytz.timezone("Pacific/Auckland")).timestamp()),
    "population_size": 2_034_000  # Actually households
}

def fetch_debt_parameters():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(DEBT_CLOCK_URL, timeout=10)
            if response.status_code == 200:
                html = response.text
                return extract_parameters_from_html(html)
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
        time.sleep(3 * (attempt + 1))

    print("⚠️ Failed to fetch live data after retries. Using fallback values.")
    return FALLBACK_PARAMS

def extract_parameters_from_html(html):
    initial_debt_match = re.search(r"var\s+initialDebt\s*=\s*([\d.]+);", html)
    target_debt_match = re.search(r"var\s+targetDebt\s*=\s*([\d.]+);", html)
    population_match = re.search(r"var\s+populationSize\s*=\s*([\d.]+);", html)
    start_match = re.search(r"var\s+startTime\s*=\s*new Date\(([^)]+)\);", html)
    end_match = re.search(r"var\s+endTime\s*=\s*new Date\(([^)]+)\);", html)

    if not all([initial_debt_match, target_debt_match, population_match, start_match, end_match]):
        raise Exception("Failed to extract required parameters from HTML.")

    initial_debt = float(initial_debt_match.group(1))
    target_debt = float(target_debt_match.group(1))
    population_size = int(float(population_match.group(1)))

    start_parts = list(map(int, start_match.group(1).split(',')))
    end_parts = list(map(int, end_match.group(1).split(',')))

    tz = pytz.timezone("Pacific/Auckland")
    start_time = int(datetime(*start_parts, tzinfo=tz).timestamp())
    end_time = int(datetime(*end_parts, tzinfo=tz).timestamp())

    return {
        "initial_debt": initial_debt,
        "target_debt": target_debt,
        "start_time": start_time,
        "end_time": end_time,
        "population_size": population_size
    }

def calculate_current_debt(params):
    now = datetime.now(pytz.timezone("Pacific/Auckland")).timestamp()
    progress = min(max((now - params["start_time"]) / (params["end_time"] - params["start_time"]), 0), 1)
    debt = params["initial_debt"] + progress * (params["target_debt"] - params["initial_debt"])
    return round(debt)

def generate_rss(debt, household_count):
    nz_now = datetime.now(pytz.timezone("Pacific/Auckland"))
    pubdate = nz_now.strftime('%a, %d %b %Y %H:%M:%S %z')

    per_household = debt / household_count
    debt_title = f"${debt:,.0f}\n(${per_household:,.2f} per household)"

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "NZ Debt Updates"
    ET.SubElement(channel, "link").text = DEBT_CLOCK_URL
    ET.SubElement(channel, "description").text = "Hourly updates on NZ's national debt."

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = debt_title
    ET.SubElement(item, "link").text = DEBT_CLOCK_URL
    ET.SubElement(item, "pubDate").text = pubdate
    ET.SubElement(item, "guid").text = f"debt-{nz_now.timestamp()}"

    tree = ET.ElementTree(rss)
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    params = fetch_debt_parameters()
    debt = calculate_current_debt(params)
    generate_rss(debt, params["population_size"])
    print(f"RSS updated: total=${debt:,.0f}, per household=${debt / params['population_size']:,.2f}")
