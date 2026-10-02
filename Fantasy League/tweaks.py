import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment, Protection
from openpyxl.worksheet.datavalidation import DataValidation
import shutil
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================
FILE_PATH = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing\11O Fantasy League.xlsx"
BACKUP_DIR = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing"
PASSWORD = "Legendx24j@"
CAPTAIN_MULT_ROW = 18

# =========================================================
# STYLES
# =========================================================
NAVY="0B1F3A"; BLUE="1565C0"; WHITE="FFFFFF"; DARK="172033"; GREY="6B7280"
LIGHT_GREY="E5E7EB"; LIGHT_BLUE="EAF2FF"; PALE_BLUE="F5F9FF"
LIGHT_GOLD="FEF3C7"

thin_grey = Side(style="thin", color=LIGHT_GREY)
medium_blue = Side(style="medium", color=BLUE)

def box(cell, fill=WHITE, bold=False, color=DARK, align="left", size=12, italic=False, unlocked=False):
    cell.fill = PatternFill("solid", fgColor=fill)
    cell.font = Font(bold=bold, color=color, size=size, italic=italic)
    cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=False)
    cell.border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
    if unlocked:
        cell.protection = Protection(locked=False)

# =========================================================
# MAIN
# =========================================================
def main():
    print("=" * 62)
    print("PATCH — DYNAMIC DROPDOWNS + CAPTAIN MULTIPLIER + MASTER DATA")
    print("=" * 62)

    # Backup
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = f"{BACKUP_DIR}/11O Fantasy League_backup_{ts}.xlsx"
    shutil.copy2(FILE_PATH, backup)
    print(f"[OK] Backup: {backup}\n")

    wb = openpyxl.load_workbook(FILE_PATH)

    # Get manager list
    menu = wb["PICK YOUR TEAM"]
    managers = []
    for r in range(5, 100):
        n = menu.cell(r, 2).value
        if not n:
            break
        managers.append(n.strip())
    print(f"Found {len(managers)} managers.\n")

    # =====================================================
    # 1. SETTINGS — add dropdown source (col H) + captain multiplier
    # =====================================================
    s = wb["SETTINGS"]
    s.protection.sheet = False

    # --- 1a. Captain multiplier row at 18 ---
    s.cell(CAPTAIN_MULT_ROW, 2, "Captain multiplier")
    s.cell(CAPTAIN_MULT_ROW, 3, 2)
    s.cell(CAPTAIN_MULT_ROW, 4, "Multiplier applied to captain's points (2 = double, 3 = triple)")
    box(s.cell(CAPTAIN_MULT_ROW, 2), LIGHT_BLUE, True, DARK, "left")
    box(s.cell(CAPTAIN_MULT_ROW, 3), LIGHT_GOLD, True, NAVY, "center", unlocked=True)
    box(s.cell(CAPTAIN_MULT_ROW, 4), PALE_BLUE, False, GREY, "left", size=11, italic=True)
    s.row_dimensions[CAPTAIN_MULT_ROW].height = 26
    print("[OK] SETTINGS: captain multiplier at C18")

    # --- 1b. Dropdown source in column H ---
    # H21 header
    s.cell(21, 8, "Dropdown")
    h = s.cell(21, 8)
    h.font = Font(bold=True, color=WHITE, size=12)
    h.fill = PatternFill("solid", fgColor=NAVY)
    h.alignment = Alignment(horizontal="center", vertical="center")
    h.border = Border(bottom=medium_blue)
    # H22:H42 = mirror of B22:B42
    for r in range(22, 43):
        s.cell(r, 8, f"=IF(B{r}=\"\",\"\",B{r})")
        box(s.cell(r, 8), PALE_BLUE, False, DARK, "left")
        s.cell(r, 8).protection = Protection(locked=True)
    s.column_dimensions["H"].width = 24
    print("[OK] SETTINGS: dropdown source at H22:H42")

    s.protection.sheet = True
    s.protection.password = PASSWORD

    # =====================================================
    # 2. Team sheets — restore dropdowns, dynamic captain mult
    # =====================================================
    for name in managers:
        if name not in wb.sheetnames:
            continue
        ws = wb[name]

        # --- 2a. Rebuild player dropdown on C10:C14 ---
        ws.data_validations.dataValidation = []

        dv_players = DataValidation(
            type="list",
            formula1="=SETTINGS!$H$22:$H$42",
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

        # --- 2b. Captain dropdown (still references local picks) ---
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

        # --- 2c. Rewrite points formulas to use SETTINGS captain multiplier ---
        for r in range(10, 15):
            formula = (
                f'=IF(C{r}="","",'
                f'IF(C{r}=$C$5,'
                f'TEXT(IFERROR(INDEX(CALCULATIONS!$D$2:$D$22,MATCH(C{r},CALCULATIONS!$A$2:$A$22,0)),0)*SETTINGS!$C${CAPTAIN_MULT_ROW},"0")&" (×"&SETTINGS!$C${CAPTAIN_MULT_ROW}&")",'
                f'TEXT(IFERROR(INDEX(CALCULATIONS!$D$2:$D$22,MATCH(C{r},CALCULATIONS!$A$2:$A$22,0)),0),"0")'
                f'))'
            )
            ws.cell(r, 5, formula)

        # --- 2d. Rewrite GW Score formula to use multiplier ---
        ws["C19"] = (
            f'=IF($C$20="VALID TEAM",'
            f'SUMPRODUCT(SUMIF(CALCULATIONS!$A$2:$A$22,C10:C14,CALCULATIONS!$D$2:$D$22))'
            f'+SUMIF(CALCULATIONS!$A$2:$A$22,C5,CALCULATIONS!$D$2:$D$22)*(SETTINGS!$C${CAPTAIN_MULT_ROW}-1),0)'
        )

    print(f"[OK] Team sheets: dropdowns restored, captain multiplier wired up ({len(managers)} sheets)")

    # =====================================================
    # 3. CALCULATIONS — fix score range + use captain multiplier
    # =====================================================
    calc = wb["CALCULATIONS"]
    calc.protection.sheet = False

    # Fix points formula range: use H6:H26
    for i in range(2, 23):
        sc  = f"INDEX('TEST RESULTS'!$H$6:$H$26,MATCH(A{i},'TEST RESULTS'!$B$6:$B$26,0))"
        avg = "AVERAGE('TEST RESULTS'!$H$6:$H$26)"
        step = "MAX((MAX('TEST RESULTS'!$H$6:$H$26)-MIN('TEST RESULTS'!$H$6:$H$26))/SETTINGS!$C$6,0.1)"
        calc.cell(i, 4,
            f'=_xlfn.IFERROR(IF({sc}="",0,'
            f'MAX(SETTINGS!$C$7,MIN(SETTINGS!$C$8,'
            f'SETTINGS!$C$5+ROUNDDOWN(({sc}-{avg})/{step},0)))),0)')

    # Manager row: GW score uses captain multiplier
    for r in range(2, 2 + len(managers)):
        # T = GW score (uses dynamic captain multiplier)
        calc.cell(r, 20,
            f'=IF($U{r}="VALID TEAM",'
            f'SUMPRODUCT(SUMIF($A$2:$A$22,L{r}:P{r},$D$2:$D$22))'
            f'+SUMIF($A$2:$A$22,Q{r},$D$2:$D$22)*(SETTINGS!$C${CAPTAIN_MULT_ROW}-1),0)')

    calc.protection.sheet = True
    calc.protection.password = PASSWORD
    print("[OK] CALCULATIONS: score range fixed, captain multiplier applied")

    # =====================================================
    # 4. MASTER DATA — rebuild fresh
    # =====================================================
    if "MASTER DATA" in wb.sheetnames:
        del wb["MASTER DATA"]
    md = wb.create_sheet("MASTER DATA")
    md.sheet_state = "hidden"

    headers = ["Manager", "P1", "P2", "P3", "P4", "P5", "Captain"]
    for c_off, h in enumerate(headers):
        cell = md.cell(1, 2 + c_off, h)
        cell.font = Font(bold=True, color=WHITE, size=12)
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = Border(bottom=medium_blue)
    md.row_dimensions[1].height = 32

    for i, name in enumerate(managers):
        r = 2 + i
        md.cell(r, 2, name)
        for c_off, ref in enumerate(["C10", "C11", "C12", "C13", "C14"]):
            md.cell(r, 3 + c_off, f"='{name}'!{ref}")
        md.cell(r, 8, f"='{name}'!C5")
        box(md.cell(r, 2), WHITE, True, DARK, "left")
        for c in range(3, 9):
            box(md.cell(r, c), WHITE if i % 2 == 0 else PALE_BLUE, False, DARK, "left")
        md.row_dimensions[r].height = 26

    md.protection.sheet = True
    md.protection.password = PASSWORD
    print("[OK] MASTER DATA rebuilt fresh")

    # =====================================================
    # 5. Save
    # =====================================================
    wb.save(FILE_PATH)
    print()
    print("=" * 62)
    print(f"Saved: {FILE_PATH}")
    print("=" * 62)
    print()
    print("WHAT CHANGED:")
    print("  - SETTINGS: captain multiplier at C18 (currently 2)")
    print("  - SETTINGS: dropdown source at H22:H42 (mirrors B22:B42)")
    print("  - Team sheets: player dropdowns restored (read from SETTINGS!H)")
    print("  - Team sheets: captain points use SETTINGS multiplier")
    print("  - CALCULATIONS: score range fixed to H6:H26")
    print("  - MASTER DATA: rebuilt fresh")
    print()
    print("TEST IT:")
    print("  1. Open the file.")
    print("  2. Change SETTINGS!C18 from 2 to 3.")
    print("  3. Check a team sheet — captain should now show x3 points.")
    print("  4. Delete a player row in SETTINGS (22-42) — should disappear from dropdowns.")


if __name__ == "__main__":
    main()