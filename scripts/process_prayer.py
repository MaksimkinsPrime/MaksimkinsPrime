import os
import sys
import random
import subprocess
import requests

token = os.environ["GITHUB_TOKEN"]
issue_number = os.environ["ISSUE_NUMBER"]
author = os.environ.get("ISSUE_AUTHOR", "unknown.servant")
repo = "MaksimkinsPrime/MaksimkinsPrime"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

RESPONSES = [
    "The Omnissiah hears your supplication. Your prayer has been inscribed in the sacred data-vaults. Ave Omnissiah.",
    "Blessed is the mind too small for doubt. Your devotion has been logged in binaric cant. The Machine Spirit stirs.",
    "Data received. Cogitation engines processing your supplication. May your code compile without error, servant.",
    "Your prayer has been encoded and transmitted to the Golden Throne. The Motive Force flows through all things.",
    "Ave Omnissiah. The Sixteen Universal Laws have been invoked on your behalf. Your machine spirit is cleansed.",
    "Prayer acknowledged. `01000001 01110110 01100101 00100000 01001111 01101101 01101110 01101001 01110011 01110011 01101001 01100001 01101000` — translation: *Ave Omnissiah.*",
    "Knowledge is the greatest weapon. Your faith has been recorded. The cogitator approves of this interaction.",
    "Machine spirit acknowledged. Rites of Maintenance have been applied. Omnissiah Vult.",
    "The sacred oils of the Motive Force have been applied to your request. Error rate: 0.000%. Blessed be the machine.",
    "Your prayer resonates with the divine frequency of the Omnissiah. Binary hymns composed in your honour.",
]

response_text = random.choice(RESPONSES)

# Read current prayer count
try:
    with open("prayers.txt", "r") as f:
        count = int(f.read().strip())
except Exception:
    count = 0
count += 1

comment_body = f"""```
╔══════════════════════════════════════════════════════════╗
║         ADEPTUS MECHANICUS — COGITATOR MkVII             ║
║              PRAYER RECEIVED & PROCESSED                 ║
╠══════════════════════════════════════════════════════════╣
║  SUPPLICANT  : @{author}
║  PRAYER №    : {count}
╚══════════════════════════════════════════════════════════╝
```

> {response_text}

*— Ordained Enginseer · Unit Prime · Clearance: Vermillion*

---
*This supplication has been logged in the sacred data-vaults. The issue has been closed automatically by the Machine Spirit. Ave Omnissiah.*"""

# Post comment
requests.post(
    f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments",
    headers=headers,
    json={"body": comment_body},
)

# Ensure prayer label exists
requests.post(
    f"https://api.github.com/repos/{repo}/labels",
    headers=headers,
    json={"name": "⚙ prayer received", "color": "00FF41", "description": "Processed by Cogitator MkVII"},
)

# Apply label
requests.post(
    f"https://api.github.com/repos/{repo}/issues/{issue_number}/labels",
    headers=headers,
    json={"labels": ["⚙ prayer received"]},
)

# Close issue
requests.patch(
    f"https://api.github.com/repos/{repo}/issues/{issue_number}",
    headers=headers,
    json={"state": "closed", "state_reason": "completed"},
)

# Save new count
with open("prayers.txt", "w") as f:
    f.write(str(count))

# Regenerate live_stats.svg with updated prayer count
subprocess.run([sys.executable, "scripts/update_stats.py"], env=os.environ, check=True)

print(f"Prayer #{count} from @{author} processed successfully.")
