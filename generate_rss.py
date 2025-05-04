from datetime import datetime
import xml.etree.ElementTree as ET

RSS_FILE = "debt_feed.xml"
DEBT_CLOCK_URL = "https://www.debtclock.nz"

def fetch_debt_parameters():
    # Forecast from Budget 2024:
    return {
        "initial_debt": 175.464,  # in billions (1 July 2024, 12:01am)
        "target_debt": 192.810,   # in billions (30 June 2025, 11:59pm)
        "start_time": int(datetime(2024, 7, 1, 0, 1).timestamp()),
        "end_time": int(datetime(2025, 6, 30, 23, 59).timestamp())
    }

def calculate_current_debt(params):
    now = datetime.utcnow().timestamp()
    start = params["start_time"]
    end = params["end_time"]
    progress = min(max((now - start) / (end - start), 0), 1)
    debt = params["initial_debt"] + progress * (params["target_debt"] - params["initial_debt"])
    return round(debt, 3)

def generate_rss(debt):
    now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "NZ Debt Updates"
    ET.SubElement(channel, "link").text = DEBT_CLOCK_URL
    ET.SubElement(channel, "description").text = "Hourly updates on NZ's national debt."

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = f"NZ National Debt: ${debt} billion"
    ET.SubElement(item, "link").text = DEBT_CLOCK_URL
    ET.SubElement(item, "pubDate").text = now
    ET.SubElement(item, "guid").text = f"debt-{datetime.utcnow().timestamp()}"

    tree = ET.ElementTree(rss)
    tree.write(RSS_FILE, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    params = fetch_debt_parameters()
    debt = calculate_current_debt(params)
    generate_rss(debt)
    print(f"RSS feed generated with debt: ${debt}B")
