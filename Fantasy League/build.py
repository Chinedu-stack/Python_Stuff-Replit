from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

# =========================================================
# DATA
# =========================================================
players = [
    ("Lia Li", 13.0),
    ("Chinedu Chile", 11.0),
    ("Emily Warburton", 11.0),
    ("Sophie Barker", 11.0),
    ("Alyza Rai", 10.5),
    ("David Wu", 10.5),
    ("Joe Paige", 10.5),
    ("Azlan Husain", 10.0),
    ("Nina De Saram", 10.0),
    ("Alexa Amesimeku", 9.5),
    ("Daniel Liu", 9.5),
    ("Rebecca Seymour", 9.5),
    ("Edwin Mayers", 9.0),
    ("Melody Zhaeentan", 8.5),
    ("Esme Beston", 8.0),
    ("Iona Smith", 8.0),
    ("Oscar Day-Duran", 8.0),
    ("Alfie Foley", 7.5),
    ("Ava Swinfen", 7.0),
    ("Rory Bowman", 7.0),
    ("Xander Meijer", 7.0),
]

managers = sorted([p[0] for p in players])

# =========================================================
# THEME
# =========================================================
NAVY = "0B1F3A"
BLUE = "1565C0"
LIGHT_BLUE = "EAF2FF"
PALE_BLUE = "F5F9FF"
WHITE = "FFFFFF"
DARK = "172033"
GREY = "6B7280"
LIGHT_GREY = "E5E7EB"
GREEN = "16A34A"
LIGHT_GREEN = "DCFCE7"
RED = "DC2626"
LIGHT_RED = "FEE2E2"
GOLD = "F59E0B"
LIGHT_GOLD = "FEF3C7"
SLATE = "475569"
SLATE_DARK = "334155"

thin_grey = Side(style="thin", color=LIGHT_GREY)
medium_blue = Side(style="medium", color=BLUE)

# =========================================================
# HELPERS
# =========================================================
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

def box(cell, fill=WHITE, bold=False, color=DARK, align="left", size=12, italic=False):
    cell.fill = PatternFill("solid", fgColor=fill)
    cell.font = Font(bold=bold, color=color, size=size, italic=italic)
    cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=False)
    cell.border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)

# =========================================================
# WORKBOOK
# =========================================================
wb = Workbook()
wb.remove(wb.active)

# ---------------------------------------------------------
# CALCULATIONS (hidden engine)
# ---------------------------------------------------------
calc = wb.create_sheet("CALCULATIONS")
calc.sheet_state = "hidden"

calc["A1"] = "Player"
calc["B1"] = "Base Price"
calc["C1"] = "Current Price"
calc["D1"] = "Points"
calc["E1"] = "Δ"

for i, (name, price) in enumerate(players, start=2):
    calc.cell(i, 1, name)
    calc.cell(i, 2, price)
    calc.cell(i, 3, f"=MIN(13,MAX(6,B{i}+E{i}))")
    calc.cell(i, 4,
        f'=IFERROR(IF(\'TEST RESULTS\'!C{i}="",0,'
        f'IF(\'TEST RESULTS\'!C{i}>=90,10,'
        f'IF(\'TEST RESULTS\'!C{i}>=80,8,'
        f'IF(\'TEST RESULTS\'!C{i}>=70,6,'
        f'IF(\'TEST RESULTS\'!C{i}>=60,5,'
        f'IF(\'TEST RESULTS\'!C{i}>=50,3,'
        f'IF(\'TEST RESULTS\'!C{i}>=40,2,1))))))),0)')
    calc.cell(i, 5,
        f'=IF(D{i}=10,2,IF(D{i}=8,1.5,IF(D{i}=6,1,'
        f'IF(D{i}=5,0,IF(D{i}=3,-1,IF(D{i}=2,-1.5,'
        f'IF(D{i}=1,-2,0)))))))')

calc["K1"] = "Manager"
calc["L1"] = "P1"
calc["M1"] = "P2"
calc["N1"] = "P3"
calc["O1"] = "P4"
calc["P1"] = "P5"
calc["Q1"] = "Captain"
calc["R1"] = "Team Value"
calc["S1"] = "Budget Left"
calc["T1"] = "GW Score"
calc["U1"] = "Status"

