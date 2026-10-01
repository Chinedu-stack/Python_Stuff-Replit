import openpyxl
import csv
import os

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
SOURCE = r"C:\Users\chine\OneDrive\School Fantasy League\Copy of The Year_11_Fantasy_League.xlsx"
OUTPUT = r"C:\Users\chine\OneDrive\Python Stuff\Fantasy League\teams_backup.csv"

# ---------------------------------------------------------
# OPEN WORKBOOK
# ---------------------------------------------------------
print(f"Reading: {SOURCE}\n")
wb = openpyxl.load_workbook(SOURCE, data_only=True)

# ---------------------------------------------------------
# GET LIST OF MANAGERS FROM THE "PICK YOUR TEAM" SHEET
# ---------------------------------------------------------
if "PICK YOUR TEAM" not in wb.sheetnames:
    raise SystemExit("ERROR: 'PICK YOUR TEAM' sheet not found. Check the file.")

menu = wb["PICK YOUR TEAM"]
managers = []
for row in menu.iter_rows(min_row=5, max_col=2, values_only=True):
    name = row[1]  # column B
    if name and isinstance(name, str) and name.strip():
        managers.append(name.strip())

print(f"Found {len(managers)} managers on PICK YOUR TEAM.\n")

# ---------------------------------------------------------
# EXTRACT EACH MANAGER'S TEAM
# ---------------------------------------------------------
teams = {}
missing_picks = []
missing_captains = []

print("Extracting teams...")
for name in managers:
    if name not in wb.sheetnames:
        print(f"  {name:<18} ⚠ Sheet not found")
        missing_picks.append(name)
        continue

    ws = wb[name]
    captain = ws["C5"].value
    players = [ws[f"C{r}"].value for r in range(10, 15)]

    teams[name] = {
        "captain": captain,
        "players": players,
    }

    filled = sum(1 for p in players if p)
    flag = ""
    if filled < 5:
        flag = f"  ⚠ {filled}/5 players"
        missing_picks.append(name)
    if not captain:
        flag += "  ⚠ No captain"
        missing_captains.append(name)

    print(f"  {name:<18} ✓ {filled}/5 players + captain{flag}")

print()

# ---------------------------------------------------------
# EXTRACT WEEK 1 SCORES FROM "TEST RESULTS"
# ---------------------------------------------------------
if "TEST RESULTS" not in wb.sheetnames:
    raise SystemExit("ERROR: 'TEST RESULTS' sheet not found. Check the file.")

results_ws = wb["TEST RESULTS"]
scores = {}
missing_scores = []

print("Extracting test scores...")
for row in results_ws.iter_rows(min_row=5, max_row=30, max_col=3, values_only=True):
    name = row[1]  # column B
    score = row[2]  # column C
    if name and isinstance(name, str) and name.strip():
        name = name.strip()
        scores[name] = score
        flag = ""
        if score is None or score == "":
            flag = "  ⚠ No score"
            missing_scores.append(name)
        print(f"  {name:<18} {score if score not in (None,'') else '—'}{flag}")

print()

# ---------------------------------------------------------
# WRITE CSV
# ---------------------------------------------------------
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Manager", "P1", "P2", "P3", "P4", "P5", "Captain", "GW1 Score"])

    for name in managers:
        t = teams.get(name, {"players": ["", "", "", "", ""], "captain": ""})
        score = scores.get(name, "")
        writer.writerow([
            name,
            t["players"][0] or "",
            t["players"][1] or "",
            t["players"][2] or "",
            t["players"][3] or "",
            t["players"][4] or "",
            t["captain"] or "",
            score if score not in (None, "") else "",
        ])

print(f"Saved to: {OUTPUT}")
print(f"Done. {len(managers)} managers extracted.")

# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Managers found:       {len(managers)}")
print(f"Missing picks:        {len(missing_picks)} {missing_picks if missing_picks else ''}")
print(f"Missing captains:     {len(missing_captains)} {missing_captains if missing_captains else ''}")
print(f"Missing scores:       {len(missing_scores)} {missing_scores if missing_scores else ''}")
print("=" * 60)