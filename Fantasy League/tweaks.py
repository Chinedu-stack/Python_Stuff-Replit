import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.formatting.rule import FormulaRule

# =========================================================
# CONFIG
# =========================================================
FILE_PATH = r"C:\Users\chine\OneDrive\School Fantasy League\11O Fantasy League.xlsx"

# =========================================================
# STYLES
# =========================================================
NAVY = "0B1F3A"
BLUE = "1565C0"
WHITE = "FFFFFF"
DARK = "172033"
LIGHT_GREY = "E5E7EB"
LIGHT_GOLD = "FEF3C7"

thin_grey = Side(style="thin", color=LIGHT_GREY)
medium_blue = Side(style="medium", color=BLUE)

# =========================================================
# MAIN
# =========================================================
def main():
    print("=" * 62)
    print("PATCH SQUAD — STRETCH TITLE + CAPTAIN HIGHLIGHT")
    print("=" * 62)
    print()

    wb = openpyxl.load_workbook(FILE_PATH)

    menu = wb["PICK YOUR TEAM"]
    managers = []
    for r in range(5, 100):
        name = menu.cell(r, 2).value
        if not name:
            break
        managers.append(name.strip())

    print(f"Found {len(managers)} team sheets.\n")

    for name in managers:
        if name not in wb.sheetnames:
            print(f"  SKIP: {name} (no sheet)")
            continue

        ws = wb[name]

        # ---- 1. Unmerge any row-8 merges, then merge B8:E8 ----
        for mr in list(ws.merged_cells.ranges):
            if mr.min_row == 8 and mr.max_row == 8:
                try:
                    ws.unmerge_cells(str(mr))
                except Exception:
                    pass

        ws.merge_cells("B8:E8")
        cell = ws.cell(8, 2)
        cell.value = "SQUAD"
        cell.font = Font(size=13, bold=True, color=WHITE)
        cell.fill = PatternFill("solid", fgColor=BLUE)
        cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[8].height = 32

        # ---- 2. Points column formulas with captain ×2 indicator ----
        for r in range(10, 15):
            formula = (
                f'=IF(C{r}="","",'
                f'IF(C{r}=$C$5,'
                f'TEXT(IFERROR(INDEX(CALCULATIONS!$D$2:$D$22,MATCH(C{r},CALCULATIONS!$A$2:$A$22,0)),0)*2,"0")&" (×2)",'
                f'TEXT(IFERROR(INDEX(CALCULATIONS!$D$2:$D$22,MATCH(C{r},CALCULATIONS!$A$2:$A$22,0)),0),"0")'
                f'))'
            )
            c = ws.cell(r, 5, formula)
            c.font = Font(bold=True, color=DARK, size=12)
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.border = Border(left=thin_grey, right=thin_grey, top=thin_grey, bottom=thin_grey)
            c.fill = PatternFill("solid", fgColor=WHITE)

        # ---- 3. Conditional formatting: gold when slot player == captain ----
        ws.conditional_formatting.add(
            "E10:E14",
            FormulaRule(
                formula=['$C10=$C$5'],
                fill=PatternFill("solid", fgColor=LIGHT_GOLD),
                font=Font(bold=True, color=NAVY, size=12),
            ),
        )

        print(f"  OK:   {name}")

    wb.save(FILE_PATH)
    print()
    print("=" * 62)
    print(f"Saved: {FILE_PATH}")
    print("=" * 62)


if __name__ == "__main__":
    main()