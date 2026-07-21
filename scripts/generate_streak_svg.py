#!/usr/bin/env python3
import datetime, json, sys, urllib.request

USER = sys.argv[1] if len(sys.argv) > 1 else "LKA09"
OUT = sys.argv[2] if len(sys.argv) > 2 else "contrib-heatmap.svg"
url = f"https://github-contributions-api.jogruber.de/v4/{USER}?y=last"
with urllib.request.urlopen(url, timeout=25) as response:
    data = json.loads(response.read().decode())

contribs = data["contributions"]
total = data["total"]["lastYear"]
CELL, GAP, RAD, LEFT, TOP = 13, 3, 2.5, 34, 24
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
weeks = (len(contribs) + 6) // 7
width = LEFT + weeks * (CELL + GAP) + 6
height = TOP + 7 * (CELL + GAP) + 22
max_order = (weeks - 1) + 6 * 0.55
labels, rects = [], []
start = datetime.date.fromisoformat(contribs[0]["date"])
last_month = None
for week in range(weeks):
    date = start + datetime.timedelta(days=week * 7)
    if date.month != last_month:
        last_month = date.month
        labels.append(f'<text class="lbl" x="{LEFT + week*(CELL+GAP)}" y="{TOP-8}">{MONTHS[date.month-1]}</text>')
for name, row in [("Mon",1),("Wed",3),("Fri",5)]:
    labels.append(f'<text class="lbl" x="2" y="{TOP + row*(CELL+GAP) + CELL - 2}">{name}</text>')
for index, item in enumerate(contribs):
    week, row, level = index // 7, index % 7, item["level"]
    x, y = LEFT + week*(CELL+GAP), TOP + row*(CELL+GAP)
    delay = round((week + row*0.55) / max_order * 3.6, 3)
    klass = "c g" if level >= 1 else "c e"
    rects.append(f'<rect class="{klass}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RAD}" fill="{COLORS[level]}" style="animation-delay:{delay}s"/>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">
<style>
.lbl{{fill:#7d8590;font-size:13px;font-weight:600}} .total{{fill:#e6edf3;font-size:15px;font-weight:700}}
.c{{transform-box:fill-box;transform-origin:center;opacity:0;animation:pop .55s ease-out both}}
.g{{animation:pop .55s ease-out both,flash .7s ease-out both}}
@keyframes pop{{0%{{opacity:0;transform:scale(.2)}}60%{{opacity:1;transform:scale(1.1)}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes flash{{0%,45%{{filter:brightness(2.4)}}100%{{filter:brightness(1)}}}}
@media (prefers-reduced-motion:reduce){{.c{{opacity:1!important;animation:none!important}}}}
</style><rect width="{width}" height="{height}" fill="none"/>{''.join(labels)}{''.join(rects)}<text class="total" x="{LEFT}" y="{height-6}">{total:,} contributions in the last year</text></svg>'''
open(OUT, "w", encoding="utf-8").write(svg)
print(f"Wrote {OUT}")
