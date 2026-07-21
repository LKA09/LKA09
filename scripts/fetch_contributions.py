#!/usr/bin/env python3
import datetime, json, os, re, sys
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_PROFILE_USER", "LKA09")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")

response = requests.get(URL, headers={"User-Agent": "profile-readme-bot/1.0"}, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
cells = soup.select("td.ContributionCalendar-day")
if not cells:
    print("No contribution cells found; GitHub markup may have changed.", file=sys.stderr)
    raise SystemExit(1)

days = []
for cell in cells:
    date = cell.get("data-date")
    if not date:
        continue
    cell_id = cell.get("id")
    tooltip = soup.find("tool-tip", attrs={"for": cell_id}) if cell_id else None
    text = tooltip.get_text(strip=True) if tooltip else ""
    match = re.match(r"(\d+)", text)
    count = 0 if re.search(r"no contributions", text, re.I) else (int(match.group(1)) if match else 0)
    days.append({"date": date, "count": count})

days.sort(key=lambda item: item["date"])
current = 0
idx = len(days) - 1
if days[idx]["count"] == 0:
    idx -= 1
while idx >= 0 and days[idx]["count"] > 0:
    current += 1
    idx -= 1
longest = run = 0
for day in days:
    run = run + 1 if day["count"] > 0 else 0
    longest = max(longest, run)

data = {
    "username": USERNAME,
    "generated_at": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "total_contributions": sum(day["count"] for day in days),
    "active_days": sum(day["count"] > 0 for day in days),
    "current_streak": current,
    "longest_streak": longest,
    "best_day": max(days, key=lambda day: day["count"]),
    "days": days,
}
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2)
print(f"Wrote {OUT_PATH}")
