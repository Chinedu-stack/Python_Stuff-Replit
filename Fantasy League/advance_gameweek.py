from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import PatternFill, Font, Border, Side, Alignment

# =========================================================
# CONFIG
# =========================================================
FILE = "Fantasy League/Year_11_Fantasy_League.xlsx"

WHITE = "FFFFFF"
PALE_BLUE = "F5F9FF"
DARK = "172033"
LIGHT_GREY = "E5E7EB"
thin_grey = Side(style="thin", color=LIGHT_GREY)

def box_cell(cell, fill=WHITE, bold=False, color=DARK, align="center"):
    cell.fill = PatternFill("solid", fgColor=fill)
    cell.font = Font(bold=bold, color=color, size=12)
    cell.alignment = Alignment(horizontal=align, vertical="center")
    cell.border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)

# =========================================================
# LOAD  (two passes: values-cache + normal)
# =========================================================
wb_values = load_workbook(FILE, data_only=True)
wb = load_workbook(FILE)

home = wb["HOME"]
current_gw = home["C7"].value

if current_gw is None:
    print("ERROR: HOME!C7 is empty. Can't determine current gameweek.")
    raise SystemExit(1)

next_gw = current_gw + 1

print(f"Loaded: {FILE}")
print(f"Current gameweek: {current_gw}")
print(f"Advancing to: {next_gw}")
print()

# ---------------------------------------------------------
# GUARD: make sure Excel has cached values
# ---------------------------------------------------------
# If the file was never opened/saved in Excel, data_only gives None everywhere.
probe = wb_values["CALCULATIONS"]["D2"].value
if probe is None:
    print("WARNING: No cached values found in the workbook.")
    print("         Open the file in Excel, save it (Ctrl+S), close it,")
    print("         then re-run this script.")
    print("         Aborting so we don't corrupt history.")
    raise SystemExit(1)

# =========================================================
# 1. FREEZE TEST RESULTS  (C -> growing column D, E, F ...)
# =========================================================
results = wb["TEST RESULTS"]
results_v = wb_values["TEST RESULTS"]

# GW1 → D=4, GW2 → E=5, ...
freeze_col = 3 + current_gw
freeze_letter = get_column_letter(freeze_col)

# Grab the live header format from C4 BEFORE writing
src_cell = results.cell(4, 3)
src_font = src_cell.font.copy()
src_fill = src_cell.fill.copy()
src_align = src_cell.alignment.copy()
src_border = src_cell.border.copy()

# Freeze values from the cached pass
for r in range(5, 26):
    results.cell(r, freeze_col).value = results_v.cell(r, 3).value

# Header for the frozen column
hdr = results.cell(4, freeze_col)
hdr.value = f"GW{current_gw} Bio %"
hdr.font = src_font
hdr.fill = src_fill
hdr.alignment = src_align
hdr.border = src_border

# Reset live header for next GW
results.cell(4, 3).value = f"Biology %  —  GW{next_gw}  —  type 90, not 90%"

# Clear live input column C for the next gameweek
for r in range(5, 26):
    results.cell(r, 3).value = None

print(f"  TEST RESULTS: GW{current_gw} frozen in column {freeze_letter}, column C cleared.")

# =========================================================
# 2. FREEZE POINTS AND PRICE CHANGES IN CALCULATIONS
# =========================================================
# Layout: F=GW1 Δ, G=GW1 Pts, H=GW2 Δ, I=GW2 Pts, ...
calc = wb["CALCULATIONS"]
calc_v = wb_values["CALCULATIONS"]

freeze_offset = current_gw - 1
delta_col = 6 + (freeze_offset * 2)      # F=6, H=8, J=10...
points_col = delta_col + 1               # G=7, I=9, K=11...

# Copy header formatting from E1 (Δ) for the Δ freeze, D1 (Points) for the Pts freeze
delta_hdr_src = calc.cell(1, 5)
pts_hdr_src = calc.cell(1, 4)
delta_hdr_font = delta_hdr_src.font.copy()
delta_hdr_fill = delta_hdr_src.fill.copy()
delta_hdr_align = delta_hdr_src.alignment.copy()
delta_hdr_border = delta_hdr_src.border.copy()
pts_hdr_font = pts_hdr_src.font.copy()
pts_hdr_fill = pts_hdr_src.fill.copy()
pts_hdr_align = pts_hdr_src.alignment.copy()
pts_hdr_border = pts_hdr_src.border.copy()

# Write frozen values (from the cached pass)
for r in range(2, 23):
    calc.cell(r, delta_col).value = calc_v.cell(r, 5).value     # frozen Δ
    calc.cell(r, points_col).value = calc_v.cell(r, 4).value    # frozen Pts

# Headers
dh = calc.cell(1, delta_col)
dh.value = f"GW{current_gw} Δ"
dh.font = delta_hdr_font
dh.fill = delta_hdr_fill
dh.alignment = delta_hdr_align
dh.border = delta_hdr_border

ph = calc.cell(1, points_col)
ph.value = f"GW{current_gw} Pts"
ph.font = pts_hdr_font
ph.fill = pts_hdr_fill
ph.alignment = pts_hdr_align
ph.border = pts_hdr_border

