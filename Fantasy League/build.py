# build_v2.py
# Rebuilds the Year 11 Fantasy League workbook with:
#   - 21 players, 30 pre-allocated slots (dynamic, soft-delete friendly)
#   - 21 managers, 13 with teams, 8 empty
#   - POINTS HISTORY sheet (new, hidden)
#   - CALCULATIONS W (Overall) + X (Overall tiebreak) columns
#   - Cumulative Overall Leaderboard (sorts by X)
#   - SETTINGS C17 (tests/GW), C18 (captain mult), SEASON CONFIG block
#   - All 12 named ranges (dynamic where they list players)
#   - GW1 scores pre-loaded, CurrentGW = 1, RAW RESULTS + POINTS HISTORY empty
#
# Output: 11O Fantasy League v2.xlsx in the "Copies" folder.
#         Test it, THEN copy over the live workbook.

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment, Protection
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.workbook.defined_name import DefinedName

# =========================================================
# CONFIG
# =========================================================
PASSWORD = "Legendx24j@"
SAVE_PATH = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing\11O Fantasy League v2.xlsx"
TOTAL_WEEKS = 20
PLAYER_SLOTS = 30           # 21 current + 9 spare
MANAGER_ROWS = 21           # 21 managers

# Slot / row anchors
SET_PLAYER_START = 22                          # SETTINGS!B22 = first player
SET_PLAYER_END = SET_PLAYER_START + PLAYER_SLOTS - 1        # row 51
SET_LOG_HEADER = 53                            # WEEKLY PRICE LOG header
SET_LOG_COL_HEADER = 54                        # Player | GW1..GW20
SET_LOG_START = 55                             # first player row in log
SET_LOG_END = SET_LOG_START + PLAYER_SLOTS - 1              # row 84
SET_CONFIG_ROW = 86                            # SEASON CONFIG header
SET_CURRENTGW_ROW = 87                         # Current GW value in C
SET_SEASONLEN_ROW = 88                         # Season length value in C

CALC_PLAYER_START = 2
CALC_PLAYER_END = CALC_PLAYER_START + PLAYER_SLOTS - 1      # row 31
CALC_MGR_START = 2
CALC_MGR_END = CALC_MGR_START + MANAGER_ROWS - 1            # row 22

TEST_HEADER = 5
TEST_START = 6
TEST_END = TEST_START + PLAYER_SLOTS - 1                    # row 35

PM_HEADER = 4
PM_START = 5
PM_END = PM_START + PLAYER_SLOTS - 1                        # row 34

PICK_START = 5
PICK_END = PICK_START + MANAGER_ROWS - 1                    # row 25

MGR_ROW_START = 2
MGR_ROW_END = MGR_ROW_START + MANAGER_ROWS - 1              # row 22

# =========================================================
# DATA
# =========================================================
# Players (name, base price) — sorted by price desc, alpha within price
players = [
    ("Lia Li", 13.0), ("Sophie Barker", 13.0),
    ("Chinedu Chile", 11.0), ("Emily Warburton", 11.0),
    ("Alyza Rai", 10.5), ("David Wu", 10.5), ("Joe Paige", 10.5),
    ("Azlan Husain", 10.0), ("Nina De Saram", 10.0),
    ("Alexa Amesimeku", 9.5), ("Daniel Liu", 9.5), ("Rebecca Seymour", 9.5),
    ("Edwin Mayers", 9.0),
    ("Melody Zhaeentan", 8.5),
    ("Esme Beston", 8.0), ("Iona Smith", 8.0), ("Oscar Day-Duran", 8.0),
    ("Alfie Foley", 7.5),
    ("Ava Swinfen", 7.0), ("Rory Bowman", 7.0), ("Xander Meijer", 7.0),
]
player_names = [p[0] for p in players]

# Managers (alphabetical)
managers = sorted([
    "Alexa Amesimeku", "Alfie Foley", "Alyza Rai", "Ava Swinfen", "Azlan Husain",
    "Chinedu Chile", "Daniel Liu", "David Wu", "Edwin Mayers", "Emily Warburton",
    "Esme Beston", "Iona Smith", "Joe Paige", "Lia Li", "Melody Zhaeentan",
    "Nina De Saram", "Oscar Day-Duran", "Rebecca Seymour", "Rory Bowman",
    "Sophie Barker", "Xander Meijer",
])

# Teams: only 13 managers have submitted. Use "" for empty slots.
teams_data = {
    "Alexa Amesimeku": {"c": "Sophie Barker",
        "p": ["Sophie Barker", "Joe Paige", "Alexa Amesimeku", "Nina De Saram", "Xander Meijer"]},
    "Alfie Foley": {"c": "Sophie Barker",
        "p": ["Ava Swinfen", "David Wu", "Alyza Rai", "Sophie Barker", "Edwin Mayers"]},
    "Ava Swinfen": {"c": "Lia Li",
        "p": ["Ava Swinfen", "Melody Zhaeentan", "Lia Li", "Chinedu Chile", "David Wu"]},
    "Azlan Husain": {"c": "Emily Warburton",
        "p": ["Emily Warburton", "Chinedu Chile", "Joe Paige", "Alfie Foley", "Edwin Mayers"]},
    "Chinedu Chile": {"c": "Chinedu Chile",
        "p": ["Chinedu Chile", "Alexa Amesimeku", "David Wu", "Edwin Mayers", "Azlan Husain"]},
    "Daniel Liu": {"c": "",
        "p": ["Alyza Rai", "Ava Swinfen", "", "David Wu", "Chinedu Chile"]},
    "David Wu": {"c": "Edwin Mayers",
        "p": ["Azlan Husain", "Rebecca Seymour", "Edwin Mayers", "Chinedu Chile", "Joe Paige"]},
    "Edwin Mayers": {"c": "Emily Warburton",
        "p": ["Sophie Barker", "Esme Beston", "Edwin Mayers", "Emily Warburton", "Ava Swinfen"]},
    "Joe Paige": {"c": "Chinedu Chile",
        "p": ["Chinedu Chile", "Joe Paige", "Alfie Foley", "Lia Li", "Oscar Day-Duran"]},
    "Melody Zhaeentan": {"c": "Lia Li",
        "p": ["Lia Li", "Edwin Mayers", "Rebecca Seymour", "Joe Paige", "Xander Meijer"]},
    "Oscar Day-Duran": {"c": "Joe Paige",
        "p": ["Oscar Day-Duran", "Chinedu Chile", "Nina De Saram", "David Wu", "Joe Paige"]},
    "Rory Bowman": {"c": "Lia Li",
        "p": ["David Wu", "Ava Swinfen", "Alyza Rai", "Edwin Mayers", "Lia Li"]},
    "Xander Meijer": {"c": "Lia Li",
        "p": ["Lia Li", "David Wu", "Ava Swinfen", "Joe Paige", "Melody Zhaeentan"]},
}

# GW1 test scores: name -> (test1, test2) or (None, None) if blank
gw1_scores = {
    "Alexa Amesimeku": (73, 88),
    "Alfie Foley": (40, 65),
    "Alyza Rai": (70, 86),
    "Ava Swinfen": (35, 74),
    "Azlan Husain": (50, 86),
    "Chinedu Chile": (60, 86),
    "Daniel Liu": (63, 74),
    "David Wu": (60, 86),
    "Edwin Mayers": (40, 81),
    "Emily Warburton": (None, None),
    "Esme Beston": (38, 56),
    "Iona Smith": (None, None),
    "Joe Paige": (83, 91),
    "Lia Li": (55, 100),
    "Melody Zhaeentan": (75, 74),
    "Nina De Saram": (75, 86),
    "Oscar Day-Duran": (38, 72),
    "Rebecca Seymour": (None, None),
    "Rory Bowman": (25, 58),
    "Sophie Barker": (88, 98),
    "Xander Meijer": (33, 81),
}

