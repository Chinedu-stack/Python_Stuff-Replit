# =========================================================
# dump_workbook.py — read-only snapshot of the whole workbook
# Writes everything useful to workbook_dump.txt
# =========================================================
import openpyxl
from openpyxl.utils import get_column_letter

FILE_PATH = r"C:\Users\chine\OneDrive\Copies School Fantasy League for editing\11O Fantasy League.xlsx"
OUT_PATH  = r"C:\Users\chine\OneDrive\Python Stuff\Fantasy League\workbook_dump.txt"

# Load twice: once with formulas, once with cached values
wb_f = openpyxl.load_workbook(FILE_PATH, data_only=False)
wb_v = openpyxl.load_workbook(FILE_PATH, data_only=True)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    def w(s=""):
        f.write(str(s) + "\n")

    w("=" * 78)
    w("WORKBOOK DUMP")
    w("=" * 78)
    w(f"File: {FILE_PATH}")
    w()

    # ---------------- Sheet list ----------------
    w("-" * 78)
    w("SHEETS (in order, with visibility state)")
    w("-" * 78)
    for ws in wb_f.worksheets:
        w(f"  {ws.title!r:45}  state={ws.sheet_state}")
    w()

    # ---------------- Named ranges ----------------
    w("-" * 78)
    w("NAMED RANGES")
    w("-" * 78)
    for name, dn in wb_f.defined_names.items():
        w(f"  {name!r:30}  ->  {dn.attr_text}")
    w()

    # ---------------- Per-sheet dump ----------------
    for ws in wb_f.worksheets:
        w("=" * 78)
        w(f"SHEET: {ws.title!r}   (state={ws.sheet_state})")
        w("=" * 78)

        w(f"  Dimensions (used range): {ws.dimensions}")
        w(f"  Max row/col: {ws.max_row} / {ws.max_column}")
        w(f"  Protected: {ws.protection.sheet}")
        w()

        # Merged cells
        merges = [str(m) for m in ws.merged_cells.ranges]
        if merges:
            w(f"  Merged ranges ({len(merges)}):")
            for m in merges:
                w(f"    {m}")
            w()

        # Data validations
        dvs = ws.data_validations.dataValidation
        if dvs:
            w(f"  Data validations ({len(dvs)}):")
            for dv in dvs:
                w(f"    type={dv.type}  formula1={dv.formula1}  range={dv.sqref}")
            w()

        # Column widths
        widths = []
        for col_letter, dim in ws.column_dimensions.items():
            if dim.width:
                widths.append((col_letter, round(dim.width, 1)))
        if widths:
            w(f"  Column widths: {widths}")
            w()

        # Cells
        w("  CELLS (non-empty only)")
        w("  " + "-" * 74)
        for row in ws.iter_rows():
            for cell in row:
                v_f = cell.value
                if v_f in (None, ""):
                    continue
                # Value from data_only book for the same coord
                v_v = wb_v[ws.title][cell.coordinate].value

                is_formula = isinstance(v_f, str) and v_f.startswith("=")
                if is_formula:
                    w(f"    {cell.coordinate:>6}  [FORMULA]  {v_f}")
                    if v_v not in (None, ""):
                        w(f"    {'':>6}   (cached value: {v_v!r})")
                else:
                    w(f"    {cell.coordinate:>6}  {v_f!r}")
        w()

print(f"Wrote: {OUT_PATH}")