import re
import requests
from datetime import datetime
import xml.etree.ElementTree as ET

RSS_FILE = "debt_feed.xml"
DEBT_CLOCK_URL = "https://www.debtclock.nz"

def fetch_debt_parameters():
    response = requests.get(DEBT_CLOCK_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {DEBT_CLOCK_URL}")

    html = response.text

    # Extract JavaScript variables
    initial_debt_match = re.search(r"var\s+initialDebt\s*=\s*([\d.]+);", html)
    target_debt_match = re.search(r"var\s+targetDebt\s*=\s*([\d.]+);", html)
    population_size_match = re.search(r"var\s+populationSize\s*=\s*([\d.]+);", html)
    start_time_match = re.search(r"var\s+startTime\s*=\s*new Date\(([^)]+)\);", html)
    end_time_match = re.search(r"var\s+endTime\s*=\s*new Date\(([^)]+)\);", html)

    if not all([initial_debt_match, target_debt_match, population_size_match, start_time_match, end_time_match]):
        raise Exception("Failed to extract necessary variables from the webpage.")

    initial_debt = float(initial_debt_match.group(1))
    target_debt = float(target_debt_match.group(1))
    population_size = int(float(population_size_match.group(1)))

    # Parse start and end times
    start_time_parts = list(map(int, start_time_match.group(1).split(',')))
    end_time_parts = list(map(int, end_time_match.group(1).split(',')))

    start_time = int(datetime(*start_time_parts).timestamp())
    end_time = int(datetime(*end_time_parts).timestamp())

    return {
        "initial_debt": initial_debt,
        "target_debt": target_debt,
        "start_time": start_time,
        "end_time": end_time,
        "population_size": population_size
    }

def calculate_current_debt(params):
    now = datetime.utcnow().timestamp()
    start = params["start_time"]
    end = params["end_time"]
    progress = min(max((now - start) / (end - start), 0), 1)
    debt = params["initial_debt"] + progress * (params["target_debt"] - params["initial_debt"])
    return round(debt)

def generate_rss(debt, population_size):
    now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
    per_person = debt / population_size
    debt_title = f"${debt:,.0f}\n(${per_person:,.2f} per person)"

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "NZ Debt Updates"
    ET.SubElement(channel, "link").text = DEBT_CLOCK_URL
    ET.SubElement(channel, "description").text = "Hourly updates on NZ's national debt."

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = debt_title
    ET.SubElement(item, "link").text = DEBT_CLOCK_URL
    ET.SubElement(item, "pubDate").text = now
    ET.SubElement(item, "guid").text = f"debt-{datetime.utcnow().timestamp()}"

    tree = ET.ElementTree(rss)
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    params = fetch_debt_parameters()
    debt = calculate_current_debt(params)
    generate_rss(debt, params["population_size"])
    print(f"RSS updated: total=${debt:,.0f}, per person=${debt / params['population_size']:,.2f}")