# =========================================================
# THEME
# =========================================================
NAVY="0B1F3A"; BLUE="1565C0"; LIGHT_BLUE="EAF2FF"; PALE_BLUE="F5F9FF"
WHITE="FFFFFF"; DARK="172033"; GREY="6B7280"; LIGHT_GREY="E5E7EB"
GREEN="16A34A"; LIGHT_GREEN="DCFCE7"; RED="DC2626"; LIGHT_RED="FEE2E2"
GOLD="F59E0B"; LIGHT_GOLD="FEF3C7"; SLATE="475569"; SLATE_DARK="334155"
ORANGE="EA580C"

thin_grey = Side(style="thin", color=LIGHT_GREY)
medium_blue = Side(style="medium", color=BLUE)

def title(ws, text, row=1, start_col=1, end_col=8):
    ws.merge_cells(start_row=row, start_column=start_col, end_row=row, end_column=end_col)
    c = ws.cell(row, start_col, text)
    c.font = Font(size=22, bold=True, color=WHITE)
    c.fill = PatternFill("solid", fgColor=NAVY)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row].height = 52

def section(ws, text, row, start_col=1, end_col=8, fill=BLUE):
    ws.merge_cells(start_row=row, start_column=start_col, end_row=row, end_column=end_col)
    c = ws.cell(row, start_col, text)
    c.font = Font(size=13, bold=True, color=WHITE)
    c.fill = PatternFill("solid", fgColor=fill)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row].height = 32

def header_row(ws, row, start_col, end_col, fill=NAVY):
    for col in range(start_col, end_col + 1):
        c = ws.cell(row, col)
        c.font = Font(bold=True, color=WHITE, size=12)
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = Border(bottom=medium_blue)
    ws.row_dimensions[row].height = 32

def box(cell, fill=WHITE, bold=False, color=DARK, align="left", size=12, italic=False, unlocked=False):
    cell.fill = PatternFill("solid", fgColor=fill)
    cell.font = Font(bold=bold, color=color, size=size, italic=italic)
    cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=False)
    cell.border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
    if unlocked:
        cell.protection = Protection(locked=False)

def protect(ws):
    ws.protection.sheet = True
    ws.protection.password = PASSWORD
    ws.protection.formatCells = False
    ws.protection.formatColumns = False
    ws.protection.formatRows = False
    ws.protection.selectLockedCells = False
    ws.protection.selectUnlockedCells = False

# =========================================================
# BUILD
# =========================================================
wb = Workbook()
wb.remove(wb.active)

# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------
home = wb.create_sheet("HOME")
home.sheet_view.showGridLines = False
for col, w in {"A":4,"B":28,"C":26,"D":26,"E":26,"F":26,"G":26,"H":4}.items():
    home.column_dimensions[col].width = w

title(home, "YEAR 11 FANTASY LEAGUE", 1, 2, 7)