print(f"  CALCULATIONS: GW{current_gw} points frozen in "
      f"{get_column_letter(points_col)}, price Δ in {get_column_letter(delta_col)}.")

# =========================================================
# 3. REBUILD CURRENT PRICE FORMULA
# =========================================================
# Current Price = MIN(13, MAX(6, Base + sum of all frozen Δs))
delta_cols = []
for gw in range(1, current_gw + 1):
    off = gw - 1
    delta_cols.append(get_column_letter(6 + off * 2))  # F, H, J ...

for r in range(2, 23):
    delta_sum = "+".join(f"{c}{r}" for c in delta_cols)
    calc.cell(r, 3).value = f"=MIN(13,MAX(6,B{r}+{delta_sum}))"

print(f"  CALCULATIONS: Current Price formula rebuilt (Base + {'+'.join(delta_cols)}).")

# =========================================================
# 4. UPDATE LEADERBOARD
# =========================================================
# Before: B=Rank, C=Manager, D=GW(current), E=Overall
# After : B=Rank, C=Manager, D=GW(current), E=GW(next), F=Overall
#
# Steps:
#   a) Freeze D (current GW live scores) as values
#   b) Insert a new column at E
#   c) Write GW{next_gw} header + formulas into E
#   d) Rename old Overall (now F) → Overall, rebuild SUM(D:E)
#   e) Rebuild Rank to use F

lb = wb["LEADERBOARD"]
lb_v = wb_values["LEADERBOARD"]

# (a) Freeze current GW column D as literal values from cache
for r in range(5, 26):
    lb.cell(r, 4).value = lb_v.cell(r, 4).value

# Grab header format from D4 for reuse
hdr_src = lb.cell(4, 4)
hdr_font = hdr_src.font.copy()
hdr_fill = hdr_src.fill.copy()
hdr_align = hdr_src.alignment.copy()
hdr_border = hdr_src.border.copy()

# (b) Insert new column at position E
lb.insert_cols(5)

# (c) New GW{next_gw} column (E)
new_hdr = lb.cell(4, 5)
new_hdr.value = f"GW{next_gw}"
new_hdr.font = hdr_font
new_hdr.fill = hdr_fill
new_hdr.alignment = hdr_align
new_hdr.border = hdr_border

for i in range(21):
    r = 5 + i
    calc_row = 2 + i
    lb.cell(r, 5).value = f"=CALCULATIONS!T{calc_row}"

# (d) Overall is now column F
overall_col = 6
ovr_hdr = lb.cell(4, overall_col)
ovr_hdr.value = "Overall"
ovr_hdr.font = hdr_font
ovr_hdr.fill = hdr_fill
ovr_hdr.alignment = hdr_align
ovr_hdr.border = hdr_border

for r in range(5, 26):
    lb.cell(r, overall_col).value = f"=SUM(D{r}:E{r})"

# (e) Rebuild Rank to use Overall (F)
for r in range(5, 26):
    lb.cell(r, 2).value = f"=RANK(F{r},$F$5:$F$25,0)"

# Re-apply box styling to new GW + Overall columns
for i in range(21):
    r = 5 + i
    fill = WHITE if i % 2 == 0 else PALE_BLUE
    box_cell(lb.cell(r, 5), fill, False, DARK, "center")   # new GW
    box_cell(lb.cell(r, 6), fill, True,  DARK, "center")   # Overall

# Also widen the columns slightly (E, F)
lb.column_dimensions["E"].width = 14
lb.column_dimensions["F"].width = 14

print(f"  LEADERBOARD: GW{current_gw} frozen, GW{next_gw} column added, Overall + Rank rebuilt.")

# =========================================================
# 5. CLEAR TEAM INPUTS  (derive manager list from PICK YOUR TEAM)
# =========================================================
menu = wb["PICK YOUR TEAM"]
manager_names = []
for r in range(5, 26):
    v = menu.cell(r, 2).value
    if v:
        manager_names.append(v)

for name in manager_names:
    if name not in wb.sheetnames:
        continue
    ws = wb[name]
    ws["C5"].value = None
    for r in range(10, 15):
        ws.cell(r, 3).value = None

print(f"  Cleared {len(manager_names)} team sheets.")

# =========================================================
# 6. UPDATE HEADERS / GAMEWEEK NUMBER
# =========================================================
home["C7"].value = next_gw
home["B2"].value = f"GAMEWEEK {next_gw}  •  BIOLOGY"

# TEST RESULTS subtitle
results["B2"].value = f"BIOLOGY  •  GAMEWEEK {next_gw}  •  Test on TBC"

# Try to update the deadline/test date on HOME too (generic placeholders)
home["B4"].value = f"DEADLINE  •  GAMEWEEK {next_gw}  •  11:59 PM"
home["B5"].value = f"TEST DATE  •  GAMEWEEK {next_gw}"

print(f"  HOME: CURRENT GAMEWEEK updated to {next_gw}.")
print(f"  Headers updated on HOME and TEST RESULTS.")

# =========================================================
# 7. SET ACTIVE SHEET + SAVE
# =========================================================
wb.active = wb.index(wb["HOME"])
wb.save(FILE)

print()
print(f"Saved. File is now on Gameweek {next_gw}.")
print()
print("REMINDER: Open the file in Excel and save it once so the next")
print("          advance has fresh cached values to work with.")