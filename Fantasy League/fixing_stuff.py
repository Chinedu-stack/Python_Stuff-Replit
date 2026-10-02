import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment, Protection
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

# =========================================================
# CONFIG
# =========================================================
FILE_PATH = r"/workspaces/Python_Stuff-Replit/Fantasy League/11O Fantasy League.xlsx"
PASSWORD = "Legendx24j@"
NUM_TESTS_MAX = 5
FIRST_STUDENT_ROW = 6
LAST_STUDENT_ROW = 26

# =========================================================
# STYLES
# =========================================================
NAVY="0B1F3A"; BLUE="1565C0"; WHITE="FFFFFF"; DARK="172033"; GREY="6B7280"
LIGHT_GREY="E5E7EB"; LIGHT_BLUE="EAF2FF"; PALE_BLUE="F5F9FF"
LIGHT_GOLD="FEF3C7"; SLATE="475569"; OFF_GREY="D9D9D9"

thin_grey = Side(style="thin", color=LIGHT_GREY)
medium_blue = Side(style="medium", color=BLUE)

def box(cell, fill=WHITE, bold=False, color=DARK, align="left", size=12, italic=False, unlocked=False):
    cell.fill = PatternFill("solid", fgColor=fill)
    cell.font = Font(bold=bold, color=color, size=size, italic=italic)
    cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=False)
    cell.border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
    if unlocked:
        cell.protection = Protection(locked=False)

