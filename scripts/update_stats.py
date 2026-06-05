import os
import requests
from datetime import datetime, timezone, timedelta

token = os.environ["GITHUB_TOKEN"]
username = "MaksimkinsPrime"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# User info
user = requests.get(f"https://api.github.com/users/{username}", headers=headers).json()
public_repos = user.get("public_repos", 0)

# Events (last 90 days, up to 100)
events_raw = requests.get(
    f"https://api.github.com/users/{username}/events?per_page=100", headers=headers
).json()
events = events_raw if isinstance(events_raw, list) else []
push_events = [e for e in events if e.get("type") == "PushEvent"]

last_date = push_events[0]["created_at"][:10] if push_events else "NO DATA"

week_ago = datetime.now(timezone.utc) - timedelta(days=7)
week_commits = sum(
    e["payload"].get("size", 0)
    for e in push_events
    if datetime.fromisoformat(e["created_at"].replace("Z", "+00:00")) > week_ago
)

# Stars across all repos
repos_raw = requests.get(
    f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers
).json()
repos = repos_raw if isinstance(repos_raw, list) else []
total_stars = sum(r.get("stargazers_count", 0) for r in repos)

# Prayer count
try:
    with open("prayers.txt", "r") as f:
        prayers = int(f.read().strip())
except Exception:
    prayers = 0

updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="200" viewBox="0 0 800 200">
  <defs>
    <style>
      @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:.5}} }}
      @keyframes scan  {{ 0%{{transform:translateY(-4px)}} 100%{{transform:translateY(204px)}} }}
      @keyframes blink {{ 0%,49%{{opacity:1}} 50%,100%{{opacity:0}} }}
      .border   {{ animation: pulse 5s ease-in-out infinite; }}
      .scanline {{ animation: scan  4.5s linear infinite; }}
      .dot      {{ animation: blink 1.2s step-end infinite; }}
    </style>
    <pattern id="sl" x="0" y="0" width="800" height="4" patternUnits="userSpaceOnUse">
      <rect width="800" height="2" fill="#000" opacity=".22"/>
    </pattern>
  </defs>

  <rect width="800" height="200" fill="#000000"/>
  <rect class="border" x="2"  y="2"  width="796" height="196" fill="none" stroke="#00FF41" stroke-width="1.8"/>
  <rect class="border" x="7"  y="7"  width="786" height="186" fill="none" stroke="#00FF41" stroke-width=".4" opacity=".4"/>
  <text class="border" x="13"  y="22"  font-size="12" font-family="'Courier New',monospace" fill="#00FF41">⚙</text>
  <text class="border" x="774" y="22"  font-size="12" font-family="'Courier New',monospace" fill="#00FF41">⚙</text>
  <text class="border" x="13"  y="194" font-size="12" font-family="'Courier New',monospace" fill="#00FF41">⚙</text>
  <text class="border" x="774" y="194" font-size="12" font-family="'Courier New',monospace" fill="#00FF41">⚙</text>

  <text x="400" y="44" font-size="13" text-anchor="middle" font-family="'Courier New',monospace" fill="#00FF41">&#9619; COGITATOR READOUTS &#8212; LIVE BINARIC MANIFEST &#9619;</text>
  <text x="400" y="58" font-size="10" text-anchor="middle" font-family="'Courier New',monospace" fill="#00FF41" opacity=".38">&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;&#9552;</text>

  <text x="30"  y="80"  font-size="13" font-family="'Courier New',monospace" fill="#00FF41">LAST OPERATION   : {last_date}</text>
  <text x="30"  y="98"  font-size="13" font-family="'Courier New',monospace" fill="#00FF41">WEEKLY SORTIES   : {week_commits} commits dispatched</text>
  <text x="30"  y="116" font-size="13" font-family="'Courier New',monospace" fill="#00FF41">REPOSITORIES     : {public_repos} active</text>
  <text x="30"  y="134" font-size="13" font-family="'Courier New',monospace" fill="#00FF41">STARS EARNED     : {total_stars}</text>
  <text x="30"  y="152" font-size="13" font-family="'Courier New',monospace" fill="#00FF41">PRAYERS RECEIVED : {prayers}</text>

  <text class="dot" x="640" y="80" font-size="12" font-family="'Courier New',monospace" fill="#00FF41">&#9673;</text>
  <text x="657" y="80" font-size="11" font-family="'Courier New',monospace" fill="#00FF41" opacity=".7">LIVE</text>

  <text x="400" y="180" font-size="9" text-anchor="middle" font-family="'Courier New',monospace" fill="#00FF41" opacity=".32">MANIFEST SYNC: {updated} &#8212; OMNISSIAH VULT</text>

  <g class="scanline"><rect x="0" y="0" width="800" height="3" fill="#00FF41" opacity=".07"/></g>
  <rect width="800" height="200" fill="url(#sl)"/>
</svg>"""

with open("live_stats.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print(f"Stats updated — repos:{public_repos} stars:{total_stars} week:{week_commits} prayers:{prayers}")
