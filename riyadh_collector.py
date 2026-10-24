"""
Collects live traffic speeds on main roads in Riyadh using the TomTom Traffic Flow API.
Every run adds one row per road to data/riyadh_traffic.csv.

We run it every 15 minutes with GitHub Actions (.github/workflows/collect.yml).
The API key has to be in the TOMTOM_KEY environment variable.

Run it by hand:
    set TOMTOM_KEY=your_key        (Windows)
    python riyadh_collector.py
"""
import csv
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

API_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
OUT_FILE = Path(__file__).parent / "data" / "riyadh_traffic.csv"
RIYADH_TZ = timezone(timedelta(hours=3))

# (road, latitude, longitude) - one point on each road
ROADS = [
    ("King Fahd Rd - Olaya", 24.7136, 46.6753),
    ("Northern Ring Rd - KAFD", 24.7743, 46.6385),
    ("Eastern Ring Rd - Exit 10", 24.7562, 46.7487),
    ("Southern Ring Rd - Shubra", 24.5821, 46.6892),
    ("Western Ring Rd - Dhahrat Laban", 24.6437, 46.5921),
    ("Makkah Rd - Al Mutamarat", 24.6712, 46.6914),
    ("Khurais Rd - Al Malaz", 24.7088, 46.7326),
    ("King Abdullah Rd - Al Wurud", 24.7431, 46.6834),
    ("King Abdulaziz Rd - Al Yasmin", 24.8115, 46.6453),
    ("Prince Turki Rd - Hittin", 24.7618, 46.6112),
    ("King Khalid Rd - Hittin", 24.7391, 46.5881),
    ("Takhassusi St - Al Mohammadiyyah", 24.7295, 46.6573),
    ("Olaya St - Al Olaya", 24.6975, 46.6852),
]

FIELDS = ["timestamp", "road", "lat", "lon", "current_speed", "free_flow_speed",
          "current_travel_time", "free_flow_travel_time", "confidence", "road_closure", "frc"]


def get_segment(lat, lon, key):
    url = f"{API_URL}?point={lat},{lon}&unit=KMPH&key={key}"
    with urllib.request.urlopen(url, timeout=20) as resp:
        return json.load(resp)["flowSegmentData"]


def main():
    key = os.environ.get("TOMTOM_KEY")
    if not key:
        sys.exit("TOMTOM_KEY is not set")

    now = datetime.now(RIYADH_TZ).strftime("%Y-%m-%d %H:%M:%S")
    rows = []
    for road, lat, lon in ROADS:
        try:
            seg = get_segment(lat, lon, key)
        except Exception as e:
            print(f"could not get {road}: {e}")
            continue
        rows.append({
            "timestamp": now,
            "road": road,
            "lat": lat,
            "lon": lon,
            "current_speed": seg["currentSpeed"],
            "free_flow_speed": seg["freeFlowSpeed"],
            "current_travel_time": seg["currentTravelTime"],
            "free_flow_travel_time": seg["freeFlowTravelTime"],
            "confidence": seg.get("confidence"),
            "road_closure": seg.get("roadClosure", False),
            "frc": seg.get("frc"),
        })
        time.sleep(0.2)

    OUT_FILE.parent.mkdir(exist_ok=True)
    new_file = not OUT_FILE.exists()
    with open(OUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerows(rows)

    print(f"{now}: saved {len(rows)} of {len(ROADS)} roads")


if __name__ == "__main__":
    main()