home.merge_cells("B2:G2")
home["B2"] = "GAMEWEEK 1"
home["B2"].font = Font(size=16, bold=True, color=BLUE)
home["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
home.row_dimensions[2].height = 32

home.row_dimensions[3].height = 12
home.merge_cells("B4:G4")
home["B4"] = "  GAMEWEEK 1: Biology and English  "
home["B4"].font = Font(size=13, bold=True, color=DARK)
home["B4"].fill = PatternFill("solid", fgColor=LIGHT_BLUE)
home["B4"].alignment = Alignment(horizontal="center", vertical="center")
home.row_dimensions[4].height = 34

home.merge_cells("B5:G5")
home["B5"] = " GAMEWEEK 1"
home["B5"].font = Font(size=13, bold=True, color=DARK)
home["B5"].fill = PatternFill("solid", fgColor=LIGHT_BLUE)
home["B5"].alignment = Alignment(horizontal="center", vertical="center")
home.row_dimensions[5].height = 34

home.row_dimensions[6].height = 12
home["B7"] = "CURRENT GAMEWEEK:"
home["B7"].font = Font(size=12, bold=True, color=GREY)
home["B7"].alignment = Alignment(horizontal="right", vertical="center")
home["C7"] = "=CurrentGW"
home["C7"].font = Font(size=14, bold=True, color=NAVY)
home["C7"].fill = PatternFill("solid", fgColor=LIGHT_GOLD)
home["C7"].alignment = Alignment(horizontal="center", vertical="center")
home["C7"].border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
home.row_dimensions[7].height = 30

home.row_dimensions[8].height = 12
section(home, "HOW TO PLAY", 9, 2, 7)
steps = [
    "1.  Go to PICK YOUR TEAM and click your name.",
    "2.  Pick 5 players from the dropdowns.",
    "3.  Pick 1 captain using the GOLD CAPTAIN BOX.",
    "4.  Stay under the £50m budget.",
    "5.  Enter your own test % on TEST RESULTS after each test.",
]
for i, text in enumerate(steps):
    r = 10 + i
    home.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
    c = home.cell(r, 2, text); box(c, PALE_BLUE)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    home.row_dimensions[r].height = 30

home.row_dimensions[16].height = 12
section(home, "HOW POINTS WORK", 17, 2, 7)
home.merge_cells("B18:G19")
home["B18"] = ("Your score is compared to the CLASS AVERAGE.\n"
               "Average = 5 points. Every small step above = +1. Every step below = −1.")
home["B18"].font = Font(size=12, color=DARK)
home["B18"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
box(home["B18"], PALE_BLUE)
home.row_dimensions[18].height = 24
home.row_dimensions[19].height = 24
pts_rows = [
    ("Well above average",   "High points"),
    ("Slightly above",       "6–7 points"),
    ("Exactly average",      "5 points"),
    ("Slightly below",       "3–4 points"),
    ("Well below",           "0–1 points"),
]
for i, (label, val) in enumerate(pts_rows):
    r = 20 + i
    home.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
    home.cell(r, 2, label).font = Font(bold=True, color=DARK, size=12)
    home.cell(r, 2).fill = PatternFill("solid", fgColor=LIGHT_BLUE)
    home.cell(r, 2).alignment = Alignment(horizontal="left", vertical="center", indent=1)
    home.cell(r, 2).border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
    home.merge_cells(start_row=r, start_column=4, end_row=r, end_column=7)
    home.cell(r, 4, val).font = Font(color=DARK, size=12)
    home.cell(r, 4).alignment = Alignment(horizontal="left", vertical="center", indent=1)
    home.cell(r, 4).border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
    home.row_dimensions[r].height = 26

home.row_dimensions[26].height = 12
section(home, "HOW PRICES WORK", 27, 2, 7)
home.merge_cells("B28:G29")
home["B28"] = ("Prices move based on your 3-WEEK FORM vs the class average.\n"
               "Cheap players rise faster. Expensive players rise slower.")
home["B28"].font = Font(size=12, color=DARK)
home["B28"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
box(home["B28"], PALE_BLUE)
home.row_dimensions[28].height = 24
home.row_dimensions[29].height = 24
price_rows = [
    ("No changes first 2 weeks",       "Settling in"),
    ("Week 3 onward",                   "Prices move based on form"),
    ("Beating average consistently",    "Price rises up to +£0.5m/week"),
    ("Below average consistently",      "Price falls up to -£0.5m/week"),
    ("Bounds",                          "£7.0m  to  £13.0m"),
]
for i, (label, val) in enumerate(price_rows):
    r = 30 + i
    home.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
    home.cell(r, 2, label).font = Font(bold=True, color=DARK, size=12)
    home.cell(r, 2).fill = PatternFill("solid", fgColor=LIGHT_BLUE)
    home.cell(r, 2).alignment = Alignment(horizontal="left", vertical="center", indent=1)
    home.cell(r, 2).border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
    home.merge_cells(start_row=r, start_column=5, end_row=r, end_column=7)
    home.cell(r, 5, val).font = Font(color=DARK, size=12)
    home.cell(r, 5).alignment = Alignment(horizontal="left", vertical="center", indent=1)
    home.cell(r, 5).border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
    home.row_dimensions[r].height = 26

home.merge_cells("B36:G36")
home["B36"] = "SETTINGS and RULES sheets have more detail. Ask Mr C if anything is unclear."
home["B36"].font = Font(size=11, italic=True, color=GREY)
home["B36"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
home.row_dimensions[36].height = 30
protect(home)

# ---------------------------------------------------------
# RULES
# ---------------------------------------------------------
rules = wb.create_sheet("RULES")
rules.sheet_view.showGridLines = False
rules.column_dimensions["A"].width = 4
rules.column_dimensions["B"].width = 28
rules.column_dimensions["C"].width = 72
title(rules, "RULES & HOW TO PLAY", 1, 2, 3)
rule_rows = [
    ("BUDGET", "£50.0m per manager. Pick exactly 5 players."),
    ("CAPTAIN", "Pick 1 captain using the GOLD box on your team sheet. Captain scores 2× points."),
    ("DEADLINE", "Set on HOME each gameweek."),
    ("TEST DATE", "Set on HOME each gameweek."),
    ("RESULT ENTRY", "Each student enters their own test % on TEST RESULTS."),
    ("POINTS", "Based on class average. Average = 5 pts. Every step above/below = ±1 pt. Step size adjusts to class spread. Capped 0–10."),
    ("PRICE CHANGES", "Move based on 3-week form vs class average. First 2 weeks: no change. Week 3 onward: max ±£0.5m per week."),
    ("PRICE SCALING", "Cheap players rise faster (×1.0). Mid-price ×0.75. Expensive ×0.5."),
    ("PRICE LIMITS", "Minimum £7.0m. Maximum £13.0m."),
    ("TRANSFERS", "Unlimited free transfers between gameweeks."),
    ("GOLDEN RULE", "Pick 5 players + captain, enter your test score. Excel does the rest."),
]
for i, (topic, explanation) in enumerate(rule_rows):
    r = 4 + (i * 2)
    rules.cell(r, 2, topic)
    rules.cell(r, 3, explanation)
    box(rules.cell(r, 2), LIGHT_BLUE, True, DARK, "left")
    box(rules.cell(r, 3), WHITE, False, DARK, "left")
    rules.cell(r, 3).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
    rules.row_dimensions[r].height = 40
    rules.row_dimensions[r + 1].height = 8
protect(rules)

# ---------------------------------------------------------
# PICK YOUR TEAM
# ---------------------------------------------------------
menu = wb.create_sheet("PICK YOUR TEAM")
menu.sheet_view.showGridLines = False
menu.column_dimensions["A"].width = 6
menu.column_dimensions["B"].width = 32
menu.column_dimensions["C"].width = 26
title(menu, "PICK YOUR TEAM", 1, 2, 3)
menu.merge_cells("B2:C2")
menu["B2"] = "Click your name to jump to your team sheet."
menu["B2"].font = Font(size=12, italic=True, color=GREY)
menu["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
menu.row_dimensions[2].height = 30
menu.row_dimensions[3].height = 12
menu["B4"] = "Manager"; menu["C4"] = "Status"
header_row(menu, 4, 2, 3)

for i, name in enumerate(managers):
    r = PICK_START + i
    c = menu.cell(r, 2, name)
    c.hyperlink = f"#'{name}'!A1"
    c.font = Font(bold=True, color=BLUE, underline="single", size=12)
    box(c, WHITE, True, BLUE); c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    menu.cell(r, 3, f"=CALCULATIONS!U{MGR_ROW_START + i}")
    box(menu.cell(r, 3), PALE_BLUE, align="center")
    menu.row_dimensions[r].height = 30

# Status line at top-right of the header row
menu["E4"] = f'=CONCATENATE("Status: ", COUNTIF(C{PICK_START}:C{PICK_END},"VALID TEAM"), "/", COUNTA(B{PICK_START}:B{PICK_END}))'
menu["E4"].font = Font(bold=True, color=DARK, size=12)
menu["E4"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
protect(menu)

# ---------------------------------------------------------
# PLAYER MARKET
# ---------------------------------------------------------
market = wb.create_sheet("PLAYER MARKET")
market.sheet_view.showGridLines = False
market.column_dimensions["A"].width = 4
market.column_dimensions["B"].width = 34
market.column_dimensions["C"].width = 14
market.column_dimensions["D"].width = 14
market.column_dimensions["E"].width = 20
title(market, "PLAYER MARKET", 1, 2, 5)
market.merge_cells("B2:E2")
market["B2"] = "Prices  •  This week's change  •  Ownership"
market["B2"].font = Font(size=12, color=GREY, italic=True)
market["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
market.row_dimensions[2].height = 30
market.row_dimensions[3].height = 12
for c, h in enumerate(["Player", "Price", "Change", "Ownership %"], start=2):
    market.cell(PM_HEADER, c, h)
header_row(market, PM_HEADER, 2, 5)

for i in range(PLAYER_SLOTS):
    r = PM_START + i
    calc_row = CALC_PLAYER_START + i
    market.cell(r, 2, f'=IF(CALCULATIONS!A{calc_row}="","",CALCULATIONS!A{calc_row})')
    market.cell(r, 3, f'=IF(CALCULATIONS!A{calc_row}="","",CALCULATIONS!C{calc_row})')
    market.cell(r, 4, f'=IF(CALCULATIONS!A{calc_row}="","",IF(CurrentGW<SETTINGS!$C$16,0,CALCULATIONS!C{calc_row}-CALCULATIONS!B{calc_row}))')
    market.cell(r, 5, f'=IF(CALCULATIONS!A{calc_row}="","",COUNTIF(CALCULATIONS!$L$2:$P${CALC_MGR_END},CALCULATIONS!A{calc_row})/COUNTA(CALCULATIONS!$K$2:$K${CALC_MGR_END}))')
    fill = WHITE if i % 2 == 0 else PALE_BLUE
    box(market.cell(r, 2), fill, False, DARK, "left")
    box(market.cell(r, 3), fill, True, DARK, "center")
    box(market.cell(r, 4), fill, True, DARK, "center")
    box(market.cell(r, 5), fill, False, DARK, "center")
    market.cell(r, 3).number_format = '£0.0"m"'
    market.cell(r, 4).number_format = '"▲ +£"0.0"m";"▼ -£"0.0"m";"— £0.0m"'
    market.cell(r, 5).number_format = '0%'
    market.row_dimensions[r].height = 28

market.conditional_formatting.add(f"D{PM_START}:D{PM_END}", FormulaRule(
    formula=[f'D{PM_START}>0'], fill=PatternFill("solid", fgColor=LIGHT_GREEN),
    font=Font(color=GREEN, bold=True)))
market.conditional_formatting.add(f"D{PM_START}:D{PM_END}", FormulaRule(
    formula=[f'D{PM_START}<0'], fill=PatternFill("solid", fgColor=LIGHT_RED),
    font=Font(color=RED, bold=True)))
market.conditional_formatting.add(f"D{PM_START}:D{PM_END}", FormulaRule(
    formula=[f'D{PM_START}=0'], fill=PatternFill("solid", fgColor="F3F4F6"),
    font=Font(color=GREY, bold=True)))

market.merge_cells("B38:E40")
market["B38"] = ("PRICE RULES\n"
                 "Prices move based on 3-week form vs class average.\n"
                 "First 2 gameweeks: no changes.  Min £7.0m  •  Max £13.0m")
market["B38"].font = Font(bold=True, color=DARK, size=12)
market["B38"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
box(market["B38"], LIGHT_BLUE)
protect(market)

# ---------------------------------------------------------
# TEST RESULTS
# ---------------------------------------------------------
results = wb.create_sheet("TEST RESULTS")
results.sheet_view.showGridLines = False
results.column_dimensions["A"].width = 4
results.column_dimensions["B"].width = 32
for col in "CDEFG":
    results.column_dimensions[col].width = 12
results.column_dimensions["H"].width = 12
title(results, "TEST RESULTS", 1, 2, 8)

results.merge_cells("B2:H2")
results["B2"] = "Enter your test scores. "
results["B2"].font = Font(size=12, bold=True, color=BLUE)
results["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
results.row_dimensions[2].height = 30
results.merge_cells("B3:H3")
results["B3"] = "Test name: English and Biology"
results["B3"].font = Font(size=12, color=GREY, italic=True)
results["B3"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
results.row_dimensions[3].height = 22
results.row_dimensions[4].height = 8

# Header row 5
results.cell(TEST_HEADER, 2, "Student")
for i, col in enumerate(range(3, 8)):   # C..G
    cell = results.cell(TEST_HEADER, col)
    cell.value = f'=IF(SUM(C{TEST_START}:C{TEST_END})=0,"Test {i+1}: no results","Test {i+1} avg = "&ROUND(AVERAGE({chr(64+col)}{TEST_START}:{chr(64+col)}{TEST_END}),1)&"%")'
results.cell(TEST_HEADER, 8, "Score")
header_row(results, TEST_HEADER, 2, 8)

for i, name in enumerate(managers):
    r = TEST_START + i
    results.cell(r, 2, name)
    t1, t2 = gw1_scores.get(name, (None, None))
    results.cell(r, 3, t1 if t1 is not None else "")
    results.cell(r, 4, t2 if t2 is not None else "")
    results.cell(r, 8, f'=IFERROR(AVERAGE(C{r}:INDEX(C{r}:G{r},SETTINGS!$C$17)),"")')
    box(results.cell(r, 2), WHITE, False, DARK, "left")
    for col in range(3, 8):
        box(results.cell(r, col), LIGHT_GOLD, False, DARK, "center")
        results.cell(r, col).number_format = '0"%"'
    box(results.cell(r, 8), LIGHT_BLUE, True, DARK, "center")
    results.row_dimensions[r].height = 30

# Pre-allocated blank slots beyond manager count (up to PLAYER_SLOTS total)
for i in range(MANAGER_ROWS, PLAYER_SLOTS):
    r = TEST_START + i
    results.cell(r, 8, f'=IFERROR(AVERAGE(C{r}:INDEX(C{r}:G{r},SETTINGS!$C$17)),"")')
    for col in range(3, 8):
        box(results.cell(r, col), LIGHT_GOLD, False, DARK, "center")
        results.cell(r, col).number_format = '0"%"'
    box(results.cell(r, 2), WHITE, False, GREY, "left")
    box(results.cell(r, 8), LIGHT_BLUE, True, DARK, "center")
    results.row_dimensions[r].height = 30

dv_pct = DataValidation(type="whole", operator="between", formula1="0", formula2="100", allow_blank=True)
dv_pct.error = "Enter a whole number from 0 to 100."
dv_pct.errorTitle = "Invalid percentage"
dv_pct.showErrorMessage = True
results.add_data_validation(dv_pct); dv_pct.add(f"C{TEST_START}:G{TEST_END}")

results.merge_cells(f"B{TEST_END+3}:H{TEST_END+5}")
results.cell(TEST_END+3, 2, "Enter a whole number 0–100 in the gold cells.")
results.cell(TEST_END+3, 2).font = Font(bold=True, color=DARK, size=12)
results.cell(TEST_END+3, 2).alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
box(results.cell(TEST_END+3, 2), LIGHT_GOLD)
# NOT protected - students enter scores

# ---------------------------------------------------------
# OVERALL LEADERBOARD (leading space!)
# ---------------------------------------------------------
overall = wb.create_sheet(" Overall Leaderboard")
overall.sheet_view.showGridLines = False
overall.column_dimensions["A"].width = 4
overall.column_dimensions["B"].width = 12
overall.column_dimensions["C"].width = 32
overall.column_dimensions["D"].width = 18
title(overall, "OVERALL LEADERBOARD", 1, 2, 4)
overall.merge_cells("B2:D2")
overall["B2"] = "All gameweeks combined  •  Sorted by points"
overall["B2"].font = Font(size=12, color=GREY, italic=True)
overall["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
overall.row_dimensions[2].height = 26

overall.merge_cells("B3:D3")
overall["B3"] = ('=IF(MAX($D$6:$D$26)=0,"🏆  OVERALL LEADER:  No results yet",'
                 '"🏆  OVERALL LEADER:  "&INDEX($C$6:$C$26,MATCH(MAX($D$6:$D$26),$D$6:$D$26,0))&"  —  "&MAX($D$6:$D$26)&" pts")')
overall["B3"].font = Font(size=14, bold=True, color="92400E")
overall["B3"].fill = PatternFill("solid", fgColor=LIGHT_GOLD)
overall["B3"].alignment = Alignment(horizontal="center", vertical="center")
overall["B3"].border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
overall.row_dimensions[3].height = 38
overall.row_dimensions[4].height = 12

for c, h in enumerate(["Rank", "Manager", "Overall Points"], start=2):
    overall.cell(5, c, h)
header_row(overall, 5, 2, 4)
for i in range(MANAGER_ROWS):
    r = 6 + i
    overall.cell(r, 3, f'=IFERROR(INDEX(CALCULATIONS!$K$2:$K${CALC_MGR_END},MATCH(LARGE(CALCULATIONS!$X$2:$X${CALC_MGR_END},ROW()-5),CALCULATIONS!$X$2:$X${CALC_MGR_END},0)),"")')
    overall.cell(r, 4, f'=IFERROR(ROUND(LARGE(CALCULATIONS!$X$2:$X${CALC_MGR_END},ROW()-5),0),"")')
    overall.cell(r, 2, f'=IF(ISNUMBER(D{r}),IF(D{r}=0,"",SUMPRODUCT((D$6:D{r}>D{r})*1)+1),"")')
    fill = WHITE if i % 2 == 0 else PALE_BLUE
    box(overall.cell(r, 2), fill, True, DARK, "center")
    box(overall.cell(r, 3), fill, False, DARK, "left")
    box(overall.cell(r, 4), fill, True, DARK, "center")
    overall.row_dimensions[r].height = 30

overall.conditional_formatting.add("B6:B26", FormulaRule(formula=['$B6=1'],
    fill=PatternFill("solid", fgColor=LIGHT_GOLD), font=Font(bold=True, color="92400E")))
overall.conditional_formatting.add("B6:B26", FormulaRule(formula=['$B6=2'],
    fill=PatternFill("solid", fgColor="E5E7EB"), font=Font(bold=True, color="374151")))
overall.conditional_formatting.add("B6:B26", FormulaRule(formula=['$B6=3'],
    fill=PatternFill("solid", fgColor="FED7AA"), font=Font(bold=True, color="9A3412")))
protect(overall)

# ---------------------------------------------------------
# GW LEADERBOARD
# ---------------------------------------------------------
gw = wb.create_sheet("GW Leaderboard")
gw.sheet_view.showGridLines = False
gw.column_dimensions["A"].width = 4
gw.column_dimensions["B"].width = 12
gw.column_dimensions["C"].width = 32
gw.column_dimensions["D"].width = 18
title(gw, "GAMEWEEK LEADERBOARD", 1, 2, 4)
gw.merge_cells("B2:D2")
gw["B2"] = "This gameweek only  •  Sorted by points"
gw["B2"].font = Font(size=12, color=GREY, italic=True)
gw["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
gw.row_dimensions[2].height = 26

gw["B3"] = "CURRENT GAMEWEEK:"
gw["B3"].font = Font(size=12, bold=True, color=GREY)
gw["B3"].alignment = Alignment(horizontal="right", vertical="center")
gw["C3"] = "=HOME!C7"
gw["C3"].font = Font(size=14, bold=True, color=NAVY)
gw["C3"].fill = PatternFill("solid", fgColor=LIGHT_GOLD)
gw["C3"].alignment = Alignment(horizontal="center", vertical="center")
gw["C3"].border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
gw.row_dimensions[3].height = 30
gw.row_dimensions[4].height = 10

gw.merge_cells("B5:D5")
gw["B5"] = ('=IF(MAX($D$8:$D$28)=0,"🏆  GW"&$C$3&" WINNER:  No results yet",'
            '"🏆  GW"&$C$3&" WINNER:  "&INDEX($C$8:$C$28,MATCH(MAX($D$8:$D$28),$D$8:$D$28,0))&"  —  "&MAX($D$8:$D$28)&" pts")')
gw["B5"].font = Font(size=14, bold=True, color="92400E")
gw["B5"].fill = PatternFill("solid", fgColor=LIGHT_GOLD)
gw["B5"].alignment = Alignment(horizontal="center", vertical="center")
gw["B5"].border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
gw.row_dimensions[5].height = 38
gw.row_dimensions[6].height = 12

for c, h in enumerate(["Rank", "Manager", "GW Points"], start=2):
    gw.cell(7, c, h)
header_row(gw, 7, 2, 4)
for i in range(MANAGER_ROWS):
    r = 8 + i
    gw.cell(r, 3, f'=IFERROR(INDEX(CALCULATIONS!$K$2:$K${CALC_MGR_END},MATCH(LARGE(CALCULATIONS!$V$2:$V${CALC_MGR_END},ROW()-7),CALCULATIONS!$V$2:$V${CALC_MGR_END},0)),"")')
    gw.cell(r, 4, f'=IFERROR(ROUND(LARGE(CALCULATIONS!$V$2:$V${CALC_MGR_END},ROW()-7),0),"")')
    gw.cell(r, 2, f'=IF(ISNUMBER(D{r}),IF(D{r}=0,"",SUMPRODUCT((D$8:D{r}>D{r})*1)+1),"")')
    fill = WHITE if i % 2 == 0 else PALE_BLUE
    box(gw.cell(r, 2), fill, True, DARK, "center")
    box(gw.cell(r, 3), fill, False, DARK, "left")
    box(gw.cell(r, 4), fill, True, DARK, "center")
    gw.row_dimensions[r].height = 30

gw.conditional_formatting.add("B8:B28", FormulaRule(formula=['$B8=1'],
    fill=PatternFill("solid", fgColor=LIGHT_GOLD), font=Font(bold=True, color="92400E")))
gw.conditional_formatting.add("B8:B28", FormulaRule(formula=['$B8=2'],
    fill=PatternFill("solid", fgColor="E5E7EB"), font=Font(bold=True, color="374151")))
gw.conditional_formatting.add("B8:B28", FormulaRule(formula=['$B8=3'],
    fill=PatternFill("solid", fgColor="FED7AA"), font=Font(bold=True, color="9A3412")))
protect(gw)

# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------
s = wb.create_sheet("SETTINGS")
s.sheet_view.showGridLines = False
for col, w in {"A":4,"B":34,"C":16,"D":44,"E":14,"F":14,"G":3,"H":18}.items():
    s.column_dimensions[col].width = w

title(s, "SETTINGS — CONTROL PANEL", 1, 2, 5)

s.merge_cells("B2:E2")
s["B2"] = "Change the numbers below to update the whole league. Only gold cells are editable."
s["B2"].font = Font(size=12, italic=True, color=GREY)
s["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
s.row_dimensions[2].height = 26

section(s, "GAME RULES", 3, 2, 5)
for c, h in enumerate(["Setting", "Value", "Notes"], start=2):
    s.cell(4, c, h)
header_row(s, 4, 2, 5)

rules_values = [
    ("Baseline points (at avg)",     5,       "Points for scoring exactly the class average"),
    ("Dynamic step divisor",          10,      "Class range (max−min) ÷ this = step size"),
    ("Minimum points",                0,       "Floor"),
    ("Maximum points",                10,      "Ceiling"),
    ("Max weekly price change",       0.5,     "Absolute cap per week (£m)"),
    ("Tier multiplier (low)",         1.0,     "£7.0–8.9m price band multiplier"),
    ("Tier multiplier (mid)",         0.75,    "£9.0–10.9m price band multiplier"),
    ("Tier multiplier (high)",        0.5,     "£11.0–13.0m price band multiplier"),
    ("Price change step",             0.1,     "Ladder increment (£m)"),
    ("Minimum price",                 7.0,     "Floor (£m)"),
    ("Maximum price",                 13.0,    "Ceiling (£m)"),
    ("Price changes start at week",   3,       "First week that price changes apply"),
    ("Tests per gameweek",            2,       "How many test columns count this week (1-5)."),
    ("Captain multiplier",            2,       "Captain's points are multiplied by this."),
]
for i, (label, val, note) in enumerate(rules_values):
    r = 5 + i
    s.cell(r, 2, label)
    s.cell(r, 3, val)
    s.cell(r, 4, note)
    box(s.cell(r, 2), LIGHT_BLUE, True, DARK, "left")
    box(s.cell(r, 3), LIGHT_GOLD, True, NAVY, "center", unlocked=True)
    box(s.cell(r, 4), PALE_BLUE, False, GREY, "left", size=11, italic=True)
    s.row_dimensions[r].height = 26

# ---- PLAYER PRICES ----
s.merge_cells("B20:F20")
s["B20"] = "PLAYER PRICES"
s["B20"].font = Font(size=13, bold=True, color=WHITE)
s["B20"].fill = PatternFill("solid", fgColor=BLUE)
s["B20"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
s.row_dimensions[20].height = 32

for c, h in enumerate(["Player", "Base", "Cumulative", "Override", "Final"], start=2):
    s.cell(21, c, h)
s.cell(21, 8, "Dropdown Source")
header_row(s, 21, 2, 6)
s.cell(21, 8).font = Font(bold=True, color=WHITE, size=12)
s.cell(21, 8).fill = PatternFill("solid", fgColor=NAVY)
s.cell(21, 8).alignment = Alignment(horizontal="center", vertical="center")
s.cell(21, 8).border = Border(bottom=medium_blue)

for i in range(PLAYER_SLOTS):
    r = SET_PLAYER_START + i
    log_row = SET_LOG_START + i
    if i < len(players):
        name, base = players[i]
        s.cell(r, 2, name)
        s.cell(r, 3, base)
    # Cumulative from log row
    s.cell(r, 4, f'=IF(B{r}="","",SUM(C{log_row}:V{log_row}))')
    # Final price
    s.cell(r, 6, f'=IF(B{r}="","",IF(E{r}<>"",E{r},MIN(SETTINGS!$C$15,MAX(SETTINGS!$C$14,C{r}+D{r}))))')
    # Dropdown mirror
    s.cell(r, 8, f'=IF(B{r}="","",B{r})')
    fill = WHITE if i % 2 == 0 else PALE_BLUE
    box(s.cell(r, 2), fill, False, DARK, "left", unlocked=True)
    box(s.cell(r, 3), fill, False, DARK, "center", unlocked=True)
    box(s.cell(r, 4), fill, False, GREY, "center")
    box(s.cell(r, 5), LIGHT_GOLD, True, NAVY, "center", unlocked=True)
    box(s.cell(r, 6), LIGHT_BLUE, True, DARK, "center")
    box(s.cell(r, 8), PALE_BLUE, False, GREY, "center")
    s.cell(r, 3).number_format = '£0.0"m"'
    s.cell(r, 4).number_format = '+£0.0"m";-£0.0"m";—'
    s.cell(r, 5).number_format = '£0.0"m"'
    s.cell(r, 6).number_format = '£0.0"m"'
    s.row_dimensions[r].height = 26

# ---- WEEKLY PRICE LOG ----
s.merge_cells(f"B{SET_LOG_HEADER}:W{SET_LOG_HEADER}")
s.cell(SET_LOG_HEADER, 2, "WEEKLY PRICE LOG (auto-written by advance script)")
s.cell(SET_LOG_HEADER, 2).font = Font(size=13, bold=True, color=WHITE)
s.cell(SET_LOG_HEADER, 2).fill = PatternFill("solid", fgColor=BLUE)
s.cell(SET_LOG_HEADER, 2).alignment = Alignment(horizontal="left", vertical="center", indent=1)
s.row_dimensions[SET_LOG_HEADER].height = 32

s.cell(SET_LOG_COL_HEADER, 2, "Player")
for w in range(1, TOTAL_WEEKS + 1):
    s.cell(SET_LOG_COL_HEADER, 2 + w, f"GW{w}")
header_row(s, SET_LOG_COL_HEADER, 2, 2 + TOTAL_WEEKS)

for i in range(PLAYER_SLOTS):
    r = SET_LOG_START + i
    s.cell(r, 2, f'=IF(SETTINGS!B{SET_PLAYER_START + i}="","",SETTINGS!B{SET_PLAYER_START + i})')
    for w in range(1, TOTAL_WEEKS + 1):
        c = s.cell(r, 2 + w)
        c.number_format = '+£0.0"m";-£0.0"m";—'
    fill = WHITE if i % 2 == 0 else PALE_BLUE
    box(s.cell(r, 2), fill, False, DARK, "left")
    for w in range(1, TOTAL_WEEKS + 1):
        box(s.cell(r, 2 + w), fill, False, DARK, "center")
    s.row_dimensions[r].height = 24

# ---- SEASON CONFIG ----
s.merge_cells(f"B{SET_CONFIG_ROW}:D{SET_CONFIG_ROW}")
s.cell(SET_CONFIG_ROW, 2, "SEASON CONFIG")
s.cell(SET_CONFIG_ROW, 2).font = Font(size=13, bold=True, color=WHITE)
s.cell(SET_CONFIG_ROW, 2).fill = PatternFill("solid", fgColor=ORANGE)
s.cell(SET_CONFIG_ROW, 2).alignment = Alignment(horizontal="left", vertical="center", indent=1)
s.row_dimensions[SET_CONFIG_ROW].height = 32

s.cell(SET_CURRENTGW_ROW, 2, "Current GW")
s.cell(SET_CURRENTGW_ROW, 3, 1)
box(s.cell(SET_CURRENTGW_ROW, 2), LIGHT_BLUE, True, DARK, "left")
box(s.cell(SET_CURRENTGW_ROW, 3), LIGHT_GOLD, True, NAVY, "center")
s.row_dimensions[SET_CURRENTGW_ROW].height = 26

s.cell(SET_SEASONLEN_ROW, 2, "Season length (weeks)")
s.cell(SET_SEASONLEN_ROW, 3, TOTAL_WEEKS)
box(s.cell(SET_SEASONLEN_ROW, 2), LIGHT_BLUE, True, DARK, "left")
box(s.cell(SET_SEASONLEN_ROW, 3), LIGHT_GOLD, True, NAVY, "center")
s.row_dimensions[SET_SEASONLEN_ROW].height = 26

protect(s)

# ---------------------------------------------------------
# MASTER DATA (hidden)
# ---------------------------------------------------------
md = wb.create_sheet("MASTER DATA")
md.sheet_state = "hidden"
md["B1"]="Manager"; md["C1"]="P1"; md["D1"]="P2"; md["E1"]="P3"
md["F1"]="P4"; md["G1"]="P5"; md["H1"]="Captain"
header_row(md, 1, 2, 8)
for i, name in enumerate(managers):
    r = MGR_ROW_START + i
    md.cell(r, 2, name)
    for c_off, ref in enumerate(["C10","C11","C12","C13","C14"]):
        md.cell(r, 3 + c_off, f"='{name}'!{ref}")
    md.cell(r, 8, f"='{name}'!C5")
    box(md.cell(r, 2), WHITE, True, DARK, "left")
    for c in range(3, 9):
        box(md.cell(r, c), WHITE if i % 2 == 0 else PALE_BLUE, False, DARK, "left")
    md.row_dimensions[r].height = 26
protect(md)

# ---------------------------------------------------------
# RAW RESULTS (hidden) — empty for GW1
# ---------------------------------------------------------
raw = wb.create_sheet("RAW RESULTS")
raw.sheet_state = "hidden"
raw.cell(1, 2, "Manager")
for w in range(1, TOTAL_WEEKS + 1):
    raw.cell(1, 2 + w, f"GW{w}")
header_row(raw, 1, 2, 2 + TOTAL_WEEKS)
for i, name in enumerate(managers):
    r = MGR_ROW_START + i
    raw.cell(r, 2, name)
    for w in range(1, TOTAL_WEEKS + 1):
        raw.cell(r, 2 + w, None)
    box(raw.cell(r, 2), WHITE, True, DARK, "left")
    for w in range(1, TOTAL_WEEKS + 1):
        box(raw.cell(r, 2 + w), WHITE if i % 2 == 0 else PALE_BLUE, False, DARK, "center")
    raw.row_dimensions[r].height = 26
protect(raw)

# ---------------------------------------------------------
# POINTS HISTORY (hidden, new) — empty for GW1
# ---------------------------------------------------------
ph = wb.create_sheet("POINTS HISTORY")
ph.sheet_state = "hidden"
ph.cell(1, 2, "Manager")
for w in range(1, TOTAL_WEEKS + 1):
    ph.cell(1, 2 + w, f"GW{w}")
header_row(ph, 1, 2, 2 + TOTAL_WEEKS)
for i, name in enumerate(managers):
    r = MGR_ROW_START + i
    ph.cell(r, 2, name)
    for w in range(1, TOTAL_WEEKS + 1):
        ph.cell(r, 2 + w, None)
    box(ph.cell(r, 2), WHITE, True, DARK, "left")
    for w in range(1, TOTAL_WEEKS + 1):
        box(ph.cell(r, 2 + w), WHITE if i % 2 == 0 else PALE_BLUE, False, DARK, "center")
    ph.row_dimensions[r].height = 26
protect(ph)

# ---------------------------------------------------------
# CALCULATIONS (hidden)
# ---------------------------------------------------------
calc = wb.create_sheet("CALCULATIONS")
calc.sheet_state = "hidden"

calc["A1"]="Player"; calc["B1"]="Base"; calc["C1"]="Current"; calc["D1"]="Pts"
calc["K1"]="Manager"; calc["L1"]="P1"; calc["M1"]="P2"; calc["N1"]="P3"
calc["O1"]="P4"; calc["P1"]="P5"; calc["Q1"]="Captain"; calc["R1"]="Team Value"
calc["S1"]="Budget Left"; calc["T1"]="GW Score"; calc["U1"]="Status"
calc["V1"]="Tiebreak"; calc["W1"]="Overall"; calc["X1"]="OverallTB"

for i in range(PLAYER_SLOTS):
    r = CALC_PLAYER_START + i
    set_row = SET_PLAYER_START + i
    # Link directly to SETTINGS
    calc.cell(r, 1, f"=SETTINGS!B{set_row}")
    calc.cell(r, 2, f"=SETTINGS!C{set_row}")
    calc.cell(r, 3, f"=SETTINGS!F{set_row}")
    # Points formula (with blank guard)
    calc.cell(r, 4,
        f'=IF(A{r}="","",IFERROR(IF(INDEX(RawScores,MATCH(A{r},RawNames,0))="",0,'
        f'MAX(ScoreFloor,MIN(ScoreCap,'
        f'BaseScore+ROUNDDOWN((INDEX(RawScores,MATCH(A{r},RawNames,0))-AVERAGE(RawScores))/'
        f'MAX((MAX(RawScores)-MIN(RawScores))/ScoreStep,0.1),0)))),0))')

for i, name in enumerate(managers):
    r = CALC_MGR_START + i
    calc.cell(r, 11, name)
    for c_off, ref in enumerate(["C10","C11","C12","C13","C14"]):
        calc.cell(r, 12 + c_off, f"='{name}'!{ref}")
    calc.cell(r, 17, f"='{name}'!C5")
    calc.cell(r, 18, f"='{name}'!C17")
    calc.cell(r, 19, f"='{name}'!C18")
    calc.cell(r, 20,
        f'=IF($U{r}="VALID TEAM",'
        f'SUMPRODUCT(SUMIF($A${CALC_PLAYER_START}:$A${CALC_PLAYER_END},L{r}:P{r},$D${CALC_PLAYER_START}:$D${CALC_PLAYER_END}))'
        f'+SUMIF($A${CALC_PLAYER_START}:$A${CALC_PLAYER_END},Q{r},$D${CALC_PLAYER_START}:$D${CALC_PLAYER_END})*(CaptainMultiplier-1),0)')
    calc.cell(r, 21, f"='{name}'!C20")
    calc.cell(r, 22, f"=T{r}+ROW()/10000")
    calc.cell(r, 23, f"=SUM('POINTS HISTORY'!C{r}:V{r})")
    calc.cell(r, 24, f"=W{r}+ROW()/10000")

protect(calc)

# ---------------------------------------------------------
# TEAM SHEETS
# ---------------------------------------------------------
def build_team_sheet(name):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 32
    ws.column_dimensions["C"].width = 34
    ws.column_dimensions["D"].width = 20
    ws.column_dimensions["E"].width = 16
    title(ws, f"{name.upper()}'S TEAM", 1, 2, 4)

    ws.merge_cells("B2:D2")
    back = ws["B2"]
    back.value = "← Back to PICK YOUR TEAM"
    back.hyperlink = "#'PICK YOUR TEAM'!A1"
    back.font = Font(size=12, bold=True, color=BLUE, underline="single")
    back.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 30
    ws.row_dimensions[3].height = 12

    section(ws, "PICK YOUR CAPTAIN  (scores 2× points)", 4, 2, 4)
    ws["C5"] = ""
    box(ws["C5"], LIGHT_GOLD, True, NAVY, "left")
    ws["C5"].font = Font(size=13, bold=True, color=NAVY)
    ws["C5"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[5].height = 34

    ws.merge_cells("B6:D6")
    ws["B6"] = "Step 1: Pick 5 players.  Step 2: Choose your captain in the GOLD box above."
    ws["B6"].font = Font(size=11, italic=True, color=GREY)
    ws["B6"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[6].height = 24
    ws.row_dimensions[7].height = 12

    section(ws, "SQUAD", 8, 2, 4)
    for c, h in enumerate(["Slot", "Player", "Price", "Points"], start=2):
        ws.cell(9, c, h)
    header_row(ws, 9, 2, 5)

    preload = teams_data.get(name)
    for r in range(10, 15):
        slot = r - 9
        ws.cell(r, 2, slot)
        if preload and slot <= len(preload["p"]):
            ws.cell(r, 3, preload["p"][slot-1] if preload["p"][slot-1] else "")
        else:
            ws.cell(r, 3, "")
        ws.cell(r, 4, f'=IF(C{r}="","",IFERROR(INDEX(CALCULATIONS!$C$2:$C${CALC_PLAYER_END},MATCH(C{r},CALCULATIONS!$A$2:$A${CALC_PLAYER_END},0)),""))')
        ws.cell(r, 5, f'=IF(C{r}="","",IF(C{r}=$C$5,TEXT(IFERROR(INDEX(CALCULATIONS!$D$2:$D${CALC_PLAYER_END},MATCH(C{r},CALCULATIONS!$A$2:$A${CALC_PLAYER_END},0)),0)*2,"0")&" (×2)",TEXT(IFERROR(INDEX(CALCULATIONS!$D$2:$D${CALC_PLAYER_END},MATCH(C{r},CALCULATIONS!$A$2:$A${CALC_PLAYER_END},0)),0),"0")))')
        box(ws.cell(r, 2), PALE_BLUE, True, DARK, "center")
        box(ws.cell(r, 3), LIGHT_GOLD, False, DARK, "left")
        box(ws.cell(r, 4), WHITE, False, DARK, "center")
        box(ws.cell(r, 5), WHITE, False, DARK, "center")
        ws.row_dimensions[r].height = 32
    ws.row_dimensions[15].height = 12

    if preload and preload.get("c"):
        ws["C5"] = preload["c"]

    section(ws, "TEAM SUMMARY", 16, 2, 4)
    summary = [
        ("Team Value", "=SUM(D10:D14)"),
        ("Budget Left", "=50-C17"),
        ("GW Score",
         f'=IF($C$20="VALID TEAM",'
         f'SUMPRODUCT(SUMIF(CALCULATIONS!$A$2:$A${CALC_PLAYER_END},C10:C14,CALCULATIONS!$D$2:$D${CALC_PLAYER_END}))'
         f'+SUMIF(CALCULATIONS!$A$2:$A${CALC_PLAYER_END},C5,CALCULATIONS!$D$2:$D${CALC_PLAYER_END})*(CaptainMultiplier-1),0)'),
        ("Team Status",
         '=IF(COUNTBLANK(C10:C14)>0,"LESS THAN 5 PLAYERS",'
         'IF(SUM(D10:D14)>50,"OVER BUDGET",'
         'IF(C5="","NO CAPTAIN",'
         'IF(COUNTIF(C10:C14,C5)=0,"CAPTAIN NOT IN SQUAD",'
         'IF(SUMPRODUCT(COUNTIF(C10:C14,C10:C14))>5,"DUPLICATE PLAYER",'
         '"VALID TEAM")))))'),
    ]
    for i, (label, formula) in enumerate(summary):
        r = 17 + i
        ws.cell(r, 2, label)
        ws.cell(r, 3, formula)
        box(ws.cell(r, 2), LIGHT_BLUE, True, DARK, "left")
        box(ws.cell(r, 3), WHITE, True, DARK, "left")
        ws.row_dimensions[r].height = 30
    ws["C17"].number_format = '£0.0"m"'
    ws["C18"].number_format = '£0.0"m"'
    ws["C19"].number_format = '0'
    ws["C20"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.conditional_formatting.add("C20", FormulaRule(
        formula=['C20="VALID TEAM"'],
        fill=PatternFill("solid", fgColor=LIGHT_GREEN),
        font=Font(color=GREEN, bold=True)))
    ws.conditional_formatting.add("C20", FormulaRule(
        formula=['C20<>"VALID TEAM"'],
        fill=PatternFill("solid", fgColor=LIGHT_RED),
        font=Font(color=RED, bold=True)))
    ws.row_dimensions[21].height = 12

    ws.merge_cells("B22:D24")
    ws["B22"] = ("INPUT CELLS ARE GOLD.\n"
                 "Only the captain cell (C5) and the 5 player cells (C10:C14) should be edited.\n"
                 "Do NOT type 'CAPTAIN' anywhere in the squad.")
    ws["B22"].font = Font(bold=True, color=DARK, size=12)
    ws["B22"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    box(ws["B22"], LIGHT_GOLD)

    # Data validation: squad uses PlayerList (dynamic)
    dv = DataValidation(type="list", formula1="=PlayerList", allow_blank=True)
    dv.error = "Choose a player from the dropdown."
    dv.errorTitle = "Invalid player"
    dv.showErrorMessage = True
    ws.add_data_validation(dv)
    dv.add("C10:C14")

    # Captain validation: restricted to own picks
    dv_c = DataValidation(type="list", formula1=f"='{name}'!$C$10:$C$14", allow_blank=True)
    dv_c.error = "Choose one of your 5 players."
    dv_c.errorTitle = "Invalid captain"
    dv_c.showErrorMessage = True
    ws.add_data_validation(dv_c)
    dv_c.add("C5")

    # NOT protected — students edit their own teams
    return ws

for name in managers:
    build_team_sheet(name)

# ---------------------------------------------------------
# _DIAGNOSTICS (veryHidden)
# ---------------------------------------------------------
diag = wb.create_sheet("_DIAGNOSTICS")
diag.sheet_state = "veryHidden"
diag["B2"] = "DIAGNOSTICS"
diag["B2"].font = Font(size=16, bold=True, color=NAVY)
diag["B4"] = "This sheet is veryHidden. Used by scripts for logs / debug info."
diag["B4"].font = Font(size=11, italic=True, color=GREY)
protect(diag)

# =========================================================
# NAMED RANGES
# =========================================================
named = {
    "BaseScore":         f"SETTINGS!$C$5",
    "ScoreStep":         f"SETTINGS!$C$6",
    "ScoreFloor":        f"SETTINGS!$C$7",
    "ScoreCap":          f"SETTINGS!$C$8",
    "CaptainMultiplier": f"SETTINGS!$C$18",
    "CurrentGW":         f"SETTINGS!$C${SET_CURRENTGW_ROW}",
    "SeasonLength":      f"SETTINGS!$C${SET_SEASONLEN_ROW}",
    "PlayerList":        f"SETTINGS!$H${SET_PLAYER_START}:$H${SET_PLAYER_END}",
    "BasePoints":        f"OFFSET(SETTINGS!$C${SET_PLAYER_START},0,0,COUNTA(SETTINGS!$B${SET_PLAYER_START}:$B$200),1)",
    "PlayerNames":       f"OFFSET(CALCULATIONS!$A${CALC_PLAYER_START},0,0,COUNTA(SETTINGS!$B${SET_PLAYER_START}:$B$200),1)",
    "RawNames":          f"OFFSET('TEST RESULTS'!$B${TEST_START},0,0,COUNTA(SETTINGS!$B${SET_PLAYER_START}:$B$200),1)",
    "RawScores":         f"OFFSET('TEST RESULTS'!$H${TEST_START},0,0,COUNTA(SETTINGS!$B${SET_PLAYER_START}:$B$200),1)",
}
for nm, ref in named.items():
    wb.defined_names.add(DefinedName(nm, attr_text=ref))

# =========================================================
# TAB COLOURS
# =========================================================
tab_colours = {
    "HOME": BLUE, "PICK YOUR TEAM": "1D4ED8", "TEST RESULTS": GOLD,
    "PLAYER MARKET": "2563EB", " Overall Leaderboard": "0F766E",
    "GW Leaderboard": "0D9488", "RULES": SLATE, "SETTINGS": ORANGE,
    "CALCULATIONS": "64748B", "MASTER DATA": "94A3B8", "RAW RESULTS": "94A3B8",
    "POINTS HISTORY": "94A3B8", "_DIAGNOSTICS": "64748B",
}
for ws in wb.worksheets:
    if ws.title in tab_colours:
        ws.sheet_properties.tabColor = tab_colours[ws.title]
for name in managers:
    wb[name].sheet_properties.tabColor = SLATE
for ws in wb.worksheets:
    ws.sheet_view.zoomScale = 90

# =========================================================
# SHEET ORDER
# =========================================================
main_order = (
    ["HOME", "RULES", "PICK YOUR TEAM", "PLAYER MARKET", "TEST RESULTS",
     " Overall Leaderboard", "GW Leaderboard", "SETTINGS",
     "MASTER DATA", "RAW RESULTS", "CALCULATIONS"]
    + managers
    + ["POINTS HISTORY", "_DIAGNOSTICS"]
)
wb._sheets = [wb[t] for t in main_order]
wb.active = wb.index(wb["HOME"])

# =========================================================
# SAVE
# =========================================================
wb.save(SAVE_PATH)
print(f"Built: {SAVE_PATH}")
print(f"Managers: {len(managers)}  Players: {len(players)}  Slots: {PLAYER_SLOTS}")
print(f"Current GW: 1")
print(f"RAW RESULTS and POINTS HISTORY empty for GW1 — run advance_gameweek.py to archive.")