for r, name in enumerate(managers, start=2):
    calc.cell(r, 11, name)
    for c_off, ref in enumerate(["C10", "C11", "C12", "C13", "C14"]):
        calc.cell(r, 12 + c_off, f"='{name}'!{ref}")
    calc.cell(r, 17, f"='{name}'!C5")
    calc.cell(r, 18, f"='{name}'!C17")
    calc.cell(r, 19, f"='{name}'!C18")
    calc.cell(r, 20, f"='{name}'!C19")
    calc.cell(r, 21, f"='{name}'!C20")

# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------
home = wb.create_sheet("HOME")
home.sheet_view.showGridLines = False
for col, w in {"A": 4, "B": 28, "C": 26, "D": 26, "E": 26, "F": 26, "G": 26, "H": 4}.items():
    home.column_dimensions[col].width = w

title(home, "YEAR 11 FANTASY LEAGUE", 1, 2, 7)

home.merge_cells("B2:G2")
home["B2"] = "GAMEWEEK 1  •  BIOLOGY"
home["B2"].font = Font(size=16, bold=True, color=BLUE)
home["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
home.row_dimensions[2].height = 32

home.merge_cells("B3:G3")
home.row_dimensions[3].height = 12

home.merge_cells("B4:G4")
home["B4"] = "DEADLINE  •  27 SEPTEMBER 2026  •  11:59 PM"
home["B4"].font = Font(size=13, bold=True, color=DARK)
home["B4"].fill = PatternFill("solid", fgColor=LIGHT_BLUE)
home["B4"].alignment = Alignment(horizontal="center", vertical="center")
home.row_dimensions[4].height = 34

home.merge_cells("B5:G5")
home["B5"] = "TEST DATE  •  28 SEPTEMBER 2026"
home["B5"].font = Font(size=13, bold=True, color=DARK)
home["B5"].fill = PatternFill("solid", fgColor=LIGHT_BLUE)
home["B5"].alignment = Alignment(horizontal="center", vertical="center")
home.row_dimensions[5].height = 34

home.merge_cells("B6:G6")
home.row_dimensions[6].height = 12

home["B7"] = "CURRENT GAMEWEEK:"
home["B7"].font = Font(size=12, bold=True, color=GREY)
home["B7"].alignment = Alignment(horizontal="right", vertical="center")
home["C7"] = 1
home["C7"].font = Font(size=14, bold=True, color=NAVY)
home["C7"].fill = PatternFill("solid", fgColor=LIGHT_GOLD)
home["C7"].alignment = Alignment(horizontal="center", vertical="center")
home["C7"].border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
home.row_dimensions[7].height = 30

home.merge_cells("B8:G8")
home.row_dimensions[8].height = 12

section(home, "HOW TO PLAY", 9, 2, 7)
steps = [
    "1.  Click PICK YOUR TEAM at the top of the workbook.",
    "2.  Click your name to jump to your team sheet.",
    "3.  Pick 5 players from the dropdowns.",
    "4.  Pick 1 captain — your captain scores double points.",
    "5.  Enter your own Biology % on TEST RESULTS.",
]
for i, text in enumerate(steps):
    r = 10 + i
    home.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
    c = home.cell(r, 2, text)
    box(c, PALE_BLUE)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    home.row_dimensions[r].height = 30

home.merge_cells("B16:G16")
home.row_dimensions[16].height = 12

section(home, "THE GOLDEN RULE", 17, 2, 7)
home.merge_cells("B18:G18")
home["B18"] = "YOU ONLY NEED TO:"
home["B18"].font = Font(size=16, bold=True, color=NAVY)
home["B18"].alignment = Alignment(horizontal="center", vertical="center")
home.row_dimensions[18].height = 32

golden = ["✓  Pick 5 players", "✓  Pick a captain", "✓  Enter your test result"]
for i, text in enumerate(golden):
    r = 19 + i
    home.merge_cells(start_row=r, start_column=2, end_row=r, end_column=7)
    c = home.cell(r, 2, text)
    box(c, LIGHT_GREEN, True, GREEN, "center")
    home.row_dimensions[r].height = 30

home.merge_cells("B23:G24")
home["B23"] = ("EXCEL DOES EVERYTHING ELSE.\n"
               "Points  •  Captain bonus  •  Scores  •  Leaderboard  •  Ownership  •  Prices")
home["B23"].font = Font(size=13, bold=True, color=WHITE)
home["B23"].fill = PatternFill("solid", fgColor=NAVY)
home["B23"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
home.row_dimensions[23].height = 30
home.row_dimensions[24].height = 30

# ---------------------------------------------------------
# PICK YOUR TEAM (menu)
# ---------------------------------------------------------
menu = wb.create_sheet("PICK YOUR TEAM")
menu.sheet_view.showGridLines = False
menu.column_dimensions["A"].width = 6
menu.column_dimensions["B"].width = 32
menu.column_dimensions["C"].width = 26
menu.column_dimensions["D"].width = 20

title(menu, "PICK YOUR TEAM", 1, 2, 4)

menu.merge_cells("B2:D2")
menu["B2"] = "Click your name to jump to your team sheet."
menu["B2"].font = Font(size=12, italic=True, color=GREY)
menu["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
menu.row_dimensions[2].height = 30

menu.merge_cells("B3:D3")
menu.row_dimensions[3].height = 12

menu["B4"] = "Manager"
menu["C4"] = "Status"
menu["D4"] = "GW Score"
header_row(menu, 4, 2, 4)

for i, name in enumerate(managers):
    r = 5 + i
    c = menu.cell(r, 2, name)
    c.hyperlink = f"#'{name}'!A1"
    c.font = Font(bold=True, color=BLUE, underline="single", size=12)
    box(c, WHITE, True, BLUE)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    calc_row = 2 + i
    menu.cell(r, 3, f"=CALCULATIONS!U{calc_row}")
    menu.cell(r, 4, f"=CALCULATIONS!T{calc_row}")
    box(menu.cell(r, 3), PALE_BLUE, align="center")
    box(menu.cell(r, 4), PALE_BLUE, align="center")
    menu.row_dimensions[r].height = 30

# ---------------------------------------------------------
# TEAM SHEETS
# ---------------------------------------------------------
def build_team_sheet(name):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 32
    ws.column_dimensions["C"].width = 30
    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 18
    ws.column_dimensions["F"].width = 16
    ws.column_dimensions["G"].width = 4

    title(ws, f"{name.upper()}'S TEAM", 1, 2, 6)

    ws.merge_cells("B2:F2")
    back = ws["B2"]
    back.value = "← Back to PICK YOUR TEAM"
    back.hyperlink = "#'PICK YOUR TEAM'!A1"
    back.font = Font(size=12, bold=True, color=BLUE, underline="single")
    back.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 30

    ws.row_dimensions[3].height = 12

    section(ws, "PICK YOUR CAPTAIN  (scores 2× points)", 4, 2, 6)
    ws["C5"] = ""
    box(ws["C5"], LIGHT_GOLD, True, DARK, "left")
    ws["C5"].font = Font(size=13, bold=True, color=NAVY)
    ws["C5"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[5].height = 34

    ws.merge_cells("B6:F6")
    ws["B6"] = "Tip: pick your 5 players below first, then choose your captain."
    ws["B6"].font = Font(size=11, italic=True, color=GREY)
    ws["B6"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[6].height = 24

    ws.row_dimensions[7].height = 12

    section(ws, "SQUAD", 8, 2, 6)
    for c, h in enumerate(["Slot", "Player", "Price", "Captain?"], start=2):
        ws.cell(9, c, h)
    header_row(ws, 9, 2, 5)

    for r in range(10, 15):
        slot = r - 9
        ws.cell(r, 2, slot)
        ws.cell(r, 3, "")
        ws.cell(r, 4, f'=IF(C{r}="","",IFERROR(VLOOKUP(C{r},\'CALCULATIONS\'!$A$2:$C$22,3,FALSE),""))')
        ws.cell(r, 5, f'=IF(C{r}="","",IF($C$5=C{r},"★ CAPTAIN",""))')
        box(ws.cell(r, 2), PALE_BLUE, True, DARK, "center")
        box(ws.cell(r, 3), LIGHT_GOLD, False, DARK, "left")
        box(ws.cell(r, 4), WHITE, False, DARK, "center")
        box(ws.cell(r, 5), WHITE, True, GOLD, "center")
        ws.row_dimensions[r].height = 32

    ws.row_dimensions[15].height = 12

    section(ws, "TEAM SUMMARY", 16, 2, 6)
    summary = [
        ("Team Value",   "=SUM(D10:D14)"),
        ("Budget Left",  "=50-C17"),
        ("GW Score",
         '=IF($C$20="VALID TEAM",'
         'SUMIF(\'CALCULATIONS\'!$A$2:$A$22,C10:C14,\'CALCULATIONS\'!$D$2:$D$22)'
         '+SUMIF(\'CALCULATIONS\'!$A$2:$A$22,C5,\'CALCULATIONS\'!$D$2:$D$22),0)'),
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

    ws.merge_cells("B22:F24")
    ws["B22"] = ("INPUT CELLS ARE GOLD.\n"
                 "Only the captain cell (C5) and the 5 player cells (C10:C14) should be edited.\n"
                 "Everything else is calculated automatically.")
    ws["B22"].font = Font(bold=True, color=DARK, size=12)
    ws["B22"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    box(ws["B22"], LIGHT_GOLD)

    ws.row_dimensions[25].height = 12

    section(ws, "EXAMPLE  (do not edit — for reference only)", 26, 2, 6, fill=SLATE)

    for c, h in enumerate(["Slot", "Player", "Price", "Captain?"], start=2):
        ws.cell(27, c, h)
    header_row(ws, 27, 2, 5, fill=SLATE_DARK)

    example = [
        (1, "Chinedu Chile",   "£11.0m", ""),
        (2, "Emily Warburton", "£11.0m", "★ CAPTAIN"),
        (3, "Joe Paige",       "£10.5m", ""),
        (4, "Edwin Mayers",    "£9.0m",  ""),
        (5, "Alfie Foley",     "£7.5m",  ""),
    ]
    for i, (slot, p, price, cap) in enumerate(example):
        r = 28 + i
        ws.cell(r, 2, slot)
        ws.cell(r, 3, p)
        ws.cell(r, 4, price)
        ws.cell(r, 5, cap)
        box(ws.cell(r, 2), PALE_BLUE, True, DARK, "center")
        box(ws.cell(r, 3), WHITE, False, DARK, "left")
        box(ws.cell(r, 4), WHITE, False, DARK, "center")
        box(ws.cell(r, 5), WHITE, True, GOLD, "center")
        ws.row_dimensions[r].height = 28

    ws.cell(33, 2, "CAPTAIN")
    box(ws.cell(33, 2), LIGHT_BLUE, True, DARK, "left")
    ws.merge_cells("C33:F33")
    ws.cell(33, 3, "Emily Warburton")
    box(ws.cell(33, 3), WHITE, True, DARK, "left")
    ws.row_dimensions[33].height = 28

    ws.cell(34, 2, "TEAM VALUE")
    box(ws.cell(34, 2), LIGHT_BLUE, True, DARK, "left")
    ws.merge_cells("C34:F34")
    ws.cell(34, 3, "£49.0m     BUDGET LEFT  £1.0m")
    box(ws.cell(34, 3), WHITE, True, DARK, "left")
    ws.row_dimensions[34].height = 28

    ws.cell(35, 2, "STATUS")
    box(ws.cell(35, 2), LIGHT_BLUE, True, DARK, "left")
    ws.merge_cells("C35:F35")
    ws.cell(35, 3, "✓ VALID TEAM")
    box(ws.cell(35, 3), LIGHT_GREEN, True, GREEN, "left")
    ws.row_dimensions[35].height = 28

    dv_players = DataValidation(
        type="list",
        formula1="=CALCULATIONS!$A$2:$A$22",
        allow_blank=True,
    )
    dv_players.error = "Please choose a player from the dropdown list."
    dv_players.errorTitle = "Invalid player"
    dv_players.prompt = "Click the arrow to choose a player."
    dv_players.promptTitle = "Pick a player"
    dv_players.showErrorMessage = True
    dv_players.showInputMessage = True
    ws.add_data_validation(dv_players)
    dv_players.add("C10:C14")

    dv_captain = DataValidation(
        type="list",
        formula1=f"='{name}'!$C$10:$C$14",
        allow_blank=True,
    )
    dv_captain.error = "Choose one of your 5 players."
    dv_captain.errorTitle = "Invalid captain"
    dv_captain.prompt = "Pick your captain from your 5 players."
    dv_captain.promptTitle = "Pick a captain"
    dv_captain.showErrorMessage = True
    dv_captain.showInputMessage = True
    ws.add_data_validation(dv_captain)
    dv_captain.add("C5")

    return ws

for name in managers:
    build_team_sheet(name)

# ---------------------------------------------------------
# TEST RESULTS
# ---------------------------------------------------------
results = wb.create_sheet("TEST RESULTS")
results.sheet_view.showGridLines = False
results.column_dimensions["A"].width = 4
results.column_dimensions["B"].width = 32
results.column_dimensions["C"].width = 42

title(results, "TEST RESULTS", 1, 2, 3)

results.merge_cells("B2:C2")
results["B2"] = "BIOLOGY  •  GAMEWEEK 1  •  Test on 28 September 2026"
results["B2"].font = Font(size=12, bold=True, color=BLUE)
results["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
results.row_dimensions[2].height = 30

results.merge_cells("B3:C3")
results.row_dimensions[3].height = 12

results["B4"] = "Student"
results["C4"] = "Biology %  —  type 90, not 90%"
header_row(results, 4, 2, 3)

for i, name in enumerate(managers):
    r = 5 + i
    results.cell(r, 2, name)
    results.cell(r, 3, "")
    box(results.cell(r, 2), WHITE, False, DARK, "left")
    box(results.cell(r, 3), LIGHT_GOLD, False, DARK, "center")
    results.cell(r, 3).number_format = '0"%"'
    results.row_dimensions[r].height = 30

dv_pct = DataValidation(
    type="whole", operator="between",
    formula1="0", formula2="100",
    allow_blank=True,
)
dv_pct.error = "Enter a whole number from 0 to 100."
dv_pct.errorTitle = "Invalid percentage"
dv_pct.showErrorMessage = True
results.add_data_validation(dv_pct)
dv_pct.add("C5:C25")

results.merge_cells("B28:C30")
results["B28"] = ("Enter a whole number between 0 and 100.\n"
                  "Do NOT type the % sign — just the number. Example: 90")
results["B28"].font = Font(bold=True, color=DARK, size=12)
results["B28"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
box(results["B28"], LIGHT_GOLD)

# ---------------------------------------------------------
# PLAYER MARKET
# ---------------------------------------------------------
market = wb.create_sheet("PLAYER MARKET")
market.sheet_view.showGridLines = False
market.column_dimensions["A"].width = 4
market.column_dimensions["B"].width = 32
market.column_dimensions["C"].width = 18
market.column_dimensions["D"].width = 20

title(market, "PLAYER MARKET", 1, 2, 4)

market.merge_cells("B2:D2")
market["B2"] = "Prices  •  Ownership"
market["B2"].font = Font(size=12, color=GREY, italic=True)
market["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
market.row_dimensions[2].height = 30

market.merge_cells("B3:D3")
market.row_dimensions[3].height = 12

for c, h in enumerate(["Player", "Price", "Ownership %"], start=2):
    market.cell(4, c, h)
header_row(market, 4, 2, 4)

for i, idx in enumerate(range(2, 23)):
    r = 5 + i
    market.cell(r, 2, f"=CALCULATIONS!A{idx}")
    market.cell(r, 3, f"=CALCULATIONS!C{idx}")
    market.cell(r, 4, f"=COUNTIF('CALCULATIONS'!$L$2:$P$22,B{r})/COUNTA('CALCULATIONS'!$K$2:$K$22)")
    box(market.cell(r, 2), WHITE if i % 2 == 0 else PALE_BLUE, False, DARK, "left")
    box(market.cell(r, 3), WHITE if i % 2 == 0 else PALE_BLUE, True, DARK, "center")
    box(market.cell(r, 4), WHITE if i % 2 == 0 else PALE_BLUE, False, DARK, "center")
    market.cell(r, 3).number_format = '£0.0"m"'
    market.cell(r, 4).number_format = '0%'
    market.row_dimensions[r].height = 28

market.merge_cells("B28:D30")
market["B28"] = ("PRICE RULES\n"
                 "Prices move after each Gameweek in £0.5m steps, from -£2.0m to +£2.0m.\n"
                 "Minimum £6.0m  •  Maximum £13.0m")
market["B28"].font = Font(bold=True, color=DARK, size=12)
market["B28"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
box(market["B28"], LIGHT_BLUE)

# ---------------------------------------------------------
# LEADERBOARD
# ---------------------------------------------------------
lb = wb.create_sheet("LEADERBOARD")
lb.sheet_view.showGridLines = False
lb.column_dimensions["A"].width = 4
lb.column_dimensions["B"].width = 12
lb.column_dimensions["C"].width = 32
lb.column_dimensions["D"].width = 14
lb.column_dimensions["E"].width = 14

title(lb, "LEADERBOARD", 1, 2, 5)

lb.merge_cells("B2:E2")
lb["B2"] = "Season so far"
lb["B2"].font = Font(size=12, color=GREY, italic=True)
lb["B2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
lb.row_dimensions[2].height = 30

lb.merge_cells("B3:E3")
lb.row_dimensions[3].height = 12

for c, h in enumerate(["Rank", "Manager", "GW1", "Overall"], start=2):
    lb.cell(4, c, h)
header_row(lb, 4, 2, 5)

for i, name in enumerate(managers):
    r = 5 + i
    calc_row = 2 + i
    lb.cell(r, 2, f"=RANK(E{r},$E$5:$E$25,0)")
    lb.cell(r, 3, f"=CALCULATIONS!K{calc_row}")
    lb.cell(r, 4, f"=CALCULATIONS!T{calc_row}")
    lb.cell(r, 5, f"=D{r}")
    box(lb.cell(r, 2), WHITE if i % 2 == 0 else PALE_BLUE, True, DARK, "center")
    box(lb.cell(r, 3), WHITE if i % 2 == 0 else PALE_BLUE, False, DARK, "left")
    box(lb.cell(r, 4), WHITE if i % 2 == 0 else PALE_BLUE, False, DARK, "center")
    box(lb.cell(r, 5), WHITE if i % 2 == 0 else PALE_BLUE, True, DARK, "center")
    lb.row_dimensions[r].height = 30

lb.conditional_formatting.add("B5:B25", FormulaRule(
    formula=['$B5=1'],
    fill=PatternFill("solid", fgColor="FEF3C7"),
    font=Font(bold=True, color="92400E")))
lb.conditional_formatting.add("B5:B25", FormulaRule(
    formula=['$B5=2'],
    fill=PatternFill("solid", fgColor="E5E7EB"),
    font=Font(bold=True, color="374151")))
lb.conditional_formatting.add("B5:B25", FormulaRule(
    formula=['$B5=3'],
    fill=PatternFill("solid", fgColor="FED7AA"),
    font=Font(bold=True, color="9A3412")))
section(lb, "AWARDS", 28, 2, 5)

awards = [
    ("🏆 Highest Scorer",
     '=INDEX(C5:C25,MATCH(MAX(E5:E25),E5:E25,0))'),
    ("📈 Most Improved Player",
     "Coming after Gameweek 2"),
    ("🔥 Most Selected Player",
     "=INDEX('PLAYER MARKET'!B5:B25,MATCH(MAX('PLAYER MARKET'!D5:D25),'PLAYER MARKET'!D5:D25,0))"),
    ("🎯 Best Captain Pick",
     "Coming after Gameweek 1 scoring is fully entered"),
    ("💎 Best Value Player",
     "=INDEX('PLAYER MARKET'!B5:B25,MATCH(MAX('PLAYER MARKET'!C5:C25),'PLAYER MARKET'!C5:C25,0))"),
]

for i, (label, formula) in enumerate(awards):
    r = 29 + i
    lb.cell(r, 2, label)
    lb.merge_cells(start_row=r, start_column=3, end_row=r, end_column=5)
    lb.cell(r, 3, formula)
    box(lb.cell(r, 2), LIGHT_BLUE, True, DARK, "left")
    box(lb.cell(r, 3), WHITE, True, DARK, "left")
    lb.row_dimensions[r].height = 32

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
    ("BUDGET",
     "£50.0m per manager. Pick exactly 5 players. Squad value cannot exceed £50.0m."),
    ("CAPTAIN",
     "Choose 1 captain. The captain scores 2× their normal Gameweek points."),
    ("DEADLINE",
     "Gameweek 1 deadline: 27 September 2026 at 11:59 PM."),
    ("TEST DATE",
     "Biology test: 28 September 2026."),
    ("RESULT ENTRY",
     "After the test, each student enters only their own percentage on TEST RESULTS."),
    ("POINTS",
     "90–100 = 10 • 80–89 = 8 • 70–79 = 6 • 60–69 = 5 • 50–59 = 3 • 40–49 = 2 • Below 40 = 1."),
    ("PRICE CHANGES",
     "Prices update after each Gameweek. 10 → +£2.0m • 8 → +£1.5m • 6 → +£1.0m • 5 → £0 • 3 → -£1.0m • 2 → -£1.5m • 1 → -£2.0m."),
    ("PRICE LIMITS",
     "Minimum £6.0m. Maximum £13.0m. Prices move only in £0.5m increments."),
    ("TRANSFERS",
     "After every Gameweek: unlimited transfers, free transfers, no penalties, captains can change."),
    ("TRANSFER DEADLINE",
     "The transfer window closes at the next Gameweek deadline."),
    ("GOLDEN RULE",
     "Users only need to pick 5 players, pick a captain and enter their own test result. Excel handles the rest."),
]

for i, (topic, explanation) in enumerate(rule_rows):
    r = 4 + (i * 2)
    rules.cell(r, 2, topic)
    rules.cell(r, 3, explanation)
    box(rules.cell(r, 2), LIGHT_BLUE, True, DARK, "left")
    box(rules.cell(r, 3), WHITE, False, DARK, "left")
    rules.cell(r, 3).alignment = Alignment(
        horizontal="left", vertical="center", wrap_text=True, indent=1)
    rules.row_dimensions[r].height = 40
    rules.row_dimensions[r + 1].height = 8

# ---------------------------------------------------------
# TAB COLOURS
# ---------------------------------------------------------
tab_colours = {
    "HOME": BLUE,
    "PICK YOUR TEAM": "1D4ED8",
    "TEST RESULTS": GOLD,
    "PLAYER MARKET": "2563EB",
    "LEADERBOARD": "0F766E",
    "RULES": SLATE,
    "CALCULATIONS": "64748B",
}
for ws in wb.worksheets:
    if ws.title in tab_colours:
        ws.sheet_properties.tabColor = tab_colours[ws.title]

for name in managers:
    wb[name].sheet_properties.tabColor = SLATE

# ---------------------------------------------------------
# ZOOM
# ---------------------------------------------------------
for ws in wb.worksheets:
    ws.sheet_view.zoomScale = 90

# ---------------------------------------------------------
# TAB ORDER + ACTIVE SHEET
# ---------------------------------------------------------
main_order = ["HOME", "PICK YOUR TEAM", "TEST RESULTS",
              "PLAYER MARKET", "LEADERBOARD", "RULES"]
ordered = main_order + managers + ["CALCULATIONS"]
wb._sheets = [wb[t] for t in ordered]

wb.active = wb.index(wb["HOME"])

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------
path = "Fantasy League/Year_11_Fantasy_League.xlsx"
wb.save(path)
print(f"Built: {path}")
print(f"Managers: {len(managers)}")
print(f"Players: {len(players)}")