def main():
    print("=" * 62)
    print("MULTI-TEST PATCH — with grey-out of inactive columns")
    print("=" * 62)

    wb = openpyxl.load_workbook(FILE_PATH)

    menu = wb["PICK YOUR TEAM"]
    managers = []
    for r in range(5, 100):
        n = menu.cell(r, 2).value
        if not n:
            break
        managers.append(n.strip())

    # =====================================================
    # 1. SETTINGS — add "Tests per gameweek" at row 17
    # =====================================================
    s = wb["SETTINGS"]
    s.protection.sheet = False

    s.cell(17, 2, "Tests per gameweek")
    s.cell(17, 3, 1)
    s.cell(17, 4, "How many test columns count this week (1-5). Others are greyed out.")
    box(s.cell(17, 2), LIGHT_BLUE, True, DARK, "left")
    box(s.cell(17, 3), LIGHT_GOLD, True, NAVY, "center", unlocked=True)
    box(s.cell(17, 4), PALE_BLUE, False, GREY, "left", size=11, italic=True)
    s.row_dimensions[17].height = 26

    s.protection.sheet = True
    s.protection.password = PASSWORD
    print("[OK] SETTINGS: 'Tests per gameweek' at C17")

    # =====================================================
    # 2. TEST RESULTS — rebuild
    # =====================================================
    tr = wb["TEST RESULTS"]
    tr.protection.sheet = False

    tr.data_validations.dataValidation = []
    for mr in list(tr.merged_cells.ranges):
        try:
            tr.unmerge_cells(str(mr))
        except Exception:
            pass
    for r in range(1, 35):
        for c in range(2, 10):
            cell = tr.cell(r, c)
            cell.value = None
            cell.fill = PatternFill(fill_type=None)
            cell.border = Border()
            cell.font = Font()
            cell.alignment = Alignment()
            cell.protection = Protection(locked=True)
    tr.conditional_formatting._cf_rules.clear()

    tr.column_dimensions["A"].width = 4
    tr.column_dimensions["B"].width = 26
    for col_letter in "CDEFG":
        tr.column_dimensions[col_letter].width = 12
    tr.column_dimensions["H"].width = 12
    tr.column_dimensions["I"].width = 4

    # Row 1 — Title
    tr.merge_cells("B1:H1")
    t = tr.cell(1, 2, "TEST RESULTS")
    t.font = Font(size=22, bold=True, color=WHITE)
    t.fill = PatternFill("solid", fgColor=NAVY)
    t.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    tr.row_dimensions[1].height = 52

    # Row 2 — Subtitle
    tr.merge_cells("B2:H2")
    c = tr.cell(2, 2, "Enter your test scores. Greyed columns are not counted this week.")
    c.font = Font(size=12, bold=True, color=BLUE)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    tr.row_dimensions[2].height = 30

    tr.merge_cells("B3:H3")
    tr.row_dimensions[3].height = 10

    # Row 4 — Test names
    box(tr.cell(4, 2, "Test name:"), SLATE, True, WHITE, "left")
    for c_off in range(NUM_TESTS_MAX):
        cell = tr.cell(4, 3 + c_off)
        box(cell, LIGHT_GOLD, True, NAVY, "center", unlocked=True)
    box(tr.cell(4, 8, "Score"), SLATE, True, WHITE, "center")
    tr.row_dimensions[4].height = 28

    # Row 5 — Headers
    headers = ["Student", "Test 1", "Test 2", "Test 3", "Test 4", "Test 5", "Score"]
    for c_off, h in enumerate(headers):
        cell = tr.cell(5, 2 + c_off, h)
        cell.font = Font(bold=True, color=WHITE, size=12)
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = Border(bottom=medium_blue)
    tr.row_dimensions[5].height = 32

    # Rows 6-26 — Students
    for i, name in enumerate(managers):
        r = FIRST_STUDENT_ROW + i
        box(tr.cell(r, 2, name), WHITE, False, DARK, "left")
        for c_off in range(NUM_TESTS_MAX):
            cell = tr.cell(r, 3 + c_off)
            box(cell, LIGHT_GOLD, False, DARK, "center", unlocked=True)
            cell.number_format = '0"%"'
        h_cell = tr.cell(r, 8)
        h_cell.value = f'=IFERROR(AVERAGE(C{r}:INDEX(C{r}:G{r},SETTINGS!$C$17)),"")'
        box(h_cell, LIGHT_BLUE, True, DARK, "center")
        h_cell.number_format = '0.0"%"'
        tr.row_dimensions[r].height = 30

    # Data validation
    dv = DataValidation(type="whole", operator="between", formula1="0", formula2="100", allow_blank=True)
    dv.error = "Enter a whole number 0–100."
    dv.errorTitle = "Invalid score"
    dv.showErrorMessage = True
    tr.add_data_validation(dv)
    dv.add(f"C{FIRST_STUDENT_ROW}:G{LAST_STUDENT_ROW}")

    # Grey-out conditional formatting
    grey_fill = PatternFill("solid", fgColor=OFF_GREY)
    grey_font = Font(color="808080", italic=True)
    rule = FormulaRule(
        formula=["COLUMN()-2 > SETTINGS!$C$17"],
        fill=grey_fill,
        font=grey_font,
    )
    for rng in ["C4:G4", "C5:G5", f"C{FIRST_STUDENT_ROW}:G{LAST_STUDENT_ROW}"]:
        tr.conditional_formatting.add(rng, rule)
    print("[OK] TEST RESULTS rebuilt with grey-out")

    # Bottom note
    note_row = LAST_STUDENT_ROW + 2
    tr.merge_cells(f"B{note_row}:H{note_row+2}")
    note = tr.cell(note_row, 2,
        "Enter a whole number 0–100 in the gold cells.\n"
        "Greyed columns are not counted — set how many count in SETTINGS!C17.")
    note.font = Font(bold=True, color=DARK, size=12)
    note.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    box(note, LIGHT_GOLD)

    # Protect
    tr.protection.sheet = True
    tr.protection.password = PASSWORD
    tr.protection.selectLockedCells = False
    tr.protection.selectUnlockedCells = False

    # =====================================================
    # 3. CALCULATIONS — points from H
    # =====================================================
    calc = wb["CALCULATIONS"]
    calc.protection.sheet = False

    for i in range(2, 23):
        sc  = f"INDEX('TEST RESULTS'!$H${FIRST_STUDENT_ROW}:$H${LAST_STUDENT_ROW},MATCH(A{i},'TEST RESULTS'!$B${FIRST_STUDENT_ROW}:$B${LAST_STUDENT_ROW},0))"
        avg = f"AVERAGE('TEST RESULTS'!$H${FIRST_STUDENT_ROW}:$H${LAST_STUDENT_ROW})"
        step = f"MAX((MAX('TEST RESULTS'!$H${FIRST_STUDENT_ROW}:$H${LAST_STUDENT_ROW})-MIN('TEST RESULTS'!$H${FIRST_STUDENT_ROW}:$H${LAST_STUDENT_ROW}))/SETTINGS!$C$6,0.1)"
        calc.cell(i, 4,
            f'=_xlfn.IFERROR(IF({sc}="",0,'
            f'MAX(SETTINGS!$C$7,MIN(SETTINGS!$C$8,'
            f'SETTINGS!$C$5+ROUNDDOWN(({sc}-{avg})/{step},0)))),0)')

    calc.protection.sheet = True
    calc.protection.password = PASSWORD
    print("[OK] CALCULATIONS updated")

    wb.save(FILE_PATH)
    print()
    print("=" * 62)
    print(f"Saved: {FILE_PATH}")
    print("=" * 62)


if __name__ == "__main__":
    main()